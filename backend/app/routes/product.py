from fastapi import Depends, HTTPException, Response, status, Path

from backend.app.auth.deps import authenticated
from backend.app.crud import product
from backend.app.routes.schemas import CreateProduct, ProfileProductInfo


def get_profile_products(profile_id: int = Depends(authenticated)) -> list[ProfileProductInfo]:
    return product.get_profile_products(profile_id)


def create_profile_product(data: CreateProduct, profile_id: int = Depends(authenticated)):
    if not product.create_profile_product(data, profile_id):
        raise HTTPException(
            detail="This product can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)


def remove_profile_product(product_id: int = Path(ge=0), profile_id: int = Depends(authenticated)):
    if not product.remove_profile_product(product_id, profile_id):
        raise HTTPException(
            detail="This product_id not found",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_200_OK)
