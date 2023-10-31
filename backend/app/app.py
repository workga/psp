from fastapi import FastAPI, APIRouter
from backend.app.routes import auth, profile, car


def get_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    router.add_api_route('/auth/register', auth.register, methods=["POST"])
    router.add_api_route('/auth/login', auth.login, methods=["POST"])
    router.add_api_route('/auth/logout', auth.logout, methods=["POST"])

    router.add_api_route('/profile', profile.get_profile, methods=["GET"])

    router.add_api_route('/cars/brands', car.get_car_brands, methods=["GET"])
    router.add_api_route('/cars/brands', car.create_car_brand, methods=["POST"])

    return router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(get_api_router())

    return app
