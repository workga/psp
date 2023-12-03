from fastapi import status, Depends, HTTPException, Response, Path

from backend.app.auth.deps import authenticated
from backend.app.crud.profile import get_profile_info, add_car, get_cars, remove_car
from backend.app.routes.schemas import ProfileInfo, GarageInfo, AddCarToGarage


def get_profile(profile_id: int = Depends(authenticated)) -> ProfileInfo:
    profile_info = get_profile_info(profile_id)
    if profile_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return profile_info


def get_cars_in_garage(profile_id: int = Depends(authenticated)) -> GarageInfo:
    cars = get_cars(profile_id)
    return GarageInfo(
        profile_id=profile_id,
        cars=cars,
    )


def add_car_to_garage(data: AddCarToGarage, profile_id: int = Depends(authenticated)) -> Response:
    if not add_car(data.car_gen_id, profile_id):
        raise HTTPException(
            detail="This car can't be added to profile's garage",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return Response(status_code=status.HTTP_201_CREATED)


def remove_car_from_garage(car_gen_id: int = Path(ge=0), profile_id: int = Depends(authenticated)) -> Response:
    if not remove_car(car_gen_id, profile_id):
        raise HTTPException(
            detail="Car not found in profile's garage",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return Response(status_code=status.HTTP_200_OK)