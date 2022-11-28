from secret_type.base import Secret
from secret_type.exceptions import SecretBoolException


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
