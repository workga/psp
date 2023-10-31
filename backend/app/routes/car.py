from fastapi import Query

from backend.app.crud.car import search_car_brands
from backend.app.routes.schemas import CarBrandInfo


def get_car_brands(search: str = Query(''), count: int = Query(10, le=100)) -> list[CarBrandInfo]:
    return search_car_brands(search, count)
