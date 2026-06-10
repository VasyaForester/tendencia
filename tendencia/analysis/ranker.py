"""Ранжирование и тегирование источников по темам."""

from __future__ import annotations

import re

from tendencia.models import SourceItem

SOURCE_TYPE_WEIGHT = {
    "gov_cert": 1.0,
    "standards": 0.95,
    "papers": 0.85,
    "vendor": 0.8,
    "incidents": 0.9,
    "news": 0.5,
    "social": 0.35,
    "unknown": 0.4,
}

SECURITY_TERMS = re.compile(
    r"\b(security|cyber|threat|vulnerab|attack|injection|jailbreak|"
    r"exfil|poison|agent|llm|mcp|compliance|ai act|governance|sandbox)\b",
    re.I,
)


def _topic_match(text: str, keywords: list[str]) -> bool:
    lower = text.lower()
    return any(kw.lower() in lower for kw in keywords)


def rank_and_tag_sources(sources: list[SourceItem], topics_cfg: dict) -> list[SourceItem]:
    must_include = topics_cfg.get("must_include", [])
    ranked: list[SourceItem] = []

    for src in sources:
        blob = f"{src.title} {src.summary} {src.url}"
        score = SOURCE_TYPE_WEIGHT.get(src.source_type, 0.4)
        if SECURITY_TERMS.search(blob):
            score += 0.15

        matched: list[str] = []
        for topic in must_include:
            if _topic_match(blob, topic.get("keywords", [])):
                matched.append(topic["id"])
                score += 0.25

        src.matched_topics = matched
        src.relevance_score = round(min(score, 1.5), 3)
        ranked.append(src)

    ranked.sort(key=lambda s: s.relevance_score, reverse=True)
    return ranked
