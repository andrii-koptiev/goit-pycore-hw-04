import pytest

from hw04 import task1_salary
from hw04.exceptions import CorruptLineError, EmptyFileError
from hw04.task1_salary import parse_salary_from_line, total_salary


def write_file(tmp_path, content: str, name: str = "staff.txt") -> str:
    """Create a UTF-8 file in tmp_path and return its path as a string."""
    file = tmp_path / name
    file.write_text(content, encoding="utf-8")
    return str(file)


# --- total_salary: happy paths -------------------------------------------


def test_total_and_average(tmp_path):
    path = write_file(tmp_path, "Alex,3000\nNikita,2000\nSitarama,1000\n")
    assert total_salary(path) == (6000, 2000)


def test_single_employee(tmp_path):
    path = write_file(tmp_path, "Alex,1500")
    assert total_salary(path) == (1500, 1500)


def test_no_trailing_newline(tmp_path):
    path = write_file(tmp_path, "Alex,100\nNikita,300")
    assert total_salary(path) == (400, 200)


def test_float_salaries(tmp_path):
    path = write_file(tmp_path, "Alex,1000.50\nNikita,2000.50\n")
    assert total_salary(path) == pytest.approx((3001, 1500.5))


def test_name_with_spaces(tmp_path):
    path = write_file(tmp_path, "Alex Korp,3000\nSitarama Raju,1000\n")
    assert total_salary(path) == (4000, 2000)


def test_windows_line_endings(tmp_path):
    file = tmp_path / "staff.txt"
    file.write_bytes(b"Alex,3000\r\nNikita,1000\r\n")
    assert total_salary(str(file)) == (4000, 2000)


def test_non_ascii_names(tmp_path):
    path = write_file(tmp_path, "Андрій,3000\nÉmilie,1000\n")
    assert total_salary(path) == (4000, 2000)


# --- total_salary: file errors -------------------------------------------


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        total_salary(str(tmp_path / "nope.txt"))


def test_path_is_directory(tmp_path):
    with pytest.raises(IsADirectoryError):
        total_salary(str(tmp_path))


def test_non_utf8_content(tmp_path):
    file = tmp_path / "staff.txt"
    file.write_bytes(b"Alex,3000\n\xff\xfe\x00bad\n")
    with pytest.raises(UnicodeDecodeError):
        total_salary(str(file))


@pytest.mark.parametrize("content", ["", "\n", "   \n"])
def test_empty_file_raises_empty_file_error(tmp_path, content):
    # An empty file must not leak ZeroDivisionError.
    path = write_file(tmp_path, content)
    with pytest.raises(EmptyFileError):
        total_salary(path)


# --- total_salary: corrupt content ---------------------------------------


@pytest.mark.parametrize(
    "content, bad_line_number",
    [
        ("Alex 3000\n", 1),  # no comma
        ("Alex,abc\n", 1),  # non-numeric salary
        ("Alex,\n", 1),  # empty salary
        ("Alex,3000\nNikita;2000\n", 2),  # wrong separator on line 2
        ("Alex,3000\nNikita,two\nSitarama,1000\n", 2),
    ],
)
def test_corrupt_line_reports_line_number(tmp_path, content, bad_line_number):
    path = write_file(tmp_path, content)
    with pytest.raises(CorruptLineError) as exc_info:
        total_salary(path)
    assert exc_info.value.line_number == bad_line_number


def test_blank_lines_are_skipped(tmp_path):
    path = write_file(tmp_path, "Alex,3000\n\nNikita,1000\n")
    assert total_salary(path) == (4000, 2000)


def test_line_number_counts_blank_lines(tmp_path):
    path = write_file(tmp_path, "Alex,3000\n\nNikita;2000\n")
    with pytest.raises(CorruptLineError) as exc_info:
        total_salary(path)
    assert exc_info.value.line_number == 3


# --- parse_salary_from_line ----------------------------------------------


@pytest.mark.parametrize(
    "line, expected",
    [
        ("Alex,3000", 3000.0),
        ("Alex,3000\n", 3000.0),
        ("  Alex,3000  ", 3000.0),
        ("Alex,0", 0.0),
        ("Alex,-50", -50.0),
        ("Alex,1e3", 1000.0),
    ],
)
def test_parse_valid_line(line, expected):
    assert parse_salary_from_line(line, 1) == expected


@pytest.mark.parametrize("line", ["", "Alex", "Alex 3000", "Alex,", "Alex,abc"])
def test_parse_invalid_line(line):
    with pytest.raises(CorruptLineError) as exc_info:
        parse_salary_from_line(line, 7)
    assert exc_info.value.line_number == 7


def test_corrupt_line_error_message():
    error = CorruptLineError(3, "Bob;abc")
    assert "3" in str(error)
    assert "Bob;abc" in str(error)


# --- run(): console behaviour --------------------------------------------


def fake_input(monkeypatch, answer: str) -> None:
    monkeypatch.setattr("builtins.input", lambda _prompt="": answer)


def test_run_prints_result(tmp_path, monkeypatch, capsys):
    path = write_file(tmp_path, "Alex,3000\nNikita,1000\n")
    fake_input(monkeypatch, path)

    task1_salary.run()

    out = capsys.readouterr().out
    assert "Total salary: $4000.00" in out
    assert "average salary: $2000.00" in out


def test_run_missing_file_prints_error(tmp_path, monkeypatch, capsys):
    fake_input(monkeypatch, str(tmp_path / "nope.txt"))

    task1_salary.run()

    out = capsys.readouterr().out
    assert "File not found" in out


def test_run_corrupt_file_prints_error(tmp_path, monkeypatch, capsys):
    fake_input(monkeypatch, write_file(tmp_path, "Alex,abc\n"))

    task1_salary.run()

    out = capsys.readouterr().out
    assert "File corrupted" in out
    assert "line 1" in out


def test_run_empty_file_prints_error(tmp_path, monkeypatch, capsys):
    fake_input(monkeypatch, write_file(tmp_path, ""))

    task1_salary.run()

    out = capsys.readouterr().out
    assert "Cannot calculate" in out


def test_run_empty_answer_uses_default_path(tmp_path, monkeypatch, capsys):
    default = write_file(tmp_path, "Alex,500\n")
    monkeypatch.setattr(task1_salary, "DEFAULT_SALARY_PATH", default)
    fake_input(monkeypatch, "")

    task1_salary.run()

    assert "Total salary: $500.00" in capsys.readouterr().out
