# Tendencia

Квартальный инструмент для мониторинга трендов **AI Security** с расширенным охватом смежных технологий (агенты, MCP, self-evolving systems), влияющих на кибербезопасность.

## Возможности

- Сбор источников: **RSS** (CISA, vendors, OWASP), **arXiv**, **DuckDuckGo**
- Фильтрация по кварталу (`2026-Q2` = 2026-04-01 … 2026-06-30)
- Тегирование по приоритетным темам (self-evolving agents, AI Act, MCP/skills)
- Markdown-отчёт для **executive/CISO** на русском языке
- Сравнение с предыдущим кварталом

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
tendencia run --quarter 2026-Q2
```

Отчёт: `reports/2026-Q2/ai-security-trends.md`  
Сырые данные: `data/2026-Q2/sources.json`, `data/2026-Q2/findings.json`

## Команды

| Команда | Описание |
|---------|----------|
| `tendencia collect --quarter 2026-Q2` | Только сбор источников |
| `tendencia report --quarter 2026-Q2` | Отчёт из уже собранных данных |
| `tendencia run --quarter 2026-Q2` | Полный цикл |

## Конфигурация

- `config/sources.yaml` — RSS, поисковые запросы, arXiv queries
- `config/topics.yaml` — обязательные темы, аудитория, число трендов
- `.env` — опциональные API-ключи (по умолчанию не требуются)

## Следующий квартал

```bash
tendencia run --quarter 2026-Q3
```

Обновите курированные формулировки в `tendencia/report/generator.py` (`CURATED_Q2_2026`) или добавьте файл по шаблону квартала.

## Лицензия

MIT
