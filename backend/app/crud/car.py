from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.app.db import db
from backend.app.db.models import CarBrand, CarModel
from backend.app.routes.schemas import CarBrandInfo, CreateCarBrand, CarModelInfo


def search_car_brands(search: str, count: int) -> list[CarBrandInfo]:
    with db.create_session() as session:
        brands = session.execute(
            select(CarBrand.id, CarBrand.brand_name, CarBrand.score)
            .where(CarBrand.brand_name.startswith(search, autoescape=True))
            .order_by(CarBrand.score.desc())
            .limit(count)
        ).all()

        return [CarBrandInfo(id=brand.id, brand_name=brand.brand_name, score=brand.score) for brand in brands]


def create_car_brand(data: CreateCarBrand) -> bool:
    try:
        with db.create_session() as session:
            session.add(CarBrand(brand_name=data.brand_name))
            session.commit()
            return True
    except IntegrityError:
        return False


def search_car_models(brand_id: int, search: str, count: int) -> list[CarModelInfo]:
    with db.create_session() as session:
        models = session.execute(
            select(CarModel.id, CarModel.car_brand_id, CarModel.model_name, CarModel.score)
            .where(CarModel.car_brand_id == brand_id)
            .where(CarModel.model_name.startswith(search, autoescape=True))
            .order_by(CarModel.score.desc())
            .limit(count)
        ).all()

        return [
            CarModelInfo(
                id=model.id,
                brand_id=model.car_brand_id,
                model_name=model.model_name,
                score=model.score
            )
            for model in models
        ]
