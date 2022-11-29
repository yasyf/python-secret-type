# `secret`
### A [Rune](https://github.com/google/rune)-style type for sensitive values in Python

[![PyPI - Version](https://img.shields.io/pypi/v/secret-type.svg)](https://pypi.org/project/secret-type)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/secret-type.svg)](https://pypi.org/project/secret-type)
[![Documentation Status](https://readthedocs.org/projects/python-secret-type/badge/?version=latest)](https://python-secret-type.readthedocs.io/en/latest/?badge=latest)

---

`secret-type` provides a convenient type (`secret`) to indicate that a value is considered sensitive, similar to the `secret` type in Google's [Rune Lang](https://github.com/google/rune).

## Installation

```console
pip install secret-type
```

## Usage

```pycon
>>> from secret_type import secret
>>> password = secret("a very secret value") # Secrets can be any primitive value

>>> print(password) # Runtime exceptions prevent logging
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "secret_type/containers/secret.py", line 91, in __str__
    raise SecretException()
secret_type.exceptions.SecretException: Secrets cannot be examined

>>> better_password = password + "!" # Operations derive new secrets
>>> >>> type(better_password)
<class 'secret_type.sequence.SecretStr'>

>>> better_password.dangerous_apply(print)
a very secret value!
```

# Features
  - When marked as secret, values cannot be printed or logged; attempting to do so will raise an exception.
  - Secrets are "viral"; any operation on a secret will also return a secret.
  - Comparison operations with a `secret` are guaranteed to be constant-time.This helps avoid timing attacks.
  - A `bool` derived from a secret cannot be used for control flow.
  - Secrets cannot be used as indexes or keys for containers.
  - Internally, the underlying value is stored encrypted in memory, and is only decrypted when deriving a new value.
  - As soon as secrets are out of scope, the Garbage Collector is encouraged to immediately collect them.

# Docs

For complete docs, see the [Quickstart](https://python-secret-type.readthedocs.io/en/latest/quickstart/).
# Comparison to Rune
Rune makes the following guarantees about a `secret`:

> - All operations on secrets occur in constant time, minimizing timing side-channel leakage.
- Secrets cannot be used in conditional branches or memory addressing.
- Even speculative branching and indexing on secrets are caught at compile-time to avoid Specter/Meltdown.
- Secrecy is sticky: any value in part derived from a secret is considered secret until "revealed".
- Secrets are automatically zeroed when no longer used

This projects attempts to do something similar, but with the runtime constraints of Python.

## License

`secret-type` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
