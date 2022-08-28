from fastapi import status, HTTPException


class UnauthorizedException(HTTPException):
    def __init__(self, detail='authorization has been refused'):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail='access not allowed'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail='not found'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class LanguageNotImplemented(HTTPException):
    def __init__(self, detail='language judge not implemented'):
        super().__init__(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=detail)


class UnprocessableEntity(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
