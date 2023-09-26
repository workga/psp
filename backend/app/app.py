from fastapi import FastAPI, APIRouter, Response


def get_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get('/products')
    def products() -> Response:
        return Response("API: products list WOW you are backender?")

    @router.get('/products/{product_id:int}')
    def products(product_id: int) -> Response:
        return Response(f"API: product {product_id} info")

    return router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(get_api_router())

    return app
