from fastapi import Query, Response, HTTPException, status, Depends, Path

from backend.app.auth.deps import authenticated_admin
from backend.app.crud import car
from backend.app.routes.schemas import CarBrandInfo, CreateCarBrand, CarModelInfo, CreateCarModel


def get_car_brands(search: str = Query(''), count: int = Query(10, ge=0, le=10)) -> list[CarBrandInfo]:
    return car.search_car_brands(search, count)


def create_car_brand(data: CreateCarBrand, admin_id: int = Depends(authenticated_admin)) -> Response:
    if not car.create_car_brand(data):
        raise HTTPException(
            detail="This brand can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)


def get_car_models(
    brand_id: int = Path(ge=0), search: str = Query(''), count: int = Query(10, ge=0, le=10)
) -> list[CarModelInfo]:
    return car.search_car_models(brand_id, search, count)


def create_car_model(
    data: CreateCarModel, brand_id: int = Path(ge=0), admin_id: int = Depends(authenticated_admin)
) -> Response:
    if not car.create_car_model(brand_id, data):
        raise HTTPException(
            detail="This model can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)
