from fastapi import APIRouter

from apps.problems.controller import problem_router
from apps.submissions.controller import submission_router

router = APIRouter(prefix='/api', responses={404: {'description': 'not found'}})
router.include_router(problem_router)
router.include_router(submission_router)
