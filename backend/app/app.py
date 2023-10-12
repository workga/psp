from fastapi import FastAPI, APIRouter
from backend.app.routes import auth, profile


def get_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    router.add_api_route('/auth/register', auth.register, methods=["POST"])
    router.add_api_route('/auth/login', auth.login, methods=["POST"])
    router.add_api_route('/auth/logout', auth.logout, methods=["POST"])

    router.add_api_route('/profile', profile.profile, methods=["GET"])

    return router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(get_api_router())

    return app
