from fastapi import status, Depends, HTTPException, Response, Path

from backend.app.auth.deps import authenticated
from backend.app.crud import profile
from backend.app.routes.schemas import ProfileInfo, AddCarToGarage, CarInfo


def get_profile(profile_id: int = Depends(authenticated)) -> ProfileInfo:
    profile_info = profile.get_profile_info(profile_id)
    if profile_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return profile_info


def get_cars_in_garage(profile_id: int = Depends(authenticated)) -> list[CarInfo]:
    return profile.get_cars_in_garage(profile_id)


def add_car_to_garage(data: AddCarToGarage, profile_id: int = Depends(authenticated)) -> Response:
    if not profile.add_car_to_garage(data.car_gen_id, profile_id):
        raise HTTPException(
            detail="This car can't be added to profile's garage",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return Response(status_code=status.HTTP_201_CREATED)


def remove_car_from_garage(car_gen_id: int = Path(ge=0), profile_id: int = Depends(authenticated)) -> Response:
    if not profile.remove_car_from_garage(car_gen_id, profile_id):
        raise HTTPException(
            detail="This car_gen_id not found in profile's garage",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return Response(status_code=status.HTTP_200_OK)
