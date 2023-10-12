from pydantic import BaseModel, EmailStr, Field


class BaseProfile(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class CreateProfile(BaseProfile):
    name: str = Field(min_length=1, max_length=30)


class LoginProfile(BaseProfile):
    pass
