from datetime import datetime
from typing import Union
from uuid import UUID
from pydantic import BaseModel


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
