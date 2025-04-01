from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os


class UserBase(BaseModel):
    email: str
    is_superuser: bool = False


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    is_superuser: Optional[bool] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class FileBase(BaseModel):
    user: int
    path: str = f'{os.getcwd}/app/storage/'


class File(FileBase):
    id: int
    create_at: datetime

    class Config:
        orm_mode = True


class FileCreate(FileBase):
    pass
