import pytest

from booktracker.domain.text import normalize_title


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Python Developer", "python developer"),
        (" Python Developer ", "python developer"),
        ("PYTHON\tDEVELOPER", "python developer"),
        ("   The   Great   Gatsby   ", "the great gatsby"),
    ],
)
def test_normalize_title(raw: str, expected: str) -> None:
    assert normalize_title(raw) == expected
