"""Модели данных для источников и трендов."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

SourceType = Literal[
    "gov_cert",
    "standards",
    "papers",
    "vendor",
    "incidents",  # формат: отчёт об инциденте/CVE, не тематический тренд
    "news",
    "social",
    "user_upload",  # формат: добавлено пользователем (ссылка / PDF)
    "unknown",
]

Confidence = Literal["High", "Medium", "Low"]


@dataclass
class SourceItem:
    title: str
    url: str
    published: str | None = None
    summary: str = ""
    source_type: SourceType = "unknown"
    origin: str = ""
    relevance_score: float = 0.0
    matched_topics: list[str] = field(default_factory=list)  # theme ids (см. taxonomy.py)


@dataclass
class TrendItem:
    id: str
    title_ru: str
    summary_ru: str
    why_matters_ru: str
    who_affected_ru: str
    confidence: Confidence
    changed_vs_prev_quarter_ru: str
    sources: list[SourceItem] = field(default_factory=list)
    attack_surface: str = "governance"
