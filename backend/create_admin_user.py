from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from password_utils import get_password_hash

def create_admin_user():
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin = db.query(User).filter(User.email == 'admin@inventory.com').first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create new admin user
        hashed_password = get_password_hash("admin123")
        admin_user = User(
            username="admin",
            email="admin@inventory.com",
            full_name="Admin User",
            hashed_password=hashed_password,
            role="superadmin",
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        print("✅ Admin user created successfully!")
        print("Email: admin@inventory.com")
        print("Password: admin123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
