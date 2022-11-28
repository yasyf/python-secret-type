import secrets
from contextlib import contextmanager
from functools import wraps
from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

StringLike = Union[str, bytes]
ProtectedValue = Union[bytes, str, int, float, bool]

T = TypeVar("T", bound=ProtectedValue)
T2 = TypeVar("T2", bound=ProtectedValue)
S = TypeVar("S", bound=StringLike)
R = TypeVar("R")


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
        elif isinstance(o, (int, float)):
            return Secret(o)
        else:
            raise TypeError("Cannot wrap type '{}'".format(type(o).__name__))


class Secret(Generic[T], SecretMonad):
    def __init__(self, value: T):
        self.__value = value

    def cast(self, t: Type[T2], *args, **kwargs) -> "Secret[T2]":
        # Up to the user to provide a valid cast
        val = self.dangerous_apply(lambda x: t(x, *args, **kwargs))  # type: ignore
        return cast(Secret[T2], val)

    @property
    def protected_type(self) -> type:
        return type(self.__value)

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
        raise SecretException("Secrets cannot be used as keys")

    def __bool__(self) -> "SecretBool":
        return SecretBool(bool(self.__value))

    def __repr__(self) -> str:
        return f"Secret({self.value_type}, <hidden>)"

    def _dangerous_apply(self, fn: Callable[[T], R]) -> R:
        return fn(self.__value)

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
        aval = a if isinstance(a, (str, bytes)) else repr(a)
        if isinstance(b, type(a)):
            bval = b if isinstance(b, (str, bytes)) else repr(b)
            return SecretBool(secrets.compare_digest(aval, bval))
        else:
            # If the types don't match, we want to always return False
            bval = type(aval)()
            secrets.compare_digest(aval, bval)
            return SecretBool(False)

    def __ne__(self, o: object) -> "SecretBool":
        return self.__eq__(o).flip()

    def __add__(self, other):
        return Secret.wrap(self.__value + other)

    def __radd__(self, other):
        return Secret.wrap(other + self.__value)

    def __mul__(self, other):
        return Secret.wrap(self.__value * other)

    def __rmul__(self, other):
        return Secret.wrap(other * self.__value)

    def __getattr__(self, name: str) -> Any:
        # Wrap any additional type methods that return a ProtectedValue
        if name not in dir(self.protected_type):
            raise SecretAttributeError(self, name)

        fn = getattr(self.__value, name)
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


class SecretBool(Secret[bool]):
    def flip(self):
        return SecretBool(not self._dangerous_extract())

    def __bool__(self):
        raise SecretBoolException()

    def __eq__(self, other):
        return self.dangerous_apply(lambda x: x == other)

    def __repr__(self):
        return repr(self._dangerous_extract())

    def __str__(self):
        return str(self._dangerous_extract())


class SecretStr(Secret[StringLike], Sequence):
    def cast(self, t: Type[T], *args, **kwargs) -> "Secret[T]":
        if self.protected_type is t:
            val = self
        elif t is bytes:
            # str -> bytes
            val = self.dangerous_apply(lambda x: cast(str, x).encode())
        elif t is str:
            # bytes -> str
            val = self.dangerous_apply(lambda x: cast(bytes, x).decode())
        else:
            return super().cast(t, *args, **kwargs)

        return cast(Secret[T], val)

    def __len__(self):
        return secrets.randbelow(10_000)

    def __getitem__(self, index):
        return self.dangerous_apply(lambda x: x[index])

    def __reverse__(self):
        return self.dangerous_apply(lambda x: x[::-1])

    def __contains__(self, item):
        return self.dangerous_apply(lambda x: item in x)

    def __iter__(self):
        return (Secret(x) for x in self._dangerous_extract())
