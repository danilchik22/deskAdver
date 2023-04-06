from datetime import datetime, timedelta
from sqlalchemy import insert, select
from src.auth.models import User


def time_over():
    return datetime.utcnow() + timedelta(days=30)


async def get_lst_of_dict_advertisement(lst):
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


async def get_lst_of_dict_comment(lst):
    lst_result_all = []
    for i in lst:
        lst_result_all.append(
            {
                "id": i[0],
                "id_adv": i[1],
                "id_user": i[2],
                "text": i[3],
                "date": i[4],
            }
        )
    return lst_result_all


async def get_lst_of_dict_users(lst):
    lst_result_all = []
    print(lst)
    for i in lst:
        lst_result_all.append(
            {
                "id": i[0].id,
                "username": i[0].username,
                "registered_at": i[0].registered_at,
                "role_id": i[0].role_id,
                "is_active": i[0].is_active,
                "is_superuser": i[0].is_superuser,
                "is_verified": i[0].is_verified,
            }
        )
    return lst_result_all


async def get_lst_of_dict_complaint(lst):
    lst_result_all = []
    for i in lst:
        lst_result_all.append(
            {
                "id": i[0],
                "id_adv": i[1],
                "id_user": i[2],
                "text": i[3],
                "status": i[4],
                "date": i[4],
            }
        )
    return lst_result_all


async def get_privilege(session, current_user):
    query = select(User).where(User.id == current_user.id)
    result = await session.execute(query)
    result_all = result.all()
    user = result_all[0][0]
    if user.role_id == 2:
        return True
    else:
        return False
