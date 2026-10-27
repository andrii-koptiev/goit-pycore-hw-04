import pytest

from hw04 import task2_cats
from hw04.exceptions import CorruptLineError, DuplicateIdError, EmptyFileError
from hw04.task2_cats import get_cats_info


# --- get_cats_info: happy paths ------------------------------------------


def test_returns_list_of_dicts(write_file):
    path = write_file("id1,Tayson,3\nid2,Vika,1\nid3,Barsik,2\n")
    assert get_cats_info(path) == [
        {"id": "id1", "name": "Tayson", "age": "3"},
        {"id": "id2", "name": "Vika", "age": "1"},
        {"id": "id3", "name": "Barsik", "age": "2"},
    ]


def test_values_stay_strings(write_file):
    path = write_file("id1,Tayson,3\n")
    cat = get_cats_info(path)[0]
    assert cat["age"] == "3"
    assert isinstance(cat["age"], str)


def test_single_cat_no_trailing_newline(write_file):
    path = write_file("id1,Tayson,3")
    assert get_cats_info(path) == [{"id": "id1", "name": "Tayson", "age": "3"}]


def test_windows_line_endings(tmp_path):
    file = tmp_path / "cats.txt"
    file.write_bytes(b"id1,Tayson,3\r\nid2,Vika,1\r\n")
    assert get_cats_info(str(file)) == [
        {"id": "id1", "name": "Tayson", "age": "3"},
        {"id": "id2", "name": "Vika", "age": "1"},
    ]


def test_non_ascii_names(write_file):
    path = write_file("id1,Мурзик,3\nid2,Chloé,1\n")
    assert [cat["name"] for cat in get_cats_info(path)] == ["Мурзик", "Chloé"]


def test_blank_lines_are_skipped(write_file):
    path = write_file("id1,Tayson,3\n\n   \nid2,Vika,1\n")
    assert len(get_cats_info(path)) == 2


# --- get_cats_info: file errors ------------------------------------------


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        get_cats_info(str(tmp_path / "nope.txt"))


def test_path_is_directory(tmp_path):
    with pytest.raises(IsADirectoryError):
        get_cats_info(str(tmp_path))


def test_non_utf8_content(tmp_path):
    file = tmp_path / "cats.txt"
    file.write_bytes(b"id1,Tayson,3\n\xff\xfe\x00bad\n")
    with pytest.raises(UnicodeDecodeError):
        get_cats_info(str(file))


@pytest.mark.parametrize("content", ["", "\n", "   \n\n"])
def test_empty_file_raises_empty_file_error(content, write_file):
    path = write_file(content)
    with pytest.raises(EmptyFileError):
        get_cats_info(path)


# --- get_cats_info: corrupt content --------------------------------------


@pytest.mark.parametrize(
    "content, bad_line_number",
    [
        ("id1,Tayson\n", 1),  # too few fields
        ("id1\n", 1),  # only one field
        ("id1,Tayson,3,extra\n", 1),  # too many fields
        ("id1,Tayson,3\nid2,Vika\n", 2),  # bad line is not the first
        ("id1,Tayson,3\n\nid2;Vika;1\n", 3),  # blank lines count; wrong separator
    ],
)
def test_corrupt_line_reports_line_number(content, bad_line_number, write_file):
    path = write_file(content)
    with pytest.raises(CorruptLineError) as exc_info:
        get_cats_info(path)
    assert exc_info.value.line_number == bad_line_number


# --- get_cats_info: duplicate ids ----------------------------------------


def test_duplicate_id_raises(write_file):
    path = write_file("id1,Tayson,3\nid2,Vika,1\nid1,Barsik,2\n")
    with pytest.raises(DuplicateIdError) as exc_info:
        get_cats_info(path)
    assert exc_info.value.line_number == 3
    assert "id1" in str(exc_info.value)


# --- run(): console behaviour --------------------------------------------


def test_run_prints_cats(capsys, write_file, fake_input):
    fake_input(write_file("id1,Tayson,3\n"))

    task2_cats.run()

    out = capsys.readouterr().out
    assert "Tayson" in out


def test_run_missing_file_prints_error(tmp_path, capsys, fake_input):
    fake_input(str(tmp_path / "nope.txt"))

    task2_cats.run()

    assert "File not found" in capsys.readouterr().out


def test_run_corrupt_file_prints_error(capsys, write_file, fake_input):
    fake_input(write_file("id1,Tayson\n"))

    task2_cats.run()

    out = capsys.readouterr().out
    assert "File corrupted" in out
    assert "line 1" in out


def test_run_empty_file_prints_error(capsys, write_file, fake_input):
    fake_input(write_file(""))

    task2_cats.run()

    assert "File is empty" in capsys.readouterr().out


def test_run_duplicate_id_prints_error(capsys, write_file, fake_input):
    fake_input(write_file("id1,Tayson,3\nid1,Vika,1\n"))

    task2_cats.run()

    assert "duplicated id" in capsys.readouterr().out


def test_run_empty_answer_uses_default_path(monkeypatch, capsys, write_file, fake_input):
    default = write_file("id9,Murka,4\n")
    monkeypatch.setattr(task2_cats, "DEFAULT_CATS_PATH", default)
    fake_input("")

    task2_cats.run()

    assert "Murka" in capsys.readouterr().out
