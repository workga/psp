from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.app.auth.security import hash_password, check_password
from backend.app.db import db
from backend.app.db.models import Profile
from backend.app.routes.schemas import CreateProfile, LoginProfile, ProfileInfo


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



