import logging
from pathlib import Path

import pytest

from booktracker.sources.jsonl import JsonlSource


def test_malformed_line_is_skipped_and_logged(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    path = tmp_path / "broken.jsonl"
    path.write_text('{"a": 1}\n{not json}\n{"a": 2}\n', encoding="utf-8")
    caplog.set_level(logging.DEBUG, logger="booktracker.sources.jsonl")
    rows = list(JsonlSource(path).read())
    assert rows == [{"a": 1}, {"a": 2}]
    assert "skip malformed line 2" in caplog.text


def test_empty_lines_ignored(tmp_path: Path) -> None:
    path = tmp_path / "empty.jsonl"
    path.write_text('\n\n{"a": 1}\n\n', encoding="utf-8")
    assert list(JsonlSource(path).read()) == [{"a": 1}]

