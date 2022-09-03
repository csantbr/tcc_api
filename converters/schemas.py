from models.submission import Submission as SubmissionModel
from models.problem import Problem as ProblemModel
from schemas.submission import Submission
from schemas.problem import Problem
from typing import Any


def convert_schema_to_model(schema: Any) -> Any:
    if isinstance(schema, Problem):
        model = ProblemModel()

        model.name = schema.name
        model.description = schema.description
        model.entry_description = schema.entry_description
        model.data_entry = schema.data_entry
        model.output_description = schema.output_description
        model.data_output = schema.data_output
    elif isinstance(schema, Submission):
        model = SubmissionModel()

        model.problem_id = schema.problem_id
        model.language_type = schema.language_type
        model.content = schema.content
        model.status = 'pending'

    return model


def set_schema_to_model(schema: Any, model: Any) -> Any:
    if isinstance(schema, Problem):
        model.name = schema.name
        model.description = schema.description
        model.entry_description = schema.entry_description
        model.data_entry = schema.data_entry
        model.output_description = schema.output_description
        model.data_output = schema.data_output
    elif isinstance(schema, Submission):
        model.problem_id = schema.problem_id
        model.language_type = schema.language_type
        model.content = schema.content
        model.status = ''

    return model
