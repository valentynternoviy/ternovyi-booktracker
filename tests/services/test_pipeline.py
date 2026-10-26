from collections.abc import Iterator
from typing import Any

from booktracker.services.pipeline import Pipeline


class FakeSource:
    def __init__(self, rows: list[dict[str, Any]], name: str = "fake") -> None:
        self.name = name
        self._rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        yield from self._rows


ROW = {"title": "Dev Book", "author": "Acme", "pages": "1500", "genre": "Sci-Fi"}


def test_invalid_row_is_skipped_not_raised() -> None:
    stats = Pipeline([FakeSource([ROW, {"title": "", "author": "B"}])]).run()
    assert stats.invalid == 1 and stats.kept == 1


def test_duplicates_across_sources() -> None:
    stats = Pipeline([FakeSource([ROW], "a"), FakeSource([ROW], "b")]).run()
    assert stats.duplicates == 1
    assert stats.by_source == {"a": 1}


def test_unknown_pages_is_not_an_error() -> None:
    row = dict(ROW, pages="за домовленістю")
    stats = Pipeline([FakeSource([row])]).run()
    assert stats.kept == 1 and stats.invalid == 0


def test_empty_source() -> None:
    stats = Pipeline([FakeSource([])]).run()
    assert stats.read == 0 and stats.kept == 0 and stats.invalid == 0


def test_multiple_genres_counted() -> None:
    rows = [
        {"title": "Book 1", "author": "A", "pages": "100", "genre": "Fantasy"},
        {"title": "Book 2", "author": "B", "pages": "200", "genre": "Fantasy"},
        {"title": "Book 3", "author": "C", "pages": "300", "genre": "Sci-Fi"},
    ]
    stats = Pipeline([FakeSource(rows)]).run()
    assert stats.kept == 3
    assert stats.by_genre == {"Fantasy": 2, "Sci-Fi": 1}
    assert stats.pages_min == 100
    assert stats.pages_max == 300
    assert stats.pages_avg == 200.0


def test_negative_pages_is_invalid() -> None:
    row = dict(ROW, pages="-50")
    stats = Pipeline([FakeSource([row])]).run()
    assert stats.invalid == 1 and stats.kept == 0
