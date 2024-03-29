from datetime import datetime
import re
from enum import StrEnum

from sqlalchemy import BigInteger, String, func, ForeignKey, UniqueConstraint, Enum, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship
from sqlalchemy.sql import expression
from sqlalchemy_utils import generic_repr


def classname_to_tablename(class_name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()


@generic_repr
class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        return classname_to_tablename(cls.__name__)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), index=True)


class Profile(Base):
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    # TODO: add email confirmation
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(72), nullable=False)
    # TODO: add phone confirmation
    phone: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    city: Mapped[str] = mapped_column(String(30), nullable=False, unique=False)

    is_confirmed: Mapped[bool] = mapped_column(nullable=False, server_default=expression.false())
    is_admin: Mapped[bool] = mapped_column(nullable=False, server_default=expression.false())

    products: Mapped[list['Product']] = relationship('Product', back_populates='profile', uselist=True)


class CarBrand(Base):
    # TODO: add index for text search
    brand_name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    score: Mapped[int] = mapped_column(nullable=False, server_default=text("0"), index=True)

    car_models: Mapped[list['CarModel']] = relationship('CarModel', back_populates='car_brand', uselist=True)


class CarModel(Base):
    car_brand_id: Mapped[int] = mapped_column(ForeignKey(CarBrand.id), nullable=False)
    model_name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    score: Mapped[int] = mapped_column(nullable=False, server_default=text("0"), index=True)

    __table_args__ = (UniqueConstraint(car_brand_id, model_name),)

    car_brand: Mapped[CarBrand] = relationship(CarBrand, back_populates='car_models', uselist=False)
    car_gens: Mapped[list['CarGen']] = relationship('CarGen', back_populates='car_model', uselist=True)


class CarGen(Base):
    car_model_id: Mapped[int] = mapped_column(ForeignKey(CarModel.id), nullable=False)
    gen_name: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    score: Mapped[int] = mapped_column(nullable=False, server_default=text("0"), index=True)

    __table_args__ = (UniqueConstraint(car_model_id, gen_name),)

    car_model: Mapped[CarModel] = relationship(CarModel, back_populates='car_gens', uselist=False)


class DetailCategory(Base):
    category_name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True, index=True)
    score: Mapped[int] = mapped_column(nullable=False, server_default=text("0"), index=True)

    detail_types: Mapped[list['DetailType']] = relationship('DetailType', back_populates='detail_category', uselist=True)


class DetailType(Base):
    detail_category_id: Mapped[int] = mapped_column(ForeignKey(DetailCategory.id), nullable=False)
    type_name: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    score: Mapped[int] = mapped_column(nullable=False, server_default=text("0"), index=True)

    __table_args__ = (UniqueConstraint(detail_category_id, type_name),)

    detail_category: Mapped[DetailCategory] = relationship(DetailCategory, back_populates='detail_types', uselist=False)


class ProductCondition(StrEnum):
    NEW = 'new'
    USED = 'used'


class Product(Base):
    price: Mapped[int] = mapped_column(nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    condition: Mapped[ProductCondition] = mapped_column(Enum(ProductCondition), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False, server_default=text("0"), index=True)
    complaints: Mapped[int] = mapped_column(nullable=False, server_default=text("0"), index=True)

    description: Mapped[str] = mapped_column(Text, nullable=True)
    # TODO: add photo_path and workflow for it

    published_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), index=True)

    profile_id: Mapped[int] = mapped_column(ForeignKey(Profile.id), nullable=False)

    car_gen_id: Mapped[int] = mapped_column(ForeignKey(CarGen.id), nullable=False)
    detail_type_id: Mapped[int] = mapped_column(ForeignKey(DetailType.id), nullable=False)

    profile: Mapped[Profile] = relationship(Profile, back_populates='products', uselist=False)
    car_gen: Mapped[CarGen] = relationship(CarGen, uselist=False)
    detail_type: Mapped[DetailType] = relationship(DetailType, uselist=False)


class CarInGarage(Base):
    profile_id: Mapped[int] = mapped_column(ForeignKey(Profile.id), nullable=False)
    car_gen_id: Mapped[int] = mapped_column(ForeignKey(CarGen.id), nullable=False)

    car_gen: Mapped[CarGen] = relationship(CarGen, uselist=False)

    __table_args__ = (UniqueConstraint(profile_id, car_gen_id),)








