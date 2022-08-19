import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = 'Judge'
    PROJECT_VERSION: str = '0.0.1'

    DATABASE_URL: str = os.environ.get('DATABASE_URL')


settings = Settings()
