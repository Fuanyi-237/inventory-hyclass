import sqlite3
import os

def create_simple_db():
    # Remove existing database if it exists
    db_path = 'inventory_simple.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create a new database and add a table with the image_url column
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a simple transactions table with image_url
    cursor.execute('''
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        action TEXT CHECK(action IN ('sign_in', 'sign_out', 'return_item')) NOT NULL,
        timestamp DATETIME,
        notes TEXT,
        state TEXT CHECK(state IN ('good', 'damaged', 'lost')),
        image_url TEXT
    )
    ''')
    
    # Insert a test record
    cursor.execute('''
    INSERT INTO transactions (item_id, user_id, action, timestamp, notes, state, image_url)
    VALUES (1, 1, 'sign_in', '2025-08-22 10:00:00', 'Test transaction', 'good', 'https://example.com/image.jpg')
    ''')
    
    # Verify the table and columns
    cursor.execute("PRAGMA table_info(transactions)")
    columns = cursor.fetchall()
    
    print("Columns in 'transactions' table:")
    for col in columns:
        print(f"- {col[1]}: {col[2]}")
    
    # Check if image_url exists
    image_url_exists = any(col[1] == 'image_url' for col in columns)
    print(f"\n'image_url' column exists: {'✅' if image_url_exists else '❌'}")
    
    # Query the test record
    cursor.execute("SELECT * FROM transactions")
    records = cursor.fetchall()
    
    print("\nTest record:")
    for row in records:
        print(row)
    
    # Save changes and close
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database created at: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    print("Creating a simple database with a transactions table...")
    create_simple_db()
