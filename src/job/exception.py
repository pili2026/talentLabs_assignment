class NotFoundException(Exception):
    """Raised when an entity is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotFoundException: {self.message}"
