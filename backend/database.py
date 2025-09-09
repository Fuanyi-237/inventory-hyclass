import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Configuration ---
# Prefer DATABASE_URL from environment (e.g., set by docker-compose). Fallback to a local sqlite file
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BACKEND_DIR, "inventory_updated.db")

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL") or f"sqlite:///{DEFAULT_DB_PATH}"

print(f"INFO:     Using SQLALCHEMY_DATABASE_URL={SQLALCHEMY_DATABASE_URL}")

# sqlite requires a special arg
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
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
