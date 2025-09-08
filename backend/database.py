import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Configuration ---
# Get the absolute path to the directory where this file is located (the backend directory)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the database file
DB_PATH = os.path.join(BACKEND_DIR, "inventory_updated.db")

# Define the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"INFO:     Connecting to database at: {DB_PATH}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database with all models
def init_db():
    from base import Base
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
