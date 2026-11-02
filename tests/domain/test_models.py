from dataclasses import FrozenInstanceError

import pytest

from booktracker.domain.models import Book


def make(**overrides: object) -> Book:
    """Будує валідну книгу, замінюючи лише потрібні поля."""
    data: dict[str, object] = {
        "title": "python developer",
        "author": "Acme",
        "pages": 1500,
        "genre": "Programming",
    }
    data.update(overrides)
    return Book(**data)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"title": ""}, "title must not be empty"),
        ({"title": " "}, "title must not be empty"),
        ({"author": ""}, "author must not be empty"),
        ({"author": " "}, "author must not be empty"),
        ({"pages": 0}, "pages must be positive"),
        ({"pages": -100}, "pages must be positive"),
    ],
)
def test_invalid_book_is_rejected(overrides: dict[str, object], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        make(**overrides)


def test_book_key() -> None:
    book = make()
    assert book.key == ("python developer", "Acme")


def test_frozen_model_immutability() -> None:
    book = make()
    with pytest.raises(FrozenInstanceError):
        book.pages = 2000  # type: ignore[misc]


def test_frozen_model_is_hashable() -> None:
    a = make()
    b = make()
    assert len({a, b}) == 1


@pytest.mark.parametrize(
    ("pages", "expected"),
    [(None, False), (200, False), (499, False), (500, True), (1000, True)],
)
def test_is_large_book(pages: int | None, expected: bool) -> None:
    assert make(pages=pages).is_large_book is expected
