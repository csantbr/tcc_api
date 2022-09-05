from fastapi import APIRouter

from routers.controllers.problem import problem_router
from routers.controllers.submission import submission_router

router = APIRouter(prefix='/api', responses={404: {'description': 'not found'}})
router.include_router(problem_router)
router.include_router(submission_router)
