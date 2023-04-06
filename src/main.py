from fastapi import FastAPI
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead
from src.advertisement.routers import router as router_adver
from src.auth.admin import router as router_admin


app = FastAPI(title="Bulletin board")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


app.include_router(router_adver)
app.include_router(router_admin)
