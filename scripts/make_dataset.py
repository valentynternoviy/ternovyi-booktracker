import json
import pathlib
import random

random.seed(7)
genres = ["Fantasy", "Sci-Fi", "Classic", "Mystery", "Poetry"]
authors = ["Author A", "Author B", "Author C", "Author D"]

path = pathlib.Path("data/large.jsonl")
prev = None

with path.open("w", encoding="utf-8") as f:
    for i in range(200_000):
        if i % 10 == 3 and prev is not None:
            row = dict(prev)  # дублікат
        else:
            row = {
                "title": f"Book {i}",
                "author": random.choice(authors),
                "pages": str(random.randint(100, 1000)) if i % 7 else "за домовленістю",
                "genre": random.choice(genres)
            }
        
        if i % 1000 == 0:
            row = dict(row, title="")  # некоректний запис (без назви)
            
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        prev = row