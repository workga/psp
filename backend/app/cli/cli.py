import random
import string

import bcrypt
import click

from backend.app.db import db
from backend.app.db.models import Profile, CarBrand, CarModel, CarGen, DetailCategory, DetailType


def get_random_pairs(n: int = 4) -> list[str]:
    pairs = [a + b for a in string.ascii_uppercase[:n] for b in string.ascii_uppercase[:n]]
    random.shuffle(pairs)
    return pairs


@click.group()
def cli() -> None:
    pass


@cli.command()
def init_data() -> None:
    random.seed(0)

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

        for brand in get_random_pairs():
            car_brand = CarBrand(
                brand_name=f"{brand} Brand",
                score=random.randint(0, 10),
            )
            session.add(car_brand)
            session.flush()

            for model in get_random_pairs():
                car_model = CarModel(
                    car_brand_id=car_brand.id,
                    model_name=f"{model} Model",
                    score=random.randint(0, 10),
                )
                session.add(car_model)
                session.flush()

                for gen in get_random_pairs():
                    session.add(
                        CarGen(
                            car_model_id=car_model.id,
                            gen_name=f"{gen} Gen",
                            score=random.randint(0, 10),
                        )
                    )

        for category in get_random_pairs():
            detail_category = DetailCategory(
                category_name=f"{category} Category",
                score=random.randint(0, 10),
            )
            session.add(detail_category)
            session.flush()

            for type_ in get_random_pairs():
                detail_type = DetailType(
                    detail_category_id=detail_category.id,
                    type_name=f"{type_} Type",
                    score=random.randint(0, 10),
                )
                session.add(detail_type)

        session.commit()
