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
v2.0  Parallel multi_search via asyncio + ThreadPoolExecutor (was sequential)
      Exponential backoff with jitter on DuckDuckGo rate limit errors
      JS-rendered page detection in fetch_page via js_rendered_hint flag
      Playwright MCP fallback guidance surfaced directly in tool responses
"""

# ─── Standard Library ────────────────────────────────────────────────────────
import asyncio
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Optional

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
FETCH_TIMEOUT     = 15          # seconds per HTTP request
MAX_REDIRECTS     = 5
JS_WORD_THRESHOLD = 80          # word count below this on a 200 = likely JS-rendered
DDG_MAX_RETRIES   = 3           # retry attempts on DuckDuckGo rate limits
DDG_BACKOFF_BASE  = 1.5         # seconds, exponential base for retry delays

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


def _extract_text(html: str, max_chars: int) -> tuple[str, str]:
    """
    Extract clean readable text from raw HTML.

    Returns (title, body_text). Strips noise tags and HTML comments before
    collecting paragraph-level content. Prefers article/main elements when
    present as they typically contain the real content.
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
    return title, text[:max_chars]


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

    Returns:
        dict with 'url', 'title', 'text', 'word_count', 'status_code',
        'js_rendered_hint', and 'timestamp'. On failure, returns 'error'.
        A 'note' key is added when js_rendered_hint is True.
    """
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
            resp = client.get(url, headers=headers)
            resp.raise_for_status()

        title, text = _extract_text(resp.text, max_chars)
        word_count = len(text.split())

        # A successful 200 with very few words almost always means the real
        # content is rendered client-side via JavaScript. Flag it so Claude
        # knows to route this URL to Playwright MCP instead.
        js_hint = word_count < JS_WORD_THRESHOLD and resp.status_code == 200

        result: dict = {
            "url"             : str(resp.url),
            "title"           : title,
            "text"            : text,
            "word_count"      : word_count,
            "status_code"     : resp.status_code,
            "timestamp"       : _now_utc(),
            "js_rendered_hint": js_hint,
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
        dict with 'timestamp', 'query_count', 'total_results', and
        'results_by_query' keyed by each query string.
    """
    if not queries:
        return {"error": "No queries provided", "timestamp": _now_utc()}

    queries = queries[:5]
    max_results_each = max(1, min(5, max_results_each))

    loop = asyncio.get_event_loop()

    def _run(query: str) -> dict:
        return web_search(
            query=query,
            max_results=max_results_each,
            region=region,
            time_filter=time_filter,
        )

    with ThreadPoolExecutor(max_workers=len(queries)) as executor:
        futures = [loop.run_in_executor(executor, _run, q) for q in queries]
        outcomes = await asyncio.gather(*futures, return_exceptions=True)

    results_by_query: dict = {}
    total = 0

    for query, outcome in zip(queries, outcomes):
        if isinstance(outcome, Exception):
            results_by_query[query] = {
                "error"    : str(outcome),
                "timestamp": _now_utc(),
                "results"  : [],
            }
        else:
            results_by_query[query] = outcome
            total += outcome.get("result_count", 0)

    return {
        "timestamp"       : _now_utc(),
        "query_count"     : len(queries),
        "total_results"   : total,
        "results_by_query": results_by_query,
    }


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
