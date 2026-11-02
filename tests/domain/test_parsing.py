from booktracker.domain.parsing import parse_pages, to_book


def test_parse_pages() -> None:
    assert parse_pages("100") == 100
    assert parse_pages(100) == 100
    assert parse_pages("invalid") is None
    assert parse_pages(None) is None


def test_to_book_valid() -> None:
    book = to_book({"title": "  Harry Potter  ", "author": "J.K. Rowling", "pages": "300", "genre": "Fantasy"})
    assert book is not None
    assert book.title == "harry potter"
    assert book.author == "J.K. Rowling"
    assert book.pages == 300
    assert book.genre == "Fantasy"


def test_to_book_invalid() -> None:
    assert to_book({"title": "", "author": "Author"}) is None
    assert to_book({"title": "Title", "author": ""}) is None
    assert to_book({"title": "Title", "author": "Author", "pages": "-10"}) is None
