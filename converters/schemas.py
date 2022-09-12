from typing import Any

from apps.problems.models import Problem
from apps.problems.schemas import ProblemIn
from apps.submissions.models import Submission
from apps.submissions.schemas import SubmissionIn


def convert_schema_to_model(schema: Any) -> Any:
    if isinstance(schema, ProblemIn):
        model = Problem()

        model.name = schema.name
        model.description = schema.description
        model.entry_description = schema.entry_description
        model.data_entry = schema.data_entry
        model.output_description = schema.output_description
        model.data_output = schema.data_output
    elif isinstance(schema, SubmissionIn):
        model = Submission()

        model.problem_id = schema.problem_id
        model.language_type = schema.language_type
        model.content = schema.content
        model.status = 'PENDING'

    return model


def set_schema_to_model(schema: Any, model: Any) -> Any:
    if isinstance(schema, ProblemIn):
        model.name = schema.name
        model.description = schema.description
        model.entry_description = schema.entry_description
        model.data_entry = schema.data_entry
        model.output_description = schema.output_description
        model.data_output = schema.data_output
    elif isinstance(schema, SubmissionIn):
        model.problem_id = schema.problem_id
        model.language_type = schema.language_type
        model.content = schema.content
        model.status = ''

    return model
