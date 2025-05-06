from src.contrib.models.base import BaseModelMixin
from src.submissions.schemas import Submission


class SubmissionModel(BaseModelMixin, Submission):
    pass
