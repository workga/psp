from fastapi import FastAPI, APIRouter
from backend.app.routes import auth, profile, car


def get_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    router.add_api_route('/auth/register', auth.register, methods=["POST"])
    router.add_api_route('/auth/login', auth.login, methods=["POST"])
    router.add_api_route('/auth/logout', auth.logout, methods=["POST"])

    router.add_api_route('/profile', profile.get_profile, methods=["GET"])

    # TODO: allow only create entire cars as (brand, model, gen) to avoid empty lists in search panel
    # TODO: OR check models and gens existence during search (use Car table)
    router.add_api_route('/cars/brands', car.get_car_brands, methods=["GET"])
    router.add_api_route('/cars/brands', car.create_car_brand, methods=["POST"])
    router.add_api_route('/cars/brands/{brand_id}/models', car.get_car_models, methods=["GET"])
    router.add_api_route('/cars/brands/{brand_id}/models', car.create_car_model, methods=["POST"])
    router.add_api_route('/cars/brands/{brand_id}/models/{model_id}/gens', car.get_car_gens, methods=["GET"])
    router.add_api_route('/cars/brands/{brand_id}/models/{model_id}/gens', car.create_car_gen, methods=["POST"])

    return router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(get_api_router())

    return app
