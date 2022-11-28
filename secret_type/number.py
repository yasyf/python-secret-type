import operator
from abc import ABCMeta
from numbers import Integral

from secret_type.base import Secret
from secret_type.exceptions import SecretFloatException, SecretKeyException
from secret_type.types import N


class SecretNumberMeta(ABCMeta):
    BI_OPS = [
        "add",
        "sub",
        "mul",
        "truediv",
        "floordiv",
        "mod",
        "divmod",
        "pow",
        "lshift",
        "rshift",
        "and",
        "xor",
        "or",
    ]
    UNI_OPS = [
        "neg",
        "pos",
        "abs",
        "invert",
        "round",
        "trunc",
        "floor",
        "ceil",
        "lt",
        "le",
    ]

    @classmethod
    def _make_wrapper(mcls, cls, op):
        def forward(self, other, *args, **kwargs):
            return cls(
                getattr(operator, op)(self._dangerous_extract(), other, *args, **kwargs)
            )

        def backward(self, other, *args, **kwargs):
            return cls(
                getattr(operator, op)(other, self._dangerous_extract(), *args, **kwargs)
            )

        forward.__name__ = f"__{op}__"
        backward.__name__ = f"__r{op}__"
        return forward, backward

    @classmethod
    def _make_concrete(mcls, cls, fn):
        setattr(cls, fn.__name__, fn)
        cls.__abstractmethods__ = cls.__abstractmethods__ - {fn.__name__}

    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)
        for op in mcls.UNI_OPS + mcls.BI_OPS:
            forward, backward = mcls._make_wrapper(cls, op)
            mcls._make_concrete(cls, forward)
            if op in mcls.BI_OPS:
                mcls._make_concrete(cls, backward)
        return cls


class SecretNumber(Secret[N], Integral, metaclass=SecretNumberMeta):
    def __index__(self) -> int:
        raise SecretKeyException()

    def __int__(self) -> "SecretNumber[int]":
        return SecretNumber(
            int(self._dangerous_extract())
        )  # pyright: ignore [reportGeneralTypeIssues]

    def __float__(self) -> float:
        raise SecretFloatException()

    def __complex__(self) -> complex:
        raise SecretFloatException()
