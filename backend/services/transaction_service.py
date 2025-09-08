from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .base_service import BaseService
from ..models import Transaction, Item
from ..schemas import TransactionCreate, TransactionUpdate
from ..repositories.transaction_repository import TransactionRepository

class TransactionService(BaseService[Transaction, TransactionCreate, TransactionUpdate]):
    """Service for transaction-related operations."""

    def __init__(self, db: Session):
        self.repository = TransactionRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Transaction]:
        """Get all transactions."""
        return self.repository.get_multi(skip=skip, limit=limit)

    def get_by_date_range(self, start: datetime, end: datetime) -> List[Transaction]:
        """Get transactions within an inclusive datetime range."""
        return self.repository.get_by_date_range(start, end)

    def create(self, transaction_in: TransactionCreate) -> Transaction:
        """Create a new transaction and update the item's state."""
        # Create the transaction
        transaction = self.repository.create(obj_in=transaction_in)

        # If the transaction includes a state update, apply it to the item
        if transaction_in.state:
            item = self.repository.db.query(Item).filter(Item.id == transaction_in.item_id).first()
            if item:
                item.state = transaction_in.state
                self.repository.db.add(item)
                self.repository.db.commit()
                self.repository.db.refresh(item)

        return transaction
