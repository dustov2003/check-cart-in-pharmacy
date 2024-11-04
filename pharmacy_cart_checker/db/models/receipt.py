from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.orm import relationship

from pharmacy_cart_checker.db import DeclarativeBase


class Receipt(DeclarativeBase):
    __tablename__ = "receipt"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(INTEGER, ForeignKey("user_account.id"), nullable=False)
    item_id = Column(INTEGER, ForeignKey("receipt_item.id"), nullable=False)

    user = relationship("UserAccount")
    item = relationship("ReceiptItem")

    __table_args__ = (UniqueConstraint("user_id", "item_id", name="_user_item_uc"),)
