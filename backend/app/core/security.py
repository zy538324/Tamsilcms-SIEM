import hashlib
import hmac
import os
from dataclasses import dataclass

from app.core.config import settings

PBKDF2_ITERATIONS = 200_000
SALT_BYTES = 16


@dataclass(frozen=True)
class ApiKeyHash:
    salt: str
    hash_hex: str

    def to_storage(self) -> str:
        return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${self.salt}${self.hash_hex}"


def _pbkdf2_hash(api_key: str, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        api_key.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return digest.hex()


def generate_api_key_hash(api_key: str) -> str:
    salt = os.urandom(SALT_BYTES)
    digest = _pbkdf2_hash(api_key + settings.api_key_pepper, salt)
    return ApiKeyHash(salt.hex(), digest).to_storage()


def verify_api_key(api_key: str, stored_hash: str) -> bool:
    try:
        _, iterations, salt_hex, hash_hex = stored_hash.split("$", maxsplit=3)
    except ValueError:
        return False

    if int(iterations) != PBKDF2_ITERATIONS:
        return False

    salt = bytes.fromhex(salt_hex)
    expected = _pbkdf2_hash(api_key + settings.api_key_pepper, salt)
    return hmac.compare_digest(expected, hash_hex)
