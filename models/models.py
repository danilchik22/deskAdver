from sqlalchemy import (
    TEXT,
    Boolean,
    MetaData,
    UUID,
    Column,
    URL,
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

categories = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("parent_id", Integer, default=0),
)

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)
users = Table(
    "user",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

cities = Table(
    "city",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

types_adv = Table(
    "type_adv",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

photos = Table(
    "photo",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("url", URL, nullable=False),
)

advertisements = Table(
    "advertisement",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("text", TEXT),
    Column("date", TIMESTAMP, default=datetime.utcnow),
    Column("confirm", Integer, default=0),
    Column("time_over", TIMESTAMP, default=datetime.utcnow + timedelta(days=30)),
    Column("is_actual", Boolean, default=True),
    Column("price", Integer),
    Column("id_user", UUID, ForeignKey=("users.id")),
    Column("id_category", Integer, ForeignKey=("categories.id")),
    Column("id_type_adv", Integer, ForeignKey=("types_adv.id")),
    Column("id_city", Integer, ForeignKey=("cities.id")),
    Column("id_photo", BigInteger, ForeignKey=("photos.id")),
)

comments = Table(
    "comments",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("id_adv", Integer, ForeignKey=("advertisements.id")),
    Column("id_user", UUID, ForeignKey=("users.id")),
    Column("text", Text, nullable=False),
)

complaints = Table(
    "comlaint",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("id_adv", Integer, ForeignKey=("advertisements.id")),
    Column("id_user", UUID, ForeignKey=("users.id")),
    Column("text", Text),
    Column("status", Integer, default=0),
)
