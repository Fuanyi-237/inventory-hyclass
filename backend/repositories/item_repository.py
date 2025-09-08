from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from .base_repository import BaseRepository
from ..models import Item
from ..schemas import ItemCreate, ItemUpdate

class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):
    """Repository for item-related database operations."""

    def __init__(self, db: Session):
        super().__init__(Item, db)

    def get_all_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get paginated items from the database, eagerly loading categories.
        
        Args:
            skip: Number of items to skip (for pagination)
            limit: Maximum number of items to return (for pagination)
            
        Returns:
            List of Item objects with their categories loaded
        """
        return (
            self.db.query(self.model)
            .options(joinedload(Item.category))
            .offset(skip)
            .limit(limit)
            .all()
        )
