import hashlib
import math
import os

import pytest
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from secret_type import Secret
from secret_type.exceptions import (
    SecretBoolException,
    SecretException,
    SecretFloatException,
)
from secret_type.number import SecretNumber


class TestSecret:
    @pytest.fixture
    def secret(self) -> Secret[str]:
        return Secret.wrap("foobar123")

    @pytest.fixture
    def int_secret(self) -> Secret[int]:
        return Secret.wrap(42)

    def test_print_secret(self, secret: Secret[str]):
        with pytest.raises(SecretException):
            print(secret)

    def test_str_secret(self, secret: Secret[str]):
        with pytest.raises(SecretException):
            str(secret)

    def test_compare_secret(self, secret: Secret[str]):
        assert str(secret != "secret") == "True"
        assert str(secret == "foobar123") == "True"

        with pytest.raises(SecretBoolException):
            if secret != "foobar123":
                assert False

    def test_secret_derived_bools(self, secret: Secret[str]):
        check = secret.isalnum()

        with pytest.raises(SecretBoolException):
            print(True if check else False)

    def test_secret_sha1_fails(self, secret: Secret[str]):
        with pytest.raises(SecretException):
            hashlib.sha1(secret.encode())

    def test_secret_sha1_succeeds(self, secret: Secret[str]):
        sha1 = secret.cast(bytes).dangerous_apply(lambda x: hashlib.sha1(x).hexdigest())

        with pytest.raises(SecretException):
            assert sha1 == b"6ffd8b80f2a76ca670ae33ab196f7936d59fb43b"

        with sha1.cast(bytes).dangerous_reveal() as revealed:
            assert revealed == b"6ffd8b80f2a76ca670ae33ab196f7936d59fb43b"

    def test_secret_kdf(self, secret: Secret[str]):
        salt = os.urandom(16)
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

        with pytest.raises(SecretException):
            kdf.derive(secret.encode())

        key = secret.cast(bytes).dangerous_apply(kdf.derive)

        # store key as plaintext
        key_plain = key._dangerous_extract()
        with pytest.raises(SecretException):
            kdf.verify(secret.encode(), key_plain)

        # verify key
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        with secret.cast(bytes).dangerous_reveal() as revealed:
            kdf.verify(revealed, key_plain)

    def test_secret_concat(self, secret: Secret[str]):
        result = secret + "foobar"

        with pytest.raises(SecretException):
            print(result)

        with result.dangerous_reveal() as revealed:
            assert revealed == "foobar123foobar"

    def test_secret_multiply(self, secret: Secret[str]):
        result = 1 * secret * 3

        with pytest.raises(SecretException):
            print(result)

        with result.dangerous_reveal() as revealed:
            assert revealed == "foobar123" * 3

    def test_int_secret(self, int_secret: SecretNumber[int]):
        one_hundred = int_secret + 58
        one_thousand_six_hundred = one_hundred << 4
        one_hundred_squared = (one_thousand_six_hundred >> 4) * one_hundred

        with pytest.raises(SecretFloatException):
            one_hundred_squared.dangerous_apply(math.sqrt)

        one_hundred_again = one_hundred_squared.dangerous_apply(lambda x: x // 100)

        with pytest.raises(SecretException):
            print(one_hundred_again)

        with one_hundred_again.dangerous_reveal() as revealed:
            assert revealed == 100

    def test_token(self):
        token = Secret.token(32)

        with pytest.raises(SecretException):
            print(token)

        with token.dangerous_reveal() as revealed:
            assert len(revealed) == 32
