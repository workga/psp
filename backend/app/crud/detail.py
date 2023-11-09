from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.app.db import db
from backend.app.db.models import DetailCategory, DetailType
from backend.app.routes.schemas import DetailCategoryInfo, CreateDetailCategory, DetailTypeInfo, CreateDetailType


def search_detail_categories(search: str, count: int) -> list[DetailCategoryInfo]:
    with db.create_session() as session:
        categories = session.execute(
            select(DetailCategory.id, DetailCategory.category_name, DetailCategory.score)
            .where(DetailCategory.category_name.startswith(search, autoescape=True))
            .order_by(DetailCategory.score.desc())
            .limit(count)
        ).all()

        return [
            DetailCategoryInfo(
                id=category.id,
                category_name=category.category_name,
                score=category.score
            )
            for category in categories
        ]


def create_detail_category(data: CreateDetailCategory) -> bool:
    try:
        with db.create_session() as session:
            session.add(DetailCategory(category_name=data.category_name))
            session.commit()
            return True
    except IntegrityError:
        return False


def search_detail_types(category_id: int, search: str, count: int) -> list[DetailTypeInfo] | None:
    with db.create_session() as session:
        category = session.execute(
            select(DetailCategory).where(DetailCategory.id == category_id)
        ).one_or_none()
        if category is None:
            return None

        types = session.execute(
            select(DetailType.id, DetailType.type_name, DetailType.score)
            .where(DetailType.detail_category_id == category_id)
            .where(DetailType.type_name.startswith(search, autoescape=True))
            .order_by(DetailType.score.desc())
            .limit(count)
        ).all()

        return [
            DetailTypeInfo(
                id=type_.id,
                category_id=category_id,
                type_name=type_.type_name,
                score=type_.score
            )
            for type_ in types
        ]


def create_detail_type(category_id: int, data: CreateDetailType) -> bool:
    try:
        with db.create_session() as session:
            session.add(DetailType(detail_category_id=category_id, type_name=data.type_name))
            session.commit()
            return True
    except IntegrityError:
        return False