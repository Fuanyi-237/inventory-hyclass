from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.dependencies import get_db, get_current_user
from backend import models, schemas
from backend.shared_enums import UserRole
from backend.services.category_service import CategoryService

router = APIRouter(tags=["categories"])

@router.post("/", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new category.
    """
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and superadmins can create categories."
        )
    category_service = CategoryService(db)
    return category_service.create(category, creator_id=current_user.id)

@router.get("/", response_model=List[schemas.CategoryRead])
def list_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all categories with pagination.
    """
    category_service = CategoryService(db)
    return category_service.get_all(skip=skip, limit=limit)

@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get a specific category by ID.
    """
    category_service = CategoryService(db)
    category = category_service.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )
    return category

@router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    category_in: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update a category.
    """
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and superadmins can update categories."
        )
    category_service = CategoryService(db)
    category = category_service.repository.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )
    return category_service.repository.update(db_obj=category, obj_in=category_in)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a category.
    """
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and superadmins can delete categories."
        )
    category_service = CategoryService(db)
    category = category_service.repository.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found"
        )
    category_service.repository.remove(id=category_id)
    return None
