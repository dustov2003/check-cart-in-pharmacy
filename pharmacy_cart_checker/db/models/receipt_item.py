from pharmacy_cart_checker.db.models.abstract_item import AbstractItem


class ReceiptItem(AbstractItem):
    __tablename__ = "receipt_item"
