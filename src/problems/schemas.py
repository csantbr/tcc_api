from pydantic import Field, ConfigDict
from typing import List

from src.contrib.collection_response import CollectionResponse
from src.contrib.schemas import Model, OutMixin
from src.problems.examples import (
    problem_collection_response_example,
    problem_in_example,
    problem_out_example,
)


class Problem(Model):
    name: str = Field(title='Problem name')
    description: str = Field(title='Problem description')
    data_entries: List[str] = Field(title='Problem data entries', default_factory=list)
    entry_description: str = Field(title='Problem entry description')
    data_outputs: List[str] = Field(title='Problem data outputs', default_factory=list)
    output_description: str = Field(title='Problem output description')


class ProblemIn(Problem):
    model_config = ConfigDict(json_schema_extra={'example': problem_in_example})


class ProblemOut(Problem, OutMixin):
    model_config = ConfigDict(json_schema_extra={'example': problem_out_example})


class ProblemCollectionResponse(CollectionResponse):
    model_config = ConfigDict(json_schema_extra={'example': problem_collection_response_example})


class ProblemUpdate(Model):
    name: str | None = Field(title='Problem name', default=None)
    description: str | None = Field(title='Problem description', default=None)
    data_entries: List[str] | None = Field(title='Problem data entries', default=None)
    entry_description: str | None = Field(title='Problem entry description', default=None)
    data_outputs: List[str] | None = Field(title='Problem data outputs', default=None)
    output_description: str | None = Field(title='Problem output description', default=None)
