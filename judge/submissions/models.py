from judge.contrib.models.base import BaseModelMixin
from judge.submissions.schemas import Submission


class SubmissionModel(BaseModelMixin, Submission):
    pass
