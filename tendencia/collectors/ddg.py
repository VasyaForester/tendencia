"""Поиск источников через DuckDuckGo."""

from __future__ import annotations

import time

from tendencia.models import SourceItem

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None  # type: ignore[misc, assignment]


def collect_ddg(queries: list[str], max_per_query: int = 8) -> list[SourceItem]:
    if DDGS is None:
        return []

    seen: set[str] = set()
    items: list[SourceItem] = []
    with DDGS() as ddgs:
        for query in queries:
            try:
                results = list(ddgs.text(query, max_results=max_per_query))
            except Exception:
                continue
            for row in results:
                url = row.get("href") or row.get("link") or ""
                if not url or url in seen:
                    continue
                seen.add(url)
                body = row.get("body", "")
                items.append(
                    SourceItem(
                        title=row.get("title", "Без названия"),
                        url=url,
                        summary=body[:500] + ("…" if len(body) > 500 else ""),
                        source_type="news",
                        origin="DuckDuckGo",
                    )
                )
            time.sleep(0.5)
    return items
