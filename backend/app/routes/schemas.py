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


class CarBrandInfo(BaseModel):
    id: int
    brand_name: str
    score: int

