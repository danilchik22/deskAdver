from fastapi import Depends, FastAPI

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.models import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.advertisement.routers import router


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

@app.post("/create_ad")
def create_ad(user: User = Depends(current_user)):
    return user


app.include_router(router)
