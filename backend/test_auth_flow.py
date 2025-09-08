import sys
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User
from password_utils import get_password_hash

# Create a test client
client = TestClient(app)

def test_login_flow():
    # First, ensure the test user exists
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            print("Creating test admin user...")
            admin = User(
                username="admin",
                email="admin@inventory.com",
                full_name="Admin User",
                hashed_password=get_password_hash("admin123"),
                role="superadmin",
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("✅ Test admin user created")
        else:
            print("✅ Test admin user exists")
            
        # Test login with correct credentials
        print("\nTesting login with correct credentials...")
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "admin", "password": "admin123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            print("✅ Login successful!")
            token = response.json().get("access_token")
            print(f"Access token: {token[:20]}...")
            
            # Test getting current user with the token
            print("\nTesting /me endpoint with token...")
            me_response = client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if me_response.status_code == 200:
                print("✅ Successfully retrieved user data:")
                user_data = me_response.json()
                print(f"Username: {user_data.get('username')}")
                print(f"Email: {user_data.get('email')}")
                print(f"Role: {user_data.get('role')}")
            else:
                print(f"❌ Failed to get user data: {me_response.status_code}")
                print(me_response.text)
                
        else:
            print(f"❌ Login failed with status code: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_login_flow()
