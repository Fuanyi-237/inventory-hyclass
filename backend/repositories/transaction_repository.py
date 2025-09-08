from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .base_repository import BaseRepository
from ..models import Transaction
from ..schemas import TransactionCreate, TransactionUpdate

class TransactionRepository(BaseRepository[Transaction, TransactionCreate, TransactionUpdate]):
    """Repository for transaction-related database operations."""

    def __init__(self, db: Session):
        super().__init__(Transaction, db)

    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions from the database."""
        return self.db.query(self.model).all()

    def get_by_date_range(self, start: datetime, end: datetime) -> List[Transaction]:
        """Get transactions within an inclusive datetime range."""
        return (
            self.db.query(self.model)
            .filter(self.model.timestamp >= start)
            .filter(self.model.timestamp <= end)
            .all()
        )
