from redis import Redis, ConnectionPool
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    url: str

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
    )


redis_settings = RedisSettings()
pool = ConnectionPool.from_url(redis_settings.url,  decode_responses=True)


def get_redis() -> Redis:
    return Redis(connection_pool=pool)
