import secrets

import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def generate_session_id():
    return secrets.token_urlsafe(16)

