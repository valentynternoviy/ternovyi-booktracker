import argparse
import logging
from collections.abc import Callable
from pathlib import Path

from .config import Settings
from .errors import BookTrackerError, SourceError
from .logging_setup import setup
from .services.pipeline import Pipeline
from .services.ports import Source
from .sources.csv_file import CsvSource
from .sources.jsonl import JsonSource, JsonlSource

logger = logging.getLogger(__name__)

FACTORIES: dict[str, Callable[[Path], Source]] = {
    ".jsonl": JsonlSource,
    ".json": JsonSource,
    ".csv": CsvSource,
}


def build_source(path: Path) -> Source:
    try:
        factory = FACTORIES[path.suffix]
    except KeyError:
        raise SourceError(f"unsupported file type: {path.suffix}") from None
    return factory(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="booktracker")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="перекриває значення з .env і змінних середовища",
    )
    parser.add_argument("--stats", action="store_true", help="показати повну статистику")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    settings = Settings()
    setup(args.log_level or settings.log_level)

    try:
        sources = [build_source(path) for path in args.paths]
        stats = Pipeline(sources).run()
    except BookTrackerError as exc:
        logger.error("%s", exc)
        raise SystemExit(1) from exc

    print(f"Прочитано записів: {stats.read}")
    print(f"Відхилено: {stats.invalid}")
    print(f"Дублікатів: {stats.duplicates}")
    print(f"Залишилось: {stats.kept}")
    if stats.pages_min is not None:
        print(f"Сторінки: min={stats.pages_min} max={stats.pages_max} avg={stats.pages_avg:.0f}")
    for genre, count in stats.by_genre.most_common():
        print(f"  {genre}: {count}")
    for name, count in stats.by_source.items():
        print(f"  з {name}: {count}")


if __name__ == "__main__":
    main()
