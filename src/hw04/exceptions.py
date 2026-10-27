class Hw04Error(Exception):
    """Base class for all errors in this app."""


class CorruptLineError(Hw04Error):
    """A line in the file has the wrong format.."""

    def __init__(self, line_number: int, line: str) -> None:
        self.line_number = line_number
        self.line = line
        super().__init__(f"line {line_number} is invalid: {line!r}")


class EmptyFileError(Hw04Error):
    def __init__(self, message: str = "the file contains no data") -> None:
        super().__init__(message)


class DuplicateIdError(Hw04Error):
    def __init__(self, line_number: int, duplicate_id: str) -> None:
        self.line_number = line_number
        self.line = duplicate_id
        super().__init__(f"line {line_number} has duplicated id: {duplicate_id!r}")
