from secret_type.containers.secret import Secret
from secret_type.exceptions import SecretBoolException
from secret_type.typing.types import BoolLike


class SecretBool(Secret[BoolLike]):
    """A specialized subclass of [`Secret[bool]`][secret_type.Secret] for holding bool results.

    This class is returned whenever a `bool` is derived from an operation on a [`Secret`][secret_type.Secret].
    It ensures that the result cannot be used for control flow,
    unless explicitly allowed by using [`dangerous_reveal`][secret_type.Secret.dangerous_reveal].
    """

    def flip(self):
        """Flip the value of the contained bool without revealing it."""
        return SecretBool(not self._dangerous_extract())

    def __bool__(self):
        raise SecretBoolException()

    def __eq__(self, other):
        return self.dangerous_map(lambda x: x == other)

    def __repr__(self):
        return repr(self._dangerous_extract())

    def __str__(self):
        return str(self._dangerous_extract())
