from fastapi import HTTPException, status
from pydantic.error_wrappers import ErrorWrapper


class BaseException(Exception):
    message: str = 'Internal server error'


class ConflictObject(BaseException):
    message: str = 'Object in conflict, you cannot delete this object because it violates foreign key constraint'

    def __init__(self, *args: object, message: str = None) -> None:
        super().__init__(*args)
        if message:
            self.message = message


class DuplicateObject(BaseException):
    message: str = 'Object already exists'

    def __init__(self, *args: object, message: str = None) -> None:
        super().__init__(*args)
        if message:
            self.message = message


class NotFoundException(HTTPException):
    def __init__(self, detail='Not found'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ValidationError(Exception):
    field = ''
    message = 'Internal server error'

    def errors(self):
        return [ErrorWrapper(ValueError(self.message), ('body', self.field))]


class InvalidLanguageType(ValidationError):
    def __init__(self, *args: object, field: str, message: str = 'Invalid language type') -> None:
        super().__init__(*args)
        self.field = field
        self.message = message


class InvalidContent(ValidationError):
    def __init__(self, *args: object, field: str, message: str = None) -> None:
        super().__init__(*args)
        self.field = field
        self.message = f'Invalid {self.field}, the {self.field} must be a valid base64.'
