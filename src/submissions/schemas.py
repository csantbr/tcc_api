from pydantic import BaseModel, Field, ConfigDict

from uuid import UUID

from src.contrib.collection_response import CollectionResponse
from src.contrib.schemas import Model, OutMixin
from src.submissions.examples import (
    submission_collection_response_example,
    submission_in_example,
    submission_out_example,
)


class Submission(Model):
    problem_id: UUID = Field(title='Problem id')
    language_type: str = Field(title='Language type')
    content: str = Field(title='Code')
    status: str = Field(title='Status')


class SubmissionIn(BaseModel):
    problem_id: UUID = Field(title='Problem id')
    language_type: str = Field(title='Language type')
    content: str = Field(title='Code')

    model_config = ConfigDict(json_schema_extra={'example': submission_in_example})


class SubmissionOut(Submission, OutMixin):
    model_config = ConfigDict(json_schema_extra={'example': submission_out_example})


class SubmissionCollectionResponse(CollectionResponse):
    model_config = ConfigDict(json_schema_extra={'example': submission_collection_response_example})
