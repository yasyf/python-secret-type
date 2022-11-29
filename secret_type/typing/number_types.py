from typing import TYPE_CHECKING, Optional, Tuple, Union

if TYPE_CHECKING:
    from secret_type.containers.number import SecretNumber


class IntegerOps:
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

    def __add__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __sub__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __mul__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __floordiv__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __truediv__(self, __x: Union[int, "SecretNumber"]) -> float:
        ...

    def __mod__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __divmod__(self, __x: Union[int, "SecretNumber"]) -> Tuple[int, int]:
        ...

    def __radd__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rsub__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rmul__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rfloordiv__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rtruediv__(self, __x: Union[int, "SecretNumber"]) -> float:
        ...

    def __rmod__(self, __x: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rdivmod__(self, __x: Union[int, "SecretNumber"]) -> Tuple[int, int]:
        ...

    def __pow__(
        self, __x: Union[int, "SecretNumber"], __modulo: int
    ) -> "SecretNumber[int]":
        ...

    def __rpow__(
        self, __x: Union[int, "SecretNumber"], __mod: Optional[int] = ...
    ) -> "SecretNumber[int]":
        ...

    def __and__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __or__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __xor__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __lshift__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rshift__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rand__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __ror__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rxor__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rlshift__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __rrshift__(self, __n: Union[int, "SecretNumber"]) -> "SecretNumber[int]":
        ...

    def __neg__(self) -> "SecretNumber[int]":
        ...

    def __pos__(self) -> "SecretNumber[int]":
        ...

    def __invert__(self) -> "SecretNumber[int]":
        ...

    def __trunc__(self) -> "SecretNumber[int]":
        ...

    def __ceil__(self) -> "SecretNumber[int]":
        ...

    def __floor__(self) -> "SecretNumber[int]":
        ...

    def __round__(self, __ndigits: int = ...) -> "SecretNumber[int]":
        ...

    def __getnewargs__(self) -> Tuple[int]:
        ...

    def __eq__(self, __x: object) -> bool:
        ...

    def __ne__(self, __x: object) -> bool:
        ...

    def __lt__(self, __x: Union[int, "SecretNumber"]) -> bool:
        ...

    def __le__(self, __x: Union[int, "SecretNumber"]) -> bool:
        ...

    def __gt__(self, __x: Union[int, "SecretNumber"]) -> bool:
        ...

    def __ge__(self, __x: Union[int, "SecretNumber"]) -> bool:
        ...

    def __abs__(self) -> "SecretNumber[int]":
        ...
