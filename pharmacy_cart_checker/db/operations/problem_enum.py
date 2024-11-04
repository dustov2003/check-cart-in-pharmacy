from enum import Enum


class Problem(Enum):
    WRONG_CATEGORY = "WRONG_CATEGORY"
    INCORRECT_ITEM_ID = "INCORRECT_ITEM_ID"
    ITEM_NOT_FOUND = "ITEM_NOT_FOUND"
    NO_USER = "NO_USER"
    NO_USER_NO_RECEIPT = "NO_USER_NO_RECEIPT"
    NO_USER_SPECIAL_ITEM = "NO_USER_SPECIAL_ITEM"
    NO_RECEIPT = "NO_RECEIPT"
    ITEM_IS_SPECIAL = "ITEM_IS_SPECIAL"
    ITEM_SPECIAL_WRONG_SPECIFIC = "ITEM_SPECIAL_WRONG_SPECIFIC"
    NO_PROBLEM = None
