import logging
from contextlib import contextmanager

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)


class DBSettings(BaseSettings):
    url: str
    echo: bool = False

    model_config = SettingsConfigDict(
        env_prefix="DB_",
    )


db_settings = DBSettings()
engine = create_engine(db_settings.url, echo=db_settings.echo)
session_maker = sessionmaker(engine)


@contextmanager
def create_session(expire_on_commit: bool = True, autoflush: bool = False, autobegin: bool = True) -> Session:
    session = session_maker(expire_on_commit=expire_on_commit, autoflush=autoflush, autobegin=autobegin)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(e)
        raise
    finally:
        session.close()
