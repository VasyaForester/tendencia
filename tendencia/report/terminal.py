"""Человекочитаемый вывод отчёта в терминал."""

from __future__ import annotations

import sys
from datetime import date

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from tendencia.models import TrendItem
from tendencia.quarter import Quarter

CONFIDENCE_STYLE = {
    "High": "bold green",
    "Medium": "bold yellow",
    "Low": "bold red",
}

RECOMMENDATIONS = [
    "Инвентаризация agent tools — каталог MCP/skills, owner, scope permissions.",
    "Разделение trusted/untrusted контекста для RAG и browser/email tools.",
    "Запрет неконтролируемого self-modification — approval на новые skills.",
    "Маппинг на AI Act / NIST AI RMF для high-risk use cases.",
    "Red-teaming агентных сценариев: indirect injection + tool chain.",
]


def _confidence_text(confidence: str) -> Text:
    return Text(confidence, style=CONFIDENCE_STYLE.get(confidence, ""))


def format_plain_text(
    quarter: Quarter,
    trends: list[TrendItem],
    source_count: int,
    *,
    brief: bool = False,
    max_sources: int = 3,
) -> str:
    """Плоский текст без ANSI-разметки (для перенаправления в файл)."""
    lines = [
        f"Тренды AI Security ({quarter}) — Executive Brief",
        f"Период: {quarter.start} — {quarter.end}",
        f"Сравнение: vs {quarter.previous()}",
        f"Дата: {date.today().isoformat()}",
        f"Источников: {source_count}",
        "",
        "КРАТКОЕ РЕЗЮМЕ",
        "-" * 60,
    ]
    for i, trend in enumerate(trends, 1):
        lines.append(
            f"{i}. {trend.title_ru} [{trend.confidence}]"
        )
        lines.append(f"   {trend.why_matters_ru}")
        lines.append(f"   Затронуты: {trend.who_affected_ru}")
        lines.append("")

    if brief:
        return "\n".join(lines)

    lines.extend(["", "ДЕТАЛИ ПО ТРЕНДАМ", "-" * 60])
    for i, trend in enumerate(trends, 1):
        lines.extend([
            "",
            f"{i}. {trend.title_ru} (уверенность: {trend.confidence})",
            "",
            trend.summary_ru,
            "",
            f"Изменение vs {quarter.previous()}: {trend.changed_vs_prev_quarter_ru}",
            f"Почему важно: {trend.why_matters_ru}",
            f"Кому актуально: {trend.who_affected_ru}",
        ])
        if trend.sources:
            lines.append("Источники:")
            for src in trend.sources[:max_sources]:
                pub = f", {src.published}" if src.published else ""
                lines.append(f"  - {src.title} ({src.source_type}{pub})")
                lines.append(f"    {src.url}")

    lines.extend(["", "РЕКОМЕНДАЦИИ", "-" * 60])
    for i, rec in enumerate(RECOMMENDATIONS, 1):
        lines.append(f"{i}. {rec}")

    return "\n".join(lines)


def print_terminal_report(
    quarter: Quarter,
    trends: list[TrendItem],
    source_count: int,
    *,
    console: Console | None = None,
    brief: bool = False,
    plain: bool = False,
    max_sources: int = 3,
) -> None:
    """Печать отчёта в терминал (rich или plain text)."""
    if plain:
        text = format_plain_text(
            quarter, trends, source_count, brief=brief, max_sources=max_sources
        )
        sys.stdout.write(text + "\n")
        return

    out = console or Console(force_terminal=True, legacy_windows=False)

    header = (
        f"[bold]Тренды AI Security[/bold] ({quarter})\n"
        f"Период: {quarter.start} — {quarter.end}\n"
        f"Сравнение: vs {quarter.previous()}\n"
        f"Источников: {source_count}"
    )
    out.print(Panel(header, title="Tendencia", border_style="cyan"))

    out.print(Rule("Краткое резюме для руководства"))
    table = Table(show_header=True, header_style="bold", expand=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Тренд", ratio=2)
    table.add_column("Уверенность", width=10)
    table.add_column("Суть", ratio=4)

    for i, trend in enumerate(trends, 1):
        table.add_row(
            str(i),
            trend.title_ru,
            _confidence_text(trend.confidence),
            trend.why_matters_ru,
        )
    out.print(table)

    if brief:
        return

    out.print(Rule(f"Детали (vs {quarter.previous()})"))
    for i, trend in enumerate(trends, 1):
        body = (
            f"{trend.summary_ru}\n\n"
            f"[bold]Изменение:[/bold] {trend.changed_vs_prev_quarter_ru}\n"
            f"[bold]Затронуты:[/bold] {trend.who_affected_ru}"
        )
        out.print(
            Panel(
                body,
                title=f"{i}. {trend.title_ru}",
                subtitle=f"Уверенность: {trend.confidence}",
                border_style="blue",
            )
        )
        if trend.sources:
            out.print("[dim]Источники:[/dim]")
            for src in trend.sources[:max_sources]:
                pub = f" ({src.published})" if src.published else ""
                out.print(f"  • [link={src.url}]{src.title}[/link] — {src.source_type}{pub}")

    out.print(Rule("Приоритетные рекомендации"))
    for i, rec in enumerate(RECOMMENDATIONS, 1):
        out.print(f"  [bold cyan]{i}.[/bold cyan] {rec}")


def print_markdown_file(path: str, *, console: Console | None = None) -> None:
    """Вывод готового Markdown-файла отчёта в терминал."""
    from pathlib import Path

    text = Path(path).read_text(encoding="utf-8")
    out = console or Console(force_terminal=True, legacy_windows=False)
    out.print(Markdown(text))
