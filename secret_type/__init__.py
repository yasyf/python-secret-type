# SPDX-FileCopyrightText: 2022-present Yasyf Mohamedali <yasyfm@gmail.com>
#
# SPDX-License-Identifier: MIT

from secret_type.base import Secret
from secret_type.types import T


def secret(o: T) -> Secret[T]:
    return Secret.wrap(o)
