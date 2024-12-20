from pydantic import Field

from judge.contrib.collection_response import CollectionResponse
from judge.contrib.schemas import Model, OutMixin
from judge.problems.examples import (
    problem_collection_response_example,
    problem_in_example,
    problem_out_example,
)


class Problem(Model):
    name: str = Field(title='Problem name')
    description: str = Field(title='Problem description')
    data_entry: str | None = Field(title='Problem data entry')
    entry_description: str = Field(title='Problem entry description')
    data_output: str = Field(title='Problem data output')
    output_description: str = Field(title='Problem output description')


class ProblemIn(Problem):
    class Config:
        json_schema_extra = {'example': problem_in_example}


class ProblemOut(Problem, OutMixin):
    class Config:
        json_schema_extra = {'example': problem_out_example}


class ProblemCollectionResponse(CollectionResponse):
    class Config:
        json_schema_extra = {'example': problem_collection_response_example}
