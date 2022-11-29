"""This module contains helper types that are used by the rest of the library."""

from numbers import Integral, Number, Rational
from typing import TypeVar, Union

from typing_extensions import ParamSpec

StringLike = Union[str, bytes]
"""A type that can be treated as a string.
[`Secret[StringLike]`][secret_type.Secret] support all `str` operations."""
IntLike = Union[int, Integral, float, Rational]
"""A numeric type that supports integer operations.

[`Secret[IntLike]`][secret_type.Secret] support all `int` operations."""
NumberLike = Union[complex, Number]
"""A numeric type that does not support integer operations.

[`Secret[NumberLike]`][secret_type.Secret] support only a limited set of numeric operations."""
BoolLike = TypeVar("BoolLike", bound=bool)
"""A boolean type."""
ProtectedValue = Union[StringLike, IntLike, NumberLike, bool]
"""A type that can be wrapped in a [`Secret`][secret_type.Secret]."""


T = TypeVar("T", bound=ProtectedValue)
"""A [`ProtectedValue`][secret_type.typing.types.ProtectedValue]."""
T2 = TypeVar("T2", bound=ProtectedValue)
"""Another [`ProtectedValue`][secret_type.typing.types.ProtectedValue]."""
T_con = TypeVar("T_con", bound=ProtectedValue, contravariant=True)
T_co = TypeVar("T_co", bound=ProtectedValue, covariant=True)

S = TypeVar("S", bound=StringLike)
"""A [`StringLike`][secret_type.typing.types.StringLike]."""
N = TypeVar("N", bound=IntLike)
"""An [`IntLike`][secret_type.typing.types.IntLike]."""

R = TypeVar("R")
P = ParamSpec("P")
