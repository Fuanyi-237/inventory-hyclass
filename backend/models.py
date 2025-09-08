from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
import enum
from sqlalchemy.orm import relationship
from backend.base import Base
from .shared_enums import UserRole

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.admin, nullable=False)
    is_active = Column(Boolean, default=True)
    

    actions = relationship("Transaction", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

    items = relationship("Item", back_populates="category")

class ItemState(enum.Enum):
    good = "good"
    moderate = "moderate"
    bad = "bad"

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    category = relationship("Category", back_populates="items")
    state = Column(Enum(ItemState), default=ItemState.good, nullable=False)
    location = Column(String)
    purchase_date = Column(DateTime)
    expiry_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id"))

    transactions = relationship("Transaction", back_populates="item", cascade="all, delete-orphan")

class TransactionType(enum.Enum):
    sign_in = "sign_in"
    sign_out = "sign_out"
    add = "add"
    edit = "edit"
    state_change = "state_change"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime)
    notes = Column(String)
    state = Column(Enum(ItemState))
    image_url = Column(String, nullable=True)

    item = relationship("Item", back_populates="transactions")
    user = relationship("User", back_populates="actions")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    sent_at = Column(DateTime)
    read = Column(Boolean, default=False)
