from backend.database import SessionLocal
from backend.models import User
from backend.shared_enums import UserRole
from backend.password_utils import get_password_hash


def setup_admin():
    db = SessionLocal()
    try:
        # Check by email
        existing = db.query(User).filter(User.email == 'admin@example.com').first()
        if existing:
            print("✅ Admin user already exists:")
            print(f"ID: {existing.id}")
            print(f"Email: {existing.email}")
            print(f"Name: {existing.full_name}")
            return

        print("Creating default admin user (role=superadmin)...")
        user = User(
            username='admin',
            email='admin@example.com',
            full_name='Admin User',
            hashed_password=get_password_hash('password'),
            role=UserRole.superadmin,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("✅ Default admin user created!")
        print("Email: admin@example.com")
        print("Password: password")
        print("⚠️ Please change the default password immediately after login!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    setup_admin()
