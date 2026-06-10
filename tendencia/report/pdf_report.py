"""Генерация подробного PDF-отчёта."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from fpdf import FPDF

from tendencia.config_loader import project_root
from tendencia.models import SourceItem, TrendItem
from tendencia.quarter import Quarter
from tendencia.report.terminal import RECOMMENDATIONS

ASSETS = Path(__file__).resolve().parent / "assets"

COLORS = {
    "primary": (26, 54, 93),
    "accent": (49, 130, 206),
    "light": (235, 248, 255),
    "muted": (113, 128, 150),
    "white": (255, 255, 255),
    "high": (39, 103, 73),
    "medium": (151, 90, 22),
    "low": (155, 44, 44),
    "border": (226, 232, 240),
}

THREAT_LANDSCAPE = [
    ("Модель и промпт", "Prompt/indirect injection, jailbreaks"),
    ("Агенты и инструменты", "MCP, skills, delegated auth, tool abuse"),
    ("RAG и данные", "Poisoning, утечки через retrieval"),
    ("Supply chain", "Целостность моделей, зависимости, артефакты"),
    ("Эксплуатация", "Логирование агентов, IR, rate limits"),
    ("Governance", "AI Act, NIST/OWASP mapping, evals"),
]

METRICS = [
    "Количество активных MCP/skills и % с security review",
    "Инциденты tool invocation вне policy",
    "Доля ответов с retrieval из untrusted corpora",
    "Время реакции на новые vendor advisories по LLM",
]

OPEN_QUESTIONS = [
    "Насколько self-evolving agents станут production-default в 2026 H2?",
    "Будут ли industry-стандарты для MCP trust и signing в Q3–Q4?",
    "Какие метрики post-market monitoring примет регулятор для agentic systems?",
]

CONFIDENCE_FILL = {
    "High": COLORS["high"],
    "Medium": COLORS["medium"],
    "Low": COLORS["low"],
}


def pdf_output_path(quarter: Quarter) -> Path:
    return project_root() / "reports" / quarter.label / "ai-security-trends.pdf"


def _resolve_fonts() -> tuple[Path, Path]:
    regular = ASSETS / "DejaVuSans.ttf"
    bold = ASSETS / "DejaVuSans-Bold.ttf"
    if regular.exists() and bold.exists():
        return regular, bold

    win = Path("C:/Windows/Fonts")
    arial = win / "arial.ttf"
    arial_b = win / "arialbd.ttf"
    if arial.exists() and arial_b.exists():
        return arial, arial_b

    raise FileNotFoundError(
        "Не найдены шрифты для PDF. Ожидаются DejaVu в tendencia/report/assets/ "
        "или Arial в C:/Windows/Fonts/"
    )


class TendenciaPDF(FPDF):
    def __init__(self, quarter: Quarter, source_count: int) -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self.quarter = quarter
        self.source_count = source_count
        self._setup_fonts()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(18, 18, 18)

    def _setup_fonts(self) -> None:
        regular, bold = _resolve_fonts()
        self.add_font("Body", "", str(regular))
        self.add_font("Body", "B", str(bold))

    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_fill_color(*COLORS["primary"])
        self.rect(0, 0, 210, 14, style="F")
        self.set_xy(18, 4)
        self.set_font("Body", "B", 9)
        self.set_text_color(*COLORS["white"])
        self.cell(0, 6, f"Tendencia · AI Security Trends · {self.quarter}", align="L")
        self.set_text_color(0, 0, 0)
        self.ln(14)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("Body", "", 8)
        self.set_text_color(*COLORS["muted"])
        self.cell(0, 8, f"Стр. {self.page_no()}/{{nb}}  ·  tendencia  ·  {date.today().isoformat()}", align="C")
        self.set_text_color(0, 0, 0)

    def _ensure_space(self, height: float) -> None:
        if self.get_y() + height > 277:
            self.add_page()

    def _section_title(self, title: str) -> None:
        self._ensure_space(16)
        self.set_fill_color(*COLORS["accent"])
        self.set_font("Body", "B", 13)
        self.set_text_color(*COLORS["white"])
        self.cell(0, 10, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def _body_text(self, text: str, size: int = 10) -> None:
        self.set_font("Body", "", size)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def _label_value(self, label: str, value: str) -> None:
        self._ensure_space(12)
        self.set_font("Body", "B", 10)
        self.set_x(self.l_margin)
        self.cell(0, 6, label, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Body", "", 10)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, value)
        self.ln(2)

    def _confidence_badge(self, confidence: str) -> None:
        fill = CONFIDENCE_FILL.get(confidence, COLORS["muted"])
        self.set_fill_color(*fill)
        self.set_font("Body", "B", 9)
        self.set_text_color(*COLORS["white"])
        self.cell(28, 7, confidence, fill=True, align="C")
        self.set_text_color(0, 0, 0)
        self.ln(6)

    def cover_page(self) -> None:
        self.add_page()
        self.set_fill_color(*COLORS["primary"])
        self.rect(0, 0, 210, 120, style="F")
        self.set_fill_color(*COLORS["accent"])
        self.rect(0, 110, 210, 10, style="F")

        self.set_xy(18, 38)
        self.set_font("Body", "B", 28)
        self.set_text_color(*COLORS["white"])
        self.multi_cell(0, 12, "AI Security\nTrends Report")
        self.ln(4)

        self.set_font("Body", "", 16)
        self.cell(0, 10, f"Квартал {self.quarter}", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Body", "", 11)
        self.cell(0, 7, f"{self.quarter.start} — {self.quarter.end}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.cell(0, 7, f"Сравнение: vs {self.quarter.previous()}", new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(0, 0, 0)
        self.set_xy(18, 135)
        self.set_font("Body", "B", 12)
        self.cell(0, 8, "Executive Brief", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Body", "", 10)
        self.set_text_color(*COLORS["muted"])
        self.multi_cell(
            0,
            6,
            "Подробный квартальный обзор трендов AI Security и смежных технологий "
            "(агенты, MCP, self-evolving systems) для руководства и CISO.",
        )
        self.set_text_color(0, 0, 0)
        self.ln(4)
        self._meta_row("Дата подготовки", date.today().isoformat())
        self._meta_row("Источников проанализировано", str(self.source_count))
        self._meta_row("Инструмент", "tendencia CLI")

    def _meta_row(self, label: str, value: str) -> None:
        self.set_font("Body", "B", 10)
        self.cell(55, 7, label + ":")
        self.set_font("Body", "", 10)
        self.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")

    def executive_summary(self, trends: list[TrendItem]) -> None:
        self.add_page()
        self._section_title("Краткое резюме для руководства")

        col_w = (174, 22, 18)
        self.set_fill_color(*COLORS["light"])
        self.set_font("Body", "B", 9)
        self.set_text_color(*COLORS["primary"])
        self.cell(col_w[0], 8, "  Тренд", border=1, fill=True)
        self.cell(col_w[1], 8, "Уверен.", border=1, fill=True, align="C")
        self.cell(col_w[2], 8, "  #", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

        for i, trend in enumerate(trends, 1):
            self._ensure_space(14)
            y0 = self.get_y()
            self.set_font("Body", "", 9)
            x, y = self.get_x(), self.get_y()
            self.multi_cell(col_w[0], 5, trend.title_ru, border="LR")
            h = self.get_y() - y
            self.set_xy(x + col_w[0], y)
            self.set_font("Body", "B", 8)
            conf_color = CONFIDENCE_FILL.get(trend.confidence, COLORS["muted"])
            self.set_text_color(*conf_color)
            self.cell(col_w[1], h, trend.confidence, border="LR", align="C")
            self.set_text_color(0, 0, 0)
            self.cell(col_w[2], h, str(i), border="LR", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Body", "", 8)
            self.set_text_color(*COLORS["muted"])
            self.multi_cell(174, 4.5, trend.why_matters_ru, border="LRB")
            self.set_text_color(0, 0, 0)
            self.ln(1)

    def threat_landscape(self) -> None:
        self.add_page()
        self._section_title("Ландшафт угроз")

        self.set_font("Body", "B", 9)
        self.set_fill_color(*COLORS["light"])
        self.cell(55, 8, "  Поверхность", border=1, fill=True)
        self.cell(119, 8, "  Сигнал квартала", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Body", "", 9)
        for surface, signal in THREAT_LANDSCAPE:
            self._ensure_space(10)
            self.cell(55, 8, surface, border=1)
            self.cell(119, 8, signal, border=1, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def trend_details(self, trends: list[TrendItem]) -> None:
        self.add_page()
        self._section_title(f"Детальный разбор трендов (vs {self.quarter.previous()})")

        for i, trend in enumerate(trends, 1):
            self._ensure_space(50)
            self.set_fill_color(*COLORS["primary"])
            self.set_font("Body", "B", 12)
            self.set_text_color(*COLORS["white"])
            self.cell(0, 9, f"  {i}. {trend.title_ru}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
            self.ln(2)
            self._confidence_badge(trend.confidence)

            self._label_value("Суть", trend.summary_ru)
            self._label_value("Изменение к прошлому кварталу", trend.changed_vs_prev_quarter_ru)
            self._label_value("Почему важно", trend.why_matters_ru)
            self._label_value("Кому актуально", trend.who_affected_ru)

            if trend.sources:
                self.set_font("Body", "B", 10)
                self.cell(0, 6, "Ключевые источники:", new_x="LMARGIN", new_y="NEXT")
                self.set_font("Body", "", 9)
                for src in trend.sources[:6]:
                    self._ensure_space(10)
                    pub = f" ({src.published})" if src.published else ""
                    line = f"• {src.title} — {src.source_type}{pub}"
                    self.set_x(self.l_margin)
                    self.multi_cell(0, 5, line)
                    self.set_text_color(*COLORS["accent"])
                    self.set_font("Body", "", 8)
                    self.set_x(self.l_margin)
                    self.multi_cell(0, 4, src.url, link=src.url)
                    self.set_text_color(0, 0, 0)
                    self.set_font("Body", "", 9)
                self.ln(2)

            self.set_draw_color(*COLORS["border"])
            self.line(18, self.get_y(), 192, self.get_y())
            self.ln(6)

    def recommendations(self) -> None:
        self._ensure_space(40)
        self._section_title("Приоритетные рекомендации")
        for i, rec in enumerate(RECOMMENDATIONS, 1):
            self._ensure_space(10)
            self.set_fill_color(*COLORS["light"])
            self.set_font("Body", "B", 10)
            self.set_text_color(*COLORS["primary"])
            self.cell(10, 8, str(i), fill=True, align="C")
            self.set_font("Body", "", 10)
            self.set_text_color(0, 0, 0)
            self.cell(164, 8, f"  {rec}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def metrics_and_questions(self) -> None:
        self.add_page()
        self._section_title("Метрики для мониторинга")
        for m in METRICS:
            self._ensure_space(8)
            self.set_font("Body", "", 10)
            self.set_x(self.l_margin)
            self.multi_cell(0, 5.5, f"- {m}")
        self.ln(4)

        self._section_title("Открытые вопросы")
        for q in OPEN_QUESTIONS:
            self._ensure_space(8)
            self.set_font("Body", "", 10)
            self.set_x(self.l_margin)
            self.multi_cell(0, 5.5, f"?  {q}")

    def sources_appendix(self, sources: list[SourceItem], limit: int = 35) -> None:
        self.add_page()
        self._section_title("Приложение: источники")
        self.set_font("Body", "", 8)
        for src in sources[:limit]:
            self._ensure_space(12)
            pub = f" · {src.published}" if src.published else ""
            self.set_font("Body", "B", 8)
            self.set_x(self.l_margin)
            self.multi_cell(0, 4.5, src.title)
            self.set_font("Body", "", 7)
            self.set_text_color(*COLORS["muted"])
            self.set_x(self.l_margin)
            self.cell(0, 4, f"{src.source_type} · {src.origin}{pub}", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*COLORS["accent"])
            self.set_x(self.l_margin)
            self.multi_cell(0, 4, src.url, link=src.url)
            self.set_text_color(0, 0, 0)
            self.ln(2)


def generate_pdf(
    quarter: Quarter,
    trends: list[TrendItem],
    sources: list[SourceItem],
    output_path: Path,
) -> Path:
    """Создать подробный PDF-отчёт."""
    pdf = TendenciaPDF(quarter, len(sources))
    pdf.alias_nb_pages()

    pdf.cover_page()
    pdf.executive_summary(trends)
    pdf.threat_landscape()
    pdf.trend_details(trends)
    pdf.recommendations()
    pdf.metrics_and_questions()
    pdf.sources_appendix(sources)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    return output_path
