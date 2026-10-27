import pytest


@pytest.fixture
def write_file(tmp_path):
    """Return a helper that creates a UTF-8 file in tmp_path and returns its path."""

    def _write_file(content: str, name: str = "data.txt") -> str:
        file = tmp_path / name
        file.write_text(content, encoding="utf-8")
        return str(file)

    return _write_file


@pytest.fixture
def fake_input(monkeypatch):
    """Return a helper that makes input() return the given answer."""

    def _fake_input(answer: str) -> None:
        monkeypatch.setattr("builtins.input", lambda _prompt="": answer)

    return _fake_input
