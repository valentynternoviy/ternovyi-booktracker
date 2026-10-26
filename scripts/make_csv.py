import csv
import json
import pathlib
import random

random.seed(42)
genres = ["Fantasy", "Sci-Fi", "Classic", "Mystery", "Poetry"]
authors = ["Author A", "Author B", "Author C", "Author D"]

# Read first 500 unique valid keys from large.jsonl
existing_books = []
with open("data/large.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            row = json.loads(line)
            if row.get("title") and row.get("author"):
                existing_books.append((row["title"].lower(), row["author"]))
                if len(existing_books) >= 500:
                    break

out_path = pathlib.Path("data/extra.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)

with out_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "author", "pages", "category"], delimiter=";")
    writer.writeheader()

    # 1. 10 invalid rows (empty title)
    for i in range(10):
        writer.writerow({
            "title": "",
            "author": random.choice(authors),
            "pages": "300",
            "category": random.choice(genres),
        })

    # 2. Exactly 500 duplicates of books in large.jsonl
    for title, author in existing_books:
        writer.writerow({
            "title": title,
            "author": author,
            "pages": "350",
            "category": random.choice(genres),
        })

    # 3. Exactly 4490 unique books
    for i in range(4490):
        writer.writerow({
            "title": f"CSV Unique Novel {i}",
            "author": random.choice(authors),
            "pages": str(random.randint(150, 850)),
            "category": random.choice(genres),
        })

print("Generated data/extra.csv with exactly 500 duplicates and 4490 unique books.")
