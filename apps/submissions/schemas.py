from uuid import UUID, uuid4

from pydantic import BaseModel as Model
from pydantic import Field

from apps.submissions.examples import submission_in_complete, submission_out_complete


class Submission(Model):
    problem_id: UUID = Field(title='Problem id')
    language_type: str = Field(title='Language type')
    content: str = Field(title='Code')


class SubmissionIn(Submission):
    class Config:
        schema_extra = {'example': submission_in_complete}


class SubmissionOut(Submission):
    id: UUID = Field(title='Id', default_factory=uuid4)
    status: str = Field(title='Submission status')

    class Config:
        schema_extra = {'example': submission_out_complete}
