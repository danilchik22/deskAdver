import uuid
from fastapi import Depends, HTTPException
from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from fastapi_users import FastAPIUsers
from src.auth.models import User
from src.auth.manager import get_user_manager
from src.config import SECRET_KEY

cookie_transport = CookieTransport(cookie_name="deskAdver", cookie_max_age=3600)


SECRET = SECRET_KEY


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


def get_current_active_user(
    current_user: User = Depends(current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_admin(current_user: User = Depends(current_user)) -> User:
    if not current_user.role_id != 2:
        raise HTTPException(
            status_code=400, detail="The user douesn't have enough privileges"
        )
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
