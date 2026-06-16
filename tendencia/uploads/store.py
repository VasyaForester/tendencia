"""Хранение пользовательских ссылок и PDF по кварталам."""

from __future__ import annotations

import json
import shutil
import uuid
from datetime import date
from pathlib import Path
from typing import Any

from tendencia.config_loader import project_root
from tendencia.quarter import Quarter
from tendencia.uploads.extract import (
    extract_pdf_text,
    fetch_url_content,
    infer_source_type,
)

MANIFEST = "manifest.json"


def uploads_dir(quarter: Quarter) -> Path:
    return project_root() / "data" / quarter.label / "uploads"


def files_dir(quarter: Quarter) -> Path:
    return uploads_dir(quarter) / "files"


def _manifest_path(quarter: Quarter) -> Path:
    return uploads_dir(quarter) / MANIFEST


def _load_manifest(quarter: Quarter) -> dict[str, Any]:
    path = _manifest_path(quarter)
    if not path.exists():
        return {"quarter": quarter.label, "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_manifest(quarter: Quarter, data: dict[str, Any]) -> None:
    path = _manifest_path(quarter)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def list_uploads(quarter: Quarter) -> list[dict[str, Any]]:
    return _load_manifest(quarter).get("items", [])


def remove_upload(quarter: Quarter, upload_id: str) -> bool:
    data = _load_manifest(quarter)
    items = data.get("items", [])
    kept: list[dict] = []
    removed = False
    for item in items:
        if item.get("id") == upload_id:
            removed = True
            if item.get("kind") == "pdf" and item.get("stored_file"):
                fp = uploads_dir(quarter) / item["stored_file"]
                fp.unlink(missing_ok=True)
            continue
        kept.append(item)
    if not removed:
        return False
    data["items"] = kept
    _save_manifest(quarter, data)
    return True


def add_link(
    quarter: Quarter,
    url: str,
    *,
    title: str | None = None,
    published: str | None = None,
    notes: str = "",
) -> dict[str, Any]:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL должен начинаться с http:// или https://")

    page_title, summary = fetch_url_content(url)
    entry: dict[str, Any] = {
        "id": uuid.uuid4().hex[:10],
        "kind": "link",
        "url": url,
        "title": title or page_title,
        "summary": summary,
        "published": published or date.today().isoformat(),
        "source_type": infer_source_type(url, "link", summary),
        "added_at": date.today().isoformat(),
        "notes": notes,
    }
    _append_entry(quarter, entry)
    return entry


def add_pdf(
    quarter: Quarter,
    pdf_path: Path,
    *,
    title: str | None = None,
    published: str | None = None,
    notes: str = "",
) -> dict[str, Any]:
    src = pdf_path.expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"Файл не найден: {src}")
    if src.suffix.lower() != ".pdf":
        raise ValueError("Ожидается файл .pdf")

    upload_id = uuid.uuid4().hex[:10]
    dest_dir = files_dir(quarter)
    dest_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{upload_id}.pdf"
    stored_rel = f"files/{stored_name}"
    shutil.copy2(src, dest_dir / stored_name)

    text = extract_pdf_text(str(dest_dir / stored_name))
    default_title = title or src.stem.replace("_", " ").replace("-", " ")

    entry: dict[str, Any] = {
        "id": upload_id,
        "kind": "pdf",
        "url": src.as_uri(),
        "original_path": str(src),
        "stored_file": stored_rel,
        "title": default_title,
        "summary": text or "Пользовательский PDF-документ.",
        "published": published or date.today().isoformat(),
        "source_type": infer_source_type(str(src), "pdf", text),
        "added_at": date.today().isoformat(),
        "notes": notes,
    }
    _append_entry(quarter, entry)
    return entry


def _append_entry(quarter: Quarter, entry: dict[str, Any]) -> None:
    data = _load_manifest(quarter)
    items: list[dict] = data.get("items", [])
    # Обновление по URL (без учёта file:// для pdf)
    if entry["kind"] == "link":
        items = [i for i in items if not (i.get("kind") == "link" and i.get("url") == entry["url"])]
    items.append(entry)
    data["items"] = items
    _save_manifest(quarter, data)
