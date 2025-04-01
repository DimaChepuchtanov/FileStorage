from sqlalchemy.future import select
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import  AsyncSession
from app.database.models import User, UserFileStorage
from app.schemas import UserCreate, FileCreate
from datetime import datetime


#  БЛОК USER
async def get_just_users(db: AsyncSession) -> list[dict]:
    """"""
    result = await db.execute(select(User).where(User.is_superuser == False))
    result = result.scalars().all()
    return [{"email": x.email, "created_at": datetime.strftime(x.create_at, "%d.%m.%Y %H:%M"), "id": x.id} for x in result]


async def get_superuser(db: AsyncSession):
    """"""
    result = await db.execute(select(User).filter(User.is_superuser == True))
    result = result.scalars().all()
    return [{"email": x.email, "created_at": datetime.strftime(x.create_at, "%d.%m.%Y %H:%M"), "id": x.id} for x in result]


async def get_user_from_email(db: AsyncSession, email: str) -> dict:
    """"""
    result = await db.execute(select(User).filter(User.email == email))
    result = result.scalars().first()
    return {"email": result.email, "created_at": datetime.strftime(result.create_at, "%d.%m.%Y %H:%M"), "id": result.id} if result is not None else None


async def get_user_from_id(db: AsyncSession, id: int):
    """"""
    result = await db.execute(select(User).filter(User.id == id))
    result = result.scalars().first()
    return {"email": result.email, "created_at": datetime.strftime(result.create_at, "%d.%m.%Y %H:%M"), "is_superuser": result.is_superuser} if result is not None else None


async def delete_user(db: AsyncSession, id: int):
    """"""
    user = await db.execute(select(User).filter(User.id == id))
    user = user.scalars().first()
    if user:
        await db.delete(user)
        await db.commit()
        return True
    else:
        return False


async def create_user(db: AsyncSession, user: UserCreate):
    """"""
    db_user = User(email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, status: bool, id: int):
    """"""
    upd_user = await db.execute(select(User).where(User.id == id))
    upd_user = upd_user.scalars().first()
    if not upd_user:
        return False
    upd_user.is_superuser = status
    await db.commit()
    await db.refresh(upd_user)


async def get_files_for_user(db: AsyncSession, id: int):
    """"""
    result = await db.execute(select(UserFileStorage).filter(UserFileStorage.user == id))
    return result.scalars().all() # TODO дописать 


async def get_file_path(db: AsyncSession, id: int) -> str:
    """"""
    result = await db.execute(select(UserFileStorage.path).where(UserFileStorage.id == id))
    return result.scalars().first()


async def create_file_for_user(db: AsyncSession, file: FileCreate):
    """"""
    db_file = UserFileStorage(user=file.user, path=file.path)
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file


async def delete_file_for_user(db: AsyncSession, id: int):
    """"""
    file = await db.execute(select(UserFileStorage).filter(UserFileStorage.id == id))
    file = file.scalars().first()
    if file:
        await db.delete(file)
        await db.commit()
        return True
    else:
        return False