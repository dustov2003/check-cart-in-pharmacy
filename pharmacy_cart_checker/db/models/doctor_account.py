from sqlalchemy import Column, ForeignKey, select
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from pharmacy_cart_checker.db.models.abstract_account import AbstractAccount
from pharmacy_cart_checker.db.operations import ItemCategory, Problem


class DoctorAccount(AbstractAccount):
    __tablename__ = "doctor_account"
    specialty_id = Column(INTEGER, ForeignKey("specialty.id"), nullable=False)
    specialty = relationship("Specialty")

    async def doctor_has_correct_specialty(self, user_id: int, specialty_id: int, session: AsyncSession):
        doctor_special_query = select(DoctorAccount).where(
            DoctorAccount.specialty_id == specialty_id, DoctorAccount.id == user_id
        )
        result_doctor_special_query = (await session.execute(doctor_special_query)).scalar()
        return result_doctor_special_query is not None

    async def check_item(self, item_category: ItemCategory, item, session: AsyncSession) -> Problem:
        if item_category == ItemCategory.special and not await self.doctor_has_correct_specialty(
            self.id, item.specialty_id, session
        ):
            return Problem.ITEM_SPECIAL_WRONG_SPECIFIC
        return Problem.NO_PROBLEM
