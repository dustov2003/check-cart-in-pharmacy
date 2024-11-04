import pytest

from pharmacy_cart_checker.db.connection import SessionManager
from pharmacy_cart_checker.db.models import CommonItem, ReceiptItem, SpecialItem
from pharmacy_cart_checker.db.operations import ItemCategory, Problem
from pharmacy_cart_checker.db.operations.finding_user_and_item import (
    find_user,
    is_valid_item_category,
    is_valid_item_id,
    item_category_to_category_table,
)
from pharmacy_cart_checker.endpoints.check import check_item_for_all_problems


def test_is_valid_item_category():
    assert is_valid_item_category(ItemCategory.common) == True
    assert is_valid_item_category(ItemCategory.special) == True
    assert is_valid_item_category("invalid_category") == False


def test_is_valid_item_id():
    assert is_valid_item_id("123") == True
    assert is_valid_item_id("-123") == False
    assert is_valid_item_id("abc") == False
    assert is_valid_item_id("0") == False


def test_item_category_to_category_table():
    assert isinstance(item_category_to_category_table(ItemCategory.common), CommonItem)
    assert isinstance(item_category_to_category_table(ItemCategory.special), SpecialItem)
    assert isinstance(item_category_to_category_table(ItemCategory.receipt), ReceiptItem)


@pytest.mark.asyncio
async def test_find_user_found():
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        user = await find_user(101, session)
        assert user == None
        user = await find_user(61, session)
        assert user.id == 61
        user = await find_user(22, session)
        assert user.id == 22


@pytest.mark.asyncio
async def test_check_item_for_all_problems():
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        assert await check_item_for_all_problems(61, "receipt_2") == Problem.NO_PROBLEM
        assert await check_item_for_all_problems(2, "special_2") == Problem.ITEM_IS_SPECIAL
        assert await check_item_for_all_problems(2, "common_2") == Problem.NO_PROBLEM
        # assert user.id == 22


if __name__ == "__main__":
    pytest.main()
