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
from tendencia.report.generator import generate_report, save_findings
from tendencia.seed_sources import Q2_2026_SEEDS

console = Console(force_terminal=True, legacy_windows=False)


def _data_dir(quarter: Quarter) -> Path:
    return project_root() / "data" / quarter.label


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
    out = _data_dir(quarter) / "sources.json"
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
    data_path = _data_dir(quarter) / "sources.json"

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

    findings_path = _data_dir(quarter) / "findings.json"
    save_findings(findings_path, quarter, sources, trends)

    report_path = project_root() / "reports" / quarter.label / "ai-security-trends.md"
    generate_report(quarter, trends, sources, report_path)

    console.print(f"[green]Отчёт: {report_path}[/green]")
    console.print(f"[green]Findings: {findings_path}[/green]")
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
    p_report.set_defaults(func=cmd_report)

    p_run = sub.add_parser("run", parents=[common], help="collect + report")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
