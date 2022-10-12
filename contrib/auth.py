from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from config import settings


def authentication(auth: HTTPBasicCredentials = Depends(HTTPBearer())):
    has_permission = settings.BEARER_KEY == auth.credentials

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authenticated',
        )
    return has_permission
