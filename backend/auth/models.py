from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, \
    TIMESTAMP, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    phone: int = Column(Integer, unique=True)
    email: str = Column(String(length=256), unique=True, index=True,
                        nullable=False)
    username: str = Column(String(64), unique=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    created: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    updated: datetime = Column(TIMESTAMP, default=datetime.utcnow,
                               onupdate=datetime.utcnow)


class Profile(Base):
    __tablename__ = 'profile'

    id: int = Column(Integer, primary_key=True)
    user: int = Column(Integer, ForeignKey('user.id'))
    first_name = Column(String(128))
    last_name = Column(String(128))
    photo = Column(LargeBinary, nullable=True)
    photo_50 = Column(LargeBinary, nullable=True)
    photo_100 = Column(LargeBinary, nullable=True)
    photo_400 = Column(LargeBinary, nullable=True)

    user_ = relationship('User', backref='Profile', uselist=False)
