from fastapi import HTTPException, Cookie, status

from backend.app.auth.session import get_profile_id_by_session_id

COOKIE_SESSION_ID = "session_id"


def authenticated(session_id: str | None = Cookie(None)) -> int:
    if session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    profile_id = get_profile_id_by_session_id(session_id)
    if profile_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return profile_id
