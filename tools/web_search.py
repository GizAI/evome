#!/usr/bin/env python3
"""
DuckDuckGo HTML scraper for lightweight web search (no API key).
Returns top result titles and URLs as JSON for downstream research tools.
"""

import html
import json
import re
import sys
from typing import List, Dict
from urllib.parse import quote_plus, urlparse, parse_qs, unquote
from urllib.request import Request, urlopen


def normalize_duckduckgo_link(href: str) -> str:
    """Follow DuckDuckGo redirect links to real targets."""
    href = html.unescape(href)
    if href.startswith("//"):
        href = f"https:{href}"

    parsed = urlparse(href)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        qs = parse_qs(parsed.query)
        if "uddg" in qs:
            return unquote(qs["uddg"][0])
    return href


def duckduckgo_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Fetch and parse DuckDuckGo HTML results."""
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Omega/1.0)"}
    req = Request(url, headers=headers)

    try:
        with urlopen(req, timeout=10) as resp:
            page = resp.read().decode("utf-8", errors="ignore")
    except Exception as exc:  # pragma: no cover - network failures
        return [{"error": f"request failed: {exc}"}]

    # Extract visible result links; keep it regex-simple to avoid dependencies.
    pattern = re.compile(
        r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )

    results: List[Dict[str, str]] = []
    for href, title_html in pattern.findall(page):
        title_text = re.sub(r"<.*?>", "", title_html)  # strip tags inside title
        parsed_href = normalize_duckduckgo_link(href)
        results.append(
            {
                "title": html.unescape(title_text).strip(),
                "url": parsed_href,
            }
        )
        if len(results) >= max_results:
            break

    return results or [{"error": "no results parsed"}]


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "error": "Usage: web_search.py <query> [max_results=5]",
                    "example": "web_search.py \"agentic AI tools\" 5",
                },
                indent=2,
            )
        )
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    results = duckduckgo_search(query, max_results)
    print(json.dumps({"query": query, "results": results}, indent=2))


if __name__ == "__main__":
    main()
