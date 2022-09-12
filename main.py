from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from api import router
from database.session import Base, engine

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

origins = [
    'http://localhost',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs', status_code=status.HTTP_302_FOUND)


app.include_router(router)


Base.metadata.create_all(bind=engine)
