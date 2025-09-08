import sqlite3
import os
import datetime
from getpass import getpass
from password_utils import get_password_hash

DB_PATH = "inventory.db"

# Raw SQL statements to create tables exactly as defined in models.py
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    is_active BOOLEAN
);
"""

CREATE_CATEGORIES_TABLE = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description VARCHAR,
    created_by INTEGER,
    FOREIGN KEY(created_by) REFERENCES users(id)
);
"""

CREATE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    unique_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    description VARCHAR,
    category_id INTEGER,
    state VARCHAR NOT NULL,
    location VARCHAR,
    purchase_date DATETIME,
    expiry_date DATETIME,
    created_by INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(id),
    FOREIGN KEY(created_by) REFERENCES users(id)
);
"""

CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    user_id INTEGER,
    action VARCHAR NOT NULL,
    timestamp DATETIME,
    notes VARCHAR,
    state VARCHAR,
    FOREIGN KEY(item_id) REFERENCES items(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

CREATE_NOTIFICATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    message VARCHAR,
    sent_at DATETIME,
    read BOOLEAN,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

TABLES = [
    CREATE_USERS_TABLE,
    CREATE_CATEGORIES_TABLE,
    CREATE_ITEMS_TABLE,
    CREATE_TRANSACTIONS_TABLE,
    CREATE_NOTIFICATIONS_TABLE
]

def main():
    print("--- Automated Database Setup ---")

    # Step 0: Delete existing database file to ensure a clean slate
    if os.path.exists(DB_PATH):
        print(f"Removing existing database file at '{DB_PATH}'...")
        os.remove(DB_PATH)
        print("Existing database removed.")

    conn = None
    try:
        # Step 1: Create all tables
        print(f"Connecting to database at '{DB_PATH}'...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("Creating tables...")
        for table_sql in TABLES:
            cursor.execute(table_sql)
        conn.commit()
        print("All tables created successfully.")

        # Step 2: Create the hardcoded superadmin user
        print("\n--- Create Superadmin User ---")
        username = "Expert"
        email = "expert@inventory.com"
        full_name = "Expert User"
        password = "John14:6"  # The password the user has been trying

        print(f"Creating user '{username}'...")

        hashed_password = get_password_hash(password)

        cursor.execute(
            """INSERT INTO users (username, email, full_name, hashed_password, role, is_active)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (username, email, full_name, hashed_password, "superadmin", True)
        )
        conn.commit()
        print(f"\nSuperadmin user '{username}' created successfully!")

    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()
