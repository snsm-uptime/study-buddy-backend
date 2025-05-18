from uuid import UUID


class UserNotFoundError(Exception):
    """Custom exception for user not found errors."""

    def __init__(self, identifier: str, message: str = ""):
        self.identifier = identifier
        self.message = message
        super().__init__(f"User with identifier {identifier} not found. " + message)


class FormValidationError(Exception):
    """Exception raised when no items are found in a query."""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Failed to validate field '{field}': {message}")


class NoItemsFoundError(Exception):
    """Exception raised when no items are found in a query."""

    def __init__(self, query: str):
        super().__init__(f"No items found for query: {query}")


class FileNotFoundError(Exception):
    """Custom exception for file not found errors."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"File {identifier} not found. ")
