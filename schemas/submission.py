from uuid import UUID

from pydantic import BaseModel


class Submission(BaseModel):
    problem_id: UUID
    language_type: str
    content: str
