from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field

from pydantic import ValidationError

from ..domain.models import Book
from .ports import Source
from .schemas import BookIn


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0
    by_source: Counter[str] = field(default_factory=Counter)
    by_genre: Counter[str] = field(default_factory=Counter)
    pages_count: int = 0
    pages_sum: int = 0
    pages_min: int | None = None
    pages_max: int | None = None

    @property
    def pages_avg(self) -> float | None:
        if not self.pages_count:
            return None
        return self.pages_sum / self.pages_count


class Pipeline:
    def __init__(self, sources: list[Source]) -> None:
        self._sources = sources

    def run(self) -> PipelineStats:
        stats = PipelineStats()
        seen: set[tuple[str, str]] = set()
        for source in self._sources:
            for book in self._parse(source, stats):
                if book.key in seen:
                    stats.duplicates += 1
                    continue
                seen.add(book.key)
                stats.kept += 1
                stats.by_source[source.name] += 1
                stats.by_genre[book.genre] += 1
                pages = book.pages
                if pages is not None:
                    stats.pages_count += 1
                    stats.pages_sum += pages
                    if stats.pages_min is None or pages < stats.pages_min:
                        stats.pages_min = pages
                    if stats.pages_max is None or pages > stats.pages_max:
                        stats.pages_max = pages
        return stats

    @staticmethod
    def _parse(source: Source, stats: PipelineStats) -> Iterator[Book]:
        for row in source.read():
            stats.read += 1
            try:
                yield BookIn.model_validate(row).to_domain()
            except ValidationError:
                stats.invalid += 1
