import gc
import pickle
import secrets
from contextlib import contextmanager
from functools import wraps
from numbers import Rational
from typing import Any, Callable, Generator, Generic, Optional, Type, Union, overload

from cryptography.fernet import Fernet

from secret_type.exceptions import *
from secret_type.types import *


class SecretMonad:
    @overload
    @classmethod
    def unwrap(cls, o: "Secret[T]") -> T:
        ...

    @overload
    @classmethod
    def unwrap(cls, o: R) -> R:
        ...

    @classmethod
    def unwrap(cls, o: Union["Secret[T]", R]) -> Union[ProtectedValue, R]:
        if isinstance(o, Secret):
            return o._dangerous_extract()
        else:
            return o

    @overload
    @classmethod
    def wrap(cls, o: "Secret[T]") -> "Secret[T]":
        ...

    @overload
    @classmethod
    def wrap(cls, o: T) -> "Secret[T]":
        ...

    @classmethod
    def wrap(cls, o):
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


class Secret(Generic[T], SecretMonad):
    @classmethod
    def token(cls, length: Optional[int] = None) -> "SecretStr":
        return SecretStr(secrets.token_hex(length // 2 if length else None))

    def __init__(self, value: T):
        key = self.__key = Fernet.generate_key()
        self.__value = Fernet(key).encrypt(pickle.dumps(value, pickle.HIGHEST_PROTOCOL))

    def __del__(self):
        del self.__key
        del self.__value
        gc.collect()

    def cast(self, t: Type[T2], *args, **kwargs) -> "Secret[T2]":
        # Up to the user to provide a valid cast
        return self.dangerous_apply(lambda x: t(x, *args, **kwargs))  # type: ignore

    @property
    def protected_type(self) -> type:
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

    def _dangerous_apply(self, fn: Callable[[T], R]) -> R:
        return fn(pickle.loads(Fernet(self.__key).decrypt(self.__value)))

    def _dangerous_extract(self) -> T:
        return self._dangerous_apply(lambda x: x)

    def dangerous_apply(
        self, fn: Callable[[T], Union["Secret[T2]", T2]]
    ) -> "Secret[T2]":
        return SecretMonad.wrap(self._dangerous_apply(fn))

    @contextmanager
    def dangerous_reveal(self) -> Generator[T, None, None]:
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


from secret_type.bool import SecretBool
from secret_type.number import SecretNumber
from secret_type.sequence import SecretStr
