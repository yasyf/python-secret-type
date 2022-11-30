# Quickstart

## tl;dr

1. Wrap any primitive value in [`secret_type.secret`](#secret_type.secret) and use like you would have used the underlying value.
2. Your secret will now be [protected](index.md#secret_type--features): it can't be logged, and all operations on it are constant-time (to avoid timing attacks).
3. See [operations](#secret_type.secret--operations) for unwrapping and using the value. Anything you do involving a secret will create a new secret.

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
