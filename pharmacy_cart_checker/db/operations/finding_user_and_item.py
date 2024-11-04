from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import ItemCategory
from .user_table_enum import UserTables
from pharmacy_cart_checker.db.models import CommonItem, Receipt, ReceiptItem, SpecialItem
from pharmacy_cart_checker.db.models.abstract_item import AbstractItem


def is_valid_item_category(item_category: str) -> bool:
    return item_category in ItemCategory


def is_valid_item_id(item_id: str) -> bool:
    return item_id.isdigit() and int(item_id) > 0


def item_category_to_category_table(item_category: ItemCategory) -> AbstractItem:
    if item_category is ItemCategory.common:
        return CommonItem()
    if item_category is ItemCategory.special:
        return SpecialItem()
    return ReceiptItem()


async def find_user(user_id: int, session: AsyncSession) -> Any | None:
    for user_table in UserTables:
        user_query = select(user_table.value).where(user_table.value.id == user_id)
        user_query_result = (await session.execute(user_query)).scalar()
        if user_query_result is not None:
            return user_query_result
    return None


async def user_has_correct_receipt(user_id: int, item_id: int, session: AsyncSession):
    receipt_query = select(Receipt).where(Receipt.user_id == user_id, Receipt.item_id == item_id)
    receipt_query_result = (await session.execute(receipt_query)).scalar()
    return receipt_query_result is not None
