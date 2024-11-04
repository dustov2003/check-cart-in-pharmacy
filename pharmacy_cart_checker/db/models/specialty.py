from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TEXT

from pharmacy_cart_checker.db import DeclarativeBase


class Specialty(DeclarativeBase):
    __tablename__ = "specialty"

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(TEXT, nullable=False, unique=True)
