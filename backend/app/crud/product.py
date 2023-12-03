from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db import db
from backend.app.db.models import Product, CarGen, CarModel, CarBrand, DetailType, DetailCategory
from backend.app.routes.schemas import CreateProduct, ProfileProductInfo, CarInfo, DetailInfo


def get_profile_products(profile_id: int) -> list[ProfileProductInfo]:
    with db.create_session() as session:
        result = session.execute(
            select(Product)
            .where(Product.profile_id == profile_id)
            .join(CarGen, CarGen.id == Product.car_gen_id)
            .join(CarModel, CarModel.id == CarGen.car_model_id)
            .join(CarBrand, CarBrand.id == CarModel.car_brand_id)
            .join(DetailType, DetailType.id == Product.detail_type_id)
            .join(DetailCategory, DetailCategory.id == DetailType.detail_category_id)
            .order_by(Product.created_at)
        ).scalars()

        profile_product_infos = []
        for product in result:
            car_gen = product.car_gen
            car_model = car_gen.car_model
            car_brand = car_model.car_brand

            detail_type = product.detail_type
            detail_category = detail_type.detail_category

            profile_product_info = ProfileProductInfo(
                id=product.id,
                car_gen_id=product.car_gen_id,
                detail_type_id=product.detail_type_id,
                price=product.price,
                address=product.address,
                condition=product.condition,
                description=product.description,
                car_info=CarInfo(
                    brand_id=car_brand.id,
                    brand_name=car_brand.brand_name,
                    model_id=car_model.id,
                    model_name=car_model.model_name,
                    gen_id=car_gen.id,
                    gen_name=car_gen.gen_name,
                ),
                detail_info=DetailInfo(
                    category_id=detail_category.id,
                    category_name=detail_category.category_name,
                    type_id=detail_type.id,
                    type_name=detail_type.type_name,
                ),
            )

            profile_product_infos.append(profile_product_info)

        return profile_product_infos


def create_profile_product(data: CreateProduct, profile_id: int) -> bool:
    try:
        with db.create_session() as session:
            product = Product(
                profile_id=profile_id,
                car_gen_id=data.car_gen_id,
                detail_type_id=data.detail_type_id,
                price=data.price,
                address=data.address,
                condition=data.condition,
                description=data.description,
            )
            session.add(product)
            session.commit()
            return True
    except IntegrityError:
        return False


def remove_profile_product(product_id: int, profile_id: int) -> bool:
    with db.create_session() as session:
        product = session.execute(
            select(Product)
            .where(
                and_(Product.profile_id == profile_id, Product.id == product_id)
            )
        ).scalar_one_or_none()
        if product is None:
            return False

        session.delete(product)
        return True
