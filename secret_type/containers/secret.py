import gc
import pickle
import secrets
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Generator, Generic, Optional, Type, Union

from cryptography.fernet import Fernet
from typing_extensions import Concatenate

from secret_type.exceptions import *
from secret_type.monad import SecretMonad
from secret_type.typing.types import *

ApplyFn = Callable[Concatenate[T, P], Any]
MapFn = Callable[Concatenate[T, P], Union["Secret[T2]", T2]]


class Secret(Generic[T], SecretMonad):
    """The base container for holding secrets.

    This class can be instantiated directly with any [`ProtectedValue`][secret_type.typing.types.ProtectedValue],
    but using the monad-like [`Secret.wrap`][secret_type.monad.SecretMonad.wrap] method is preferred,
    as it will use specialized subclasses that provide extra functionality."""

    @classmethod
    def token(cls, length: Optional[int] = None) -> "SecretStr":
        """Generate a cryptographically secure random token, and wrap it in a [`SecretStr`][secret_type.containers.SecretStr].

        Args:
            length: The length of the token to generate.
        """
        return SecretStr(secrets.token_hex(length // 2 if length else None))

    def __init__(self, value: T):
        key = self.__key = Fernet.generate_key()
        self.__value = Fernet(key).encrypt(pickle.dumps(value, pickle.HIGHEST_PROTOCOL))

    def __del__(self):
        del self.__key
        del self.__value
        gc.collect()

    def cast(self, t: Type[T2], *args, **kwargs) -> "Secret[T2]":
        """Casts the content of the secret to a new type.
        Any additional arguments are passed to the constructor of the new type.

        Returns:
            A new [`Secret`][secret_type.Secret] of the new type.

        Args:
            t: The primitive type to cast to.

        Raises:
            ValueError: If the value cannot be cast to the new type.
        """
        # Up to the user to provide a valid cast
        return self.dangerous_map(lambda x: t(x, *args, **kwargs))  # type: ignore

    @property
    def protected_type(self) -> type:
        """The type of the protected value."""
        return type(self._dangerous_extract())

    def __int__(self) -> int:
        raise SecretException()

    def __float__(self) -> float:
        raise SecretException()

    def __complex__(self) -> complex:
        raise SecretException()

    def __str__(self) -> str:
        raise SecretException()

    def __bytes__(self) -> bytes:
        raise SecretException()

    def encode(self, encoding: str = "utf-8") -> bytes:
        raise SecretException()

    def __hash__(self) -> str:
        raise SecretKeyException()

    def __bool__(self) -> "SecretBool":
        return SecretBool(bool(self._dangerous_extract()))

    def __repr__(self) -> str:
        return f"Secret({self.protected_type}, <hidden>)"

    def _dangerous_map(self, fn: Callable[[T], R], *args, **kwargs) -> R:
        return fn(
            pickle.loads(Fernet(self.__key).decrypt(self.__value)), *args, **kwargs
        )

    def _dangerous_extract(self) -> T:
        return self._dangerous_map(lambda x: x)

    def dangerous_apply(self, fn: ApplyFn[T, P], *args, **kwargs) -> None:
        """Apply a function to the secret value, discarding the result.
        Any additional arguments are passed to the function.

        Use this method when you want to enact a side-effect with the contents of your secret.
        If you want to return a new secret, use [`dangerous_map`][secret_type.Secret.dangerous_map] instead.

        Args:
            fn (Callable[[T, ...], Any]): The function to apply to the secret value.
                The first positional argument must be the unwrapped value.

        Examples: Example:
            This is how one would print the secret value.

            ```python
            Secret.wrap("hello").dangerous_apply(print)
            ```
        """
        self._dangerous_map(fn, *args, **kwargs)

    def dangerous_map(self, fn: MapFn[T, P, T2], *args, **kwargs) -> "Secret[T2]":
        """Apply a function to the secret value, and wrap the result in a new secret.
        Any additional arguments are passed to the function.

        You must ensure the return type of `fn` is a [`Secret`][secret_type.Secret] or a primitive type.

        Args:
            fn (Callable[[T, ...], Union[Secret[T2], T2]]): The function to apply to the secret value.
                The first positional argument must be the unwrapped value.

        Returns:
            A new [`Secret`][secret_type.Secret] of the return type of `fn`.

        Examples: Example:
            This is how one would hash the secret value.

            ```python
            Secret.wrap("foobar").cast(bytes).dangerous_map(lambda x: hashlib.sha1(x).hexdigest())
            ```

        Raises:
            TypeError: If the return of `fn` cannot be wrapped in a [`Secret`][secret_type.Secret].
        """
        return SecretMonad.wrap(self._dangerous_map(fn, *args, **kwargs))

    @contextmanager
    def dangerous_reveal(self) -> Generator[T, None, None]:
        """A context manager that provides the unwrapped secret value.

        This method is intended to be used in a `with` statement,
        and allows you to operate on the secret value in it's original form.

        Examples: Example:
            This is how one would persist the secret value.

            ```python
            with Secret.wrap("foobar").dangerous_reveal() as value:
                save_to_db(value)
            ```
        """
        yield self._dangerous_extract()

    def __eq__(self, o: Union["Secret[T2]", R]) -> "SecretBool":
        a, b = SecretMonad.unwrap(self), SecretMonad.unwrap(o)
        aval = a if isinstance(a, (str, bytes)) else str(a)
        if isinstance(b, type(a)):
            bval = b if isinstance(b, (str, bytes)) else str(b)
            return SecretBool(secrets.compare_digest(aval, bval))
        else:
            # If the types don't match, we want to always return False
            bval = type(aval)()
            secrets.compare_digest(aval, bval)
            return SecretBool(False)

    def __ne__(self, o: object) -> "SecretBool":
        return self.__eq__(o).flip()

    def __add__(self, other) -> "Secret[T]":
        return Secret.wrap(self._dangerous_extract() + other)

    def __radd__(self, other) -> "Secret[T]":
        return Secret.wrap(other + self._dangerous_extract())

    def __mul__(self, other) -> "Secret[T]":
        return Secret.wrap(self._dangerous_extract() * other)

    def __rmul__(self, other) -> "Secret[T]":
        return Secret.wrap(other * self._dangerous_extract())

    def __getattr__(self, name: str) -> Any:
        # Wrap any additional type methods that return a ProtectedValue
        if name not in dir(self.protected_type):
            raise SecretAttributeError(self, name)

        fn = getattr(self._dangerous_extract(), name)
        if not isinstance(fn, Callable):
            raise SecretAttributeError(self, name)

        @wraps(fn)
        def wrapped(*args, **kwargs):
            val = fn(*args, **kwargs)
            try:
                return SecretMonad.wrap(val)
            except TypeError:
                raise NotImplementedError(fn.__name__)

        return wrapped


from secret_type.containers.bool import SecretBool
from secret_type.containers.sequence import SecretStr
