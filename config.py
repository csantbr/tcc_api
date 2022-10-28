import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = 'Judge'
    PROJECT_VERSION: str = '0.0.1'

    BASE_URL: str = 'http://localhost:8000'

    DATABASE_URL: str = os.environ.get('DATABASE_URL')

    BEARER_KEY: str = 'MV2022'

    TLE_TIMEOUT: int = 30


settings = Settings()
