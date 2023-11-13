import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

SECRET_KEY = os.environ.get('SECRET_KEY', default='secret_key')
ALGORITHM: str = os.environ.get('ALGORITHM', default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', default=30))
REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES', default=60))

"""
alembic init migrations
alembic revision --autogenerate -m 'database create'
alembic upgrade head
"""

# DATABASE_URL = f'postgresql+asyncpg:' \
#                f'//{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
#                f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

DATABASE_URL = 'sqlite+aiosqlite:///./../db.sqlite3'

# Datetime settings
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'
SECOND_FORMAT = ':%S'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}{SECOND_FORMAT}'
