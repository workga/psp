from fastapi import status, Depends, HTTPException

from backend.app.auth.deps import authenticated
from backend.app.crud.profile import get_profile_info
from backend.app.routes.schemas import ProfileInfo


def get_profile(profile_id: int = Depends(authenticated)) -> ProfileInfo:
    profile_info = get_profile_info(profile_id)
    if profile_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return profile_info
