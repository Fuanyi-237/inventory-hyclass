import json
import sqlite3
from pathlib import Path
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

def create_database():
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
        image_url = Column(String, nullable=True)
        
        item = relationship("Item", back_populates="transactions")
        user = relationship("User", back_populates="actions")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    return engine, SessionLocal, {
        'User': User,
        'Category': Category,
        'Item': Item,
        'Transaction': Transaction
    }

def import_data(session, models, data):
    # Import data in the correct order to respect foreign key constraints
    model_order = ['Category', 'User', 'Item', 'Transaction']
    
    for model_name in model_order:
        if model_name in data and model_name in models:
            print(f"Importing {len(data[model_name])} records to {model_name} table...")
            for row in data[model_name]:
                # Skip if the record already exists
                existing = session.query(models[model_name]).get(row['id'])
                if existing is None:
                    # Convert string enums back to enum values
                    if model_name == 'Transaction':
                        if 'action' in row and row['action'] is not None:
                            row['action'] = TransactionType(row['action'])
                        if 'state' in row and row['state'] is not None:
                            row['state'] = ItemState(row['state'])
                    
                    # Create and add the record
                    record = models[model_name](**row)
                    session.add(record)
            
            # Commit after each model to maintain referential integrity
            session.commit()

if __name__ == "__main__":
    # Step 1: Create the new database with the correct schema
    print("Creating new database with updated schema...")
    engine, SessionLocal, models = create_database()
    
    # Step 2: Import data from the export
    export_file = Path('database_export.json')
    if export_file.exists():
        print(f"Importing data from {export_file}...")
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        session = SessionLocal()
        try:
            import_data(session, models, data)
            print("Data import completed successfully!")
        except Exception as e:
            print(f"Error during import: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    else:
        print("No export file found. Created empty database with updated schema.")
    
    print("\nDatabase setup complete!")
    print("Please update your application to use 'inventory_updated.db' as the database.")
