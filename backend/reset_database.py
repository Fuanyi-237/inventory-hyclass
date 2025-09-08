import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

# Define enums
class TransactionType(enum.Enum):
    sign_in = "sign_in"
    sign_out = "sign_out"
    return_item = "return_item"

class ItemState(enum.Enum):
    good = "good"
    damaged = "damaged"
    lost = "lost"

# Create a new database
DB_URL = 'sqlite:///inventory_updated.db'
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Integer, default=1)
    is_superuser = Column(Integer, default=0)
    actions = relationship("Transaction", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    state = Column(Enum(ItemState), default=ItemState.good)
    location = Column(String, nullable=True)
    transactions = relationship("Transaction", back_populates="item")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime)
    notes = Column(String, nullable=True)
    state = Column(Enum(ItemState), nullable=True)
    image_url = Column(String, nullable=True)  # This is the column we need
    
    item = relationship("Item", back_populates="transactions")
    user = relationship("User", back_populates="actions")

# Drop all existing tables and recreate them with the correct schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database has been reset with the updated schema.")
print("Please update your application to use 'inventory_updated.db' as the database.")
