from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from secret_type.secret import Secret


class SecretException(Exception):
    def __init__(self, message: str = "Secrets cannot be examined") -> None:
        super().__init__(message)


class SecretBoolException(SecretException):
    def __init__(
        self,
        message: str = "bools derived from Secrets cannot be used for control flow",
    ) -> None:
        super().__init__(message)


class SecretAttributeError(AttributeError, SecretException):
    def __init__(self, s: "Secret", name: str) -> None:
        message = f"{s.protected_type.__name__} has no attribute {name}"
        super().__init__(message)
