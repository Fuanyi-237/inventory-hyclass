from sqlalchemy.orm import Session
from typing import List, Optional

from .base_repository import BaseRepository
from ..models import Category
from ..schemas import CategoryCreate, CategoryUpdate

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    """Repository for category-related database operations."""

    def __init__(self, db: Session):
        super().__init__(Category, db)

    def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Get paginated categories from the database.
        
        Args:
            skip: Number of categories to skip (for pagination)
            limit: Maximum number of categories to return (for pagination)
            
        Returns:
            List of Category objects
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
