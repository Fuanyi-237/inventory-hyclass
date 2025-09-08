import sqlite3
from password_utils import verify_password, get_password_hash

def verify_user():
    print("Verifying admin user...")
    
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE email = 'expert@gmail.com'")
        user = cursor.fetchone()
        
        if not user:
            print("❌ User with email 'expert@gmail.com' not found!")
            return
            
        print("✅ User found in database:")
        print(f"ID: {user[0]}")
        print(f"Username: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"Full Name: {user[3]}")
        print(f"Role: {user[6]}")
        print(f"Is Active: {bool(user[7])}")
        print(f"Is Superuser: {bool(user[8])}")
        
        # Test the password
        test_password = "admin123"
        hashed_password = user[4]  # hashed_password is at index 4
        
        # Print the stored hash for debugging
        print(f"\nStored password hash: {hashed_password}")
        
        # Manually verify the password
        if verify_password(test_password, hashed_password):
            print("✅ Password 'admin123' is correct!")
        else:
            print("❌ Password 'admin123' is NOT correct!")
            
            # Generate a new hash for the password
            new_hash = get_password_hash(test_password)
            print(f"\nNew hash for 'admin123': {new_hash}")
            
            # Update the password in the database
            update = input("\nUpdate password with new hash? (y/n): ")
            if update.lower() == 'y':
                cursor.execute(
                    "UPDATE users SET hashed_password = ? WHERE id = ?",
                    (new_hash, user[0])
                )
                conn.commit()
                print("✅ Password updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_user()
