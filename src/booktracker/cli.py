import argparse
from collections.abc import Callable
from pathlib import Path

from .services.pipeline import Pipeline
from .services.ports import Source
from .sources.csv_file import CsvSource
from .sources.jsonl import JsonlSource

FACTORIES: dict[str, Callable[[Path], Source]] = {
    ".jsonl": JsonlSource,
    ".csv": CsvSource,
}


def build_source(path: Path) -> Source:
    try:
        factory = FACTORIES[path.suffix]
    except KeyError:
        raise SystemExit(f"unsupported file type: {path.suffix}") from None
    return factory(path)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="booktracker")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--stats", action="store_true", help="показати повну статистику")
    args = parser.parse_args(argv)

    sources = [build_source(p) for p in args.paths]
    stats = Pipeline(sources).run()

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
