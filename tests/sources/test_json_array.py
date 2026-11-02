import json
from pathlib import Path

import pytest

from booktracker.errors import SourceError
from booktracker.sources.jsonl import JsonSource


def test_json_source_reads_array(tmp_path: Path) -> None:
    path = tmp_path / "books.json"
    path.write_text(
        json.dumps([{"title": "Book 1", "author": "A", "pages": 100, "genre": "Fiction"}]),
        encoding="utf-8",
    )
    source = JsonSource(path)
    assert source.name == "json"
    rows = list(source.read())
    assert len(rows) == 1
    assert rows[0]["title"] == "Book 1"


def test_json_missing_file_raises_source_error() -> None:
    with pytest.raises(SourceError, match="cannot open"):
        list(JsonSource(Path("data/no-such.json")).read())
