from fastapi import APIRouter

from apps.problem.controller import problem_router
from apps.submission.controller import submission_router

router = APIRouter(prefix='/api', responses={404: {'description': 'not found'}})
router.include_router(problem_router)
router.include_router(submission_router)
