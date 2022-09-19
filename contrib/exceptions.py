from fastapi import HTTPException, status


class BaseException(Exception):
    message: str = 'Internal Server Error'


class DuplicatedObject(BaseException):
    message: str = 'Object already exists'

    def __init__(self, *args: object, message: str = None) -> None:
        super().__init__(*args)
        if message:
            self.message = message


class UnauthorizedException(HTTPException):
    def __init__(self, detail='authorization has been refused'):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail='access not allowed'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail='not found'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidLanguageType(HTTPException):
    def __init__(self, detail='invalid language type on language type field'):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class InvalidBase64(HTTPException):
    def __init__(self, detail='invalid base64 encode on content field'):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
