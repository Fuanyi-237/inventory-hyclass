import sqlite3

def check_schema():
    print("Checking database schema...")
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # List all tables
        print("\nTables in database:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}")
            
        # Show users table schema
        print("\nUsers table schema:")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"- {col[1]}: {col[2]} {'(PK)' if col[5] > 0 else ''}")
        
        # Show users in the database
        print("\nUsers in database:")
        try:
            cursor.execute("SELECT id, username, email, role, is_active FROM users")
            users = cursor.fetchall()
            if users:
                for user in users:
                    print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}, Active: {user[4]}")
            else:
                print("No users found in the database.")
        except sqlite3.Error as e:
            print(f"Error fetching users: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_schema()
