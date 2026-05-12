# glenski-web-research-mcp

**API-free web research MCP server for Claude.**

Adds three live research tools to Claude via the Model Context Protocol. No Perplexity key, no Brave key, no paid accounts. Uses DuckDuckGo for search and httpx + BeautifulSoup for content extraction.

Part of the [Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit).

---

## Tools

| Tool | Description |
|---|---|
| `web_search` | DuckDuckGo full-web search. Returns titles, URLs, snippets. Optional region + recency filter. |
| `fetch_page` | Fetches any URL, strips nav / ads / scripts, returns clean readable body text. |
| `multi_search` | Runs 2-5 queries in sequence for cross-referencing and multi-angle coverage. |

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

### 2. Wire into Claude Desktop

Edit your config file:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this block under `"mcpServers"`. Update the path to match where you cloned:

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

Restart Claude Desktop. The server appears in your connected tools list.

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

**Multi-angle research:**
```
Compare what different sources say about Cloudflare Workers vs Vercel Edge Functions
```
Claude calls `multi_search(["Cloudflare Workers performance 2025", "Vercel Edge Functions benchmark", "Workers vs Vercel comparison"])`.

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
3. Use `multi_search` for comparative or multi-angle queries
4. Cite every source with URL and access timestamp
5. Flag conflicts between sources explicitly
6. Rate confidence: High / Medium / Low based on consensus and recency

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
