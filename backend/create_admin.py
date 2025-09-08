from sqlalchemy.orm import Session
import crud
import schemas
from password_utils import get_password_hash

def create_superadmin_logic(db: Session, username: str, email: str, full_name: str, password: str):
    """Core logic to create a superadmin user."""
    if crud.get_user_by_username(db, username=username):
        raise ValueError(f"User with username '{username}' already exists.")

    user_in = schemas.UserCreate(
        username=username,
        email=email,
        full_name=full_name,
        password=password,
        role="superadmin",
        is_active=True
    )

    hashed_password = get_password_hash(user_in.password)
    db_user = crud.create_user(db=db, user=user_in, hashed_password=hashed_password)
    return db_user
