from sqlalchemy import select, and_, Column, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from backend.app.db import db
from backend.app.db.models import Product, CarGen, CarModel, DetailType, ProductCondition, Profile
from backend.app.routes.schemas import CreateProduct, CarInfo, DetailInfo, SortBy, ProductInfo


def get_base_product_info_dict(product: Product):
    car_gen = product.car_gen
    car_model = car_gen.car_model
    car_brand = car_model.car_brand

    detail_type = product.detail_type
    detail_category = detail_type.detail_category

    return dict(
        id=product.id,
        car_gen_id=product.car_gen_id,
        detail_type_id=product.detail_type_id,
        price=product.price,
        address=product.address,
        condition=product.condition,
        description=product.description,
        published_at=product.published_at,
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
        phone=product.profile.phone,
        score=product.score,
        complaints=product.complaints,
    )


def get_profile_products(profile_id: int) -> list[ProductInfo]:
    with db.create_session() as session:
        query = select(Product).where(Product.profile_id == profile_id)
        query = query.options(
            joinedload(
                Product.car_gen
            ).joinedload(
                CarGen.car_model
            ).joinedload(
                CarModel.car_brand
            ),
            joinedload(
                Product.detail_type
            ).joinedload(
                DetailType.detail_category
            ),
            joinedload(
                Product.profile
            ).load_only(
                Profile.phone
            )
        )
        query = query.order_by(Product.created_at)
        result = session.execute(query).scalars()

        profile_product_infos = []
        for product in result:
            profile_product_info = ProductInfo.model_validate(
                get_base_product_info_dict(product)
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


def column_with_optional_desc(column: Column, desc):
    if desc:
        return column.desc()
    return column


def search_products(
    car_gen_id: int | None,
    detail_type_id: int | None,
    city: str | None,
    min_price: int | None,
    max_price: int | None,
    condition: ProductCondition | None,
    count: int,
    page: int,
    sort_by: SortBy,
    desc: bool,
) -> list[ProductInfo]:
    with db.create_session() as session:
        query = select(Product).join(Profile)
        if car_gen_id is not None:
            query = query.where(Product.car_gen_id == car_gen_id)
        if detail_type_id is not None:
            query = query.where(Product.detail_type_id == detail_type_id)
        if city is not None:
            query = query.where(Profile.city == city)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)
        if condition is not None:
            query = query.where(Product.condition == condition)

        if sort_by is SortBy.SCORE:
            query = query.order_by(column_with_optional_desc(Product.score, desc))
        elif sort_by is SortBy.TIME:
            query = query.order_by(column_with_optional_desc(Product.created_at, desc))
        else:
            query = query.order_by(column_with_optional_desc(Product.price, desc))

        query = query.options(
            joinedload(
                Product.car_gen
            ).joinedload(
                CarGen.car_model
            ).joinedload(
                CarModel.car_brand
            ),
            joinedload(
                Product.detail_type
            ).joinedload(
                DetailType.detail_category
            ),
            joinedload(
                Product.profile
            ).load_only(
                Profile.phone
            )
        )
        query = query.offset((page - 1) * count)
        query = query.limit(count)

        result = session.execute(query).scalars()

        search_product_infos = []
        for product in result:
            search_product_info = ProductInfo.model_validate(
                get_base_product_info_dict(product)
            )

            search_product_infos.append(search_product_info)

        return search_product_infos


def increase_score(product_id: int) -> bool:
    with db.create_session() as session:
        product = session.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(score=Product.score + 1)
            .returning(Product.id)
        ).scalar_one_or_none()

        return bool(product)


def add_complaint(product_id: int) -> bool:
    with db.create_session() as session:
        product = session.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(complaints=Product.complaints + 1)
            .returning(Product.id)
        ).scalar_one_or_none()

        return bool(product)

