from pathlib import Path

import pytest

from booktracker.errors import SourceError
from booktracker.sources.csv_file import CsvSource


def test_csv_source_reads_rows(tmp_path: Path) -> None:
    path = tmp_path / "books.csv"
    path.write_text(
        "title;author;pages;category\nBook A;Author A;100;Fiction\n",
        encoding="utf-8",
    )
    source = CsvSource(path)
    assert source.name == "csv"
    rows = list(source.read())
    assert len(rows) == 1
    assert rows[0]["title"] == "Book A"
    assert rows[0]["author"] == "Author A"


def test_csv_missing_file_raises_source_error() -> None:
    with pytest.raises(SourceError, match="cannot open"):
        list(CsvSource(Path("data/no-such.csv")).read())
