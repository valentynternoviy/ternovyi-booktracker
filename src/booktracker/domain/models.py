from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Book:
    title: str
    author: str
    pages: int | None
    genre: str

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.author