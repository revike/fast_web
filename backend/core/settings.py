import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

SECRET_KEY = os.environ.get('SECRET_KEY')

"""
alembic init migrations
alembic revision --autogenerate -m 'database create'
alembic upgrade head
"""

# DATABASE_URL = f'postgresql+asyncpg:' \
#                f'//{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
#                f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

DATABASE_URL = 'sqlite+aiosqlite:///./../db.sqlite3'
