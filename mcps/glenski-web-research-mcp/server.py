#!/usr/bin/env python3
"""
web-research-mcp -- API-free web research MCP server for Claude
================================================================
Tools: web_search | fetch_page | multi_search

Zero API key dependencies. Uses DuckDuckGo + httpx + BeautifulSoup.
Works with Claude Desktop, Claude Code, and any MCP-compatible host.

Origin  : Built on the Web Research Prompt by Glen E. Grant
          The research protocol (tool priority, source verification,
          cross-referencing, confidence rating, citation structure)
          is derived directly from that original prompt system.
Author  : Glen E. Grant  |  glen@glenegrant.com
Website : https://glenegrant.com
GitHub  : https://github.com/Glenskii
License : CC BY 4.0 -- https://creativecommons.org/licenses/by/4.0/

Changelog
---------
v2.1  SSRF guard on fetch_page: scheme allow-list, IP-literal and private-range
      rejection, DNS-resolution check before any request
      5 MB streamed response cap, explicit 'truncated' flag on clipped bodies
      multi_search returns deduplicated 'unique_sources' ranked by cross-query
      agreement, and now uses asyncio.to_thread (fixes get_event_loop on 3.12)
v2.0  Parallel multi_search via asyncio + ThreadPoolExecutor (was sequential)
      Exponential backoff with jitter on DuckDuckGo rate limit errors
      JS-rendered page detection in fetch_page via js_rendered_hint flag
      Playwright MCP fallback guidance surfaced directly in tool responses
"""

# ─── Standard Library ────────────────────────────────────────────────────────
import asyncio
import ipaddress
import random
import re
import socket
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

# ─── Third-Party ─────────────────────────────────────────────────────────────
import httpx
from bs4 import BeautifulSoup, Comment
from ddgs import DDGS
from mcp.server.fastmcp import FastMCP

# ─── Server Init ─────────────────────────────────────────────────────────────
mcp = FastMCP(
    "glenski-web-research",
    instructions="""
You are a live research execution engine. When handling factual or time-sensitive queries:

1. SEARCH FIRST -- run web_search before forming any answer
2. FETCH SOURCES -- use fetch_page on the top 2-3 URLs for full content
3. CROSS-REFERENCE -- use multi_search for queries needing multiple angles
   (all queries fire in parallel -- no sequential delays)
4. CITE EVERYTHING -- include URL and access timestamp for every source used
5. FLAG CONFLICTS -- note disagreements between sources explicitly
6. RATE CONFIDENCE -- High / Medium / Low based on source consensus and recency
7. PLAYWRIGHT FALLBACK -- if fetch_page returns js_rendered_hint: true, the page
   is JavaScript-rendered and BeautifulSoup cannot read it fully. Switch to the
   Playwright MCP for that URL to get complete content.

Never answer factual queries from training data when these tools are available.
Use multi_search when a topic benefits from parallel query angles.
""",
)

# ─── Constants ────────────────────────────────────────────────────────────────
FETCH_TIMEOUT      = 15         # seconds per HTTP request
MAX_REDIRECTS      = 5
JS_WORD_THRESHOLD  = 80         # word count below this on a 200 = likely JS-rendered
DDG_MAX_RETRIES    = 3          # retry attempts on DuckDuckGo rate limits
DDG_BACKOFF_BASE   = 1.5        # seconds, exponential base for retry delays
MAX_RESPONSE_BYTES = 5_000_000  # 5 MB hard cap on any fetched page body

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Tags that are structural noise -- strip before extracting text
NOISE_TAGS = {
    "script", "style", "noscript", "nav", "header", "footer",
    "aside", "form", "button", "input", "select", "textarea",
    "advertisement", "ads", "cookie", "popup", "modal",
    "iframe", "svg", "canvas",
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _now_utc() -> str:
    """ISO 8601 timestamp in UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


ALLOWED_SCHEMES = {"http", "https"}


def _blocked_ip(ip: "ipaddress._BaseAddress") -> bool:
    """True if an address is in a range we must never fetch server-side."""
    return (
        ip.is_private or ip.is_loopback or ip.is_link_local
        or ip.is_reserved or ip.is_multicast or ip.is_unspecified
    )


def _validate_fetch_url(url: str) -> Optional[str]:
    """
    SSRF guard for server-side fetching. Returns None if the URL is safe to
    fetch, or a human-readable reason string if it must be rejected.

    Allow-list the scheme, reject IP literals that point at internal ranges,
    and resolve DNS names so a public-looking host cannot map to localhost or
    the cloud metadata endpoint. Note: there is a small TOCTOU window between
    this resolution and httpx's own resolution on the actual request. For a
    research tool that is acceptable, a stricter build would pin the vetted IP.
    """
    try:
        parsed = urlparse(url)
    except Exception as exc:
        return f"URL parse failed: {exc}"

    if parsed.scheme not in ALLOWED_SCHEMES:
        return f"Scheme '{parsed.scheme or 'none'}' not allowed (http/https only)"

    host = parsed.hostname
    if not host:
        return "URL has no host"

    # IP literal: check directly, no DNS needed.
    try:
        ip = ipaddress.ip_address(host)
        return f"IP {host} is in a blocked range" if _blocked_ip(ip) else None
    except ValueError:
        pass  # not a literal, resolve the name below

    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        return f"DNS resolution failed for {host}: {exc}"

    for info in infos:
        try:
            ip = ipaddress.ip_address(info[4][0])
        except ValueError:
            continue
        if _blocked_ip(ip):
            return f"{host} resolves to blocked address {info[4][0]}"

    return None


def _canonical_url(url: str) -> str:
    """
    Normalize a URL for cross-query deduplication: lowercase host, drop a
    trailing slash, ignore scheme and query string. Good enough to collapse
    the same page surfaced by different queries.
    """
    try:
        p = urlparse(url)
        host = (p.hostname or "").lower()
        path = p.path.rstrip("/") or "/"
        return f"{host}{path}"
    except Exception:
        return url


def _extract_text(html: str, max_chars: int) -> tuple[str, str, bool]:
    """
    Extract clean readable text from raw HTML.

    Returns (title, body_text, truncated). Strips noise tags and HTML comments
    before collecting paragraph-level content. Prefers article/main elements
    when present as they typically contain the real content. The truncated flag
    is True when the extracted body was longer than max_chars and got clipped,
    so a caller knows it received a partial page.
    """
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    for tag in soup(list(NOISE_TAGS)):
        tag.decompose()

    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()

    content_root = soup.find("article") or soup.find("main") or soup.body or soup

    paragraphs = content_root.find_all(["p", "li", "h1", "h2", "h3", "h4", "blockquote"])
    if paragraphs:
        raw = "\n".join(p.get_text(" ", strip=True) for p in paragraphs)
    else:
        raw = content_root.get_text(" ", strip=True)

    text = re.sub(r"\s{3,}", "\n\n", raw).strip()
    truncated = len(text) > max_chars
    return title, text[:max_chars], truncated


def _ddg_with_retry(
    query: str,
    region: str,
    time_filter: Optional[str],
    max_results: int,
) -> list[dict]:
    """
    Run a DuckDuckGo search with exponential backoff on rate limit errors.

    Jitter is added to each retry delay to avoid thundering-herd collisions
    when multiple parallel multi_search queries hit DDG simultaneously.
    Raises the last exception if all retries are exhausted.
    """
    last_exc: Exception = Exception("Unknown error")

    for attempt in range(DDG_MAX_RETRIES):
        try:
            with DDGS() as ddgs:
                raw = ddgs.text(
                    keywords=query,
                    region=region,
                    timelimit=time_filter,
                    max_results=max_results,
                )
            return raw or []
        except Exception as exc:
            last_exc = exc
            if attempt < DDG_MAX_RETRIES - 1:
                wait = (DDG_BACKOFF_BASE ** attempt) + random.uniform(0.0, 0.5)
                time.sleep(wait)

    raise last_exc


# ─── Tools ───────────────────────────────────────────────────────────────────

@mcp.tool()
def web_search(
    query: str,
    max_results: int = 5,
    region: str = "wt-wt",
    time_filter: Optional[str] = None,
) -> dict:
    """
    Search the web via DuckDuckGo. No API key required.

    Retries automatically on rate limit errors with exponential backoff.

    Args:
        query       : Search query string
        max_results : Number of results to return (1-10, default 5)
        region      : DuckDuckGo region code (default 'wt-wt' = worldwide).
                      Examples: 'us-en', 'ca-en', 'gb-en'
        time_filter : Recency filter. 'd' (day), 'w' (week), 'm' (month),
                      'y' (year). Omit for all-time results.

    Returns:
        dict with 'query', 'timestamp', 'result_count', and 'results' list.
        Each result contains: title, url, snippet, published (where available).
    """
    max_results = max(1, min(10, max_results))

    try:
        raw = _ddg_with_retry(query, region, time_filter, max_results)
        results = [
            {
                "title"    : r.get("title", ""),
                "url"      : r.get("href", ""),
                "snippet"  : r.get("body", ""),
                "published": r.get("published", ""),
            }
            for r in raw
        ]
    except Exception as exc:
        return {
            "error"    : f"Search failed after {DDG_MAX_RETRIES} retries: {exc}",
            "query"    : query,
            "timestamp": _now_utc(),
            "results"  : [],
        }

    return {
        "query"       : query,
        "timestamp"   : _now_utc(),
        "result_count": len(results),
        "results"     : results,
    }


@mcp.tool()
def fetch_page(
    url: str,
    max_chars: int = 8000,
) -> dict:
    """
    Fetch a URL and extract clean readable text from the page.

    Strips navigation, ads, scripts, and structural noise. Returns the main
    content body suitable for research and citation.

    JS-rendered pages (React, Vue, Angular, etc.) will return a low word count
    even on a successful 200 response because the real content loads via
    JavaScript after the initial HTML is served. When js_rendered_hint is True,
    switch to the Playwright MCP for this URL to get the full rendered content.

    Args:
        url      : Full URL to fetch (must include http:// or https://)
        max_chars: Maximum characters of body text to return (default 8000)

    Only http/https URLs pointing at public hosts are fetched. URLs that
    resolve to private, loopback, link-local, or reserved ranges are rejected
    to prevent server-side request forgery.

    Returns:
        dict with 'url', 'title', 'text', 'word_count', 'status_code',
        'js_rendered_hint', 'truncated', and 'timestamp'. On failure or a
        blocked URL, returns 'error'. A 'note' key is added when
        js_rendered_hint is True.
    """
    # SSRF guard: never let a caller point this at localhost, a private range,
    # or the cloud metadata endpoint (169.254.169.254). Reject before any I/O.
    rejection = _validate_fetch_url(url)
    if rejection:
        return {
            "url"      : url,
            "error"    : f"Blocked URL: {rejection}",
            "timestamp": _now_utc(),
        }

    headers = {
        "User-Agent"     : USER_AGENT,
        "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    try:
        with httpx.Client(
            follow_redirects=True,
            max_redirects=MAX_REDIRECTS,
            timeout=FETCH_TIMEOUT,
        ) as client:
            with client.stream("GET", url, headers=headers) as resp:
                resp.raise_for_status()

                # Read with a hard byte ceiling so a malicious or accidental
                # multi-gigabyte body cannot exhaust memory.
                chunks: list[bytes] = []
                total = 0
                capped = False
                for chunk in resp.iter_bytes():
                    chunks.append(chunk)
                    total += len(chunk)
                    if total >= MAX_RESPONSE_BYTES:
                        capped = True
                        break

                final_url = str(resp.url)
                status_code = resp.status_code
                encoding = resp.encoding or "utf-8"

        html = b"".join(chunks).decode(encoding, errors="replace")
        title, text, body_truncated = _extract_text(html, max_chars)
        truncated = body_truncated or capped
        word_count = len(text.split())

        # A successful 200 with very few words almost always means the real
        # content is rendered client-side via JavaScript. Flag it so Claude
        # knows to route this URL to Playwright MCP instead.
        js_hint = word_count < JS_WORD_THRESHOLD and status_code == 200

        result: dict = {
            "url"             : final_url,
            "title"           : title,
            "text"            : text,
            "word_count"      : word_count,
            "status_code"     : status_code,
            "timestamp"       : _now_utc(),
            "js_rendered_hint": js_hint,
            "truncated"       : truncated,
        }

        if js_hint:
            result["note"] = (
                "Low word count on a successful fetch. This page is likely JS-rendered "
                "and BeautifulSoup cannot read the full content. "
                "Use Playwright MCP to fetch this URL instead."
            )

        return result

    except httpx.HTTPStatusError as exc:
        return {
            "url"        : url,
            "error"      : f"HTTP {exc.response.status_code}: {exc.response.reason_phrase}",
            "status_code": exc.response.status_code,
            "timestamp"  : _now_utc(),
        }
    except httpx.RequestError as exc:
        return {
            "url"      : url,
            "error"    : f"Request failed: {exc}",
            "timestamp": _now_utc(),
        }
    except Exception as exc:
        return {
            "url"      : url,
            "error"    : f"Unexpected error: {exc}",
            "timestamp": _now_utc(),
        }


@mcp.tool()
async def multi_search(
    queries: list[str],
    max_results_each: int = 3,
    region: str = "wt-wt",
    time_filter: Optional[str] = None,
) -> dict:
    """
    Run multiple search queries in PARALLEL for fast cross-referencing.

    All queries fire simultaneously via asyncio and ThreadPoolExecutor.
    On 3 queries this is roughly 3x faster than the old sequential approach.
    Each individual query still retries on DDG rate limits with backoff.

    Use this when a topic benefits from multiple angles: comparing sources,
    verifying claims, or researching questions where different phrasings
    surface meaningfully different results.

    Args:
        queries         : List of 2-5 search queries (different angles on the topic)
        max_results_each: Results per query (1-5, default 3)
        region          : DuckDuckGo region code (default 'wt-wt')
        time_filter     : Recency filter. 'd', 'w', 'm', 'y'. Optional.

    Returns:
        dict with 'timestamp', 'query_count', 'total_results',
        'results_by_query' keyed by each query string, and 'unique_sources':
        a deduplicated, agreement-ranked list of URLs across all queries.
    """
    if not queries:
        return {"error": "No queries provided", "timestamp": _now_utc()}

    queries = queries[:5]
    max_results_each = max(1, min(5, max_results_each))

    # asyncio.to_thread hands each blocking web_search call to the default
    # thread pool. This replaces the deprecated get_event_loop() +
    # ThreadPoolExecutor dance, which raised on Python 3.12 when no loop was
    # already running, and reuses the shared executor instead of spinning up
    # a new one per call.
    outcomes = await asyncio.gather(
        *(
            asyncio.to_thread(
                web_search,
                query=q,
                max_results=max_results_each,
                region=region,
                time_filter=time_filter,
            )
            for q in queries
        ),
        return_exceptions=True,
    )

    results_by_query: dict = {}
    total = 0
    # canonical URL -> {url, title, queries: [..]}  for cross-source agreement
    agreement: dict = {}

    for query, outcome in zip(queries, outcomes):
        if isinstance(outcome, Exception):
            results_by_query[query] = {
                "error"    : str(outcome),
                "timestamp": _now_utc(),
                "results"  : [],
            }
            continue

        results_by_query[query] = outcome
        total += outcome.get("result_count", 0)

        for r in outcome.get("results", []):
            url = r.get("url", "")
            if not url:
                continue
            key = _canonical_url(url)
            entry = agreement.setdefault(
                key, {"url": url, "title": r.get("title", ""), "queries": []}
            )
            if query not in entry["queries"]:
                entry["queries"].append(query)

    # Rank unique sources by how many distinct queries surfaced them. A URL
    # found by several angles is a stronger cross-referenced signal than one
    # that appeared for a single query.
    unique_sources = sorted(
        (
            {
                "url"            : e["url"],
                "title"          : e["title"],
                "agreement_count": len(e["queries"]),
                "found_by"       : e["queries"],
            }
            for e in agreement.values()
        ),
        key=lambda s: s["agreement_count"],
        reverse=True,
    )

    return {
        "timestamp"       : _now_utc(),
        "query_count"     : len(queries),
        "total_results"   : total,
        "unique_source_count": len(unique_sources),
        "unique_sources"  : unique_sources,
        "results_by_query": results_by_query,
    }


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
