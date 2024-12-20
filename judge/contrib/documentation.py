from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(description='Detail')


class NotFoundErrorResponse(ErrorResponse):
    detail: str = 'Not Found'


class ConflictErrorResponse(ErrorResponse):
    detail: str = 'Conflict'


class UnprocessableEntityErrorResponse(ErrorResponse):
    detail: str = 'Unprocessable Entity'


class InternalServerErrorResponse(ErrorResponse):
    detail: str = 'Internal Server Error'
