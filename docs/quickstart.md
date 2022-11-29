# Quickstart

## tl;dr

Wrap any value in [`secret_type.secret`](#secret_type.secret) and use like you would have used the underlying value. See [operations](#secret_type.secret--operations) for unwrapping and using the value.

```python
from secret_type import secret

protected = secret("hello") + ", world!"
# `print(protected)` would raise an exception
with protected.dangerous_reveal() as value:
    assert value == "hello, world!"
```

## One Function to Rule Them All

<!-- prettier-ignore -->
::: secret_type.secret
    options:
      show_root_heading: true
