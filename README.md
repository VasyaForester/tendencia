# Tendencia

Квартальный инструмент для мониторинга трендов **AI Security** с расширенным охватом смежных технологий (агенты, MCP, self-evolving systems), влияющих на кибербезопасность.

## Возможности

- Сбор источников: **RSS** (CISA, vendors, OWASP), **arXiv**, **DuckDuckGo**
- **Пользовательские ссылки и PDF** — включаются в аналитику наряду с автопоиском
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
| `tendencia show --quarter 2026-Q2` | Человекочитаемый вывод в терминал |
| `tendencia show --quarter 2026-Q2 --brief` | Только краткое резюме (таблица трендов) |
| `tendencia show --quarter 2026-Q2 --plain` | Плоский текст без цветов |
| `tendencia show -o report.txt` | Сохранить plain-text в файл |
| `tendencia report --print` | Сгенерировать MD и сразу показать в терминале |
| `tendencia pdf --quarter 2026-Q2` | Подробный PDF-отчёт |
| `tendencia pdf --open` | PDF и открыть в просмотрщике |
| `tendencia pdf -o my-report.pdf` | PDF в указанный файл |
| `tendencia upload link URL` | Добавить ссылку вручную |
| `tendencia upload pdf file.pdf` | Загрузить PDF (текст извлекается автоматически) |
| `tendencia upload list` | Список пользовательских материалов |
| `tendencia upload remove ID` | Удалить загрузку |
| `tendencia collect --no-search` | Только загрузки + seed, без интернет-поиска |

PDF включает графики по **темам** (отдельно) и **форматам публикаций** (отдельно), плюс матрицу «тема × формат».

## Пользовательские материалы

```bash
tendencia upload link https://example.com/advisory --quarter 2026-Q2
tendencia upload pdf ./docs/whitepaper.pdf --title "MCP Security Whitepaper"
tendencia upload list --quarter 2026-Q2
tendencia report --quarter 2026-Q2   # загрузки подхватятся автоматически
```

Файлы хранятся в `data/<quarter>/uploads/` (manifest + копии PDF).

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
