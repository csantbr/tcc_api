from uuid import UUID

from pydantic import BaseModel

from apps.submissions.examples import submission_complete


class SubmissionIn(BaseModel):
    problem_id: UUID
    language_type: str
    content: str

    class Config:
        schema_extra = {'example': submission_complete}
