from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.dependencies import get_db, get_current_user
from backend.services.item_service import ItemService
from backend.schemas import ItemRead, ItemCreate
from backend.models import User
from backend.shared_enums import UserRole

router = APIRouter(tags=["items"])

@router.get("/", response_model=List[ItemRead])
def read_items(db: Session = Depends(get_db)):
    """Retrieve all items."""
    item_service = ItemService(db)
    return item_service.get_all()

@router.post("/", response_model=ItemRead)
def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create an item."""
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and superadmins can create items."
        )
    item_service = ItemService(db)
    return item_service.create(item=item, user_id=current_user.id)

@router.delete("/{item_id}", response_model=ItemRead)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete an item."""
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and superadmins can delete items."
        )
    item_service = ItemService(db)
    deleted_item = item_service.delete(item_id=item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
