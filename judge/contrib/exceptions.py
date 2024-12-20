class BaseException(Exception):
    message: str = 'Internal Server Error'

    def __init__(self: 'BaseException', message: str | None = None) -> None:
        if message:
            self.message = message

    def __str__(self: 'BaseException') -> str:
        return self.message


class ValidationError(Exception):
    def __init__(
        self, *args: object, field: str, message: str = 'Internal Server Error'
    ) -> None:
        super().__init__(*args)
        self.field = field
        self.message = message

    def errors(self):
        return [
            {
                'loc': ('body', self.field),
                'msg': self.message,
                'type': 'value_error',
            }
        ]


class ObjectNotFound(BaseException):
    pass
