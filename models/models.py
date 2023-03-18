from sqlalchemy import (
    TEXT,
    Boolean,
    MetaData,
    UUID,
    Column,
    Table,
    BigInteger,
    Integer,
    JSON,
    String,
    TIMESTAMP,
    ForeignKey,
    Text,
)
from datetime import datetime, timedelta

metadata = MetaData()


def time_over():
    return datetime.utcnow + timedelta(days=30)


role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)
user = Table(
    "user",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

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
    Column("parent_id", Integer, default=0),
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
    Column("date", TIMESTAMP, default=datetime.utcnow),
    Column("confirm", Integer, default=0),
    Column("time_over", TIMESTAMP, default=time_over),
    Column("is_actual", Boolean, default=True),
    Column("photo", Integer, ForeignKey(photo.c.id)),
    Column("user", UUID, ForeignKey(user.c.id)),
    Column("category", Integer, ForeignKey(category.c.id)),
    Column("type_adv", Integer, ForeignKey(type_adv.c.id)),
    Column("city", Integer, ForeignKey(city.c.id)),
    Column("price", Integer),
)

comment = Table(
    "comment",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("id_adv", Integer, ForeignKey(advertisement.c.id)),
    Column("id_user", UUID, ForeignKey(user.c.id)),
    Column("text", Text, nullable=False),
)

complaint = Table(
    "complaint",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("id_adv", Integer, ForeignKey(advertisement.c.id)),
    Column("id_user", UUID, ForeignKey(user.c.id)),
    Column("text", Text),
    Column("status", Integer, default=0),
)
