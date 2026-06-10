"""Парсинг и границы кварталов."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime

QUARTER_RE = re.compile(r"^(\d{4})-Q([1-4])$")


@dataclass(frozen=True)
class Quarter:
    year: int
    number: int

    @classmethod
    def parse(cls, value: str) -> Quarter:
        match = QUARTER_RE.match(value.strip())
        if not match:
            raise ValueError(f"Неверный формат квартала: {value!r}. Ожидается YYYY-QN, например 2026-Q2")
        return cls(year=int(match.group(1)), number=int(match.group(2)))

    @property
    def label(self) -> str:
        return f"{self.year}-Q{self.number}"

    @property
    def start(self) -> date:
        month = (self.number - 1) * 3 + 1
        return date(self.year, month, 1)

    @property
    def end(self) -> date:
        if self.number == 1:
            return date(self.year, 3, 31)
        if self.number == 2:
            return date(self.year, 6, 30)
        if self.number == 3:
            return date(self.year, 9, 30)
        return date(self.year, 12, 31)

    def previous(self) -> Quarter:
        if self.number == 1:
            return Quarter(self.year - 1, 4)
        return Quarter(self.year, self.number - 1)

    def contains(self, dt: date | datetime) -> bool:
        d = dt.date() if isinstance(dt, datetime) else dt
        return self.start <= d <= self.end

    def __str__(self) -> str:
        return self.label
