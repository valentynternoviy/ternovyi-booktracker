from booktracker.domain.text import normalize_title


def main() -> None:
    print("BookTracker 0.1.0")
    print(normalize_title("   The   Great  Gatsby   "))


if __name__ == "__main__":
    main()
