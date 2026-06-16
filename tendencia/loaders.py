"""Загрузка данных для отчётов и вывода."""

from __future__ import annotations

import json
from pathlib import Path

from tendencia.analysis.trends import build_trend_candidates
from tendencia.config_loader import load_yaml, project_root
from tendencia.models import SourceItem, TrendItem
from tendencia.pipeline import finalize_sources
from tendencia.quarter import Quarter
from tendencia.report.generator import apply_curated
from tendencia.uploads import list_uploads


def data_dir(quarter: Quarter) -> Path:
    return project_root() / "data" / quarter.label


def report_path(quarter: Quarter) -> Path:
    return project_root() / "reports" / quarter.label / "ai-security-trends.md"


def pdf_path(quarter: Quarter) -> Path:
    return project_root() / "reports" / quarter.label / "ai-security-trends.pdf"


def load_finalized_sources(quarter: Quarter) -> list[SourceItem]:
    """Автопоиск + пользовательские загрузки + seed, с тегами тем."""
    topics_cfg = load_yaml("topics.yaml")
    data_path = data_dir(quarter) / "sources.json"
    base: list[SourceItem] = []
    if data_path.exists():
        raw = json.loads(data_path.read_text(encoding="utf-8"))
        base = [SourceItem(**row) for row in raw if row.get("origin") != "user_upload"]
    return finalize_sources(base, quarter, topics_cfg)


def load_sources(quarter: Quarter) -> list[SourceItem]:
    sources = load_finalized_sources(quarter)
    if not sources:
        raise FileNotFoundError(
            f"Нет данных для {quarter}. Запустите: tendencia collect --quarter {quarter} "
            "или tendencia upload …"
        )
    return sources


def load_trends(quarter: Quarter) -> tuple[list[SourceItem], list[TrendItem]]:
    """Собрать актуальные источники (с upload) и тренды."""
    if not list_uploads(quarter) and not (data_dir(quarter) / "sources.json").exists():
        raise FileNotFoundError(
            f"Нет данных для {quarter}. Запустите collect или upload."
        )
    topics_cfg = load_yaml("topics.yaml")
    sources = load_finalized_sources(quarter)
    trends = build_trend_candidates(
        sources,
        topics_cfg,
        max_trends=topics_cfg.get("report", {}).get("trend_count", 10),
    )
    return sources, apply_curated(trends)
