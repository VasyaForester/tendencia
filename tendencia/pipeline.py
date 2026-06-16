"""Общий pipeline объединения и ранжирования источников."""

from __future__ import annotations

from tendencia.analysis.ranker import rank_and_tag_sources
from tendencia.models import SourceItem
from tendencia.quarter import Quarter
from tendencia.seed_sources import Q2_2026_SEEDS
from tendencia.uploads.collector import merge_user_uploads


def finalize_sources(
    sources: list[SourceItem],
    quarter: Quarter,
    topics_cfg: dict,
    *,
    include_seeds: bool = True,
    include_uploads: bool = True,
) -> list[SourceItem]:
    merged = list(sources)

    if include_uploads:
        merged = merge_user_uploads(merged, quarter)

    if include_seeds and quarter.label == "2026-Q2":
        seen = {s.url for s in merged}
        for seed in Q2_2026_SEEDS:
            if seed.url not in seen:
                merged.append(seed)
                seen.add(seed.url)

    return rank_and_tag_sources(merged, topics_cfg)
