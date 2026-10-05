from booktracker.services.pipeline import PipelineStats, batched, parse_all


def test_invalid_rows_are_counted():
    rows = [
        {"title": "Book 1", "author": "A", "pages": "100", "genre": "Sci-Fi"},
        {"title": "", "author": "B", "pages": "200", "genre": "Sci-Fi"}
    ]
    stats = PipelineStats()
    result = list(parse_all(rows, stats))
    
    assert len(result) == 1
    assert stats.read == 2
    assert stats.invalid == 1

def test_batched_splits_tail():
    assert [len(b) for b in batched(range(7), 3)] == [3, 3, 1]