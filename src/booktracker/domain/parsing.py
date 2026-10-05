from .models import Book


def normalize_title(raw: str) -> str:
    return " ".join(raw.split()).lower()

def parse_pages(raw: object) -> int | None:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None

def to_book(row: dict) -> Book | None:
    title = row.get("title") or ""
    if not title.strip():
        return None
    
    return Book(
        title=normalize_title(title),
        author=row.get("author", ""),
        pages=parse_pages(row.get("pages")),
        genre=row.get("genre", ""),
    )