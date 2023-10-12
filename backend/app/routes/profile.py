from fastapi import Response, status, Depends

from backend.app.auth.deps import authenticated


def profile(profile_id: int = Depends(authenticated)):
    return Response(f"Hello it's profile_id={profile_id}", status_code=status.HTTP_200_OK)