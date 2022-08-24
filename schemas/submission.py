from pydantic import BaseModel
from uuid import UUID


class Submission(BaseModel):
    problem_id: UUID
    language_type: str
    content: str
