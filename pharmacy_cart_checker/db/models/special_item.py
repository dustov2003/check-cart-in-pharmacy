from sqlalchemy import INTEGER, Column, ForeignKey
from sqlalchemy.orm import relationship

from .abstract_item import AbstractItem


class SpecialItem(AbstractItem):
    __tablename__ = "special_item"
    specialty_id = Column(INTEGER, ForeignKey("specialty.id"), nullable=False)

    specialty = relationship("Specialty")
