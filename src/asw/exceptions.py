"""AISUP exceptions."""


class AisupError(Exception):
    """Base AISUP exception."""


class NetworkError(AisupError):
    """Raises when a network error occurs."""


class HTTPError(AisupError):
    """Raises when AISUP responses with HTTP error status code."""


class UnauthorizedError(HTTPError):
    """Raises when user not authenticated."""

    def __init__(self) -> None:
        """Initialize an exception."""
        super().__init__("Not authenticated")


class FileError(AisupError):
    """Base exception for file's errors."""


class HashError(AisupError):
    """Raises when the hash does not match."""

    def __init__(self, guid: str) -> None:
        """Initialize an exception."""
        super().__init__(f"Hash mismatch for file: {guid}")


class JSONDecodeError(AisupError):
    """Raises when couldn't decode response into json."""

    def __init__(self) -> None:
        """Initialize an exception."""
        super().__init__("Couldn't decode response into json")
