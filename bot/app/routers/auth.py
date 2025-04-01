from fastapi import APIRouter, Depends, HTTPException, Response, Request, Cookie
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import setting
from app.dependecies import get_db
from app.database.crud import (get_user_from_email as get_user,
                           create_user)
from app.utils.security import create_access_token, get_current_token, update_access_token
from app.schemas import UserCreate
import os

router = APIRouter(tags=["auth"])

YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"


@router.get('/login')
async def login():
    """"""
    return  Response(f"""<!DOCTYPE html>
                            <html>
                            <head>
                                <title>Target Page</title>
                            </head>
                            <body>
                                <script>
                                                window.location.replace("https://oauth.yandex.ru/authorize?response_type=code&client_id={setting.YANDEX_CLIENT_ID}")
                                </script>
                            </body>
                            </html>
                    """)


@router.get("/auth/yandex/callback")
async def yandex_callback(code: str,
                          db: AsyncSession = Depends(get_db)):
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": setting.YANDEX_CLIENT_ID,
        "client_secret": setting.YANDEX_CLIENT_SECRET
    }

    response = requests.post(YANDEX_TOKEN_URL, data=token_data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid code")
    access_token = response.json()["access_token"]

    user_info = requests.get(YANDEX_USER_INFO_URL, params={"oauth_token": access_token})
    if user_info.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not fetch user info")
    email = user_info.json().get("default_email")

    user = await get_user(db, email)
    if not user:
        user = await create_user(db, user=UserCreate(email=email))
        os.mkdir(f'{os.getcwd()}/app/storage/{email.split("@")[0]}')

    jwt = create_access_token({"sub": email})

    response = Response("""<!DOCTYPE html>
                            <html>
                            <head>
                                <title>Target Page</title>
                            </head>
                            <body>
                                <script>
                                                window.location.replace("/docs")
                                </script>
                            </body>
                            </html>
                    """)

    response.set_cookie(key="token", value=jwt, max_age=1900)
    return response


@router.get('/update-token')
async def update_token(token: str = Cookie(alise="token")):
    """"""

    if token is None:
        raise HTTPException(404, detail="Invalid Token")

    return await update_access_token(token)

