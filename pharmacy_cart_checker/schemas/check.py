from typing import List

from fastapi import Query
from pydantic import BaseModel, RootModel

from pharmacy_cart_checker.db.operations import Problem


class CheckRequest(BaseModel):
    user_id: int
    item_id: List[str] = Query(...)


def get_check_request(user_id: int = Query(...), item_id: List[str] = Query(...)) -> CheckRequest:
    return CheckRequest(user_id=user_id, item_id=item_id)


class ProblemItem(BaseModel):
    item_id: str
    problem: Problem


class CheckResponse(RootModel):
    root: List[ProblemItem]
