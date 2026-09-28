import argparse
from pathlib import Path
from .services.pipeline import count_by_genre, load_books

def main() -> None:
    parser = argparse.ArgumentParser(prog="booktracker")
    parser.add_argument("path", type=Path, help="файл із даними")
    args = parser.parse_args()
    
    books = load_books(args.path)
    print(f"Завантажено унікальних записів: {len(books)}")
    
    print("\nСтатистика за жанрами:")
    for genre, count in count_by_genre(books).most_common():
        print(f"  {genre}: {count}")

if __name__ == "__main__":
    main()