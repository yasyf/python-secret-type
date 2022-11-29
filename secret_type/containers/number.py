import operator
from abc import ABCMeta
from numbers import Integral

from secret_type.containers.secret import Secret
from secret_type.exceptions import SecretFloatException, SecretKeyException
from secret_type.typing.number_types import IntegerOps
from secret_type.typing.types import N


class SecretNumberMeta(ABCMeta):
    @classmethod
    def _make_wrapper(mcls, cls, op):
        def forward(self, other, *args, **kwargs):
            return Secret.wrap(
                getattr(operator, op)(self._dangerous_extract(), other, *args, **kwargs)
            )

        def backward(self, other, *args, **kwargs):
            return Secret.wrap(
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
        for op in IntegerOps.UNI_OPS + IntegerOps.BI_OPS:
            forward, backward = mcls._make_wrapper(cls, op)
            mcls._make_concrete(cls, forward)
            if op in IntegerOps.BI_OPS:
                mcls._make_concrete(cls, backward)
        return cls


class SecretNumber(IntegerOps, Secret[N], Integral, metaclass=SecretNumberMeta):
    """A specialized subclass of [`Secret[IntLike]`][secret_type.Secret] for holding ints or floats.

    This class provides wrappers for every major numeric operation supported by `int`.
    Simply call the methods as you would on a regular `int`.
    The result will, of course, be another `SecretNumber`.
    """

    def __index__(self) -> "SecretNumber[int]":
        raise SecretKeyException()

    def __int__(self) -> "SecretNumber[int]":
        return SecretNumber(int(self._dangerous_extract()))

    def __float__(self) -> "SecretNumber[float]":
        return SecretNumber(float(self._dangerous_extract()))

    def __complex__(self) -> complex:
        raise SecretFloatException()
