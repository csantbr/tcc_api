from pydantic import Field, ConfigDict

from src.contrib.collection_response import CollectionResponse
from src.contrib.schemas import Model, OutMixin
from enum import Enum
from src.users.examples import (
    user_collection_response_example,
    user_in_example,
    user_out_example,
)


class Role(str, Enum):
    JUDGE = "JUDGE"
    PARTICIPANT = "PARTICIPANT"
    GHOST = "GHOST"
    MASTER = "MASTER"


class User(Model):
    username: str = Field(title="Username")
    password: str = Field(title="Password")
    role: Role = Field(default=Role.PARTICIPANT, title="Role")


class UserIn(User):
    model_config = ConfigDict(json_schema_extra={'example': user_in_example})


class UserOut(User, OutMixin):
    model_config = ConfigDict(json_schema_extra={'example': user_out_example})


class UserCollectionResponse(CollectionResponse):
    model_config = ConfigDict(json_schema_extra={'example': user_collection_response_example})
