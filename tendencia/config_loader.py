"""Загрузка YAML-конфигурации."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(name: str) -> dict:
    path = ROOT / "config" / name
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def project_root() -> Path:
    return ROOT
