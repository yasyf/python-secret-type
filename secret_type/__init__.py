# SPDX-FileCopyrightText: 2022-present Yasyf Mohamedali <yasyfm@gmail.com>
#
# SPDX-License-Identifier: MIT
"""`secret-type` provides a convenient type (`secret`) to indicate that a value is considered sensitive,
    similar to the `secret` type in Google's [Rune Lang](https://github.com/google/rune).

    ```pycon
    >>> from secret_type import secret
    >>> password = secret("a very secret value") # (1)!

    >>> print(password) # (2)!
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "secret_type/containers/secret.py", line 91, in __str__
        raise SecretException()
    secret_type.exceptions.SecretException: Secrets cannot be examined

    >>> better_password = password + "!" # (3)!
    >>> >>> type(better_password)
    <class 'secret_type.sequence.SecretStr'>

    >>> better_password.dangerous_apply(print) # (4)!
    a very secret value!
    ```

    1. Secrets can be any primitive value
    2. Runtime exceptions prevent logging
    3. Operations derive new secrets
    4. Use [`dangerous_apply`][secret_type.Secret.dangerous_apply] or [`dangerous_map`][secret_type.Secret.dangerous_map] to access the underlying value

    # Docs

    For complete docs, see the [Quickstart](quickstart.md), or check out the [API Reference](reference/index.md).

    # Features
      - When marked as secret, values cannot be printed or logged; attempting to do so will raise an exception.
      - Secrets are "viral"; any operation on a secret will also return a secret.
      - Comparison operations with a `secret` are guaranteed to be constant-time.
        This helps avoid timing attacks.
      - A `bool` derived from a secret cannot be used for control flow.
      - Secrets cannot be used as indexes or keys for containers.
      - Internally, the underlying value is stored encrypted in memory, and is only decrypted when deriving a new value.
      - As soon as secrets are out of scope, the Garbage Collector is encouraged to immediately collect them.

    # Comparison to Rune
    Rune makes the following guarantees about a `secret`:

    > - All operations on secrets occur in constant time, minimizing timing side-channel leakage.
    - Secrets cannot be used in conditional branches or memory addressing.
    - Even speculative branching and indexing on secrets are caught at compile-time to avoid Specter/Meltdown.
    - Secrecy is sticky: any value in part derived from a secret is considered secret until "revealed".
    - Secrets are automatically zeroed when no longer used

    This projects attempts to do something similar, but with the runtime constraints of Python.
    """

from typing import Union as Union

from secret_type.containers.secret import Secret as Secret
from secret_type.monad import SecretMonad as SecretMonad
from secret_type.typing.types import T


def secret(o: T) -> Secret[T]:
    """This single function provides a convenient to indicate that a value is considered sensitive.

    Sensitive values can be any (subclass of a) non-container primitive.
    Simply wrap the value in a call to `secret`, and off you go!
    Any operations you do on that wrapped value will also return a `secret`.

    Attributes:
      o (Union[str, bytes, int, float, bool]): The value to mark as secret.

    Examples: Example:
      Here is an example using `secret` to protect a key derived from a user password.
      We want to make sure that no one is able to accidentally log either of these values,
      that all comparison operations are constant-time, and that any derived values are also secret.

      ```python
      from secret_type import secret
      from cryptography.hazmat.primitives.kdf.scrypt import Scrypt # (1)!

      salt = os.urandom(16) # (2)!

      def derive_key(user_password: str):
        password = secret(user_password)
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

        key = password.cast(bytes).dangerous_map(kdf.derive) # (3)!

        with key.dangerous_reveal() as key: # (4)!
          persist_to_database(key)

      # Some time later...

      def check_password(entered_password: str):
        password = secret(entered_password)
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

        key = secret(get_key_from_database()) # (5)!
        password.cast(bytes).dangerous_apply(kdf.verify, key) # (6)!
      ```

      1. We're using `Scrypt` as an example, but `secret` is not specific to the `cryptography` package.
      2. A random salt that does not need to be secret.
      3. We first use [`cast`][secret_type.Secret.cast] to convert the `secret` to a `bytes` object,
        then use [`dangerous_map`][secret_type.Secret.dangerous_map] to run the key derivation function,
        wrapping the result in a new `secret`.
      4. We must use [`dangerous_reveal`][secret_type.Secret.dangerous_reveal] to expose the actual key,
        which we persist to a database.
      5. We retreive the plain-text key from the database, and immediately call `secret` on it to resume
        our protections.
      6. Here we use [`dangerous_apply`][secret_type.Secret.dangerous_apply] to run the key verification function,
        which raises if it fails. We use this instead of [`dangerous_map`][secret_type.Secret.dangerous_map] as we don't care about the return value.
    """
    return Secret.wrap(o)
