from typing import Generator, Optional
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import SessionLocal
from .repositories.user_repository import UserRepository
from .services.user_service import UserService
from .schemas import UserInDB

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Read secrets from environment for production, with a safe fallback for dev
SECRET_KEY = os.getenv("INVENTORY_SECRET_KEY", os.getenv("SECRET_KEY", "your-secret-key-here"))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db() -> Generator:
    """Dependency that provides DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserInDB:
    """Dependency to get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user)
) -> UserInDB:
    """Dependency to get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency that provides UserRepository."""
    return UserRepository(db)

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    """Dependency that provides UserService."""
    return UserService(user_repo)

# Add more repository and service dependencies here as needed

class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self._db = SessionLocal()
        self._repositories = {}
        self._services = {}
    
    @property
    def db(self) -> Session:
        return self._db
    
    def get_repository(self, repo_type):
        """Get a repository instance."""
        if repo_type not in self._repositories:
            if repo_type == "user":
                self._repositories[repo_type] = UserRepository(self._db)
            # Add more repository types here
        return self._repositories.get(repo_type)
    
    def get_service(self, service_type):
        """Get a service instance."""
        if service_type not in self._services:
            if service_type == "user":
                repo = self.get_repository("user")
                self._services[service_type] = UserService(repo)
            # Add more service types here
        return self._services.get(service_type)
    
    def close(self):
        """Close the database connection."""
        self._db.close()

# Global container instance
container = Container()

def get_container() -> Container:
    """Dependency that provides the DI container."""
    return container
