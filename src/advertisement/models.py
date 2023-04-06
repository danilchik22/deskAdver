from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import (
    TEXT,
    Boolean,
    MetaData,
    UUID,
    Column,
    Table,
    BigInteger,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Text,
)

from src.auth.models import User
from src.advertisement.utils import time_over

from src.database import metadata

photo = Table(
    "photo",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String, nullable=False),
)

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("parent_id", Integer, default=0, nullable=False),
)

city = Table(
    "city",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

type_adv = Table(
    "type_adv",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

advertisement = Table(
    "advertisement",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("text", TEXT),
    Column("date", TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column("confirm", Integer, default=0, nullable=False),
    Column("time_over", TIMESTAMP, default=time_over, nullable=False),
    Column("is_actual", Boolean, default=True, nullable=False),
    Column("photo_id", Integer, ForeignKey(photo.c.id)),
    Column("user_id", UUID, ForeignKey(User.id), nullable=False),
    Column("category_id", Integer, ForeignKey(category.c.id), nullable=False),
    Column("type_adv_id", Integer, ForeignKey(type_adv.c.id), nullable=False),
    Column("city_id", Integer, ForeignKey(city.c.id), nullable=False),
    Column("price", Integer),
)


class DeleteAdvertisementResponse(BaseModel):
    deleted_ad_id: int


comment = Table(
    "comment",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("id_adv", Integer, ForeignKey(advertisement.c.id), nullable=False),
    Column("id_user", UUID, ForeignKey(User.id), nullable=False),
    Column("text", Text, nullable=False),
    Column("date", TIMESTAMP, default=datetime.utcnow, nullable=False),
)

complaint = Table(
    "complaint",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("id_adv", Integer, ForeignKey(advertisement.c.id), nullable=False),
    Column("id_user", UUID, ForeignKey(User.id), nullable=False),
    Column("text", Text),
    Column("status", Integer, default=0, nullable=False),
    Column("date", TIMESTAMP, default=datetime.utcnow, nullable=False),
)
