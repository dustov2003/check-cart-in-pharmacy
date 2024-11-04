from enum import Enum

from pharmacy_cart_checker.db.models import DoctorAccount, UserAccount


class UserTables(Enum):
    user_account = UserAccount
    doctor_account = DoctorAccount
