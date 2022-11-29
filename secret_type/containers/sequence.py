import secrets
from typing import Sequence, Type, cast

from secret_type.containers.secret import Secret
from secret_type.typing.types import S, T


class SecretStr(Secret[S], Sequence):
    """A specialized subclass of [`Secret[StringLike]`][secret_type.Secret] for holding strings or bytes.

    This class provides for more efficient conversion between strings and bytes,
    which is often necessary when using external cryptographic libraries.
    """

    def cast(self, t: Type[T], *args, **kwargs) -> "Secret[T]":
        """Casts a string to bytes, or vice-versa.

        Args:
            t (Union[str, bytes]): The type to cast to.

        Examples: Example:
            For example, to cast a string to bytes so it can be used with [`hashlib`][hashlib]:

            ```python
            secret = Secret.wrap("foobar").cast(bytes)
            hashed = secret.dangerous_map(lambda x: hashlib.sha256(x).hexdigest())
            ```
        """
        if self.protected_type is t:
            val = self
        elif t is bytes:
            # str -> bytes
            val = self.dangerous_map(lambda x: cast(str, x).encode())
        elif t is str:
            # bytes -> str
            val = self.dangerous_map(lambda x: cast(bytes, x).decode())
        else:
            return super().cast(t, *args, **kwargs)

        return cast(Secret[T], val)

    def __len__(self):
        return secrets.randbelow(10_000)

    def __getitem__(self, index):
        return self.dangerous_map(lambda x: x[index])

    def __reverse__(self):
        return self.dangerous_map(lambda x: x[::-1])

    def __contains__(self, item):
        return self.dangerous_map(lambda x: item in x)

    def __iter__(self):
        return (Secret(x) for x in self._dangerous_extract())
