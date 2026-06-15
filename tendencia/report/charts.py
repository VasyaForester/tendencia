"""Графики: темы и форматы публикаций — в разных визуализациях."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from tendencia.config_loader import project_root
from tendencia.models import SourceItem
from tendencia.quarter import Quarter
from tendencia.taxonomy import (
    FORMAT_CHART_COLORS,
    SOURCE_FORMAT_LABELS,
    SOURCE_FORMAT_ORDER,
    THEME_CHART_COLORS,
    primary_theme,
    theme_labels,
    theme_priority,
)

LEGACY_THEME_ALIASES = {
    "rag_attacks": "rag_data_layer",
    "supply_chain": "model_supply_chain",
    "mcp_supply_chain": "model_supply_chain",
    "agent_gateways": "agent_runtime_governance",
}


@dataclass
class ChartPaths:
    theme_weekly: Path
    theme_totals: Path
    source_formats: Path
    theme_by_format: Path


def charts_dir(quarter: Quarter) -> Path:
    return project_root() / "reports" / quarter.label / "charts"


def _parse_published(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _week_starts(quarter: Quarter) -> list[date]:
    weeks: list[date] = []
    current = quarter.start
    while current <= quarter.end:
        weeks.append(current)
        current += timedelta(days=7)
    return weeks


def _week_index(weeks: list[date], day: date) -> int:
    for i, start in enumerate(weeks):
        if start + timedelta(days=6) >= day:
            return i
    return len(weeks) - 1


def _dated_sources(sources: list[SourceItem], quarter: Quarter) -> list[SourceItem]:
    result = []
    for src in sources:
        pub = _parse_published(src.published)
        if pub and quarter.contains(pub):
            result.append(src)
    return result


def build_theme_weekly_series(
    sources: list[SourceItem],
    quarter: Quarter,
) -> tuple[list[date], dict[str, list[int]]]:
    weeks = _week_starts(quarter)
    series: dict[str, list[int]] = {tid: [0] * len(weeks) for tid in theme_priority()}
    for src in _dated_sources(sources, quarter):
        theme = primary_theme(src)
        if not theme:
            continue
        theme = LEGACY_THEME_ALIASES.get(theme, theme)
        if theme not in series:
            continue
        idx = _week_index(weeks, _parse_published(src.published))  # type: ignore[arg-type]
        series[theme][idx] += 1
    active = {k: v for k, v in series.items() if sum(v) > 0}
    return weeks, active


def build_theme_totals(sources: list[SourceItem], quarter: Quarter) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for src in _dated_sources(sources, quarter):
        theme = primary_theme(src)
        if theme:
            totals[LEGACY_THEME_ALIASES.get(theme, theme)] += 1
    return dict(totals)


def build_format_counts(sources: list[SourceItem]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for src in sources:
        counts[src.source_type] += 1
    ordered = [k for k in SOURCE_FORMAT_ORDER if counts.get(k)]
    return {k: counts[k] for k in ordered}


def build_theme_format_matrix(
    sources: list[SourceItem],
    quarter: Quarter,
) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for src in _dated_sources(sources, quarter):
        theme = primary_theme(src)
        if not theme:
            continue
        theme = LEGACY_THEME_ALIASES.get(theme, theme)
        matrix[theme][src.source_type] += 1
    return {k: dict(v) for k, v in matrix.items()}


def _setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "#FFFFFF",
            "axes.facecolor": "#F7FAFC",
            "axes.edgecolor": "#CBD5E0",
            "grid.color": "#E2E8F0",
            "grid.linestyle": "--",
            "grid.alpha": 0.7,
        }
    )


def _save_fig(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def _short_label(text: str, max_len: int = 30) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def render_theme_weekly_chart(
    weeks: list[date],
    series: dict[str, list[int]],
    quarter: Quarter,
    output: Path,
) -> Path:
    _setup_style()
    labels = theme_labels()
    fig, ax = plt.subplots(figsize=(8.5, 4.2))

    for theme_id, counts in series.items():
        color = THEME_CHART_COLORS.get(theme_id, "#718096")
        cumulative: list[int] = []
        total = 0
        for c in counts:
            total += c
            cumulative.append(total)
        ax.plot(
            weeks,
            cumulative,
            marker="o",
            linewidth=2.2,
            markersize=4,
            label=_short_label(labels.get(theme_id, theme_id)),
            color=color,
        )
        ax.plot(weeks, counts, linestyle="--", linewidth=1.2, alpha=0.45, color=color)

    ax.set_title(f"Динамика публикаций по темам · {quarter}")
    ax.set_xlabel("Неделя квартала")
    ax.set_ylabel("Источников (1 главная тема на публикацию)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    fig.autofmt_xdate(rotation=30)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, axis="y")
    ax.legend(loc="upper left", fontsize=7, framealpha=0.9, title="Сплошная — накопительно")
    fig.text(
        0.01,
        0.01,
        "Пунктир — новые публикации за неделю. Каждый источник отнесён к одной главной теме.",
        fontsize=7,
        color="#718096",
    )
    return _save_fig(fig, output)


def render_theme_totals_chart(
    totals: dict[str, int],
    quarter: Quarter,
    output: Path,
) -> Path:
    _setup_style()
    labels = theme_labels()
    priority = theme_priority()
    items = [(tid, totals[tid]) for tid in priority if totals.get(tid)]
    items = sorted(items, key=lambda x: x[1], reverse=True)
    names = [_short_label(labels.get(k, k), 34) for k, _ in items]
    values = [v for _, v in items]
    colors = [THEME_CHART_COLORS.get(k, "#718096") for k, _ in items]

    fig, ax = plt.subplots(figsize=(8.5, 4.0))
    bars = ax.barh(names[::-1], values[::-1], color=colors[::-1], height=0.65)
    ax.set_title(f"Объём публикаций по темам · {quarter}")
    ax.set_xlabel("Источников с датой (уникальная главная тема)")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, axis="x")
    for bar, val in zip(bars, values[::-1]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, str(val), va="center", fontsize=8)
    return _save_fig(fig, output)


def render_source_formats_chart(sources: list[SourceItem], quarter: Quarter, output: Path) -> Path:
    _setup_style()
    counts = build_format_counts(sources)
    labels = [SOURCE_FORMAT_LABELS.get(k, k) for k in counts]
    values = list(counts.values())
    colors = [FORMAT_CHART_COLORS.get(k, "#CBD5E0") for k in counts]

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    wedges, _, autotexts = ax.pie(
        values,
        labels=labels,
        autopct=lambda p: f"{p:.0f}%" if p >= 4 else "",
        startangle=90,
        colors=colors,
        pctdistance=0.75,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    for t in autotexts:
        t.set_fontsize(8)
        t.set_color("white")
        t.set_fontweight("bold")
    ax.set_title(f"Формат публикаций (тип источника) · {quarter}\n(n={len(sources)})")
    return _save_fig(fig, output)


def render_theme_by_format_chart(
    matrix: dict[str, dict[str, int]],
    quarter: Quarter,
    output: Path,
) -> Path:
    _setup_style()
    labels = theme_labels()
    priority = [tid for tid in theme_priority() if tid in matrix]
    priority = sorted(priority, key=lambda t: sum(matrix[t].values()), reverse=True)[:7]
    format_keys = [k for k in SOURCE_FORMAT_ORDER if any(matrix[t].get(k) for t in priority)]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    y_pos = range(len(priority))
    left = [0.0] * len(priority)

    for fmt in format_keys:
        vals = [matrix[t].get(fmt, 0) for t in priority]
        ax.barh(
            list(y_pos),
            vals,
            left=left,
            height=0.6,
            label=SOURCE_FORMAT_LABELS.get(fmt, fmt),
            color=FORMAT_CHART_COLORS.get(fmt, "#CBD5E0"),
        )
        left = [l + v for l, v in zip(left, vals)]

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels([_short_label(labels.get(t, t), 36) for t in priority], fontsize=8)
    ax.set_xlabel("Количество публикаций")
    ax.set_title(f"Тема × формат публикации · {quarter}")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(loc="lower right", fontsize=7, framealpha=0.9, title="Формат")
    ax.grid(True, axis="x")
    fig.text(
        0.01,
        0.01,
        "Одна публикация = одна главная тема; цвет сегмента = формат (исследование, advisory, CVE-отчёт…).",
        fontsize=7,
        color="#718096",
    )
    return _save_fig(fig, output)


def generate_charts(quarter: Quarter, sources: list[SourceItem]) -> ChartPaths:
    out_dir = charts_dir(quarter)
    weeks, series = build_theme_weekly_series(sources, quarter)
    totals = build_theme_totals(sources, quarter)
    matrix = build_theme_format_matrix(sources, quarter)

    return ChartPaths(
        theme_weekly=render_theme_weekly_chart(weeks, series, quarter, out_dir / "theme_weekly.png"),
        theme_totals=render_theme_totals_chart(totals, quarter, out_dir / "theme_totals.png"),
        source_formats=render_source_formats_chart(sources, quarter, out_dir / "source_formats.png"),
        theme_by_format=render_theme_by_format_chart(matrix, quarter, out_dir / "theme_by_format.png"),
    )
