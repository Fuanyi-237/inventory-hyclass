import os
import sqlite3

def check_database():
    db_path = os.path.join(os.getcwd(), 'inventory_updated.db')
    
    # Check if file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return
        
    print(f"✅ Database file exists at: {db_path}")
    print(f"File size: {os.path.getsize(db_path)} bytes")
    
    try:
        # Try to connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ No tables found in the database!")
            return
            
        print("\nTables in the database:")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print("Columns:")
            for col in columns:
                col_id, col_name, col_type, notnull, default_val, pk = col
                print(f"  - {col_name}: {col_type} {'(PRIMARY KEY)' if pk else ''}")
        
        # Check transactions table specifically
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
        if cursor.fetchone():
            print("\n✅ 'transactions' table exists!")
            cursor.execute("PRAGMA table_info(transactions);")
            columns = [col[1] for col in cursor.fetchall()]
            if 'image_url' in columns:
                print("✅ 'image_url' column exists in 'transactions' table!")
            else:
                print("❌ 'image_url' column is missing from 'transactions' table!")
        else:
            print("\n❌ 'transactions' table does not exist!")
            
    except sqlite3.Error as e:
        print(f"\n❌ SQLite error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database()
