from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from itertools import islice

from ..domain.models import Book
from ..domain.parsing import to_book


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0
    by_genre: Counter = field(default_factory=Counter)
    pages_count: int = 0
    pages_sum: int = 0
    pages_min: int | None = None
    pages_max: int | None = None

    @property
    def pages_avg(self) -> float | None:
        if not self.pages_count:
            return None
        return self.pages_sum / self.pages_count

def parse_all(rows: Iterable[dict], stats: PipelineStats) -> Iterator[Book]:
    for row in rows:
        stats.read += 1
        book = to_book(row)
        if book is None:
            stats.invalid += 1
            continue
        yield book

def deduplicate(items: Iterable[Book], stats: PipelineStats) -> Iterator[Book]:
    seen: set[tuple[str, str]] = set()
    for book in items:
        if book.key in seen:
            stats.duplicates += 1
            continue
        seen.add(book.key)
        yield book

def collect(items: Iterable[Book], stats: PipelineStats) -> None:
    for book in items:
        stats.kept += 1
        stats.by_genre[book.genre] += 1
        pages = book.pages
        if pages is None:
            continue
        stats.pages_count += 1
        stats.pages_sum += pages
        if stats.pages_min is None or pages < stats.pages_min:
            stats.pages_min = pages
        if stats.pages_max is None or pages > stats.pages_max:
            stats.pages_max = pages

def batched(items: Iterable[Book], size: int) -> Iterator[tuple[Book, ...]]:
    iterator = iter(items)
    while batch := tuple(islice(iterator, size)):
        yield batch