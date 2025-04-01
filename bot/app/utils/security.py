from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Query, Cookie, Response
from fastapi.security import OAuth2PasswordBearer
from app.config import setting
from app.dependecies import get_db
from app.database.crud import get_user_from_email
from sqlalchemy.ext.asyncio import AsyncSession


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, setting.YANDEX_CLIENT_SECRET, algorithm="HS256")


async def get_current_user(token: str):
    payload = jwt.decode(token, setting.YANDEX_CLIENT_SECRET, algorithms=["HS256"])
    email: str = payload.get("sub")
    return email


async def get_current_token(token: str = Cookie(alias='token'), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, setting.YANDEX_CLIENT_SECRET, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(404, 'Invalid Token')
        user = await get_user_from_email(db, email)
        if not user:
            raise HTTPException(404, 'Invalid Token')
    except JWTError as e:
        raise HTTPException(404, 'Invalid Token')
    return token


async def update_access_token(token):
    decoded_payload = jwt.decode(token, setting.YANDEX_CLIENT_SECRET, algorithms=["HS256"], options={"verify_exp": False})

    if 'exp' in decoded_payload and datetime.utcfromtimestamp(decoded_payload['exp']) < datetime.utcnow():
        # Токен истек, создаем новый токен
        user_data = {
            "sub": decoded_payload.get("sub")
        }
        new_token = create_access_token(user_data)
        resp = Response("Yes")
        resp.set_cookie(key="token", value=new_token)
        return resp
    else:
        raise HTTPException(status_code=400, detail="Token has not expired yet")