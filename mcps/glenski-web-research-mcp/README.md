# glenski-web-research-mcp

**API-free web research MCP server for Claude.**

Adds three live research tools to Claude via the Model Context Protocol. No Perplexity key, no Brave key, no paid accounts. Uses DuckDuckGo for search and httpx + BeautifulSoup for content extraction.

Part of the [Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit).

---

## Tools

| Tool | Description |
|---|---|
| `web_search` | DuckDuckGo full-web search. Returns titles, URLs, snippets. Optional region + recency filter. Retries automatically on rate limit errors with exponential backoff. |
| `fetch_page` | Fetches any URL, strips nav / ads / scripts, returns clean readable body text. Returns `js_rendered_hint: true` when a page is JS-rendered and BeautifulSoup cannot read the full content -- signals Claude to route to Playwright MCP instead. |
| `multi_search` | Runs 2-5 queries in PARALLEL via asyncio + ThreadPoolExecutor for fast multi-angle coverage. All queries fire simultaneously. |

---

## Why this exists

Every popular web-search MCP ties you to a specific vendor API (Perplexity, Brave, Bing). This one does not. DuckDuckGo is free, requires no account, and works out of the box. If you later want to layer in a paid API for higher volume or better ranking, the architecture supports it. Add a key via environment variable and a new tool in `server.py`.

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/Glenskii/Glenski-Toolkit
cd Glenski-Toolkit/mcps/glenski-web-research-mcp
pip install -r requirements.txt
```

### 2. Wire into Claude Code

Edit `~/.claude/mcp.json` (create it if it does not exist):

```json
{
  "mcpServers": {
    "glenski-web-research": {
      "command": "python",
      "args": ["C:/path/to/Glenski-Toolkit/mcps/glenski-web-research-mcp/server.py"]
    }
  }
}
```

Restart Claude Code. The server appears in your connected tools list.

### 2b. Wire into Claude Desktop

Edit your config file:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the same block under `"mcpServers"` with the corrected path. Restart Claude Desktop.

### 3. Verify

Ask Claude: *"Search for the latest news on MCP servers and summarize what you find."*

Claude will call `web_search`, optionally `fetch_page` on top results, and return a sourced response.

---

## Usage Patterns

**Single search with recency filter:**
```
What's happened with WordPress security in the last month?
```
Claude calls `web_search(query, time_filter="m")`.

**Deep read of a specific page:**
```
Get the full content of https://example.com/article
```
Claude calls `fetch_page(url)`, which returns clean text with no nav clutter.

**Multi-angle research (parallel):**
```
Compare what different sources say about Cloudflare Workers vs Vercel Edge Functions
```
Claude calls `multi_search(["Cloudflare Workers performance 2025", "Vercel Edge Functions benchmark", "Workers vs Vercel comparison"])`. All three queries fire simultaneously.

**JS-rendered page fallback:**
```
Get the full content of https://some-react-app.com/pricing
```
Claude calls `fetch_page(url)`. If the response includes `js_rendered_hint: true`, Claude automatically switches to Playwright MCP to fetch the fully rendered content.

---

## Parameters

### `web_search`

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `query` | str | required | Search string |
| `max_results` | int | 5 | 1-10 |
| `region` | str | `wt-wt` | Worldwide. Use `us-en`, `ca-en`, `gb-en`, etc. |
| `time_filter` | str | None | `d` day, `w` week, `m` month, `y` year |

### `fetch_page`

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `url` | str | required | Full URL including `https://` |
| `max_chars` | int | 8000 | Body text character limit |

**Response includes `js_rendered_hint: bool`.** When `true`, the page returned a successful 200 but suspiciously few words -- a reliable indicator of JS-rendered content. Claude will route the URL to Playwright MCP automatically when this flag fires.

### `multi_search`

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `queries` | list[str] | required | 2-5 query strings |
| `max_results_each` | int | 3 | 1-5 per query |
| `region` | str | `wt-wt` | Same as web_search |
| `time_filter` | str | None | Same as web_search |

---

## Research Protocol

The MCP's system instructions embed the research protocol directly. Claude sees it as behavioral context for all tool use:

1. Search before answering, no training-data fallbacks for current facts
2. Fetch top 2-3 URLs for full content, not just snippets
3. Use `multi_search` for comparative or multi-angle queries (all parallel)
4. Cite every source with URL and access timestamp
5. Flag conflicts between sources explicitly
6. Rate confidence: High / Medium / Low based on consensus and recency
7. If `fetch_page` returns `js_rendered_hint: true`, route that URL to Playwright MCP for full rendered content

---

## Requirements

```
python >= 3.10
mcp >= 1.0.0
ddgs >= 0.1.0
httpx >= 0.27.0
beautifulsoup4 >= 4.12.0
```

> `ddgs` is the current package name for DuckDuckGo search (renamed from `duckduckgo-search` in 2025).

---

## No API Keys

Zero vendor dependencies. The `env: {}` block in `claude_desktop_config.json` is intentionally empty.

If you want to add optional enhancements (Brave free tier, Perplexity, Bing), add the key as `"BRAVE_API_KEY": "your_key"` in the `env` block and wire a new tool in `server.py` that checks for it.

---

## Changelog

### v2.0
- `multi_search` now runs all queries in parallel via asyncio + ThreadPoolExecutor (was sequential with 0.75s delays between queries)
- Added exponential backoff with jitter on DuckDuckGo rate limit errors across all search calls
- `fetch_page` now returns `js_rendered_hint: true` when a page is likely JS-rendered, with a note directing Claude to use Playwright MCP for that URL
- Added Claude Code install instructions alongside Claude Desktop

### v1.0
- Initial release: web_search, fetch_page, multi_search via DuckDuckGo + httpx + BeautifulSoup

---

## Origin and Credits

This MCP server is the executable form of the **Web Research Prompt** created by Glen E. Grant.

The core research protocol embedded in this tool: tool priority order, mandatory source fetching, cross-referencing via multi-angle queries, confidence rating, and citation structure. It was designed, field-tested, and refined by Glen as a standalone AI prompt system before being encoded here as an MCP. The `multi_search` tool directly implements his parallel-query cross-referencing methodology.

**Author and original prompt author:** [Glen E. Grant](https://glenegrant.com)
**Contact:** [glen@glenegrant.com](mailto:glen@glenegrant.com)
**GitHub:** [github.com/Glenskii](https://github.com/Glenskii)
**Portfolio:** [glenegrant.com](https://glenegrant.com)

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), share freely, credit appreciated.

---

*Part of the [Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit) - practical AI tools built for real workflows.*
