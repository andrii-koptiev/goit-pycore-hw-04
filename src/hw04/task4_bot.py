"""Task 4: assistant bot.

A console bot that keeps contacts (name -> phone) in a dict.

Requirements:

* Handlers take strings or lists and RETURN strings. They never print.
  All ``print`` and ``input`` happen only in ``main()``.
* ``parse_input(user_input)`` returns ``(command, args)``:
  - the command is lower-cased, the args keep their case
  - extra spaces are ignored (``"  add   Bob   123 "`` -> ``("add", ["Bob", "123"])``)
  - empty or blank input gives ``("", [])`` instead of crashing
* ``add_contact(args, contacts)``  args = ``[name, phone]``
  - ok                       -> ``"Contact added."``
  - name already exists      -> ``"Contact already exists."`` (nothing changes)
  - wrong number of args     -> ``"Give me name and phone please."``
* ``change_contact(args, contacts)``  args = ``[name, phone]``
  - ok                       -> ``"Contact updated."``
  - unknown name             -> ``"Contact not found."``
  - wrong number of args     -> ``"Give me name and phone please."``
* ``show_phone(args, contacts)``  args = ``[name]``
  - ok                       -> the phone number
  - unknown name             -> ``"Contact not found."``
  - wrong number of args     -> ``"Give me a name please."``
* ``show_all(contacts)``
  - one ``"name: phone"`` line per contact, in insertion order, joined by ``"\\n"``
  - no contacts              -> ``"No contacts."``
* ``main()`` prints ``"Welcome to the assistant bot!"``, then loops on
  ``input("Enter a command: ")``. Commands are case-insensitive:
  - ``hello``        -> ``"How can I help you?"``
  - ``add``, ``change``, ``phone``, ``all`` -> the handlers above
  - ``close``/``exit`` -> ``"Good bye!"`` and the loop stops
  - empty input      -> ignored (just asks again)
  - anything else    -> ``"Invalid command."``
* ``run()`` is the entry point for the menu and simply starts ``main()``.
"""

from hw04.exceptions import (
    Hw04Error,
    NameExistsError,
    NotFoundError,
    WrongArgumentsError,
)
from hw04.log import (
    format_option,
    log_error,
    log_goodbye,
    log_prompt,
    log_result,
    log_title,
)

type Args = list[str]
type Contacts = dict[str, str]


COMMANDS: list[tuple[str, str]] = [
    ("hello", "greet the bot"),
    ("add <name> <phone>", "save a new contact"),
    ("change <name> <phone>", "update the phone of an existing contact"),
    ("phone <name>", "show the phone of a contact"),
    ("all", "show all contacts"),
    ("help", "show this list of commands"),
    ("close | exit", "leave the bot"),
]

PROMPT = "Enter a command: "


def parse_input(user_input: str) -> tuple[str, Args]:
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args


def add_contact(args: Args, contacts: Contacts) -> str:
    if len(args) != 2:
        raise WrongArgumentsError("Give me name and phone please.")
    name, phone = args

    if name in contacts:
        raise NameExistsError("Contact already exists.")

    contacts[name] = phone
    return "Contact added."


def change_contact(args: Args, contacts: Contacts) -> str:
    if len(args) != 2:
        raise WrongArgumentsError("Give me name and phone please.")
    name, phone = args

    if name not in contacts:
        raise NotFoundError("Contact not found.")

    contacts[name] = phone
    return "Contact updated."


def show_phone(args: Args, contacts: Contacts) -> str:
    if len(args) != 1:
        raise WrongArgumentsError("Give me a name please.")
    (name,) = args

    if name not in contacts:
        raise NotFoundError("Contact not found.")

    return contacts[name]


def show_all(contacts: Contacts) -> str:
    if not contacts:
        return "No contacts."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def show_help() -> str:
    width = max(len(usage) for usage, _ in COMMANDS)
    lines = [format_option(usage, description, width) for usage, description in COMMANDS]
    return "\n".join(["Available commands (case-insensitive):", *lines])


def main() -> None:
    contacts: Contacts = {}
    log_title("Welcome to the assistant bot!")
    print(show_help())
    while True:
        command, args = parse_input(log_prompt(PROMPT))
        if not command:
            continue

        try:
            match command:
                case "close" | "exit":
                    log_goodbye()
                    break
                case "hello":
                    log_result("How can I help you?")
                case "add":
                    log_result(add_contact(args, contacts))
                case "change":
                    log_result(change_contact(args, contacts))
                case "phone":
                    log_result(show_phone(args, contacts))
                case "all":
                    print(show_all(contacts))
                case "help":
                    print(show_help())
                case _:
                    log_error("Invalid command. Type 'help' to see the commands.")
        except Hw04Error as e:
            log_error(str(e))


def run() -> None:
    main()
