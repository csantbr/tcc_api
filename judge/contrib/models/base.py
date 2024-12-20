from datetime import datetime, timezone

from pydantic import UUID4, Field

from judge.contrib.schemas import Model, UTCDatetime


class BaseModelMixin(Model):
    id: UUID4 = Field(title='Identifier id')
    created_at: UTCDatetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title='Creation date',
    )
