from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Cookie, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependecies import get_db
from app.database.crud import (get_files_for_user as get_files,
                           get_user_from_email as get_user,
                           create_file_for_user as up_file,
                           delete_file_for_user as delete_file,
                           get_file_path)
import os
from app.utils.security import get_current_user
from app.schemas import FileCreate

router = APIRouter(tags=["audio"])


@router.get("/audio/list")
async def get_user_audio(token: str = Cookie(alias="token"),
                         db: AsyncSession = Depends(get_db)):

    email = await get_current_user(token)
    user = await get_user(db, email)
    if not user:
        raise HTTPException(404, "User don't founded")

    return await get_files(db, user['id'])


@router.put("/audio/upload")
async def upload_user_audio(file: UploadFile = File(...),
                            token: str = Cookie(alias="token"),
                            db: AsyncSession = Depends(get_db)):

    email = await get_current_user(token)

    path = os.getcwd() + f"/app/storage/{email.split('@')[0]}/{file.filename}"
    user = await get_user(db, email)

    with open(path, "wb") as f:
        f.write(file.file.read())


    result = await up_file(db, FileCreate(user=user['id'], path=path))
    return result


@router.delete('/audio/delete')
async def delete_user_audio(token: str = Cookie(alias="token"),
                            db: AsyncSession = Depends(get_db),
                            id: int = Query(alias='id')):
    """"""
    path = await get_file_path(db, id)
    result = await delete_file(db, id)
    os.remove(path)
    return result
