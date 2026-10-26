import csv
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from ..errors import SourceError

logger = logging.getLogger(__name__)


class CsvSource:
    name = "csv"

    def __init__(self, path: Path, delimiter: str = ";") -> None:
        self._path = path
        self._delimiter = delimiter

    def read(self) -> Iterator[dict[str, Any]]:
        try:
            handle = self._path.open(encoding="utf-8", newline="")
        except OSError as exc:
            raise SourceError(f"cannot open {self._path}") from exc

        with handle as f:
            yield from csv.DictReader(f, delimiter=self._delimiter)
