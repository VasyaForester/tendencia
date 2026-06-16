"""Таксономия: темы (subject) vs форматы публикаций (evidence type)."""

from __future__ import annotations

from tendencia.config_loader import load_yaml
from tendencia.models import SourceItem

# Формат публикации — НЕ тема. Используется только в графиках «структура источников».
SOURCE_FORMAT_LABELS: dict[str, str] = {
    "papers": "Исследования / препринты",
    "gov_cert": "Gov / CERT advisories",
    "standards": "Стандарты и фреймворки",
    "vendor": "Vendor / engineering блоги",
    "incidents": "Отчёты об инцидентах / CVE",
    "news": "Новости и обзоры",
    "social": "Соцсети / конференции",
    "user_upload": "Пользовательские материалы",
    "unknown": "Прочее",
}

SOURCE_FORMAT_ORDER = [
    "papers",
    "gov_cert",
    "standards",
    "vendor",
    "incidents",
    "news",
    "social",
    "user_upload",
    "unknown",
]

THEME_CHART_COLORS: dict[str, str] = {
    "self_evolving_agents": "#3182CE",
    "ai_regulation": "#805AD5",
    "agent_tools": "#DD6B20",
    "prompt_injection": "#E53E3E",
    "rag_data_layer": "#38A169",
    "model_supply_chain": "#319795",
    "agent_runtime_governance": "#D69E2E",
}

FORMAT_CHART_COLORS: dict[str, str] = {
    "papers": "#1A365D",
    "gov_cert": "#2C5282",
    "standards": "#3182CE",
    "vendor": "#4299E1",
    "incidents": "#E53E3E",
    "news": "#63B3ED",
    "social": "#90CDF4",
    "user_upload": "#ED8936",
    "unknown": "#CBD5E0",
}


def load_theme_definitions(cfg: dict | None = None) -> list[dict]:
    cfg = cfg or load_yaml("topics.yaml")
    themes: list[dict] = []
    seen: set[str] = set()
    for block in ("must_include", "secondary_themes"):
        for theme in cfg.get(block, []):
            tid = theme["id"]
            if tid in seen:
                continue
            seen.add(tid)
            themes.append(theme)
    return themes


def theme_labels(cfg: dict | None = None) -> dict[str, str]:
    return {t["id"]: t["title_ru"] for t in load_theme_definitions(cfg)}


def theme_priority(cfg: dict | None = None) -> list[str]:
    return [t["id"] for t in load_theme_definitions(cfg)]


def _blob(source: SourceItem) -> str:
    return f"{source.title} {source.summary} {source.url}".lower()


def _match_keywords(blob: str, keywords: list[str]) -> bool:
    return any(kw.lower() in blob for kw in keywords)


def detect_themes(source: SourceItem, cfg: dict | None = None) -> set[str]:
    """Темы по содержанию. Формат публикации (source_type) не учитывается."""
    themes = load_theme_definitions(cfg)
    matched: set[str] = set()
    blob = _blob(source)
    for theme in themes:
        if _match_keywords(blob, theme.get("keywords", [])):
            matched.add(theme["id"])
    # Унаследованные теги — только если это валидные theme id
    valid_ids = {t["id"] for t in themes}
    for tid in source.matched_topics:
        if tid in valid_ids:
            matched.add(tid)
    return matched


def primary_theme(source: SourceItem, cfg: dict | None = None) -> str | None:
    """Одна главная тема для источника (для сопоставимых подсчётов)."""
    matched = detect_themes(source, cfg)
    if not matched:
        return None
    for tid in theme_priority(cfg):
        if tid in matched:
            return tid
    return next(iter(matched))


def attack_surface_for_theme(theme_id: str, cfg: dict | None = None) -> str:
    for theme in load_theme_definitions(cfg):
        if theme["id"] == theme_id:
            return theme.get("attack_surface", "governance")
    return "governance"
