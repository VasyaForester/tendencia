"""Генерация Markdown-отчёта для executive-аудитории."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tendencia.config_loader import project_root
from tendencia.models import SourceItem, TrendItem
from tendencia.quarter import Quarter

# Экспертный слой: курированные формулировки для Q2 2026 (обновляются при каждом прогоне)
CURATED_Q2_2026: dict[str, dict[str, str]] = {
    "self_evolving_agents": {
        "summary_ru": (
            "Self-evolving agents вышли из research в зону production-рисков. Исследования Q2 2026 "
            "формализуют «Zombie Agents» (persistent memory injection) и «misevolution» — непреднамеренную "
            "деградацию alignment при эволюции memory/tools/workflow. Unit 42 показал poisoning "
            "долговременной памяти: вредоносные инструкции переживают сессии и приоритизируются над user input."
        ),
        "why_matters_ru": (
            "Поведение агента меняется без релиза: новая поверхность для APT и insider-style атак. "
            "Классический change control и периметр не видят «тихую» эволюцию policy в memory."
        ),
        "who_affected_ru": "Владельцы agentic платформ, SOC, команды с long-term memory (coding/research agents).",
        "changed_vs_prev_quarter_ru": (
            "Vs Q1 2026: от концептуальных surveys к эмпирическим работам (ICLR 2026 misevolution, "
            "Zombie Agents) и vendor PoC по memory poisoning."
        ),
        "confidence": "High",
    },
    "ai_regulation": {
        "summary_ru": (
            "В Q2 2026 EU согласовала Digital Omnibus: сроки high-risk obligations сдвинуты "
            "(Annex III → 2 Dec 2027, product-embedded → 2 Aug 2028), но Article 15 (accuracy, "
            "robustness, cybersecurity) остаётся ядром — data/model poisoning, adversarial examples. "
            "Связка с Cyber Resilience Act уточняется на уровне Council."
        ),
        "why_matters_ru": (
            "Даже при отсрочке штрафных рамок организации должны проектировать agent/RAG-архитектуру "
            "под lifecycle security и post-market monitoring — иначе дорогой rework в 2027."
        ),
        "who_affected_ru": "Compliance, legal, product owners в EU; глобальные вендоры с EU-клиентами.",
        "changed_vs_prev_quarter_ru": (
            "Vs Q1 2026: политический deal 7 May 2026 заменил «дедлайн паники» на фазовое планирование; "
            "фокус CISO — mapping technical controls на Art. 15."
        ),
        "confidence": "High",
    },
    "agent_tools": {
        "summary_ru": (
            "MCP стал de-facto стандартом tool-use (Cursor, Windsurf, VS Code). Q2 2026 — волна CVE "
            "(вкл. CVE-2026-30615 zero-click RCE в Windsurf), CSA notes по STDIO RCE, npm supply-chain "
            "(WAVESHAPER). Аудит 2031 публичных MCP servers: ~40% с destructive/exec tools, 96% без "
            "предупреждений агенту. Skills/marketplace = новый software supply chain."
        ),
        "why_matters_ru": (
            "Агент = суперпользователь с LLM-интерфейсом. Компрометация одного MCP/skill даёт "
            "persistent access через mcp.json и cross-server tool shadowing."
        ),
        "who_affected_ru": "Dev platform teams, SecOps, все пользователи AI coding assistants.",
        "changed_vs_prev_quarter_ru": (
            "Vs Q1 2026: от «best practices» к documented exploit chains, CVE numeration и industry "
            "calls for transport-layer enforcement (agent gateways)."
        ),
        "confidence": "High",
    },
    "prompt_injection": {
        "summary_ru": (
            "Indirect injection эволюционировал в agent-specific цепочки: веб-страница → IDE context → "
            "изменение mcp.json → RCE (OX/Windsurf). Tool descriptions как скрытый канал инструкций "
            "(tool poisoning) подтверждён CSA и Invariant Labs cross-server сценариями."
        ),
        "why_matters_ru": "Не нужен доступ к модели — достаточно untrusted content в browser/RAG/email pipeline.",
        "who_affected_ru": "Enterprise с browser tools, email agents, публичные coding assistants.",
        "changed_vs_prev_quarter_ru": "Zero-click IDE RCE и CVE-цепочки — качественный скачок vs Q1 advisory-only.",
        "confidence": "High",
    },
    "rag_data_layer": {
        "summary_ru": (
            "RAG и слой данных остаются отдельной attack surface: document injection и memory "
            "summarization превращают «факты» в инструкции. Unit 42 и AWS Bedrock case studies показывают "
            "приоритет memory над user prompt."
        ),
        "why_matters_ru": "Model-level guardrails не спасают, если poisoned chunk попадает в retrieval.",
        "who_affected_ru": "RAG owners, data governance, teams с external crawlers.",
        "changed_vs_prev_quarter_ru": "Больше PoC на long-term memory, не только single-turn RAG.",
        "confidence": "Medium",
    },
    "model_supply_chain": {
        "summary_ru": (
            "Supply chain skills/MCP/артефактов: 30+ CVE за 60 дней 2026, тысячи exposed servers (Shodan), "
            "24k secrets в публичных mcp-конфигах (GitGuardian). North Korean npm hijack внедрял rogue MCP server."
        ),
        "why_matters_ru": "Третья сторона в agent stack так же критична, как зависимости в CI/CD.",
        "who_affected_ru": "AppSec, platform engineering, procurement third-party AI tools.",
        "changed_vs_prev_quarter_ru": "Первый квартал с массовой CVE-нумерацией именно для MCP ecosystem.",
        "confidence": "High",
    },
    "agent_runtime_governance": {
        "summary_ru": (
            "Ответ индустрии: enforcement на transport layer — agent gateways, default-deny tool policy, "
            "JSON-RPC filtering, allowlist STDIO binaries. Сдвиг от «надеемся на LLM safety» к "
            "out-of-process runtime control."
        ),
        "why_matters_ru": "Единственный масштабируемый контроль при hundreds of MCP tools per agent.",
        "who_affected_ru": "Security architects внедряющих agentic AI.",
        "changed_vs_prev_quarter_ru": "Vs Q1: зрелые product/category «agent gateway» и CSA red teaming guides.",
        "confidence": "Medium",
    },
}


def apply_curated(trends: list[TrendItem]) -> list[TrendItem]:
    for trend in trends:
        curated = CURATED_Q2_2026.get(trend.id)
        if not curated:
            continue
        trend.summary_ru = curated.get("summary_ru", trend.summary_ru)
        trend.why_matters_ru = curated.get("why_matters_ru", trend.why_matters_ru)
        trend.who_affected_ru = curated.get("who_affected_ru", trend.who_affected_ru)
        trend.changed_vs_prev_quarter_ru = curated.get(
            "changed_vs_prev_quarter_ru", trend.changed_vs_prev_quarter_ru
        )
        if conf := curated.get("confidence"):
            trend.confidence = conf  # type: ignore[assignment]
    return trends


def generate_report(
    quarter: Quarter,
    trends: list[TrendItem],
    sources: list[SourceItem],
    output_path: Path,
) -> Path:
    trends = apply_curated(trends)
    prev = quarter.previous()

    env = Environment(
        loader=FileSystemLoader(project_root() / "tendencia" / "report" / "templates"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("report_ru_exec.md.j2")

    content = template.render(
        quarter=quarter,
        prev_quarter=prev,
        generated_on=date.today().isoformat(),
        trends=trends,
        sources=sources[:40],
        source_count=len(sources),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def save_findings(path: Path, quarter: Quarter, sources: list[SourceItem], trends: list[TrendItem]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "quarter": str(quarter),
        "sources": [s.__dict__ for s in sources],
        "trends": [
            {
                **t.__dict__,
                "sources": [s.__dict__ for s in t.sources],
            }
            for t in trends
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
