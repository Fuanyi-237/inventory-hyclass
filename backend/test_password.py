from password_utils import get_password_hash, verify_password

def test_password_hashing():
    password = "admin123"
    print("Testing password hashing...")
    
    # Test hashing
    hashed = get_password_hash(password)
    print(f"Hashed password: {hashed}")
    
    # Test verification
    is_valid = verify_password(password, hashed)
    print(f"Password verification: {'✅ Success' if is_valid else '❌ Failed'}")
    
    # Test with wrong password
    is_valid_wrong = verify_password("wrongpassword", hashed)
    print(f"Wrong password test: {'✅ Correctly failed' if not is_valid_wrong else '❌ Should have failed'}")

if __name__ == "__main__":
    test_password_hashing()
