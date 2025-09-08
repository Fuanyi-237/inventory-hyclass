import sys
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from password_utils import verify_password

def verify_admin():
    db = SessionLocal()
    try:
        # Get admin user
        admin = db.query(User).filter(User.username == 'admin').first()
        
        if not admin:
            print("❌ Admin user not found!")
            return False
            
        print(f"✅ Found admin user: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Is Active: {admin.is_active}")
        print(f"Is Superuser: {admin.is_superuser}")
        
        # Test password
        password = "admin123"
        is_valid = verify_password(password, admin.hashed_password)
        print(f"\nPassword verification for 'admin123': {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        if not is_valid:
            print("\nCurrent password hash:", admin.hashed_password)
            print("\nTry these troubleshooting steps:")
            print("1. Check if the password was hashed with a different algorithm")
            print("2. Verify the password_utils.py is using the correct hashing method")
            print("3. Try manually resetting the admin password")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = verify_admin()
    sys.exit(0 if success else 1)
