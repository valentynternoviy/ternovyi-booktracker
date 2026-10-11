import pytest

from booktracker.domain.models import Book


@pytest.mark.parametrize(
    "title, author, pages",
    [
        (" ", "Author", 100),  # порожня назва
        ("Book", "", 100),  # порожній автор
        ("Book", "Author", -5),  # від'ємні сторінки
        ("Book", "Author", 0),  # нульові сторінки
    ],
)
def test_invalid_book_rejected(title: str, author: str, pages: int) -> None:
    with pytest.raises(ValueError):
        Book(title, author, pages, "Fantasy")


def test_frozen_model_is_hashable() -> None:
    a = Book("Title", "Author", 100, "Fantasy")
    b = Book("Title", "Author", 100, "Fantasy")
    assert len({a, b}) == 1
