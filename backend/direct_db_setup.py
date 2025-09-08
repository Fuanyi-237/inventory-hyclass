import sqlite3
import os

def create_database():
    # Remove existing database if it exists
    if os.path.exists('inventory_updated.db'):
        os.remove('inventory_updated.db')
    
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect('inventory_updated.db')
    cursor = conn.cursor()
    
    # Create tables with the correct schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT,
        is_active INTEGER DEFAULT 1,
        is_superuser INTEGER DEFAULT 0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER DEFAULT 0,
        category_id INTEGER,
        state TEXT CHECK( state IN ('good','damaged','lost') ) NOT NULL DEFAULT 'good',
        location TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        action TEXT CHECK( action IN ('sign_in','sign_out','return_item') ) NOT NULL,
        timestamp DATETIME,
        notes TEXT,
        state TEXT CHECK( state IN ('good','damaged','lost') ),
        image_url TEXT,
        FOREIGN KEY (item_id) REFERENCES items (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    
    # Verify the schema
    print("✅ Database created with the following tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("Columns:")
        for col in columns:
            print(f"  - {col[1]}: {col[2]} {'(PRIMARY KEY)' if col[5] else ''}")
    
    # Check if image_url exists in transactions
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'image_url' in columns:
        print("\n✅ 'image_url' column exists in 'transactions' table!")
    else:
        print("\n❌ 'image_url' column is missing from 'transactions' table!")
    
    conn.close()
    print("\n✨ Database setup complete!")

if __name__ == "__main__":
    print("Setting up database with direct SQL...")
    create_database()
