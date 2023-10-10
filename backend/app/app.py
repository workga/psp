from fastapi import FastAPI, APIRouter, Response
from sqlalchemy import text

from backend.app.db import db
from backend.app.db.redis import get_redis


def get_api_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    # @router.get('/products')
    # def products() -> Response:
    #     c = get_redis()
    #     c.set("lol", "1")
    #     v = c.get('lol')
    #     with db.create_session() as session:
    #         result = session.execute(text("SELECT 'Hello!'")).scalar_one()
    #     return Response(f"API: products list WOW you are backender? DB says: {result} and REDIS says {v}")
    #
    # @router.get('/products/{product_id:int}')
    # def products(product_id: int) -> Response:
    #     return Response(f"API: product {product_id} info")

    return router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(get_api_router())

    return app
