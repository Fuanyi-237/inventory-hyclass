import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from models import Base, User
from password_utils import get_password_hash

def init_db():
    # Create engine and bind it to the session
    engine = create_engine('sqlite:///inventory_updated.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Drop all tables
        print("Dropping existing tables...")
        Base.metadata.drop_all(engine)
        
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(engine)
        
        # Create admin user
        admin = User(
            username="admin",
            email="admin@inventory.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role="superadmin",
            is_active=True,
            is_superuser=True
        )
        
        session.add(admin)
        session.commit()
        
        print("✅ Database initialized successfully!")
        print("Admin user created with username: admin")
        print("Password: admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("Initializing database...")
    success = init_db()
    sys.exit(0 if success else 1)
