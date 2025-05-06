from judge.contrib.models.base import BaseModelMixin
from pydantic import Field

from judge.users.schemas import Role


class UserModel(BaseModelMixin):
    username: str = Field(title="Username")
    password: str = Field(title="Password")
    role: Role = Field(title="Role")
