"""Password utility functions."""

import bcrypt
import hashlib
import os

# commom way to hash password and verify password
# bcrypt is designed to be secure and slow to thwart brute-force attacks, no system is entirely immune to attacks.

def hash_password(password: str) -> str:
    """Return a salted password hash."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Return True if password matches hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


# you can store salt and hashed password in the database
# attacker need password and salt to crack the password

def hash_password_with_salt(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  # 16 bytes salt
    hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt, hash

def verify_password_with_salt(stored_salt, stored_hash, input_password):
    _, hash = hash_password(input_password, stored_salt)
    return hash == stored_hash