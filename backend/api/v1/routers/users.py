from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend import schemas, models
from backend.services.user_service import UserService
from backend.dependencies import get_db, get_current_user
from backend.shared_enums import UserRole


router = APIRouter()


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    # This endpoint is public for now, but in a real app, you'd want protection
    # current_user: models.User = Depends(get_current_user) 
): 
    """
    Create a new user.
    """
    user_service = UserService(db)
    user = user_service.get_by_username(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return user_service.create(user_in=user_in)

@router.get("/", response_model=List[schemas.UserRead])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all users. Only accessible by superadmins.
    """
    if current_user.role != UserRole.superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    user_service = UserService(db)
    users = user_service.get_all_users(skip=skip, limit=limit)
    return users


@router.put("/{user_id}/role", response_model=schemas.UserRead)
def update_user_role(
    user_id: int,
    user_role_update: schemas.UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update a user's role. Only accessible by superadmins.
    """
    if current_user.role != UserRole.superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )

    user_service = UserService(db)
    user = user_service.update_role(user_id=user_id, role=user_role_update.role)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )

    return user
