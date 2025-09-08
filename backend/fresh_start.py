import os
import sqlite3
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

def create_fresh_database():
    # Remove existing database if it exists
    db_path = os.path.join(os.getcwd(), 'inventory_updated.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing database file.")
    
    # Create a new database
    DB_URL = 'sqlite:///inventory_updated.db'
    engine = create_engine(DB_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    # Define models
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
        image_url = Column(String, nullable=True)  # This is our target column
        
        item = relationship("Item", back_populates="transactions")
        user = relationship("User", back_populates="actions")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("\n✅ Fresh database created with the following tables:")
    inspector = engine.dialect.inspector.Inspector.from_engine(engine)
    for table_name in inspector.get_table_names():
        print(f"\nTable: {table_name}")
        for column in inspector.get_columns(table_name):
            print(f"  - {column['name']}: {column['type']}")
    
    return engine, SessionLocal

if __name__ == "__main__":
    print("Creating a fresh database with the correct schema...")
    engine, SessionLocal = create_fresh_database()
    
    # Test the database connection
    try:
        with engine.connect() as conn:
            print("\n✅ Successfully connected to the new database!")
            
            # Check if transactions table has image_url column
            inspector = engine.dialect.inspector.Inspector.from_engine(engine)
            if 'transactions' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('transactions')]
                if 'image_url' in columns:
                    print("✅ 'transactions' table has 'image_url' column!")
                else:
                    print("❌ 'transactions' table is missing 'image_url' column!")
            else:
                print("❌ 'transactions' table not found!")
                
    except Exception as e:
        print(f"❌ Error testing database connection: {e}")
    
    print("\n✨ Database setup complete! You can now start the application.")
