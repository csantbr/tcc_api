from fastapi import APIRouter, Depends

from apps.problems.controller import problem_router
from apps.submissions.controller import submission_router
from contrib.auth import authentication

router = APIRouter(prefix='/api', dependencies=[Depends(authentication)])

router.include_router(problem_router)
router.include_router(submission_router)
