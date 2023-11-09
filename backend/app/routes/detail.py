from fastapi import Query, Response, HTTPException, status, Depends, Path

from backend.app.auth.deps import authenticated_admin
from backend.app.crud import detail
from backend.app.routes.schemas import DetailCategoryInfo, CreateDetailCategory, DetailTypeInfo, CreateDetailType


def get_detail_categories(search: str = Query(''), count: int = Query(10, ge=0, le=10)) -> list[DetailCategoryInfo]:
    return detail.search_detail_categories(search, count)


def create_detail_category(data: CreateDetailCategory, admin_id: int = Depends(authenticated_admin)) -> Response:
    if not detail.create_detail_category(data):
        raise HTTPException(
            detail="This category can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)


def get_detail_types(
    category_id: int = Path(ge=0), search: str = Query(''), count: int = Query(10, ge=0, le=10)
) -> list[DetailTypeInfo]:
    types = detail.search_detail_types(category_id, search, count)
    if types is None:
        raise HTTPException(
            detail="This type doesn't exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return types


def create_detail_type(
    data: CreateDetailType, category_id: int = Path(ge=0), admin_id: int = Depends(authenticated_admin)
) -> Response:
    if not detail.create_detail_type(category_id, data):
        raise HTTPException(
            detail="This type can't be created",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return Response(status_code=status.HTTP_201_CREATED)