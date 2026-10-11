import argparse
from itertools import islice
from pathlib import Path

from .services.pipeline import PipelineStats, collect, deduplicate, parse_all
from .sources.json_file import read_rows_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(prog="booktracker")
    parser.add_argument("path", type=Path, help="файл із даними")
    parser.add_argument("--stats", action="store_true", help="вивести повну статистику")
    parser.add_argument("--preview", type=int, help="показати перші N записів")
    args = parser.parse_args()

    rows = read_rows_jsonl(args.path)
    stats = PipelineStats()
    pipeline = deduplicate(parse_all(rows, stats), stats)

    if args.preview:
        for book in islice(pipeline, args.preview):
            print(book)
        print(f"\nпрочитано рядків: {stats.read} із загальної кількості")
        return

    if args.stats:
        collect(pipeline, stats)
        print(f"Прочитано записів: {stats.read}")
        print(f"Відхилено: {stats.invalid}")
        print(f"Дублікатів: {stats.duplicates}")
        print(f"Залишилось: {stats.kept}")
        if stats.pages_min is not None:
            print(
                f"Сторінки: min={stats.pages_min} max={stats.pages_max} avg={stats.pages_avg:.0f}"
            )
        for genre, count in stats.by_genre.most_common():
            print(f"  {genre}: {count}")


if __name__ == "__main__":
    main()
