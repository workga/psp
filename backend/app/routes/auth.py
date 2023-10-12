from fastapi import status, HTTPException, Response, Depends, Cookie

from backend.app.auth.deps import COOKIE_SESSION_ID, authenticated
from backend.app.auth.session import create_auth_session, auth_settings, delete_auth_session
from backend.app.crud.profile import create_profile, login_profile
from backend.app.routes.schemas import CreateProfile, LoginProfile


# TODO: supress password in response if data validation fails
def register(data: CreateProfile) -> Response:
    if not create_profile(data):
        raise HTTPException(
            detail="This email can't be registered",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # TODO: add email confirmation
    return Response(status_code=status.HTTP_201_CREATED)


def login(data: LoginProfile) -> Response:
    profile_id = login_profile(data)
    if profile_id is None:
        raise HTTPException(
            detail="Incorrect email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    session_id = create_auth_session(profile_id)

    response = Response(status_code=status.HTTP_200_OK)
    # TODO: set additional options in cookie for security reason
    response.set_cookie(
        key=COOKIE_SESSION_ID,
        value=session_id,
        httponly=True,
        max_age=auth_settings.session_cookie_ttl.seconds
    )
    return response


def logout(session_id: str = Cookie(), profile_id: int = Depends(authenticated)) -> Response:
    delete_auth_session(session_id)
    return Response(status_code=status.HTTP_200_OK)
