from src.contrib.models.base import BaseModelMixin
from pydantic import Field
from src.contrib.schemas import UTCDatetime

from src.users.schemas import Role


class UserModel(BaseModelMixin):
    username: str = Field(title="Username")
    password: str = Field(title="Password")
    role: Role = Field(title="Role")
    updated_at: UTCDatetime | None = Field(default=None, title='Last update date')
