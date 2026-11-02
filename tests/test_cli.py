from pathlib import Path

import pytest

from booktracker.cli import main


def test_missing_file_exits_with_code_1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("sys.argv", ["booktracker", str(tmp_path / "no.jsonl")])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1


def test_unsupported_file_exits_with_code_1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("sys.argv", ["booktracker", str(tmp_path / "file.xml")])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1


def test_main_prints_summary(
    jsonl_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("sys.argv", ["booktracker", str(jsonl_file)])
    main()
    out = capsys.readouterr().out
    assert "Прочитано записів: 4" in out
    assert "Залишилось: 2" in out


def test_flag_beats_environment(
    jsonl_file: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Пріоритет: аргумент командного рядка > змінна середовища > .env."""
    levels: list[str] = []
    monkeypatch.setattr("booktracker.cli.setup", levels.append)
    monkeypatch.setenv("LOG_LEVEL", "ERROR")
    monkeypatch.setattr(
        "sys.argv",
        ["booktracker", str(jsonl_file), "--log-level", "DEBUG"],
    )
    main()
    assert levels == ["DEBUG"]


def test_environment_beats_default(
    jsonl_file: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    levels: list[str] = []
    monkeypatch.setattr("booktracker.cli.setup", levels.append)
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setattr("sys.argv", ["booktracker", str(jsonl_file)])
    main()
    assert levels == ["WARNING"]
