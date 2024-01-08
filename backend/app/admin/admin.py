from fastapi import FastAPI
from sqladmin import Admin

from backend.app.admin.views import get_view_classes
from backend.app.auth.deps import COOKIE_SESSION_ID
from backend.app.auth.session import create_auth_session, get_profile_id_by_session_id
from backend.app.crud.profile import login_profile, is_profile_admin
from backend.app.db.db import session_maker
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from backend.app.routes.schemas import LoginProfile


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        profile_id = login_profile(LoginProfile(email=email, password=password))
        if not profile_id or not is_profile_admin(profile_id):
            return False

        request.session.update({COOKIE_SESSION_ID: create_auth_session(profile_id)})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        session_id = request.session.get(COOKIE_SESSION_ID)

        if not session_id or not get_profile_id_by_session_id(session_id):
            return False

        return True


def create_admin(app: FastAPI) -> None:
    admin = Admin(app, session_maker=session_maker, base_url='/admin', authentication_backend=AdminAuth(secret_key="..."))

    for view_class in get_view_classes():
        admin.add_view(view_class)
