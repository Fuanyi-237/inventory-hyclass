import sqlite3
from hashlib import sha256

def get_password_hash(password):
    """Simple password hashing function"""
    return sha256(password.encode('utf-8')).hexdigest()

def reset_password():
    print("Admin Password Reset Tool")
    print("========================")
    
    # Set new password
    new_password = "admin123"  # Default password, should be changed after login
    hashed_password = get_password_hash(new_password)
    
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Update or create admin user with all required fields
        cursor.execute(
            """
            INSERT OR REPLACE INTO users 
            (email, username, full_name, hashed_password, is_active, is_superuser, role)
            VALUES (?, ?, ?, ?, 1, 1, 'superadmin')
            """,
            ('expert@gmail.com', 'expert', 'IT Expert', hashed_password)
        )
        
        if cursor.rowcount > 0:
            conn.commit()
            print("\n✅ Password has been reset successfully!")
            print(f"Email: expert@gmail.com")
            print(f"New Password: {new_password}")
            print("\n⚠️ Please log in and change this password immediately!")
        else:
            print("\n❌ Could not find user with email 'expert@gmail.com'")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    reset_password()
