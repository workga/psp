import bcrypt
import click

from backend.app.db import db
from backend.app.db.models import Profile


@click.group()
def cli() -> None:
    pass


@cli.command()
def init_data() -> None:
    with db.create_session() as session:
        for i in range(10):
            password_hash = bcrypt.hashpw(f"testing_profile".encode(), bcrypt.gensalt()).decode()

            session.add(
                Profile(
                    name=f"Profile {i}",
                    email=f"testing{i}@example.com",
                    password_hash=password_hash,
                    is_confirmed=True,
                )
            )
        session.commit()
