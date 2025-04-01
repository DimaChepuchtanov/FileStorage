from fastapi import APIRouter, Depends, HTTPException, Query, Response
from app.schemas import User
from app.database.models import User as UserTable
from app.database.crud import get_just_users, get_superuser, delete_user, get_user_from_id, update_user
from app.dependecies import get_db
from app.utils.security import get_current_token
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["users"])


@router.get('/user/list-user')
async def get_list_user(token: str = Depends(get_current_token),
                        db: AsyncSession = Depends(get_db),
                        is_superuser: bool = Query(default=False, alias="is_super")):
    result = []
    if is_superuser:
        result = await get_superuser(db)
    else:
        result = await get_just_users(db)

    return result


@router.get('/user')
async def get_info_user(token: str = Depends(get_current_token),
                        db: AsyncSession = Depends(get_db),
                        id: int = Query(alias="id")):
    """"""
    user = await get_user_from_id(db, id)
    if not user:
        return Response("Not found user", 404)

    return user


@router.patch('/user/update')
async def patch_user_status(token: str = Depends(get_current_token),
                            db: AsyncSession = Depends(get_db),
                            id: int = Query(alias="id"),
                            status: bool = Query(alias='status')):
    """"""
    result = await update_user(db, status, id)
    return "200"


@router.delete("/user/delete")
async def delete_user_from_id(token: str = Depends(get_current_token),
                              db: AsyncSession = Depends(get_db),
                              id: int = Query(alias='id')):

    is_super = await get_user_from_id(db, id)
    if is_super is None:
        return Response("Not found user", 404)

    is_super = is_super['is_superuser']
    if is_super is not True:
        return Response("Not super user", 401)

    result = await delete_user(db, id)
    if result:
        return 'Успешно'
    else:
        return 'Ошибка'

    """Блок работы с блек листом"""
    pass