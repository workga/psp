from fastapi import Query, Response, HTTPException, status, Depends, Path

from backend.app.auth.deps import authenticated_admin
from backend.app.crud import car
from backend.app.routes.schemas import CarBrandInfo, CreateCarBrand, CarModelInfo, CreateCarModel, CarGenInfo, \
    CreateCarGen


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
    models = car.search_car_models(brand_id, search, count)
    if models is None:
        raise HTTPException(
            detail="This brand doesn't exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return models


def create_car_model(
    data: CreateCarModel, brand_id: int = Path(ge=0), admin_id: int = Depends(authenticated_admin)
) -> Response:
    if not car.create_car_model(brand_id, data):
        raise HTTPException(
            detail="This model can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)


def get_car_gens(
    brand_id: int = Path(ge=0), model_id: int = Path(ge=0), search: str = Query(''), count: int = Query(10, ge=0, le=10)
) -> list[CarGenInfo]:
    gens = car.search_car_gens(brand_id, model_id, search, count)
    if gens is None:
        raise HTTPException(
            detail="This brand doesn't exist or this model does not belong to this brand",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return gens


def create_car_gen(
    data: CreateCarGen,
    brand_id: int = Path(ge=0),
    model_id: int = Path(ge=0),
    admin_id: int = Depends(authenticated_admin),
) -> Response:
    if not car.create_car_gen(brand_id, model_id, data):
        raise HTTPException(
            detail="This gen can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)
