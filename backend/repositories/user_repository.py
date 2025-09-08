import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from ..models import User
from .base_repository import BaseRepository
from ..schemas import UserCreate, UserUpdate
from ..password_utils import verify_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User repository with additional user-specific operations."""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self.get_by_field("username", username)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.get_by_field("email", email)
    
    def get_active_users(self) -> List[User]:
        """Get all active users."""
        return self.db.query(self.model).filter(self.model.is_active == True).all()
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        logger.info(f"Attempting to authenticate user: {username}")
        user = self.get_by_username(username)
        if not user:
            logger.warning(f"Authentication failed: User '{username}' not found.")
            return None
        
        logger.info(f"User '{username}' found. Verifying password.")
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed: Incorrect password for user '{username}'.")
            return None
            
        logger.info(f"Password verification successful for user '{username}'.")
        return user
    
    def create(self, obj_in: UserCreate, hashed_password: str) -> User:
        """Create a new user with hashed password."""
        db_user = User(
            username=obj_in.username,
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=hashed_password,
            role=obj_in.role,
            is_active=obj_in.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_password(self, user_id: int, hashed_password: str) -> Optional[User]:
        """Update user's password."""
        user = self.get(user_id)
        if not user:
            return None
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user
