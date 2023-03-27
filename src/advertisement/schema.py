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
    id_user: int
    text: str


class ComplaintCreate(BaseModel):
    id: int
    id_adv: int
    id_user: int
    text: str
    status: int


async def del_ad(ad_id: Integer, session: AsyncSession = Depends(get_async_session)) -> Union[Integer, None]:
    query = update(advertisement).\
        where(and_(advertisement.c.id == ad_id, advertisement.c.is_actual == True)).\
        values(is_actual=False).\
        returning(advertisement.c.id)
    res = await session.execute(query)
    await session.commit()
    deleted_ad_row = res.fetchone()
    if deleted_ad_row is not None:
        return deleted_ad_row[0]


def get_lst_of_dict_advertisement(lst):
    lst_result_all = []
    for i in lst:
        lst_result_all.append(
            {
                "id": i[0],
                "title": i[1],
                "text": i[2],
                "date": i[3],
                "confirm": i[4],
                "time_over": i[5],
                "is_actual": i[6],
                "photo_id": i[7],
                "user_id": i[8],
                "category_id": i[9],
                "type_adv_id": i[10],
                "city_id": i[11],
                "price": i[12],
            }
        )
    return lst_result_all
