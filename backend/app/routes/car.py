from fastapi import Query, Response, HTTPException, status, Depends

from backend.app.auth.deps import authenticated_admin
from backend.app.crud import car
from backend.app.routes.schemas import CarBrandInfo, CreateCarBrand


def get_car_brands(search: str = Query(''), count: int = Query(10, le=100)) -> list[CarBrandInfo]:
    return car.search_car_brands(search, count)


def create_car_brand(data: CreateCarBrand, admin_id: int = Depends(authenticated_admin)) -> Response:
    if not car.create_car_brand(data):
        raise HTTPException(
            detail="This brand can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)
