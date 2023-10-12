from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.app.auth.security import generate_session_id
from backend.app.db.redis import get_redis

REDIS_SESSION_ID_KEY_TEMPLATE = "session_id.{}"


class AuthSettings(BaseSettings):
    session_ttl: timedelta = timedelta(days=1)
    session_cookie_ttl: timedelta = timedelta(days=1)

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
    )


auth_settings = AuthSettings()


def create_auth_session(profile_id: int) -> str | None:
    session_id = generate_session_id()

    key = REDIS_SESSION_ID_KEY_TEMPLATE.format(session_id)
    ttl = int(auth_settings.session_ttl.total_seconds())
    print(ttl)
    conn = get_redis()
    if not conn.set(key, profile_id, ex=ttl):
        return None

    return session_id


def delete_auth_session(session_id: str) -> None:
    key = REDIS_SESSION_ID_KEY_TEMPLATE.format(session_id)

    conn = get_redis()
    conn.delete(key)


def get_profile_id_by_session_id(session_id: str) -> int | None:
    key = REDIS_SESSION_ID_KEY_TEMPLATE.format(session_id)

    conn = get_redis()
    profile_id = conn.get(key)

    return profile_id
