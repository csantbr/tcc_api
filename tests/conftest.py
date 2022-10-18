import os
import sys
# from typing import Any, Generator

import pytest
from fastapi import FastAPI

from typing import AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from api import router
from database.session import Base, engine, SessionLocal, get_database


# def start_application():
#     app = FastAPI()
#     app.include_router(router)
#     return app


# SQLALCHEMY_DATABASE_URL = 'sqlite:///./test_db.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# https://fastapi.tiangolo.com/advanced/testing-database/
# https://fastapi.tiangolo.com/tutorial/sql-databases/

# @pytest.fixture(scope='function')
# def app() -> Generator[FastAPI, Any, None]:
#     Base.metadata.create_all(engine)
#     _app = start_application()
#     yield _app
#     Base.metadata.drop_all(engine)


# @pytest.fixture(scope='function')
# def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = SessionTesting(bind=connection)
#     yield session

#     session.close()
#     transaction.rollback()
#     connection.close()


# @pytest.fixture(scope='function')
# def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
#     def _get_test_db():
#         try:
#             yield db_session
#         finally:
#             pass

#     app.dependency_overrides[get_database] = _get_test_db
#     with TestClient(app) as client:
#         yield client

@pytest.fixture
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

        async with SessionLocal(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture
def database(db_session: AsyncSession) -> Callable:
    async def _database():
        yield db_session

    return _database

@pytest.fixture
def app(database: Callable) -> FastAPI:
    from main import app

    app.dependency_overrides[get_database] = database

    return app


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        app=app, base_url='http://judge'
    ) as ac:
        yield ac