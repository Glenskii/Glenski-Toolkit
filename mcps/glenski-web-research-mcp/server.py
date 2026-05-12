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
"""

# ─── Standard Library ────────────────────────────────────────────────────────
import re
import time
import json
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

1. SEARCH FIRST — run web_search before forming any answer
2. FETCH SOURCES — use fetch_page on the top 2–3 URLs for full content
3. CROSS-REFERENCE — use multi_search for queries needing multiple angles
4. CITE EVERYTHING — include URL + access timestamp for every source used
5. FLAG CONFLICTS — note disagreements between sources explicitly
6. RATE CONFIDENCE — High / Medium / Low based on source consensus and recency

Never answer factual queries from training data when these tools are available.
Use multi_search when a topic benefits from parallel query angles (e.g., "best X",
comparative questions, or anything requiring verification across domains).
""",
)

# ─── Constants ────────────────────────────────────────────────────────────────
FETCH_TIMEOUT = 15          # seconds
MAX_REDIRECTS = 5
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Tags that are structurally noise — strip before extracting text
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

    Returns (title, body_text). Strips nav/footer/script/style elements
    and HTML comments before extracting paragraph text.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Pull title before stripping
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    # Remove noise tags
    for tag in soup(list(NOISE_TAGS)):
        tag.decompose()

    # Remove HTML comments
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()

    # Prefer <article> or <main> when present — usually the real content
    content_root = soup.find("article") or soup.find("main") or soup.body or soup

    # Collect paragraph-level text; fallback to all text
    paragraphs = content_root.find_all(["p", "li", "h1", "h2", "h3", "h4", "blockquote"])
    if paragraphs:
        raw = "\n".join(p.get_text(" ", strip=True) for p in paragraphs)
    else:
        raw = content_root.get_text(" ", strip=True)

    # Collapse whitespace
    text = re.sub(r"\s{3,}", "\n\n", raw).strip()

    return title, text[:max_chars]


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

    Args:
        query       : Search query string
        max_results : Number of results to return (1–10, default 5)
        region      : DuckDuckGo region code (default 'wt-wt' = worldwide)
                      Examples: 'us-en', 'ca-en', 'gb-en'
        time_filter : Recency filter — 'd' (day), 'w' (week), 'm' (month),
                      'y' (year). Omit for all-time.

    Returns:
        dict with 'query', 'timestamp', 'result_count', and 'results' list.
        Each result has: title, url, snippet, published (if available).
    """
    max_results = max(1, min(10, max_results))

    try:
        with DDGS() as ddgs:
            raw = ddgs.text(
                keywords=query,
                region=region,
                timelimit=time_filter,
                max_results=max_results,
            )
        results = [
            {
                "title"    : r.get("title", ""),
                "url"      : r.get("href", ""),
                "snippet"  : r.get("body", ""),
                "published": r.get("published", ""),
            }
            for r in (raw or [])
        ]
    except Exception as exc:
        return {
            "error"    : f"Search failed: {exc}",
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

    Strips navigation, ads, scripts, and other noise. Returns the main
    content body suitable for research and citation.

    Args:
        url      : Full URL to fetch (must include http:// or https://)
        max_chars: Maximum characters of body text to return (default 8000)

    Returns:
        dict with 'url', 'title', 'text', 'word_count', 'timestamp',
        and 'status_code'. On failure, returns an 'error' key.
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

        return {
            "url"        : str(resp.url),
            "title"      : title,
            "text"       : text,
            "word_count" : len(text.split()),
            "status_code": resp.status_code,
            "timestamp"  : _now_utc(),
        }

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
def multi_search(
    queries: list[str],
    max_results_each: int = 3,
    region: str = "wt-wt",
    time_filter: Optional[str] = None,
) -> dict:
    """
    Run multiple search queries in sequence for cross-referencing.

    Use this when a topic benefits from parallel angles — e.g., comparing
    sources, verifying claims, or researching "best X" style questions where
    different query phrasings surface different results.

    Args:
        queries         : List of 2–5 search queries (different angles)
        max_results_each: Results per query (1–5, default 3)
        region          : DuckDuckGo region code (default 'wt-wt')
        time_filter     : Recency filter — 'd', 'w', 'm', 'y'. Optional.

    Returns:
        dict with 'timestamp', 'query_count', 'total_results', and
        'results_by_query' — a dict keyed by each query string.
    """
    if not queries:
        return {"error": "No queries provided", "timestamp": _now_utc()}

    queries = queries[:5]  # Guard: max 5 queries
    max_results_each = max(1, min(5, max_results_each))

    results_by_query = {}
    total = 0

    for query in queries:
        outcome = web_search(
            query=query,
            max_results=max_results_each,
            region=region,
            time_filter=time_filter,
        )
        results_by_query[query] = outcome
        total += outcome.get("result_count", 0)

        # Brief pause between queries — polite to the search engine
        time.sleep(0.75)

    return {
        "timestamp"        : _now_utc(),
        "query_count"      : len(queries),
        "total_results"    : total,
        "results_by_query" : results_by_query,
    }


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
