"""Загрузка данных для отчётов и вывода."""

from __future__ import annotations

import json
from pathlib import Path

from tendencia.analysis.trends import build_trend_candidates
from tendencia.config_loader import load_yaml, project_root
from tendencia.models import SourceItem, TrendItem
from tendencia.quarter import Quarter
from tendencia.report.generator import apply_curated


def data_dir(quarter: Quarter) -> Path:
    return project_root() / "data" / quarter.label


def report_path(quarter: Quarter) -> Path:
    return project_root() / "reports" / quarter.label / "ai-security-trends.md"


def pdf_path(quarter: Quarter) -> Path:
    return project_root() / "reports" / quarter.label / "ai-security-trends.pdf"


def load_sources(quarter: Quarter) -> list[SourceItem]:
    path = data_dir(quarter) / "sources.json"
    if not path.exists():
        raise FileNotFoundError(f"Нет данных: {path}. Запустите: tendencia collect --quarter {quarter}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [SourceItem(**row) for row in raw]


def load_trends(quarter: Quarter) -> tuple[list[SourceItem], list[TrendItem]]:
    """Загрузить тренды из findings.json или пересобрать из sources.json."""
    findings = data_dir(quarter) / "findings.json"
    if findings.exists():
        payload = json.loads(findings.read_text(encoding="utf-8"))
        sources = [SourceItem(**row) for row in payload.get("sources", [])]
        trends: list[TrendItem] = []
        for row in payload.get("trends", []):
            src_rows = row.pop("sources", [])
            trend = TrendItem(**row)
            trend.sources = [SourceItem(**s) for s in src_rows]
            trends.append(trend)
        return sources, apply_curated(trends)

    sources = load_sources(quarter)
    topics_cfg = load_yaml("topics.yaml")
    trends = build_trend_candidates(
        sources,
        topics_cfg,
        max_trends=topics_cfg.get("report", {}).get("trend_count", 10),
    )
    return sources, apply_curated(trends)
