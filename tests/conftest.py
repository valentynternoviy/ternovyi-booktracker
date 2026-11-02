import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest


class FakeSource:
    """Підставне джерело: віддає задані записи без файлів і мережі."""

    def __init__(self, rows: list[dict[str, Any]], name: str = "fake") -> None:
        self.name = name
        self._rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        yield from self._rows


@pytest.fixture
def row() -> dict[str, Any]:
    """Один коректний сирий запис."""
    return {
        "title": "Python Developer",
        "author": "Acme",
        "pages": "1500",
        "genre": "Programming",
    }


@pytest.fixture
def rows(row: dict[str, Any]) -> list[dict[str, Any]]:
    """1 валідний, 1 дублікат, 1 битий, 1 без числових сторінок."""
    return [
        row,
        {
            "title": " python developer ",
            "author": "Acme",
            "pages": "1500",
            "genre": "Programming",
        },
        {"title": "", "author": "Beta", "pages": "900", "genre": "Fantasy"},
        {
            "title": "Data Analyst",
            "author": "Beta",
            "pages": "за домовленістю",
            "genre": "Fantasy",
        },
    ]


@pytest.fixture
def jsonl_file(tmp_path: Path, rows: list[dict[str, Any]]) -> Path:
    """Тимчасовий .jsonl – зникає разом із tmp_path."""
    path = tmp_path / "books.jsonl"
    body = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    path.write_text(body + "\n", encoding="utf-8")
    return path
