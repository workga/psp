from pydantic import BaseModel, EmailStr, Field


class LoginProfile(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class CreateProfile(LoginProfile):
    name: str = Field(min_length=1, max_length=30)


class ProfileInfo(BaseModel):
    id: int
    email: EmailStr
    name: str


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


class GarageInfo(BaseModel):
    profile_id: int
    cars: list[CarInfo]

