import secrets
from typing import Sequence, Type, cast

from secret_type.base import Secret
from secret_type.types import StringLike, T


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
