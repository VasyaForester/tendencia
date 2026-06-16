"""Ранжирование и тегирование источников по темам."""

from __future__ import annotations

import re

from tendencia.models import SourceItem
from tendencia.taxonomy import detect_themes, load_theme_definitions

SOURCE_TYPE_WEIGHT = {
    "gov_cert": 1.0,
    "standards": 0.95,
    "papers": 0.85,
    "vendor": 0.8,
    "incidents": 0.9,
    "user_upload": 1.0,
    "news": 0.5,
    "social": 0.35,
    "unknown": 0.4,
}

SECURITY_TERMS = re.compile(
    r"\b(security|cyber|threat|vulnerab|attack|injection|jailbreak|"
    r"exfil|poison|agent|llm|mcp|compliance|ai act|governance|sandbox)\b",
    re.I,
)


def rank_and_tag_sources(sources: list[SourceItem], topics_cfg: dict) -> list[SourceItem]:
    ranked: list[SourceItem] = []

    for src in sources:
        blob = f"{src.title} {src.summary} {src.url}"
        score = SOURCE_TYPE_WEIGHT.get(src.source_type, 0.4)
        if SECURITY_TERMS.search(blob):
            score += 0.15

        matched = sorted(detect_themes(src, topics_cfg))
        score += 0.2 * min(len(matched), 3)

        src.matched_topics = matched
        src.relevance_score = round(min(score, 1.5), 3)
        ranked.append(src)

    ranked.sort(key=lambda s: s.relevance_score, reverse=True)
    return ranked
