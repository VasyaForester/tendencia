"""Преобразование пользовательских загрузок в SourceItem."""

from __future__ import annotations

from tendencia.models import SourceItem
from tendencia.quarter import Quarter
from tendencia.uploads.store import list_uploads, uploads_dir


def collect_user_uploads(quarter: Quarter) -> list[SourceItem]:
    items: list[SourceItem] = []
    for row in list_uploads(quarter):
        url = row.get("url", "")
        if row.get("kind") == "pdf" and row.get("stored_file"):
            local = uploads_dir(quarter) / row["stored_file"]
            if local.exists():
                url = local.as_uri()

        source_type = row.get("source_type", "user_upload")
        if source_type not in _VALID_TYPES:
            source_type = "user_upload"

        items.append(
            SourceItem(
                title=row.get("title", "Пользовательский источник"),
                url=url,
                published=row.get("published"),
                summary=row.get("summary", ""),
                source_type=source_type,  # type: ignore[arg-type]
                origin="user_upload",
                relevance_score=1.25,
            )
        )
    return items


_VALID_TYPES = {
    "gov_cert",
    "standards",
    "papers",
    "vendor",
    "incidents",
    "news",
    "social",
    "user_upload",
    "user_upload",
    "unknown",
}


def merge_user_uploads(sources: list[SourceItem], quarter: Quarter) -> list[SourceItem]:
    """Добавить загрузки пользователя, не дублируя по URL/названию."""
    user_items = collect_user_uploads(quarter)
    if not user_items:
        return sources

    seen_urls = {s.url.rstrip("/") for s in sources}
    seen_titles = {s.title.lower().strip() for s in sources}
    merged = list(sources)

    for item in user_items:
        key_url = item.url.rstrip("/")
        key_title = item.title.lower().strip()
        if key_url in seen_urls or key_title in seen_titles:
            continue
        merged.append(item)
        seen_urls.add(key_url)
        seen_titles.add(key_title)

    return merged
