"""Сбор препринтов с arXiv API."""

from __future__ import annotations

import urllib.parse
import xml.etree.ElementTree as ET

import requests

from tendencia.models import SourceItem
from tendencia.quarter import Quarter

ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _fetch_query(query: str, max_results: int = 30) -> list[SourceItem]:
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    items: list[SourceItem] = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        title = (entry.findtext("atom:title", default="", namespaces=ARXIV_NS) or "").strip()
        link = ""
        for link_el in entry.findall("atom:link", ARXIV_NS):
            if link_el.attrib.get("rel") == "alternate":
                link = link_el.attrib.get("href", "")
                break
        published = entry.findtext("atom:published", default="", namespaces=ARXIV_NS)
        summary = (entry.findtext("atom:summary", default="", namespaces=ARXIV_NS) or "").strip()
        if len(summary) > 500:
            summary = summary[:500] + "…"
        items.append(
            SourceItem(
                title=title,
                url=link,
                published=published[:10] if published else None,
                summary=summary,
                source_type="papers",
                origin="arXiv",
            )
        )
    return items


def collect_arxiv(queries: list[str], quarter: Quarter) -> list[SourceItem]:
    seen: set[str] = set()
    result: list[SourceItem] = []
    for query in queries:
        for item in _fetch_query(query):
            if item.url in seen:
                continue
            if item.published:
                try:
                    from datetime import date

                    pub = date.fromisoformat(item.published)
                    if not quarter.contains(pub):
                        continue
                except ValueError:
                    pass
            seen.add(item.url)
            result.append(item)
    return result
