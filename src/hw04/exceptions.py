class Hw04Error(Exception):
    """Base class for all errors in this app."""


class CorruptLineError(Hw04Error):
    """A line in the file has the wrong format."""

    def __init__(self, line_number: int, line: str) -> None:
        self.line_number = line_number
        self.line = line
        super().__init__(f"File corrupted: line {line_number} is invalid: {line!r}")


class EmptyFileError(Hw04Error):
    """When file is empty."""

    def __init__(self, message: str = "File is empty.") -> None:
        super().__init__(message)


class DuplicateIdError(Hw04Error):
    """File has duplicated ids."""

    def __init__(self, line_number: int, duplicate_id: str) -> None:
        self.line_number = line_number
        self.duplicate_id = duplicate_id
        super().__init__(
            f"File has duplicated id: line {line_number} repeats {duplicate_id!r}"
        )


class WrongArgumentsError(Hw04Error):
    """User not provided required arguments."""

    def __init__(self, message: str = "missing arguments") -> None:
        super().__init__(message)


class NameExistsError(Hw04Error):
    """Name already exist."""

    def __init__(self, message: str = "already exist") -> None:
        super().__init__(message)


class NotFoundError(Hw04Error):
    """Not found value"""

    def __init__(self, message: str = "not found") -> None:
        super().__init__(message)
