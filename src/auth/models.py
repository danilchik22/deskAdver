from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
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

from datetime import datetime

from src.database import Base

from src.database import metadata


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
    Column("registered_at", TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column("role_id", Integer, ForeignKey(role.c.id), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    id = Column(UUID, primary_key=True, index=True, unique=True)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id), nullable=False)
    email: str = Column(String(length=320), unique=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
