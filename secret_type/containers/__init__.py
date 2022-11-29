"""This class contains specialized containers for holding secrets of various types."""

from secret_type.containers.secret import (  # noqa # isort:skip
    Secret as Secret,
)

from secret_type.containers.bool import SecretBool as SecretBool
from secret_type.containers.number import SecretNumber as SecretNumber
from secret_type.containers.sequence import SecretStr as SecretStr
