from sqlalchemy import select

from backend.app.db import db
from backend.app.db.models import CarBrand
from backend.app.routes.schemas import CarBrandInfo


def search_car_brands(search: str, count: int) -> list[CarBrandInfo]:
    with db.create_session() as session:
        brands = session.execute(
            select(CarBrand.id, CarBrand.brand_name, CarBrand.score)
            .where(CarBrand.brand_name.startswith(search, autoescape=True))
            .order_by(CarBrand.score.desc())
            .limit(count)
        ).all()

        return [CarBrandInfo(id=brand.id, brand_name=brand.brand_name, score=brand.score) for brand in brands]
