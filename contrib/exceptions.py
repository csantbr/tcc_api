from fastapi import HTTPException, status
from pydantic.error_wrappers import ErrorWrapper


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


class ValidationError(Exception):
    error_field = ''
    message = 'Internal server error'

    def errors(self):
        return [ErrorWrapper(ValueError(self.message), ('body', self.error_field))]


class InvalidLanguageType(ValidationError):
    def __init__(self, *args: object, error_field: str, message: str = 'Invalid language type') -> None:
        super().__init__(*args)
        self.error_field = error_field
        self.message = message


class InvalidBase64(ValidationError):
    def __init__(self, *args: object, error_field: str, message: str = 'Invalid base64 encode') -> None:
        super().__init__(*args)
        self.error_field = error_field
        self.message = message
