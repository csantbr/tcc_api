from src.contrib.models.base import BaseModelMixin
from pydantic import Field

from src.users.schemas import Role


class UserModel(BaseModelMixin):
    username: str = Field(title="Username")
    password: str = Field(title="Password")
    role: Role = Field(title="Role")
