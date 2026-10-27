class Hw04Error(Exception):
    """Base class for all errors in this app."""


class CorruptLineError(Hw04Error):
    """A line in the file is not in 'Name,salary' format."""

    def __init__(self, line_number: int, line: str) -> None:
        self.line_number = line_number
        self.line = line
        super().__init__(f"line {line_number} is invalid: {line!r}")


class EmptyFileError(Hw04Error):
    def __init__(self, message: str = "the file contains no salary data") -> None:
        super().__init__(message)
