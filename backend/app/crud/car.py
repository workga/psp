from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.app.db import db
from backend.app.db.models import CarBrand, CarModel, CarGen
from backend.app.routes.schemas import CarBrandInfo, CreateCarBrand, CarModelInfo, CreateCarModel, CarGenInfo, \
    CreateCarGen


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


def search_car_models(brand_id: int, search: str, count: int) -> list[CarModelInfo] | None:
    with db.create_session() as session:
        brand = session.execute(
            select(CarBrand).where(CarBrand.id == brand_id)
        ).one_or_none()
        if brand is None:
            return None

        models = session.execute(
            select(CarModel.id, CarModel.model_name, CarModel.score)
            .where(CarModel.car_brand_id == brand_id)
            .where(CarModel.model_name.startswith(search, autoescape=True))
            .order_by(CarModel.score.desc())
            .limit(count)
        ).all()

        return [
            CarModelInfo(
                id=model.id,
                brand_id=brand_id,
                model_name=model.model_name,
                score=model.score
            )
            for model in models
        ]


def create_car_model(brand_id: int, data: CreateCarModel) -> bool:
    try:
        with db.create_session() as session:
            session.add(CarModel(car_brand_id=brand_id, model_name=data.model_name))
            session.commit()
            return True
    except IntegrityError:
        return False


def search_car_gens(brand_id: int, model_id: int, search: str, count: int) -> list[CarGenInfo] | None:
    with db.create_session() as session:
        model = session.execute(
            select(CarModel)
            .where(CarModel.id == model_id)
            .where(CarModel.car_brand_id == brand_id)
        ).one_or_none()
        if model is None:
            return None

        gens = session.execute(
            select(CarGen.id, CarGen.gen_name, CarGen.score)
            .where(CarGen.car_model_id == model_id)
            .where(CarGen.gen_name.startswith(search, autoescape=True))
            .order_by(CarGen.score.desc())
            .limit(count)
        ).all()

        return [
            CarGenInfo(
                id=gen.id,
                brand_id=brand_id,
                model_id=model_id,
                gen_name=gen.gen_name,
                score=gen.score,
            )
            for gen in gens
        ]


def create_car_gen(brand_id: int, model_id: int, data: CreateCarGen) -> bool:
    try:
        with db.create_session() as session:
            model = session.execute(
                select(CarModel)
                .where(CarModel.id == model_id)
                .where(CarModel.car_brand_id == brand_id)
            ).one_or_none()
            if model is None:
                return False

            session.add(CarGen(car_model_id=model_id, gen_name=data.gen_name))
            session.commit()
            return True
    except IntegrityError:
        return False
