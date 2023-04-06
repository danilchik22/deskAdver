from datetime import datetime
import logging
from asyncpg import UniqueViolationError
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy import delete, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.advertisement.schema import AdvertisementCreate, AdvertisementRead
from src.auth.models import User
from src.auth.schemas import UserRead
from src.database import get_async_session
from .models import DeleteAdvertisementResponse, advertisement
from fastapi.encoders import jsonable_encoder
from .schema import CommentCreate, CommentRead, ComplaintCreate, del_ad
from .utils import (
    get_lst_of_dict_advertisement,
    get_lst_of_dict_comment,
    get_lst_of_dict_complaint,
    get_privilege,
)
from src.auth.base_config import (
    current_user,
    get_current_active_admin,
    get_current_active_superuser,
)
from src.advertisement.models import comment, complaint
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/advertisements", tags=["Advertisements"])


@router.get("/")
async def get_ad(
    skip: int = 0,
    limit: int = 20,
    city_id: int = None,
    sort: str = "time",
    session: AsyncSession = Depends(get_async_session),
):
    """Получить все актуальные, подтвержденные объявления, у которых не вышел срок размещения"""
    if sort == "price":
        sort_item = advertisement.c.price
    if sort == "time":
        sort_item = advertisement.c.date
    if city_id:
        query = (
            select(advertisement)
            .where(
                advertisement.c.is_actual == True,
                advertisement.c.time_over > datetime.now(),
                advertisement.c.confirm == 1,
                advertisement.c.city_id == city_id,
            )
            .offset(skip)
            .limit(limit)
            .order_by(sort_item)
        )
    else:
        query = (
            select(advertisement)
            .where(
                advertisement.c.is_actual == True,
                advertisement.c.time_over > datetime.now(),
                advertisement.c.confirm == 1,
            )
            .offset(skip)
            .limit(limit)
            .order_by(sort_item)
        )
    result = await session.execute(query)
    return {"status": 200, "data": await get_lst_of_dict_advertisement(result.all())}


@router.post("/addadver")
async def add_ad(
    new_ad: AdvertisementCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Размещение объявления"""
    dict_new_ad = new_ad.dict()
    dict_new_ad["user_id"] = user.id
    try:
        stmt = insert(advertisement).values(**dict_new_ad)
    except IntegrityError:
        return HTTPException(status_code=400, detail="Такой объект уже существует")
    await session.execute(stmt)
    await session.commit()
    return {"status": "201", "details": "Объект создан"}


@router.get("/{id}")
async def detail(id, session: AsyncSession = Depends(get_async_session)):
    """Детальный просмотр объявления"""
    query = select(advertisement).where(advertisement.c.id == int(id))
    result = await session.execute(query)
    result = await get_lst_of_dict_advertisement(result.all())
    if result:
        return result[0]
    else:
        return HTTPException(status_code=404, detail="Объект не найден")


@router.delete("/{id}")
async def delete_ad(
    id,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление объявления (либо своего, либо любого если вы админ)"""
    query = select(advertisement).where(advertisement.c.id == int(id))
    ad = await session.execute(query)
    ad = ad.first()
    user_id = ad[8]
    privilege = await get_privilege(session, user)
    if user_id != user.id and privilege == False:
        return HTTPException(status_code=403, detail=f"User don't have rights")
    deleted_ad_id = await del_ad(int(id), session)
    if deleted_ad_id is None:
        return HTTPException(
            status_code=404, detail=f"Advertisement with id {id} not found"
        )
    return DeleteAdvertisementResponse(deleted_ad_id=deleted_ad_id)


@router.post("/{id_adv}/comments")
async def create_comment(
    id_adv: int,
    new_comment: CommentCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """ " Размещение комментария к объявлению"""
    if user.is_active == False:
        return HTTPException(status_code=401, detail=f"Пользователь заблокирован")
    dict_new_comment = new_comment.dict()
    dict_new_comment["id_adv"] = id_adv
    dict_new_comment["id_user"] = user.id
    stmt = insert(comment).values(**dict_new_comment)
    await session.execute(stmt)
    await session.commit()
    return {"status": "201", "details": "Объект создан"}


@router.get("/{id_adv}/comments")
async def get_comments(
    id_adv: int,
    skip: int,
    limit: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Просмотр всех комментариев к объявлению"""
    query = select(comment).where(comment.c.id_adv == id_adv).offset(skip).limit(limit)
    result = await session.execute(query)
    return {"status": 200, "data": await get_lst_of_dict_comment(result.all())}


@router.get("/{id_adv}/complaints")
async def get_comments(
    id_adv: int,
    skip: int,
    limit: int,
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """Просмотр всех жалоб на конкретное объявление"""
    query = (
        select(complaint).where(complaint.c.id_adv == id_adv).offset(skip).limit(limit)
    )
    result = await session.execute(query)
    return {"status": 200, "data": await get_lst_of_dict_complaint(result.all())}


@router.post("/{id_adv}/complaints/new_complaints")
async def add_complaint(
    id_adv: int,
    new_complaint: ComplaintCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Отправка жалобы не объявление"""
    dict_complaint = new_complaint.dict()
    dict_complaint["id_user"] = user.id
    dict_complaint["id_adv"] = id_adv
    stmt = insert(complaint).values(**dict_complaint)
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, "details": "Complaint added"}


@router.delete("{id_adv}/comments/{id_comment}")
async def delete_comment(
    id_comment: int,
    user: User = Depends(get_current_active_admin),
    session: AsyncSession = Depends(get_async_session),
):
    """ " Удаление комментария к объявлению"""
    stmt = delete(comment).where(comment.c.id == id_comment)
    await session.execute(stmt)
    await session.commit()
    return {"status": 200, "details": "Комментарий удалён"}
