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
      heading_level: 3

## Operations

Of course, to actually be useful, secrets must at some point be _used_, which necessitates them being in plain-text.
There are three ways to use the underlying value of a `secret`.

### 1. Derive a new secret

[`dangerous_map`][secret_type.Secret.dangerous_map] takes a function that operates on the underlying value, and returns a new value to protect.
```python
    new_secret = secret("foo").dangerous_map(lambda x: x + "bar")
```

### 2. Apply a side-effect

[`dangerous_apply`][secret_type.Secret.dangerous_apply] takes a function that operates on the underlying value, and discards the return value.
```python
    secret("foo").dangerous_apply(logger.info)
```

### 3. Access the raw value

[`dangerous_reveal`][secret_type.Secret.dangerous_reveal] is a context manager that yields the underlying value.
```python
    with secret("foo").dangerous_reveal() as value:
    assert value == "foo"
```

## More Docs

For more details, see the [`Secret`][secret_type.Secret] class.
