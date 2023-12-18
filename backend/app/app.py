from fastapi import FastAPI, APIRouter
from backend.app.routes import auth, profile, car, detail, product


def get_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    router.add_api_route('/auth/register', auth.register, methods=["POST"])
    router.add_api_route('/auth/login', auth.login, methods=["POST"])
    router.add_api_route('/auth/logout', auth.logout, methods=["POST"])

    router.add_api_route('/profile', profile.get_profile, methods=["GET"])
    router.add_api_route('/profile', profile.edit_profile, methods=["PATCH"])
    router.add_api_route('/profile/garage', profile.get_cars_in_garage, methods=["GET"])
    router.add_api_route('/profile/garage/cars', profile.add_car_to_garage, methods=["POST"])
    router.add_api_route('/profile/garage/cars/{car_gen_id}', profile.remove_car_from_garage, methods=["DELETE"])
    router.add_api_route('/profile/products', product.get_profile_products, methods=["GET"])
    router.add_api_route('/profile/products', product.create_profile_product, methods=["POST"])
    router.add_api_route('/profile/products/{product_id}', product.remove_profile_product, methods=["DELETE"])
    router.add_api_route('/profile/products/{product_id}', product.edit_profile_product, methods=["PATCH"])

    # TODO: allow only create entire cars as (brand, model, gen) to avoid empty lists in search panel
    # TODO: OR check models and gens existence during search (use Car table)
    router.add_api_route('/cars/brands', car.get_car_brands, methods=["GET"])
    router.add_api_route('/cars/brands', car.create_car_brand, methods=["POST"])  # use sqladmin
    router.add_api_route('/cars/brands/{brand_id}/models', car.get_car_models, methods=["GET"])
    router.add_api_route('/cars/brands/{brand_id}/models', car.create_car_model, methods=["POST"])  # use sqladmin
    router.add_api_route('/cars/brands/{brand_id}/models/{model_id}/gens', car.get_car_gens, methods=["GET"])
    router.add_api_route('/cars/brands/{brand_id}/models/{model_id}/gens', car.create_car_gen, methods=["POST"])  # use sqladmin

    router.add_api_route('/details/categories', detail.get_detail_categories, methods=["GET"])
    router.add_api_route('/details/categories', detail.create_detail_category, methods=["POST"])
    router.add_api_route('/details/categories/{category_id}/types', detail.get_detail_types, methods=["GET"])
    router.add_api_route('/details/categories/{category_id}/types', detail.create_detail_type, methods=["POST"])

    # TODO: add endpoints for get_car_info, get_detail_info
    # router.add_api_route('/car_info/{car_gen_id}', car.get_car_info, methods=["GET"])
    # router.add_api_route('/detail_info/{car_gen_id}', car.get_car_info, methods=["GET"])

    router.add_api_route('/products', product.search_products, methods=["GET"])
    router.add_api_route('/products/{product_id}/increase_score', product.increase_score, methods=["POST"])
    router.add_api_route('/products/{product_id}/add_complaint', product.add_complaint, methods=["POST"])

    return router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(get_api_router())

    return app
