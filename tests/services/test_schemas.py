import pytest
from pydantic import ValidationError

from booktracker.services.schemas import BookIn


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("1500", 1500), (1500, 1500), ("за домовленістю", None), (None, None)],
)
def test_pages_is_parsed(raw: int | str | None, expected: int | None) -> None:
    schema = BookIn.model_validate({"title": "Dev Book", "author": "Acme", "pages": raw})
    assert schema.pages == expected


def test_book_in_to_domain() -> None:
    schema = BookIn.model_validate(
        {
            "title": "  Python In Action  ",
            "author": "  Acme Corp  ",
            "pages": "350",
            "category": "Tech",
        }
    )
    domain = schema.to_domain()
    assert domain.title == "python in action"
    assert domain.author == "Acme Corp"
    assert domain.pages == 350
    assert domain.genre == "Tech"


def test_invalid_book_in_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        BookIn.model_validate({"title": "", "author": "Acme"})
