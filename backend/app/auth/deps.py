from fastapi import HTTPException, Cookie, status, Depends

from backend.app.auth.session import get_profile_id_by_session_id
from backend.app.crud.profile import is_profile_admin

COOKIE_SESSION_ID = "session_id"


def authenticated_or_not_valid(session_id: str | None = Cookie(None)) -> int | None:
    if session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    profile_id = get_profile_id_by_session_id(session_id)
    return profile_id


def authenticated(profile_id: int = Depends(authenticated_or_not_valid)) -> int:
    if profile_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return profile_id


def authenticated_admin(profile_id: int = Depends(authenticated)) -> int:
    if not is_profile_admin(profile_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return profile_id
