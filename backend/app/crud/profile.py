from sqlalchemy import select, delete, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from backend.app.auth.security import hash_password, check_password
from backend.app.db import db
from backend.app.db.models import Profile, CarInGarage, CarGen, CarModel, CarBrand
from backend.app.routes.schemas import CreateProfile, LoginProfile, ProfileInfo, CarInfo


def create_profile(data: CreateProfile) -> bool:
    try:
        with db.create_session() as session:
            profile = Profile(
                name=data.name,
                email=data.email,
                password_hash=hash_password(data.password),
            )
            session.add(profile)
            session.commit()
            return True
    except IntegrityError:
        return False


def login_profile(data: LoginProfile) -> int | None:
    with db.create_session() as session:
        profile = session.execute(
            select(Profile.id, Profile.password_hash)
            .where(Profile.email == data.email)
        ).one_or_none()

        if profile and check_password(data.password, profile.password_hash):
            return profile.id

        return None


def get_profile_info(profile_id: int) -> ProfileInfo | None:
    with db.create_session() as session:
        profile = session.execute(
            select(Profile.email, Profile.name)
            .where(Profile.id == profile_id)
        ).one_or_none()

        if profile:
            return ProfileInfo(
                id=profile_id,
                email=profile.email,
                name=profile.name,
            )

        return None


def is_profile_admin(profile_id: int) -> bool:
    with db.create_session() as session:
        is_admin = session.execute(
            select(Profile.is_admin)
            .where(Profile.id == profile_id)
        ).scalar_one_or_none()

        return is_admin


def get_cars(profile_id: int) -> list[CarInfo]:
    with db.create_session() as session:
        result = session.execute(
            select(CarInGarage)
            .where(CarInGarage.profile_id == profile_id)
            .join(CarGen, CarGen.id == CarInGarage.car_gen_id)
            .join(CarModel, CarModel.id == CarGen.car_model_id)
            .join(CarBrand, CarBrand.id == CarModel.car_brand_id)
            .order_by(CarInGarage.created_at)
        ).scalars()

        car_infos = []
        for car_info in result:
            car_gen = car_info.car_gen
            car_model = car_gen.car_model
            car_brand = car_model.car_brand

            car_infos.append(
                CarInfo(
                    brand_id=car_brand.id,
                    brand_name=car_brand.brand_name,
                    model_id=car_model.id,
                    model_name=car_model.model_name,
                    gen_id=car_gen.id,
                    gen_name=car_gen.gen_name,
                )
            )

        return car_infos


def add_car(car_gen_id: int, profile_id: int) -> bool:
    try:
        with db.create_session() as session:
            car_in_garage = CarInGarage(
                profile_id=profile_id,
                car_gen_id=car_gen_id,
            )

            session.add(car_in_garage)
            session.commit()
            return True
    except IntegrityError:
        return False


def remove_car(car_gen_id: int, profile_id: int) -> bool:
    with db.create_session() as session:
        car_in_garage = session.execute(
            select(CarInGarage)
            .where(
                and_(CarInGarage.profile_id == profile_id, CarInGarage.car_gen_id == car_gen_id)
            )
        ).scalar_one_or_none()
        if car_in_garage is None:
            return False

        session.delete(car_in_garage)
        return True
