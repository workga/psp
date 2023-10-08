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
            session.add(Profile(username=f"Profile {i}"))
        session.commit()
