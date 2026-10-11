from dataclasses import dataclass

LARGE_BOOK_THRESHOLD = 500


@dataclass(frozen=True, slots=True)
class Book:
    title: str
    author: str
    pages: int | None
    genre: str

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if not self.author.strip():
            raise ValueError("author must not be empty")
        if self.pages is not None and self.pages <= 0:
            raise ValueError("pages must be positive")

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.author

    @property
    def is_large_book(self) -> bool:
        return self.pages is not None and self.pages >= LARGE_BOOK_THRESHOLD
