from secret_type.exceptions import SecretBoolException
from secret_type.secret import Secret


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
