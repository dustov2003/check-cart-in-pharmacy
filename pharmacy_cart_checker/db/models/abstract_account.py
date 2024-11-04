from abc import abstractmethod

from sqlalchemy import INTEGER, TEXT, Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import AbstractConcreteBase

from pharmacy_cart_checker.db import DeclarativeBase
from pharmacy_cart_checker.db.operations import ItemCategory


class AbstractAccount(DeclarativeBase, AbstractConcreteBase):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    full_name = Column(TEXT, nullable=False)
    phone = Column(TEXT, unique=True, nullable=False)
    password_hash = Column(TEXT, nullable=False)

    @abstractmethod
    async def check_item(self, item_category: ItemCategory, item, session: AsyncSession):
        pass
