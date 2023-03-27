from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.advertisement.schema import AdvertisementCreate, AdvertisementRead
from src.auth.models import User
from src.auth.schemas import UserRead
from src.database import get_async_session
from .models import DeleteAdvertisementResponse, advertisement
from fastapi.encoders import jsonable_encoder
from .models import category
from .schema import del_ad, get_lst_of_dict_advertisement
from src.auth.base_config import current_user


router = APIRouter(prefix="/advertisements", tags=["Advertisements"])

def get_paginator(limit: int = 20, skip: int = 0):
    return {"limit": limit, "skip": skip}


@router.get("/")
async def get_ad(pg: dict = Depends(get_paginator), session: AsyncSession = Depends(get_async_session)):
    query = select(advertisement).where(advertisement.c.confirm == 1
                           and advertisement.c.is_actual == True).offset(pg["skip"]).limit(pg["limit"])
    result = await session.execute(query)
    return {
        "status": 200,
        "data": get_lst_of_dict_advertisement(result.all())
    }


@router.post("/addadver")
async def add_ad(
    new_ad: AdvertisementCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    stmt = insert(advertisement).values(**new_ad.dict())
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "201",
        "details": 'Объект создан'
            }


@router.get("/{id}")
async def detail(id, session: AsyncSession = Depends(get_async_session)):
    query = select(advertisement).where(advertisement.c.id == int(id))
    result = await session.execute(query)
    result = get_lst_of_dict_advertisement(result.all())
    if result:
        return result[0]
    else:
        return {
                "status": "404",
                "data": None,
                "details": "Объект не найден"
                }

@router.delete("/{id}", response_model=DeleteAdvertisementResponse)
async def delete_ad(id, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    print(user.id)
    query = select(advertisement).where(advertisement.c.id == int(id))
    ad = await session.execute(query).fetchall()
    ad_id = ad.getInt(ad.getColumnIndex(points))
    if ad.user_id != user.id:
        return HTTPException(status_code=403, detail=f"User don't have rights")
    deleted_ad_id = await del_ad(int(id), session)
    if deleted_ad_id is None:
        return HTTPException(status_code=404, detail=f"Advertisement with id {id} not found")
    return DeleteAdvertisementResponse(deleted_ad_id=deleted_ad_id)
