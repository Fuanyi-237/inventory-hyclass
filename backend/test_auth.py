import sys
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from password_utils import verify_password, get_password_hash

def test_authentication():
    db = SessionLocal()
    try:
        username = "admin"
        password = "admin123"
        
        print(f"Testing authentication for user: {username}")
        
        # Find the user
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print("❌ User not found!")
            return
            
        print(f"✅ User found: {user.username} (ID: {user.id}, Email: {user.email})")
        print(f"Hashed password: {user.hashed_password}")
        
        # Verify password
        is_valid = verify_password(password, user.hashed_password)
        print(f"Password verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        if not is_valid:
            print("\nAttempting to fix password...")
            user.hashed_password = get_password_hash(password)
            db.commit()
            print("✅ Password has been reset to 'admin123'")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_authentication()
