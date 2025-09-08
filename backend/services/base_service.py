from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from ..repositories.base_repository import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base service class with common business logic operations."""
    
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository
    
    def get(self, id: Any) -> Optional[ModelType]:
        """Get a single item by ID."""
        return self.repository.get(id)
    
    def get_multi(
        self, *, skip: int = 0, limit: int = 100, **filters
    ) -> List[ModelType]:
        """Get multiple items with optional filtering and pagination."""
        return self.repository.get_multi(skip=skip, limit=limit, **filters)
    
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new item."""
        return self.repository.create(obj_in)
    
    def update(
        self, *, id: int, obj_in: UpdateSchemaType
    ) -> Optional[ModelType]:
        """Update an existing item."""
        db_obj = self.repository.get(id)
        if not db_obj:
            return None
        return self.repository.update(db_obj=db_obj, obj_in=obj_in)
    
    def remove(self, *, id: int) -> Optional[ModelType]:
        """Remove an item."""
        return self.repository.remove(id=id)
    
    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get an item by a specific field."""
        return self.repository.get_by_field(field, value)
