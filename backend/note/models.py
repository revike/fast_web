from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Note(Base):
    __tablename__ = 'note'

    id: int = Column(Integer, primary_key=True)
    text: str = Column(String)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    updated: datetime = Column(TIMESTAMP, default=datetime.utcnow,
                               onupdate=datetime.utcnow)
