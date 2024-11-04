from sqlalchemy import INTEGER, NUMERIC, TEXT, Column, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import AbstractConcreteBase

from pharmacy_cart_checker.db import DeclarativeBase


class AbstractItem(DeclarativeBase, AbstractConcreteBase):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)
    amount = Column(INTEGER, nullable=False)
    price = Column(NUMERIC(8, 2), nullable=False)
    dosage_form = Column(TEXT, nullable=False)
    manufacturer = Column(TEXT, nullable=False)
    barcode = Column(TEXT, unique=True, nullable=False)

    async def find_item_by_id(self, item_id: int, session: AsyncSession):
        item_query = select(self.__class__).where(self.__class__.id == item_id)
        item_query_result = (await session.execute(item_query)).scalar()
        return item_query_result
