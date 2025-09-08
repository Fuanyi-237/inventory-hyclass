import sys
import sqlite3
from password_utils import get_password_hash

def reset_admin_password():
    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Get the admin user
        cursor.execute("SELECT id, username, hashed_password FROM users WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if not admin:
            print("❌ Admin user not found!")
            return False
            
        admin_id, username, current_hash = admin
        print(f"✅ Found admin user: {username} (ID: {admin_id})")
        print(f"Current password hash: {current_hash}")
        
        # Generate a new password hash
        new_password = "admin123"
        new_hash = get_password_hash(new_password)
        
        # Update the password
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE id = ?",
            (new_hash, admin_id)
        )
        conn.commit()
        
        print(f"✅ Password for '{username}' has been reset to '{new_password}'")
        print(f"New password hash: {new_hash}")
        
        # Verify the new password
        from password_utils import verify_password
        is_valid = verify_password(new_password, new_hash)
        print(f"Password verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = reset_admin_password()
    sys.exit(0 if success else 1)
