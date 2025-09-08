import os
import sys
import sqlite3

def check_database():
    db_path = 'inventory_updated.db'
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' does not exist!")
        return False
    
    print(f"✅ Database file found at: {os.path.abspath(db_path)}")
    print(f"File size: {os.path.getsize(db_path)} bytes")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ No tables found in the database!")
            return False
            
        print("\nTables in database:")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            if not columns:
                print("  No columns found!")
                continue
                
            print("  Columns:")
            for col in columns:
                print(f"  - {col[1]}: {col[2]} {'(PK)' if col[5] > 0 else ''}")
                
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"  Rows: {count}")
            
            # If it's the users table, check for admin user
            if table_name == 'users':
                cursor.execute("SELECT * FROM users WHERE username = 'admin';")
                admin = cursor.fetchone()
                
                if admin:
                    print("\n✅ Admin user found:")
                    print(f"ID: {admin[0]}")
                    print(f"Username: {admin[1]}")
                    print(f"Email: {admin[2]}")
                    print(f"Role: {admin[5] if len(admin) > 5 else 'N/A'}")
                else:
                    print("❌ Admin user not found!")
                    return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Checking database...")
    success = check_database()
    sys.exit(0 if success else 1)
