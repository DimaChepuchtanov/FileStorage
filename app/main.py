from fastapi import FastAPI, HTTPException, Cookie, Depends
from app.utils.security import get_current_token
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.database.database import engine, Base
from app.routers import auth, audio, user
from app.config import setting
import uvicorn

app = FastAPI(docs_url=None, redoc_url=None)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Переопределение маршрута для документации
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(token: str = Depends(get_current_token)):
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )


# Переопределение маршрута для JSON-документации
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(token: str = Depends(get_current_token)):
    return get_openapi(
        title="API",
        version=app.version,
        routes=app.routes,
    )

app.include_router(auth.router)
app.include_router(audio.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)