from pydantic import UUID4, BaseModel, Field
from uuid import uuid4
from apps.problems.examples import problem_complete


class Problem(BaseModel):
    name: str
    description: str
    data_entry: str | None
    entry_description: str
    data_output: str
    output_description: str

    class Config:
        schema_extra = {'example': problem_complete}


class ProblemIn(Problem):
    pass


class ProblemOut(Problem):
    id: UUID4 = Field(default_factory=uuid4)
