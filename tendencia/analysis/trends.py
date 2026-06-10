"""Формирование кандидатов в тренды из источников."""

from __future__ import annotations

from collections import defaultdict

from tendencia.models import Confidence, SourceItem, TrendItem


def _confidence_from_sources(sources: list[SourceItem]) -> Confidence:
    if len(sources) >= 3 and any(s.source_type in ("gov_cert", "standards", "papers") for s in sources):
        return "High"
    if len(sources) >= 2:
        return "Medium"
    return "Low"


def _best_sources_for_topic(
    all_sources: list[SourceItem],
    topic_id: str,
    matched: list[SourceItem],
) -> list[SourceItem]:
    explicit = [s for s in all_sources if topic_id in s.matched_topics]
    primary = [
        s
        for s in explicit
        if s.relevance_score >= 1.15
        or s.source_type in ("gov_cert", "standards", "incidents", "vendor")
    ]
    pool = primary or explicit or matched
    return sorted(pool, key=lambda s: s.relevance_score, reverse=True)


def build_trend_candidates(
    sources: list[SourceItem],
    topics_cfg: dict,
    max_trends: int = 10,
) -> list[TrendItem]:
    must_include = topics_cfg.get("must_include", [])
    by_topic: dict[str, list[SourceItem]] = defaultdict(list)

    for src in sources:
        for topic_id in src.matched_topics:
            by_topic[topic_id].append(src)

    trends: list[TrendItem] = []
    used_urls: set[str] = set()

    for topic in must_include:
        tid = topic["id"]
        topic_sources = _best_sources_for_topic(sources, tid, by_topic.get(tid, []))[:5]
        for s in topic_sources:
            used_urls.add(s.url)
        if not topic_sources:
            continue
        trends.append(
            TrendItem(
                id=tid,
                title_ru=topic["title_ru"],
                summary_ru=_auto_summary(topic_sources),
                why_matters_ru="Тема отмечена как приоритетная для квартального обзора.",
                who_affected_ru="Организации, внедряющие LLM и AI-агентов.",
                confidence=_confidence_from_sources(topic_sources),
                changed_vs_prev_quarter_ru="Требует верификации по сравнению с предыдущим кварталом.",
                sources=topic_sources,
                attack_surface=_surface_for_topic(tid),
            )
        )

    # Дополнительные тренды из высокорелевантных источников без явной темы
    general = [s for s in sources if s.url not in used_urls and s.relevance_score >= 0.7]
    clusters = _cluster_general(general)
    for cluster_id, cluster_sources in clusters.items():
        if len(trends) >= max_trends:
            break
        trends.append(
            TrendItem(
                id=cluster_id,
                title_ru=_title_for_cluster(cluster_id),
                summary_ru=_auto_summary(cluster_sources[:4]),
                why_matters_ru="Повторяющийся сигнал в собранных источниках квартала.",
                who_affected_ru="Команды безопасности и владельцы AI-продуктов.",
                confidence=_confidence_from_sources(cluster_sources),
                changed_vs_prev_quarter_ru="См. сравнение с предыдущим кварталом в полном отчёте.",
                sources=cluster_sources[:5],
                attack_surface="model_prompt",
            )
        )

    # Дополняем до max_trends курированными слотами Q2 2026
    extra_order = [
        "mcp_supply_chain",
        "agent_gateways",
        "zombie_memory",
        "incidents",
        "emerging_signals",
    ]
    existing_ids = {t.id for t in trends}
    for extra_id in extra_order:
        if len(trends) >= max_trends:
            break
        if extra_id in existing_ids:
            continue
        related = [s for s in sources if extra_id in s.matched_topics or _matches_extra(s, extra_id)]
        trends.append(
            TrendItem(
                id=extra_id,
                title_ru=_title_for_extra(extra_id),
                summary_ru=_auto_summary(related[:4]),
                why_matters_ru="Курированный тренд квартала на основе первичных источников.",
                who_affected_ru="См. полный отчёт.",
                confidence=_confidence_from_sources(related),
                changed_vs_prev_quarter_ru="См. сравнение с предыдущим кварталом.",
                sources=related[:5],
                attack_surface="agents_tools",
            )
        )
        existing_ids.add(extra_id)

    return trends[:max_trends]


def _matches_extra(src: SourceItem, extra_id: str) -> bool:
    blob = f"{src.title} {src.summary}".lower()
    rules = {
        "mcp_supply_chain": ["supply chain", "npm", "cve", "shodan", "secrets"],
        "agent_gateways": ["gateway", "transport layer", "default-deny", "policy"],
        "zombie_memory": ["zombie", "persistent", "long-term memory", "memory"],
        "incidents": ["cve-", "incident", "rce", "ox security"],
    }
    return any(kw in blob for kw in rules.get(extra_id, []))


def _title_for_extra(extra_id: str) -> str:
    titles = {
        "mcp_supply_chain": "MCP как новый software supply chain",
        "agent_gateways": "Agent gateways и enforcement на transport layer",
        "zombie_memory": "Zombie agents и persistent memory attacks",
        "incidents": "CVE и инциденты в AI coding assistants",
        "emerging_signals": "Ранние сигналы (autonomous worms, multi-agent trust)",
    }
    return titles.get(extra_id, extra_id)


def _surface_for_topic(topic_id: str) -> str:
    mapping = {
        "self_evolving_agents": "agents_tools",
        "ai_regulation": "governance",
        "agent_tools": "agents_tools",
    }
    return mapping.get(topic_id, "governance")


def _auto_summary(sources: list[SourceItem]) -> str:
    if not sources:
        return "Источники за квартал не найдены автоматическим сбором."
    parts = [f"• {s.title}" for s in sources[:3]]
    return "Ключевые сигналы:\n" + "\n".join(parts)


def _cluster_general(sources: list[SourceItem]) -> dict[str, list[SourceItem]]:
    clusters: dict[str, list[SourceItem]] = defaultdict(list)
    rules = [
        ("prompt_injection", ["prompt injection", "indirect prompt", "jailbreak"]),
        ("rag_attacks", ["rag", "retrieval", "poisoning", "data leakage"]),
        ("supply_chain", ["supply chain", "model weights", "backdoor", "tamper"]),
        ("incidents", ["incident", "breach", "exploit", "abuse"]),
    ]
    for src in sources:
        blob = f"{src.title} {src.summary}".lower()
        placed = False
        for cluster_id, kws in rules:
            if any(kw in blob for kw in kws):
                clusters[cluster_id].append(src)
                placed = True
                break
        if not placed:
            clusters["emerging_signals"].append(src)
    return {k: v for k, v in clusters.items() if v}


def _title_for_cluster(cluster_id: str) -> str:
    titles = {
        "prompt_injection": "Prompt injection и обход политик моделей",
        "rag_attacks": "Атаки на RAG и слой данных",
        "supply_chain": "Риски supply chain моделей и артефактов",
        "incidents": "Инциденты и злоупотребления в продакшене",
        "emerging_signals": "Новые сигналы в ландшафте AI Security",
    }
    return titles.get(cluster_id, "Прочие тренды")
