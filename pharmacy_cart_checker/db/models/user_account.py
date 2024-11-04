from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pharmacy_cart_checker.db.models import Receipt
from pharmacy_cart_checker.db.models.abstract_account import AbstractAccount
from pharmacy_cart_checker.db.operations import ItemCategory, Problem


class UserAccount(AbstractAccount):
    __tablename__ = "user_account"

    async def user_has_correct_receipt(self, user_id: int, item_id: int, session: AsyncSession):
        receipt_query = select(Receipt).where(Receipt.user_id == user_id, Receipt.item_id == item_id)
        receipt_query_result = (await session.execute(receipt_query)).scalar()
        return receipt_query_result is not None

    async def check_item(self, item_category: ItemCategory, item, session: AsyncSession) -> Problem:
        if item_category == ItemCategory.common:
            return Problem.NO_PROBLEM
        if item_category == ItemCategory.special:
            return Problem.ITEM_IS_SPECIAL
        if await self.user_has_correct_receipt(self.id, item.id, session):
            return Problem.NO_PROBLEM
        return Problem.NO_RECEIPT
