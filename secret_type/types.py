from numbers import Integral, Number
from typing import TypeVar, Union

StringLike = Union[str, bytes]
IntLike = Union[int, Integral]
FloatLike = Union[float, complex, Number]
ProtectedValue = Union[StringLike, IntLike, FloatLike, bool]

T = TypeVar("T", bound=ProtectedValue)
T2 = TypeVar("T2", bound=ProtectedValue)
S = TypeVar("S", bound=StringLike)
N = TypeVar("N", bound=IntLike)
R = TypeVar("R")
