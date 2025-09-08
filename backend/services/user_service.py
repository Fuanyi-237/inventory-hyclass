from typing import Optional, List
from ..models import User
from ..schemas import UserCreate, UserUpdate, UserInDB, UserRoleUpdate
from ..shared_enums import UserRole
from .base_service import BaseService
from ..repositories.user_repository import UserRepository
from ..password_utils import get_password_hash, verify_password

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for user operations."""
    
    def __init__(self, db):
        self.repository = UserRepository(db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self.repository.get_by_username(username)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.repository.get_by_email(email)
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        return self.repository.authenticate(username, password)
    
    def create(self, user_in: UserCreate) -> User:
        """Create a new user with hashed password."""
        hashed_password = get_password_hash(user_in.password)
        db_user = self.repository.create(user_in, hashed_password)
        return db_user
    
    def update_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Update user's password after verifying current password."""
        user = self.get(user_id)
        if not user or not verify_password(current_password, user.hashed_password):
            return False
        
        hashed_password = get_password_hash(new_password)
        self.repository.update_password(user_id, hashed_password)
        return True
    
    def update_role(self, user_id: int, role: UserRole) -> Optional[User]:
        """Update a user's role."""
        user = self.repository.get(id=user_id)
        if not user:
            return None
        
        user.role = role
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user
    
    def update_user_active(self, user_id: int, is_active: bool) -> Optional[User]:
        """Update user's active status."""
        user = self.get(user_id)
        if not user:
            return None
        
        user.is_active = is_active
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user
    
    def get_active_users(self) -> list[User]:
        """Get all active users."""
        return self.repository.get_active_users()
    
    def is_superuser(self, user: User) -> bool:
        """Check if user is a superuser."""
        return user.role == "superadmin"

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retrieve all users."""
        return self.repository.get_multi(skip=skip, limit=limit)
