from database.session import Base
from fastapi import FastAPI, status
from database.session import engine
from starlette.responses import RedirectResponse
from routers.api import router


tags_metadata = [
    {
        'name': 'problems',
        'description': 'List information of problems',
    },
    {
        'name': 'submissions',
        'description': 'List submissions of problems',
    },
]


app = FastAPI(openapi_tags=tags_metadata, title='Judge')


@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs', status_code=status.HTTP_302_FOUND)


app.include_router(router)


Base.metadata.create_all(bind=engine)
