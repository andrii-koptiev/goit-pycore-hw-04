"""Tests for task 3. The requirements are in the docstring of hw04/task3_tree.py."""

import pytest
from colorama import Fore

from hw04 import task3_tree
from hw04.task3_tree import build_tree


@pytest.fixture
def sample_dir(tmp_path):
    """root/ with: docs/readme.txt, src/pkg/mod.py, src/main.py, notes.txt."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "readme.txt").write_text("hi", encoding="utf-8")
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "mod.py").write_text("", encoding="utf-8")
    (tmp_path / "src" / "main.py").write_text("", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("", encoding="utf-8")
    return tmp_path


# --- build_tree: happy paths ---------------------------------------------


def test_nested_structure(sample_dir):
    assert build_tree(sample_dir) == [
        "docs/",
        "    readme.txt",
        "src/",
        "    pkg/",
        "        mod.py",
        "    main.py",
        "notes.txt",
    ]


def test_accepts_str_path(sample_dir):
    assert build_tree(str(sample_dir)) == build_tree(sample_dir)


def test_empty_directory(tmp_path):
    assert build_tree(tmp_path) == []


def test_only_files(tmp_path):
    (tmp_path / "b.txt").write_text("", encoding="utf-8")
    (tmp_path / "a.txt").write_text("", encoding="utf-8")
    assert build_tree(tmp_path) == ["a.txt", "b.txt"]


def test_directories_come_before_files(tmp_path):
    (tmp_path / "a_file.txt").write_text("", encoding="utf-8")
    (tmp_path / "z_dir").mkdir()
    assert build_tree(tmp_path) == ["z_dir/", "a_file.txt"]


def test_empty_subdirectory_is_listed(tmp_path):
    (tmp_path / "empty").mkdir()
    assert build_tree(tmp_path) == ["empty/"]


def test_hidden_files_and_dirs_are_included(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".env").write_text("", encoding="utf-8")
    assert build_tree(tmp_path) == [".git/", ".env"]


def test_non_ascii_names(tmp_path):
    (tmp_path / "папка").mkdir()
    (tmp_path / "папка" / "файл.txt").write_text("", encoding="utf-8")
    assert build_tree(tmp_path) == ["папка/", "    файл.txt"]


# --- build_tree: errors --------------------------------------------------


def test_missing_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        build_tree(tmp_path / "nope")


def test_path_is_file(write_file):
    with pytest.raises(NotADirectoryError):
        build_tree(write_file("hello"))


# --- run(): console behaviour --------------------------------------------


def test_run_prints_names(sample_dir, capsys, fake_input):
    fake_input(str(sample_dir))

    task3_tree.run()

    out = capsys.readouterr().out
    assert "docs" in out
    assert "mod.py" in out


def test_run_colours_directories_and_files_differently(tmp_path, capsys, fake_input):
    (tmp_path / "sub").mkdir()
    (tmp_path / "file.txt").write_text("", encoding="utf-8")
    fake_input(str(tmp_path))

    task3_tree.run()

    out = capsys.readouterr().out
    assert Fore.BLUE in out
    assert Fore.GREEN in out
    # the colour sits right before the matching name
    assert Fore.BLUE + "sub" in out
    assert Fore.GREEN + "file.txt" in out


def test_run_missing_path_prints_error(tmp_path, capsys, fake_input):
    fake_input(str(tmp_path / "nope"))

    task3_tree.run()

    assert "not found" in capsys.readouterr().out.lower()


def test_run_file_path_prints_error(write_file, capsys, fake_input):
    fake_input(write_file("hello"))

    task3_tree.run()

    assert "not a directory" in capsys.readouterr().out.lower()
