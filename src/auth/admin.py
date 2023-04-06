import logging
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import delete, select, update
from src.advertisement.utils import get_lst_of_dict_advertisement, get_lst_of_dict_users
from src.auth.base_config import get_current_active_admin, get_current_active_superuser
from src.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.advertisement.models import comment, advertisement
from sqlalchemy import and_


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/check_logging")
async def check_logging():
    """ "Point для проверки логирования"""
    logger = logging.getLogger("Логгер доски объявлений")
    logger.error("Критическая ошибка!!!")
    logger.warning("Внимание!!!")
    logger.debug("Debug лог")
    logger.info("Инфо лог")


@router.patch("/make_admin")
async def make_admin(
    id_user: UUID,
    user: User = Depends(get_current_active_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    """Сделать пользователя админом"""
    stmt = update(User).where(User.id == id_user).values(role_id=2)
    await session.execute(stmt)
    await session.commit()
    return {"status": "200", "details": "Объект изменен"}


@router.patch("/del_admin")
async def del_admin(
    id_user: UUID,
    user: User = Depends(get_current_active_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    """Аннулировать права админа у пользователя"""
    stmt = update(User).where(User.id == id_user).values(role_id=1)
    await session.execute(stmt)
    await session.commit()
    return {"status": "200", "details": "Объект изменен"}


@router.get("/alladvertisements")
async def get_ad(
    skip: int = 0,
    limit: int = 20,
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """Просмотреть все объявления, в том числе не актуальные и не подтвержденные"""
    query = select(advertisement).offset(skip).limit(limit)
    result = await session.execute(query)
    return {"status": 200, "data": await get_lst_of_dict_advertisement(result.all())}


@router.patch("/alladvertisements/{id_ad}")
async def confirm_ad(
    id_ad: int,
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """Одобрить размещения объявления"""
    stmt = update(advertisement).where(advertisement.c.id == id_ad).values(confirm=1)
    await session.execute(stmt)
    await session.commit()
    return {"status": "200", "details": "Объявление подтверждено"}


@router.patch("/alladvertisement/{id_ad}/changecategory")
async def change_category(
    id_ad: int,
    id_new_category: int,
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """Сменить категорию у объявления"""
    stmt = (
        update(advertisement)
        .where(advertisement.c.id == id_ad)
        .values(category_id=id_new_category)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "200", "details": "Категория объявления изменена"}


@router.get("/users/")
async def get_users(
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список всех пользователей"""
    query = select(User)
    result = await session.execute(query)
    return {"status": "200", "data": await get_lst_of_dict_users(result.all())}


@router.patch("/users/{id_user}/block")
async def block_users(
    id_user: UUID,
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """Заблокировать пользователя"""
    stmt = (
        update(User)
        .where(and_(User.id == id_user, User.is_superuser == False))
        .values(is_active=True)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "200", "detail": "Пользователь заблокирован"}


@router.patch("/users/{id_user}/unblock")
async def block_users(
    id_user: UUID,
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """Разблокировать пользователя"""
    stmt = update(User).where(User.id == id_user).values(is_active=True)
    await session.execute(stmt)
    await session.commit()
    return {"status": "200", "detail": "Пользователь разблокирован"}
