from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List

from .base_service import BaseService
from ..models import Category
from ..schemas import CategoryCreate, CategoryRead, CategoryUpdate
from ..repositories.category_repository import CategoryRepository

class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate]):
    """Service for category-related operations."""

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create(self, obj_in: CategoryCreate, creator_id: int) -> CategoryRead:
        """Create a new category.
        
        Stores the user who created the category in the `created_by` column and
        returns a serialized `CategoryRead`.
        
        If a category with the same name already exists, returns 409 Conflict.
        """
        try:
            db_obj = self.repository.create(obj_in, created_by=creator_id)
        except IntegrityError:
            # Likely UNIQUE constraint on name; ensure session is rolled back
            self.repository.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with name '{obj_in.name}' already exists",
            )
        return CategoryRead.model_validate(db_obj, from_attributes=True)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CategoryRead]:
        """Get all categories with pagination.
        
        Args:
            skip: Number of categories to skip (for pagination)
            limit: Maximum number of categories to return (for pagination)
            
        Returns:
            List of CategoryRead objects
        """
        db_objs = self.repository.get_all_categories(skip=skip, limit=limit)
        return [CategoryRead.model_validate(db_obj, from_attributes=True) for db_obj in db_objs] if db_objs else []
