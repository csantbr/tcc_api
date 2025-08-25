from src.contrib.models.base import BaseModelMixin
from src.problems.schemas import Problem
from src.contrib.schemas import OutMixin


class ProblemModel(BaseModelMixin, Problem, OutMixin):
    pass
