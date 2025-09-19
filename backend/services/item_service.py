from typing import List
from sqlalchemy.orm import Session

from .base_service import BaseService
from ..models import Item
from ..schemas import ItemCreate, ItemUpdate, ItemRead, CategoryRead
from ..repositories.item_repository import ItemRepository

class ItemService(BaseService[Item, ItemCreate, ItemUpdate]):
    """Service for item-related operations."""

    def __init__(self, db: Session):
        self.repository = ItemRepository(db)

    def create(self, item: ItemCreate, user_id: int) -> ItemRead:
        """Create a new item."""
        db_obj = self.repository.create(obj_in=item, created_by=user_id)
        return self._convert_to_read_model(db_obj)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ItemRead]:
        """Get all items."""
        db_objs = self.repository.get_all_items(skip=skip, limit=limit)
        return [self._convert_to_read_model(db_obj) for db_obj in db_objs]

    def update(self, item_id: int, item_update: ItemUpdate, user_id: int) -> ItemRead:
        """Update an item."""
        db_obj = self.repository.get(item_id)
        if not db_obj:
            return None
        
        # Add last_modified_by to the update data
        update_data = item_update.model_dump(exclude_unset=True)
        update_data['last_modified_by'] = user_id
        
        updated_obj = self.repository.update(db_obj=db_obj, obj_in=update_data)
        return self._convert_to_read_model(updated_obj)

    def delete(self, item_id: int) -> ItemRead:
        """Delete an item."""
        db_obj = self.repository.remove(id=item_id)
        return self._convert_to_read_model(db_obj)
        
    def _convert_to_read_model(self, db_obj: Item) -> ItemRead:
        """Convert SQLAlchemy model to Pydantic model."""
        # Create a dict with the object's attributes
        item_data = {}
        
        # Copy all columns from the database object
        for c in db_obj.__table__.columns:
            value = getattr(db_obj, c.name)
            # Ensure the state field is a valid ItemState enum value
            if c.name == 'state' and value is not None:
                from ..schemas import ItemState
                try:
                    # Convert string to ItemState enum if needed
                    if isinstance(value, str):
                        value = ItemState(value)
                except ValueError:
                    # If the value is not a valid enum, use the first valid value as default
                    value = ItemState.good
            item_data[c.name] = value
        
        # Handle relationships
        if hasattr(db_obj, 'category') and db_obj.category:
            item_data['category'] = CategoryRead.model_validate(db_obj.category, from_attributes=True)
        
        # Create and return the Pydantic model
        return ItemRead(**item_data)
