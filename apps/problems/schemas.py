from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from apps.problems.examples import problem_in_complete, problem_out_complete


class Problem(BaseModel):
    name: str = Field(title='Problem name')
    description: str = Field(title='Problem description')
    data_entry: str | None = Field(title='Problem data entry')
    entry_description: str = Field(title='Problem entry description')
    data_output: str = Field(title='Problem data output')
    output_description: str = Field(title='Problem output description')


class ProblemIn(Problem):
    class Config:
        schema_extra = {'example': problem_in_complete}


class ProblemOut(Problem):
    id: UUID = Field(title='Id', default_factory=uuid4)

    class Config:
        schema_extra = {'example': problem_out_complete}
