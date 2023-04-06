from datetime import datetime
from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import Integer, and_, update
from src.advertisement.models import advertisement
from src.database import get_async_session


class PhotoCreate(BaseModel):
    id: int
    url: str


class CategoryCreate(BaseModel):
    id: int
    name: str
    parent_id: int


class CityCreate(BaseModel):
    id: int
    name: str


class TypeAdvCreate(BaseModel):
    id: int
    name: str


class AdvertisementCreate(BaseModel):
    id: int
    title: str
    text: str
    confirm: int
    is_actual: bool
    photo_id: Union[int, None]
    user_id: UUID
    category_id: int
    type_adv_id: int
    city_id: int
    price: int


class AdvertisementRead(BaseModel):
    id: int
    title: str
    text: str
    date: datetime
    confirm: int
    time_over: datetime
    is_actual: bool
    photo_id: Union[int, None]
    user_id: UUID
    category_id: int
    type_adv_id: int
    city_id: int
    price: int


class CommentCreate(BaseModel):
    id: int
    id_adv: int
    text: str
    date: datetime


class CommentRead(BaseModel):
    id: int
    id_adv: int
    id_user: int
    text: str
    date: datetime


class ComplaintCreate(BaseModel):
    id: int
    text: str
    status: int
    id_adv: int
    id_user: UUID
    date: datetime


async def del_ad(
    ad_id: Integer, session: AsyncSession = Depends(get_async_session)
) -> Union[Integer, None]:
    query = (
        update(advertisement)
        .where(and_(advertisement.c.id == ad_id, advertisement.c.is_actual == True))
        .values(is_actual=False)
        .returning(advertisement.c.id)
    )
    res = await session.execute(query)
    await session.commit()
    deleted_ad_row = res.fetchone()
    if deleted_ad_row is not None:
        return deleted_ad_row[0]
