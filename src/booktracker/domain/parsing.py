from typing import Any

from .models import Book


def normalize_title(raw: str) -> str:
    return " ".join(raw.split()).lower()


def parse_pages(raw: object) -> int | None:
    if isinstance(raw, (int, str, bytes, bytearray)):
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None
    return None


def to_book(row: dict[str, Any]) -> Book | None:
    title = str(row.get("title") or "")
    author = str(row.get("author") or "")
    if not title.strip() or not author.strip():
        return None

    pages = parse_pages(row.get("pages"))
    if pages is not None and pages <= 0:
        return None

    return Book(
        title=normalize_title(title),
        author=author.strip(),
        pages=pages,
        genre=str(row.get("genre") or ""),
    )
