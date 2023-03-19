from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.advertisement.schema import AdvertisementCreate, AdvertisementRead
from src.auth.schemas import UserRead
from src.database import get_async_session
from .models import advertisement
from fastapi.encoders import jsonable_encoder
from .models import category
from .schema import get_lst_of_dict_advertisement


router = APIRouter(prefix="/advertisements", tags=["Advertisements"])


@router.get("/getalladver")
async def get_ad(page: int, session: AsyncSession = Depends(get_async_session)):
    if page < 0:
        return {"status": "error", "data": "null", "details": "Page cannot less then 1"}
    query = select(advertisement).offset(page * 20)
    result = await session.execute(query)
    return get_lst_of_dict_advertisement(result.all())


@router.post("/addadver")
async def add_ad(
    new_ad: AdvertisementCreate, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(advertisement).values(**new_ad.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
