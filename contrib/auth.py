from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from config import settings


def authentication(credentials: HTTPBasicCredentials = Depends(HTTPBearer())):
    has_permission = settings.BEARER_KEY == credentials.credentials

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized',
        )
    return has_permission
