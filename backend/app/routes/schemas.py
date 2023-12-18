import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, EmailStr, Field, model_validator

from backend.app.db.models import ProductCondition


class LoginProfile(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class CreateProfile(LoginProfile):
    name: str = Field(min_length=1, max_length=30)
    city: str = Field(min_length=1, max_length=30)
    phone: str = Field(min_length=10, max_length=12)


class ProfileInfo(BaseModel):
    id: int
    email: EmailStr
    name: str
    city: str
    phone: str


class UpdateProfile(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=30)
    city: str | None = Field(None, min_length=1, max_length=30)
    phone: str | None = Field(None, min_length=10, max_length=12)

    @model_validator(mode='before')
    def not_empty(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not any(values.values()):
            raise ValueError("No fields to update")
        return values


class CreateCarBrand(BaseModel):
    brand_name: str


class CarBrandInfo(CreateCarBrand):
    id: int
    score: int


class CreateCarModel(BaseModel):
    model_name: str


class CarModelInfo(CreateCarModel):
    brand_id: int
    id: int
    score: int


class CreateCarGen(BaseModel):
    gen_name: str


class CarGenInfo(CreateCarGen):
    brand_id: int
    model_id: int
    id: int
    score: int


class CreateDetailCategory(BaseModel):
    category_name: str


class DetailCategoryInfo(CreateDetailCategory):
    id: int
    score: int


class CreateDetailType(BaseModel):
    type_name: str


class DetailTypeInfo(CreateDetailType):
    category_id: int
    id: int
    score: int


class AddCarToGarage(BaseModel):
    car_gen_id: int


class CarInfo(BaseModel):
    brand_id: int
    brand_name: str
    model_id: int
    model_name: str
    gen_id: int
    gen_name: str


class DetailInfo(BaseModel):
    category_id: int
    category_name: str
    type_id: int
    type_name: str


class CreateProduct(BaseModel):
    price: int = Field(gt=1)
    address: str = Field(min_length=1, max_length=100)
    condition: ProductCondition
    description: str | None
    car_gen_id: int
    detail_type_id: int


class ProductInfo(CreateProduct):
    id: int
    car_info: CarInfo
    detail_info: DetailInfo
    # TODO: add time zones
    published_at: datetime.datetime
    phone: str
    score: int
    complaints: int


class SortBy(StrEnum):
    TIME = 'time'
    PRICE = 'price'
    SCORE = 'score'
