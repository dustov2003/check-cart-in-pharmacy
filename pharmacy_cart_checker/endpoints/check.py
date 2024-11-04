from typing import List

from fastapi import APIRouter, Depends

from pharmacy_cart_checker.db.connection import SessionManager
from pharmacy_cart_checker.db.operations import ItemCategory, Problem
from pharmacy_cart_checker.db.operations.finding_user_and_item import (
    find_user,
    is_valid_item_category,
    is_valid_item_id,
    item_category_to_category_table,
)
from pharmacy_cart_checker.schemas.check import CheckRequest, CheckResponse, ProblemItem, get_check_request


api_router = APIRouter(tags=["Check"])


async def check_item_for_all_problems(user_id: int, item_category_and_id: str) -> Problem:
    item_category, item_id = item_category_and_id.split("_")
    if not is_valid_item_category(item_category):
        return Problem.WRONG_CATEGORY
    if not is_valid_item_id(item_id):
        return Problem.INCORRECT_ITEM_ID
    item_category, item_id = ItemCategory(item_category), int(item_id)
    session_maker = SessionManager().get_session_maker()
    item_table = item_category_to_category_table(item_category)
    async with session_maker() as session:
        found_item = await item_table.find_item_by_id(item_id, session)
        if found_item is None:
            return Problem.ITEM_NOT_FOUND
        found_user = await find_user(user_id, session)
        if found_user is None:
            return item_category.get_problem_if_user_not_found()
        return await found_user.check_item(item_category, found_item, session)


async def set_problem_to_items(carts_item: CheckRequest) -> List[ProblemItem]:
    item_with_problems = []
    for item in carts_item.item_id:
        lower_item = item.lower()
        problem = await check_item_for_all_problems(carts_item.user_id, lower_item)
        if problem is not Problem.NO_PROBLEM:
            problem_item = ProblemItem(item_id=lower_item, problem=problem)
            item_with_problems.append(problem_item)

    return item_with_problems


@api_router.get("/check", response_model=CheckResponse)
async def check(model: CheckRequest = Depends(get_check_request)):
    item_with_problems = await set_problem_to_items(model)
    return CheckResponse(root=item_with_problems)
