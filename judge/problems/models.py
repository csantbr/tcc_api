from judge.contrib.models.base import BaseModelMixin
from judge.problems.schemas import Problem


class ProblemModel(BaseModelMixin, Problem):
    pass
