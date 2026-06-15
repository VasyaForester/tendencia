"""Формирование трендов только по тематической таксономии."""

from __future__ import annotations

from collections import defaultdict

from tendencia.models import Confidence, SourceItem, TrendItem
from tendencia.taxonomy import (
    attack_surface_for_theme,
    detect_themes,
    load_theme_definitions,
    primary_theme,
    theme_labels,
)


def _confidence_from_sources(sources: list[SourceItem]) -> Confidence:
    if len(sources) >= 3 and any(s.source_type in ("gov_cert", "standards", "papers") for s in sources):
        return "High"
    if len(sources) >= 2:
        return "Medium"
    return "Low"


def _best_sources_for_theme(
    all_sources: list[SourceItem],
    theme_id: str,
    matched: list[SourceItem],
) -> list[SourceItem]:
    explicit = [s for s in all_sources if theme_id in detect_themes(s)]
    primary = [
        s
        for s in explicit
        if s.relevance_score >= 1.15
        or s.source_type in ("gov_cert", "standards", "papers", "vendor", "incidents")
    ]
    pool = primary or explicit or matched
    return sorted(pool, key=lambda s: s.relevance_score, reverse=True)


def build_trend_candidates(
    sources: list[SourceItem],
    topics_cfg: dict,
    max_trends: int = 10,
) -> list[TrendItem]:
    themes = load_theme_definitions(topics_cfg)
    labels = theme_labels(topics_cfg)
    by_theme: dict[str, list[SourceItem]] = defaultdict(list)

    for src in sources:
        for theme_id in detect_themes(src, topics_cfg):
            by_theme[theme_id].append(src)

    trends: list[TrendItem] = []
    for theme in themes:
        if len(trends) >= max_trends:
            break
        tid = theme["id"]
        theme_sources = _best_sources_for_theme(sources, tid, by_theme.get(tid, []))[:6]
        if not theme_sources:
            continue
        trends.append(
            TrendItem(
                id=tid,
                title_ru=labels[tid],
                summary_ru=_auto_summary(theme_sources),
                why_matters_ru="Тематический сигнал квартала по собранным источникам.",
                who_affected_ru="См. детальный разбор и список источников.",
                confidence=_confidence_from_sources(theme_sources),
                changed_vs_prev_quarter_ru="Сравнение с предыдущим кварталом — в курированном слое отчёта.",
                sources=theme_sources,
                attack_surface=attack_surface_for_theme(tid, topics_cfg),
            )
        )

    return trends


def _auto_summary(sources: list[SourceItem]) -> str:
    if not sources:
        return "Источники за квартал не найдены автоматическим сбором."
    parts = [f"• {s.title}" for s in sources[:3]]
    return "Ключевые сигналы:\n" + "\n".join(parts)
