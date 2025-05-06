from datetime import datetime
from typing import Any

from bson import ObjectId
from pydantic import UUID4, BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema


class UTCDatetime(datetime):
    """
    Custom datetime class for enforcing UTC timezone.
    """

    @classmethod
    def validate(cls, value: Any) -> datetime:
        if not isinstance(value, datetime):
            value = datetime.fromisoformat(value)

        if not value.tzinfo:
            raise ValueError('Timezone is required')

        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: Any
    ) -> dict:
        """
        Provide a JSON Schema representation for Swagger/OpenAPI.
        """
        return {
            'type': 'string',
            'format': 'date-time',
            'description': 'UTC datetime in ISO 8601 format',
        }


class Model(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}


class OutMixin(BaseModel):
    id: UUID4 = Field(default='', title='Identifier id')
    created_at: UTCDatetime = Field(title='Creation date')
