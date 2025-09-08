from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict
from typing import Optional, List
from datetime import datetime
from .models import ItemState, TransactionType
from .shared_enums import UserRole

class UserBase(BaseModel):
    username: str
    full_name: Optional[str]
    email: Optional[EmailStr]
    role: UserRole = UserRole.admin
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserRoleUpdate(BaseModel):
    role: UserRole

class UserInDB(UserBase):
    id: int
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    name: str
    description: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(CategoryBase):
    pass


class ItemBase(BaseModel):
    unique_id: str
    name: str
    description: Optional[str]
    category_id: Optional[int] = None
    state: ItemState = ItemState.good
    location: Optional[str] = None
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    category: Optional[CategoryRead] = None

    model_config = ConfigDict(from_attributes=True)

class ItemUpdate(BaseModel):
    unique_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    state: Optional[ItemState] = None
    location: Optional[str] = None
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

class TransactionBase(BaseModel):
    item_id: int
    user_id: int
    action: TransactionType
    timestamp: datetime
    notes: Optional[str]
    state: Optional[ItemState]
    image_url: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    item: "ItemRead"
    user: "UserRead"

    model_config = ConfigDict(from_attributes=True)

class TransactionUpdate(BaseModel):
    item_id: Optional[int] = None
    user_id: Optional[int] = None
    action: Optional[TransactionType] = None
    timestamp: Optional[datetime] = None
    notes: Optional[str] = None
    state: Optional[ItemState] = None

class NotificationBase(BaseModel):
    user_id: int
    message: str
    sent_at: datetime
    read: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
