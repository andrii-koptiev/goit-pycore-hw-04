"""Tests for task 4. The requirements are in the docstring of hw04/task4_bot.py."""

import re

import pytest

from hw04 import task4_bot
from hw04.exceptions import NameExistsError, NotFoundError, WrongArgumentsError
from hw04.task4_bot import (
    add_contact,
    change_contact,
    parse_input,
    show_all,
    show_help,
    show_phone,
)

ANSI = re.compile(r"\x1b\[[0-9;]*m")


LOG_PREFIX = re.compile(r"^\s*\[(RESULT|ERROR|ACTION)\]\s+", re.MULTILINE)


def plain(text: str) -> str:
    """Strip colour codes so tests can compare the visible text."""
    return ANSI.sub("", text)


def bare(text: str) -> str:
    """Like plain(), but also drop the [RESULT]/[ERROR] label from each line."""
    return LOG_PREFIX.sub("", plain(text))


@pytest.fixture
def feed_inputs(monkeypatch):
    """Return a helper that makes input() return the given answers in order."""

    def _feed_inputs(*answers: str) -> None:
        iterator = iter(answers)
        monkeypatch.setattr("builtins.input", lambda _prompt="": next(iterator))

    return _feed_inputs


# --- parse_input ---------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello", ("hello", [])),
        ("add Bob 123", ("add", ["Bob", "123"])),
        ("ADD Bob 123", ("add", ["Bob", "123"])),  # command lower-cased
        ("Phone Bob", ("phone", ["Bob"])),
        ("  add   Bob   123  ", ("add", ["Bob", "123"])),  # extra spaces
        ("add Bob 123 456", ("add", ["Bob", "123", "456"])),  # extra args kept
        ("", ("", [])),  # "".split() would give [] and crash on [0]
        ("   ", ("", [])),
    ],
)
def test_parse_input(text, expected):
    assert parse_input(text) == expected


def test_parse_input_keeps_arg_case():
    assert parse_input("add BoB +380")[1] == ["BoB", "+380"]


# --- add_contact ---------------------------------------------------------


def test_add_contact():
    contacts = {}
    assert add_contact(["Bob", "123"], contacts) == "Contact added."
    assert contacts == {"Bob": "123"}


def test_add_existing_contact_does_not_overwrite():
    contacts = {"Bob": "123"}
    with pytest.raises(NameExistsError, match="already exists"):
        add_contact(["Bob", "999"], contacts)
    assert contacts == {"Bob": "123"}


@pytest.mark.parametrize("args", [[], ["Bob"], ["Bob", "123", "456"]])
def test_add_contact_wrong_arg_count(args):
    contacts = {}
    with pytest.raises(WrongArgumentsError, match="name and phone"):
        add_contact(args, contacts)
    assert contacts == {}


# --- change_contact ------------------------------------------------------


def test_change_contact():
    contacts = {"Bob": "123"}
    assert change_contact(["Bob", "999"], contacts) == "Contact updated."
    assert contacts == {"Bob": "999"}


def test_change_unknown_contact():
    contacts = {"Bob": "123"}
    with pytest.raises(NotFoundError, match="not found"):
        change_contact(["Alice", "999"], contacts)
    assert contacts == {"Bob": "123"}


@pytest.mark.parametrize("args", [[], ["Bob"], ["Bob", "1", "2"]])
def test_change_contact_wrong_arg_count(args):
    contacts = {"Bob": "123"}
    with pytest.raises(WrongArgumentsError, match="name and phone"):
        change_contact(args, contacts)
    assert contacts == {"Bob": "123"}


# --- show_phone ----------------------------------------------------------


def test_show_phone():
    assert show_phone(["Bob"], {"Bob": "123"}) == "123"


def test_show_phone_unknown_contact():
    with pytest.raises(NotFoundError, match="not found"):
        show_phone(["Alice"], {"Bob": "123"})


@pytest.mark.parametrize("args", [[], ["Bob", "extra"]])
def test_show_phone_wrong_arg_count(args):
    with pytest.raises(WrongArgumentsError, match="a name"):
        show_phone(args, {"Bob": "123"})


# --- show_all ------------------------------------------------------------


def test_show_all_lists_every_contact_in_order():
    contacts = {"Bob": "123", "Alice": "456"}
    assert show_all(contacts) == "Bob: 123\nAlice: 456"


def test_show_all_single_contact_has_no_trailing_newline():
    assert show_all({"Bob": "123"}) == "Bob: 123"


def test_show_all_empty():
    assert show_all({}) == "No contacts."


# --- show_help -----------------------------------------------------------


def test_show_help_lists_every_command():
    text = plain(show_help())
    for word in ["hello", "add", "change", "phone", "all", "help", "close", "exit"]:
        assert word in text


# --- main(): console loop ------------------------------------------------


def test_main_help_command(capsys, feed_inputs):
    feed_inputs("HELP", "exit")

    task4_bot.main()

    out = plain(capsys.readouterr().out)
    assert out.count("Available commands") == 2  # once at start, once for "help"


def test_main_welcome_and_exit(capsys, feed_inputs):
    feed_inputs("exit")

    task4_bot.main()

    lines = plain(capsys.readouterr().out).splitlines()
    assert lines[0] == "Welcome to the assistant bot!"
    assert "Good bye!" in lines[-1]


def test_main_close_also_stops(capsys, feed_inputs):
    feed_inputs("close")

    task4_bot.main()

    assert "Good bye!" in capsys.readouterr().out


def test_main_prompt_text(monkeypatch):
    prompts = []

    def fake_input(prompt=""):
        prompts.append(prompt)
        return "exit"

    monkeypatch.setattr("builtins.input", fake_input)

    task4_bot.main()

    assert len(prompts) == 1
    assert bare(prompts[0]) == "Enter a command: "


def test_main_full_session(capsys, feed_inputs):
    feed_inputs(
        "hello",
        "add Bob 123",
        "add Alice 456",
        "change Bob 999",
        "phone Bob",
        "all",
        "exit",
    )

    task4_bot.main()

    lines = bare(capsys.readouterr().out).splitlines()
    help_lines = len(bare(show_help()).splitlines())
    assert lines[1 : 1 + help_lines] == bare(show_help()).splitlines()
    body = [lines[0], *lines[1 + help_lines :]]
    assert "Good bye!" in body.pop()  # farewell comes from log_goodbye()
    assert [line for line in body if line] == [
        "Welcome to the assistant bot!",
        "How can I help you?",
        "Contact added.",
        "Contact added.",
        "Contact updated.",
        "999",
        "Bob: 999",
        "Alice: 456",
    ]


def test_main_commands_are_case_insensitive(capsys, feed_inputs):
    feed_inputs("HELLO", "Add Bob 123", "PHONE Bob", "EXIT")

    task4_bot.main()

    out = capsys.readouterr().out
    assert "How can I help you?" in out
    assert "123" in out
    assert "Good bye!" in out


@pytest.mark.parametrize("command", ["foo", "add-contact Bob 1", "?"])
def test_main_unknown_command(command, capsys, feed_inputs):
    feed_inputs(command, "exit")

    task4_bot.main()

    assert "Invalid command." in capsys.readouterr().out


@pytest.mark.parametrize("empty", ["", "   "])
def test_main_empty_input_is_ignored(empty, capsys, feed_inputs):
    feed_inputs(empty, "exit")

    task4_bot.main()

    out = capsys.readouterr().out
    assert "Invalid command." not in out
    assert "Good bye!" in out


def test_main_errors_do_not_stop_the_loop(capsys, feed_inputs):
    feed_inputs("add Bob", "phone Alice", "change Alice 1", "all", "exit")

    task4_bot.main()

    out = capsys.readouterr().out
    assert "Give me name and phone please." in out
    assert "Contact not found." in out
    assert "No contacts." in out
    assert "Good bye!" in out
