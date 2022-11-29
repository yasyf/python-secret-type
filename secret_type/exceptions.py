"""This module contains exceptions that are used by the rest of the library."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from secret_type.containers.secret import Secret


class SecretException(Exception):
    """The base exception for this library.

    All other exceptions are subclasses of this one."""

    def __init__(self, message: str = "Secrets cannot be examined") -> None:
        super().__init__(message)


class SecretFloatException(SecretException):
    """Raised when an unsupported operation is attempted on a [`Secret[NumberLike]`][secret_type.typing.types.NumberLike]."""

    def __init__(
        self,
        message: str = "Secrets cannot be used as non-integral numbers",
    ) -> None:
        super().__init__(message)


class SecretKeyException(SecretException):
    """Raised when a [`Secret`][secret_type.Secret] is used as a key or index."""

    def __init__(
        self,
        message: str = "Secrets cannot be used as keys",
    ) -> None:
        super().__init__(message)


class SecretBoolException(SecretException):
    """Raised when a [`Secret[bool]`][secret_type.Secret] is used for control flow."""

    def __init__(
        self,
        message: str = "bools derived from Secrets cannot be used for control flow",
    ) -> None:
        super().__init__(message)


class SecretAttributeError(AttributeError, SecretException):
    def __init__(self, s: "Secret", name: str) -> None:
        message = f"{s.protected_type.__name__} has no attribute {name}"
        super().__init__(message)
