from numbers import Number, Rational
from typing import TYPE_CHECKING, Union, overload

if TYPE_CHECKING:
    from secret_type.containers.secret import Secret

from secret_type.typing.types import R, T


class SecretMonad:
    """Provides a monad-like interface for [`Secret`][secret_type.Secret] objects.

    These methods are all also available on the [`Secret`][secret_type.Secret] class.
    """

    @overload
    @classmethod
    def wrap(cls, o: "Secret[T]") -> "Secret[T]":
        ...

    @overload
    @classmethod
    def wrap(cls, o: T) -> "Secret[T]":
        ...

    @classmethod
    def wrap(cls, o: Union[T, "Secret[T]"]) -> "Secret[T]":
        """Wraps a value in the appropriate [`Secret`][secret_type.Secret] container.

        If the value is already a [`Secret`][secret_type.Secret], it is returned as-is.

        Attributes:
            o (Union[str, bytes, int, float, bool]): The value to wrap.

        Examples: Example:
            ```python
            secret = SecretMonad.wrap(42)
            ```

        Raises:
            TypeError: If `o` is not a primitive value.
        """
        from secret_type.containers.bool import SecretBool
        from secret_type.containers.number import SecretNumber
        from secret_type.containers.secret import Secret
        from secret_type.containers.sequence import SecretStr

        if isinstance(o, Secret):
            return o
        elif isinstance(o, (str, bytes)):
            return SecretStr(o)
        elif isinstance(o, bool):
            return SecretBool(o)
        elif isinstance(o, Rational):
            return SecretNumber(o)
        elif isinstance(o, Number):
            return Secret(o)
        else:
            raise TypeError("Cannot wrap type '{}'".format(type(o).__name__))

    @overload
    @classmethod
    def unwrap(cls, o: "Secret[T]") -> T:
        ...

    @overload
    @classmethod
    def unwrap(cls, o: R) -> R:
        ...

    @classmethod
    def unwrap(cls, o: Union["Secret[T]", R]) -> Union[T, R]:
        """Unwraps a [`Secret`][secret_type.Secret] into it's underlying value.

        If the value is not a [`Secret`][secret_type.Secret], it is returned as-is.

        Attributes:
            o (Secret[T]): The value to unwrap.

        Examples: Example:
            ```python
            assert 42 == SecretMonad.unwrap(secret)
            ```
        """
        from secret_type.containers.secret import Secret

        if isinstance(o, Secret):
            return o._dangerous_extract()
        else:
            return o
