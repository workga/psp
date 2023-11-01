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

