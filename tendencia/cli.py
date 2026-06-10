"""CLI для квартального мониторинга AI Security трендов."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console

from tendencia.analysis.ranker import rank_and_tag_sources
from tendencia.analysis.trends import build_trend_candidates
from tendencia.collectors import collect_arxiv, collect_ddg, collect_rss
from tendencia.config_loader import load_yaml, project_root
from tendencia.quarter import Quarter
from tendencia.loaders import data_dir, load_trends, pdf_path, report_path
from tendencia.report.generator import generate_report, save_findings
from tendencia.report.pdf_report import generate_pdf
from tendencia.report.terminal import format_plain_text, print_markdown_file, print_terminal_report
from tendencia.seed_sources import Q2_2026_SEEDS

console = Console(force_terminal=True, legacy_windows=False)


def _add_output_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--print",
        action="store_true",
        help="Вывести отчёт в терминал после генерации",
    )
    parser.add_argument(
        "--brief",
        action="store_true",
        help="Только краткое резюме (без деталей по трендам)",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="Плоский текст без ANSI-цветов (удобно для > file.txt)",
    )


def cmd_collect(args: argparse.Namespace) -> int:
    quarter = Quarter.parse(args.quarter)
    sources_cfg = load_yaml("sources.yaml")
    topics_cfg = load_yaml("topics.yaml")

    all_sources = []
    console.print("Сбор RSS-лент...")
    all_sources.extend(collect_rss(sources_cfg.get("rss_feeds", []), quarter))
    console.print("Сбор arXiv...")
    all_sources.extend(collect_arxiv(sources_cfg.get("arxiv_queries", []), quarter))
    console.print("Поиск DuckDuckGo...")
    all_sources.extend(collect_ddg(sources_cfg.get("search_queries", [])))

    if quarter.label == "2026-Q2":
        seen = {s.url for s in all_sources}
        for seed in Q2_2026_SEEDS:
            if seed.url not in seen:
                all_sources.append(seed)
                seen.add(seed.url)

    ranked = rank_and_tag_sources(all_sources, topics_cfg)
    out = data_dir(quarter) / "sources.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps([s.__dict__ for s in ranked], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    console.print(f"[green]Собрано {len(ranked)} источников → {out}[/green]")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    quarter = Quarter.parse(args.quarter)
    topics_cfg = load_yaml("topics.yaml")
    data_path = data_dir(quarter) / "sources.json"

    if not data_path.exists():
        console.print("[red]Сначала выполните: tendencia collect --quarter", quarter.label, "[/red]")
        return 1

    raw = json.loads(data_path.read_text(encoding="utf-8"))
    from tendencia.models import SourceItem

    sources = [SourceItem(**row) for row in raw]
    trends = build_trend_candidates(
        sources,
        topics_cfg,
        max_trends=topics_cfg.get("report", {}).get("trend_count", 10),
    )

    findings_path = data_dir(quarter) / "findings.json"
    save_findings(findings_path, quarter, sources, trends)

    md_path = report_path(quarter)
    generate_report(quarter, trends, sources, md_path)

    console.print(f"[green]Отчёт: {md_path}[/green]")
    console.print(f"[green]Findings: {findings_path}[/green]")

    if args.print:
        _print_report(quarter, trends, len(sources), args)
    return 0


def _print_report(
    quarter: Quarter,
    trends: list,
    source_count: int,
    args: argparse.Namespace,
) -> None:
    print_terminal_report(
        quarter,
        trends,
        source_count,
        console=console,
        brief=args.brief,
        plain=args.plain,
    )


def cmd_show(args: argparse.Namespace) -> int:
    quarter = Quarter.parse(args.quarter)

    if args.from_markdown:
        md = report_path(quarter)
        if not md.exists():
            console.print(f"[red]Markdown-отчёт не найден: {md}[/red]")
            return 1
        if args.plain:
            sys.stdout.write(md.read_text(encoding="utf-8") + "\n")
        else:
            print_markdown_file(str(md), console=console)
        return 0

    try:
        sources, trends = load_trends(quarter)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    if args.output:
        text = format_plain_text(
            quarter,
            trends,
            len(sources),
            brief=args.brief,
        )
        Path(args.output).write_text(text, encoding="utf-8")
        console.print(f"[green]Сохранено: {args.output}[/green]")
        return 0

    _print_report(quarter, trends, len(sources), args)
    return 0


def cmd_pdf(args: argparse.Namespace) -> int:
    quarter = Quarter.parse(args.quarter)
    try:
        sources, trends = load_trends(quarter)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    out = Path(args.output) if args.output else pdf_path(quarter)
    generate_pdf(quarter, trends, sources, out)
    console.print(f"[green]PDF: {out}[/green]")

    if args.open:
        import os
        import subprocess

        if sys.platform == "win32":
            os.startfile(out)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(out)], check=False)
        else:
            subprocess.run(["xdg-open", str(out)], check=False)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if cmd_collect(args) != 0:
        return 1
    return cmd_report(args)


def main(argv: list[str] | None = None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--quarter",
        default="2026-Q2",
        help="Квартал в формате YYYY-QN (по умолчанию 2026-Q2)",
    )

    parser = argparse.ArgumentParser(
        prog="tendencia",
        description="Квартальный мониторинг трендов AI Security",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_collect = sub.add_parser("collect", parents=[common], help="Собрать источники")
    p_collect.set_defaults(func=cmd_collect)

    p_report = sub.add_parser("report", parents=[common], help="Сгенерировать отчёт из sources.json")
    _add_output_flags(p_report)
    p_report.set_defaults(func=cmd_report)

    p_run = sub.add_parser("run", parents=[common], help="collect + report")
    _add_output_flags(p_run)
    p_run.set_defaults(func=cmd_run)

    p_show = sub.add_parser("show", parents=[common], help="Показать отчёт в терминале")
    _add_output_flags(p_show)
    p_show.add_argument(
        "--from-markdown",
        action="store_true",
        help="Вывести готовый Markdown-файл вместо структурированного вида",
    )
    p_show.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Сохранить plain-text в файл (без ANSI)",
    )
    p_show.set_defaults(func=cmd_show)

    p_pdf = sub.add_parser("pdf", parents=[common], help="Создать подробный PDF-отчёт")
    p_pdf.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Путь к PDF (по умолчанию reports/<quarter>/ai-security-trends.pdf)",
    )
    p_pdf.add_argument(
        "--open",
        action="store_true",
        help="Открыть PDF после создания",
    )
    p_pdf.set_defaults(func=cmd_pdf)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
