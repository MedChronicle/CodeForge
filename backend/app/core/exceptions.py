class DomainError(Exception):
    """Expected business error that can safely be returned to the client."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(DomainError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, 404)


class AuthenticationError(DomainError):
    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, 401)
