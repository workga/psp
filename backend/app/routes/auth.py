from fastapi import status, HTTPException, Response, Depends, Cookie

from backend.app.auth.deps import COOKIE_SESSION_ID, authenticated
from backend.app.auth.session import create_auth_session, auth_settings, delete_auth_session
from backend.app.crud.profile import create_profile, login_profile
from backend.app.routes.schemas import CreateProfile, LoginProfile


# TODO: suppress password in response if data validation fails, i.e. send filtered fastapi response
def register(data: CreateProfile, session_id: str | None = Cookie(None)) -> Response:
    if session_id:
        raise HTTPException(
            detail="Already logged in",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    if not create_profile(data):
        raise HTTPException(
            detail="This email can't be registered",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # TODO: add email confirmation
    return Response(status_code=status.HTTP_201_CREATED)


def login(data: LoginProfile, session_id: str | None = Cookie(None)) -> Response:
    if session_id:
        raise HTTPException(
            detail="Already logged in",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    profile_id = login_profile(data)
    if profile_id is None:
        raise HTTPException(
            detail="Incorrect email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    session_id = create_auth_session(profile_id)

    response = Response(status_code=status.HTTP_200_OK)
    # TODO: set additional options in cookie for security reason (secure etc.)
    response.set_cookie(
        key=COOKIE_SESSION_ID,
        value=session_id,
        httponly=True,
        max_age=int(auth_settings.session_cookie_ttl.total_seconds())
    )
    return response


def logout(session_id: str = Cookie(), profile_id: int = Depends(authenticated)) -> Response:
    delete_auth_session(session_id)
    response = Response(status_code=status.HTTP_200_OK)
    response.delete_cookie(key=COOKIE_SESSION_ID, httponly=True)
    return response
