from fastapi import Depends, HTTPException, Response, status, Path, Query

from backend.app.auth.deps import authenticated
from backend.app.crud import product
from backend.app.db.models import ProductCondition
from backend.app.routes.schemas import CreateProduct, ProductInfo, SortBy, UpdateProduct


def get_profile_products(profile_id: int = Depends(authenticated)) -> list[ProductInfo]:
    return product.get_profile_products(profile_id)


def create_profile_product(data: CreateProduct, profile_id: int = Depends(authenticated)):
    if not product.create_profile_product(data, profile_id):
        raise HTTPException(
            detail="This product can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)


def edit_profile_product(data: UpdateProduct, product_id: int = Path(ge=0), profile_id: int = Depends(authenticated)):
    product_info = product.update_product(data, product_id, profile_id)
    if product_info is None:
        raise HTTPException(
            detail="Can't update product",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return product_info


def remove_profile_product(product_id: int = Path(ge=0), profile_id: int = Depends(authenticated)):
    if not product.remove_profile_product(product_id, profile_id):
        raise HTTPException(
            detail="This product_id not found",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_200_OK)


def search_products(
    car_gen_id: int | None = Query(None, ge=0),
    detail_type_id: int | None = Query(None, ge=0),
    city: str | None = Query(None, min_length=1),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    condition: ProductCondition | None = Query(None),
    count: int = Query(10, ge=0, le=10),
    page: int = Query(1, ge=1),
    sort_by: SortBy = Query(SortBy.SCORE),
    desc: bool = Query(False),
):
    return product.search_products(
        car_gen_id,
        detail_type_id,
        city,
        min_price,
        max_price,
        condition,
        count,
        page,
        sort_by,
        desc,
    )


def increase_score(product_id: int = Path(ge=0)):
    if not product.increase_score(product_id):
        raise HTTPException(
            detail="Can't increase score of this product",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)


def add_complaint(product_id: int = Path(ge=0)):
    if not product.add_complaint(product_id):
        raise HTTPException(
            detail="Can't add complaint to this product",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)
