import json, random, pathlib
genres = ["Fantasy", "Sci-Fi", "Classic", "Mystery"]
with pathlib.Path("data/large.jsonl").open("w", encoding="utf-8") as f:
    for i in range(200_000):
        row = {"title": f"Book {i % 500}", "author": f"Author {i % 300}", 
               "pages": str(random.randint(100, 1000)), 
               "genre": random.choice(genres)}
        f.write(json.dumps(row, ensure_ascii=False) + "\n")