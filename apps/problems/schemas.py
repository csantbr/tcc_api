from pydantic import BaseModel

from apps.problems.examples import problem_complete


class ProblemIn(BaseModel):
    name: str
    description: str
    data_entry: str | None
    entry_description: str
    data_output: str
    output_description: str

    class Config:
        schema_extra = {'example': problem_complete}
