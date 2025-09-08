# This script is for one-time database setup.
from base import Base
from database import engine
import models  # Import models to register them with Base

print("Creating database and all tables...")
Base.metadata.create_all(bind=engine)
print("Database and tables created successfully.")
