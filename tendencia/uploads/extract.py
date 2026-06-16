"""Извлечение текста и метаданных из URL и PDF."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import urlparse

import requests

USER_AGENT = "Tendencia/0.1 (+https://github.com/VasyaForester/tendencia)"
REQUEST_TIMEOUT = 25


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.og_title = ""
        self.og_description = ""
        self.description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            name = (attr.get("name") or attr.get("property") or "").lower()
            content = attr.get("content") or ""
            if name in ("og:title", "twitter:title"):
                self.og_title = content
            elif name in ("og:description", "twitter:description", "description"):
                if name == "description" and not self.description:
                    self.description = content
                if "description" in name:
                    self.og_description = content or self.og_description

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def _clean_text(text: str, max_len: int = 500) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        return text[: max_len - 1] + "…"
    return text


def extract_pdf_text(path: str, max_chars: int = 4000) -> str:
    from pypdf import PdfReader

    reader = PdfReader(path)
    chunks: list[str] = []
    total = 0
    for page in reader.pages[:20]:
        piece = page.extract_text() or ""
        chunks.append(piece)
        total += len(piece)
        if total >= max_chars:
            break
    return _clean_text(" ".join(chunks), max_chars)


def fetch_url_content(url: str) -> tuple[str, str]:
    """Вернуть (title, summary) для HTTP(S)-ссылки."""
    resp = requests.get(
        url,
        timeout=REQUEST_TIMEOUT,
        headers={"User-Agent": USER_AGENT},
        allow_redirects=True,
    )
    resp.raise_for_status()
    ctype = resp.headers.get("Content-Type", "").lower()

    if "pdf" in ctype or url.lower().endswith(".pdf"):
        # Временно сохранять не будем — вызывающий код обработает отдельно
        raise ValueError("URL указывает на PDF — используйте: tendencia upload pdf")

    parser = _MetaParser()
    parser.feed(resp.text[:500_000])
    title = parser.og_title or parser.title or url
    summary = parser.og_description or parser.description or _extract_body_snippet(resp.text)
    return _clean_text(title, 200), _clean_text(summary, 500)


def _extract_body_snippet(html: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:500]


def infer_source_type(url: str, kind: str, text: str = "") -> str:
    host = urlparse(url).netloc.lower()
    blob = f"{url} {text}".lower()

    if kind == "pdf" or url.lower().endswith(".pdf"):
        return "papers"
    if "arxiv.org" in host:
        return "papers"
    if any(x in host for x in ("cisa.gov", "ncsc.gov.uk", "cert.", "europa.eu")):
        return "gov_cert"
    if any(x in host for x in ("owasp.org", "nist.gov", "cloudsecurityalliance.org")):
        return "standards"
    if any(x in blob for x in ("cve-", "incident", "advisory")):
        return "incidents"
    if any(x in host for x in ("openai.com", "anthropic.com", "google", "microsoft.com", "paloaltonetworks")):
        return "vendor"
    return "user_upload"
