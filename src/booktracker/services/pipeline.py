from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path

from ..domain.models import Book
from ..domain.parsing import to_book
from ..sources.json_file import read_rows

def deduplicate(items: Iterable[Book]) -> Iterator[Book]:
    seen: set[tuple[str, str]] = set()
    for book in items:
        if book.key not in seen:
            seen.add(book.key)
            yield book

def count_by_genre(items: Iterable[Book]) -> Counter[str]:
    return Counter(book.genre for book in items)

def load_books(path: Path) -> list[Book]:
    rows = read_rows(path)
    parsed = (to_book(row) for row in rows)
    valid = (b for b in parsed if b is not None)
    return list(deduplicate(valid))