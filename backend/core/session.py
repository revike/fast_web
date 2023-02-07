from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.core.settings import DATABASE_URL

# create async engine for interaction with database
engine = create_async_engine(DATABASE_URL,
                             connect_args={'check_same_thread': False},
                             echo=True, future=True)

# create session for the interaction with database
async_session_maker = sessionmaker(engine, class_=AsyncSession,
                                   expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async session"""
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        await session.close()
