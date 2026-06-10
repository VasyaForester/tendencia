"""Сбор статей из RSS-лент."""

from __future__ import annotations

from datetime import datetime

import feedparser

from tendencia.models import SourceItem
from tendencia.quarter import Quarter


def _parse_date(entry: dict) -> datetime | None:
    for key in ("published_parsed", "updated_parsed"):
        parsed = entry.get(key)
        if parsed:
            return datetime(*parsed[:6])
    return None


def collect_rss(feeds: list[dict], quarter: Quarter) -> list[SourceItem]:
    items: list[SourceItem] = []
    for feed_cfg in feeds:
        parsed = feedparser.parse(feed_cfg["url"])
        category = feed_cfg.get("category", "unknown")
        origin = feed_cfg.get("name", feed_cfg["url"])
        for entry in parsed.entries:
            dt = _parse_date(entry)
            if dt and not quarter.contains(dt):
                continue
            link = entry.get("link", "")
            if not link:
                continue
            summary = entry.get("summary", entry.get("description", ""))
            if len(summary) > 500:
                summary = summary[:500] + "…"
            items.append(
                SourceItem(
                    title=entry.get("title", "Без названия"),
                    url=link,
                    published=dt.date().isoformat() if dt else None,
                    summary=summary,
                    source_type=category,
                    origin=origin,
                )
            )
    return items
