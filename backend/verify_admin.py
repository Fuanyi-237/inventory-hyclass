import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from password_utils import get_password_hash, verify_password

def verify_admin():
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            print("Admin user not found. Creating admin user...")
            hashed_password = get_password_hash("admin123")
            admin = User(
                username="admin",
                email="admin@inventory.com",
                full_name="Admin User",
                hashed_password=hashed_password,
                role="superadmin",
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created successfully!")
        else:
            print("✅ Admin user found:")
            print(f"ID: {admin.id}")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Role: {admin.role}")
            print(f"Is Active: {admin.is_active}")
            print(f"Is Superuser: {admin.is_superuser}")
            
            # Verify password
            password_ok = verify_password("admin123", admin.hashed_password)
            print(f"\nPassword verification: {'✅ Correct' if password_ok else '❌ Incorrect'}")
            
            if not password_ok:
                update = input("\nUpdate password? (y/n): ")
                if update.lower() == 'y':
                    admin.hashed_password = get_password_hash("admin123")
                    db.commit()
                    print("✅ Password updated successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    verify_admin()
