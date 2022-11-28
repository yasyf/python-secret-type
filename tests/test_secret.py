import hashlib
import os

import pytest
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from secret_type import Secret
from secret_type.exceptions import SecretBoolException, SecretException


class TestSecret:
    @pytest.fixture
    def secret(self) -> Secret[str]:
        return Secret.wrap("foobar123")

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
