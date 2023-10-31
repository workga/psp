import random
import string

import bcrypt
import click

from backend.app.db import db
from backend.app.db.models import Profile, CarBrand


@click.group()
def cli() -> None:
    pass


@cli.command()
def init_data() -> None:
    with db.create_session() as session:
        password_hash = bcrypt.hashpw(f"admin_profile".encode(), bcrypt.gensalt()).decode()
        session.add(
            Profile(
                name=f"admin",
                email=f"admin@example.com",
                password_hash=password_hash,
                is_confirmed=True,
                is_admin=True,
            )
        )
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

        random.seed(0)
        brands = [a + b for a in string.ascii_uppercase for b in string.ascii_uppercase]
        random.shuffle(brands)
        for brand in brands:
            session.add(
                CarBrand(
                    brand_name=f"{brand} Brand",
                    score=random.randint(0, 10),
                )
            )
        session.commit()
