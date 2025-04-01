from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String, Boolean, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_superuser = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.utcnow)


class UserFileStorage(Base):
    __tablename__ = "storage"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    path = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow)