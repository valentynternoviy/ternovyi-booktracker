from pydantic import ValidationError

from booktracker.services.schemas import BookIn

print(
    ">>> BookIn.model_validate({'title': '  Python IN Action  ', 'author': 'Acme', 'pages': '1500', 'category': 'Programming'})"
)
v1 = BookIn.model_validate(
    {"title": "  Python IN Action  ", "author": "Acme", "pages": "1500", "category": "Programming"}
)
print(repr(v1))

print(
    "\n>>> BookIn.model_validate({'title': 'Refactoring', 'author': 'Fowler', 'pages': 'unknown'})"
)
v2 = BookIn.model_validate({"title": "Refactoring", "author": "Fowler", "pages": "unknown"})
print(repr(v2))

print("\n>>> BookIn.model_validate({'title': ' ', 'pages': '-100'})")
try:
    BookIn.model_validate({"title": " ", "pages": "-100"})
except ValidationError as e:
    print(e)
