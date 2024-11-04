from enum import Enum

from .problem_enum import Problem


class ItemCategory(Enum):
    common = "common"
    special = "special"
    receipt = "receipt"

    def get_problem_if_user_not_found(self) -> Problem:
        if self == ItemCategory.special:
            return Problem.NO_USER_SPECIAL_ITEM
        if self == ItemCategory.receipt:
            return Problem.NO_USER_NO_RECEIPT
        return Problem.NO_USER
