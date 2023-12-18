from fastapi import FastAPI
from sqladmin import Admin

from backend.app.admin.views import get_view_classes
from backend.app.db.db import session_maker


def create_admin(app: FastAPI) -> None:
    admin = Admin(app, session_maker=session_maker, base_url='/admin')

    for view_class in get_view_classes():
        admin.add_view(view_class)