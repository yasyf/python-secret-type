from typing import TypeVar, Union

StringLike = Union[str, bytes]
ProtectedValue = Union[bytes, str, int, float, bool]

T = TypeVar("T", bound=ProtectedValue)
T2 = TypeVar("T2", bound=ProtectedValue)
S = TypeVar("S", bound=StringLike)
R = TypeVar("R")
