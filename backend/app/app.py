from fastapi import FastAPI, APIRouter, Response


def get_pages_router() -> APIRouter:
    router = APIRouter()

    @router.get('/')
    def index() -> Response:
        return Response("Main page")

    @router.get('/products/{product_id:int}')
    def index(product_id: int) -> Response:
        return Response(f"Information about product {product_id}")

    @router.get('/profile')
    def index() -> Response:
        return Response("User profile")

    @router.get('/info')
    def index() -> Response:
        return Response("Information")

    return router


def get_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get('/products')
    def products() -> Response:
        return Response("API: products list")

    @router.get('/products/{product_id:int}')
    def products(product_id: int) -> Response:
        return Response(f"API: product {product_id} info")

    return router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(get_pages_router())
    app.include_router(get_api_router())

    return app
