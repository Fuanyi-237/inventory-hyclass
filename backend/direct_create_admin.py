import sqlite3
from getpass import getpass
from hashlib import sha256
import os

DB_PATH = "inventory_updated.db"  # Updated to use the new database

def get_password_hash(password: str) -> str:
    """Generate a simple SHA256 hash for the password.
    In production, you should use a proper password hashing function like bcrypt."""
    return sha256(password.encode('utf-8')).hexdigest()

def main():
    print("Creating superadmin user via direct database insertion...")

    email = input("Enter email: ")
    full_name = input("Enter full name: ")
    password = getpass("Enter password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match. Aborting.")
        return

    hashed_password = get_password_hash(password)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if user already exists by email
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"User with email '{email}' already exists. Aborting.")
            return

        # Insert new user with proper schema
        hashed_password = get_password_hash(password)
        cursor.execute(
            """
            INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser)
            VALUES (?, ?, ?, ?, ?)
            """,
            (email, hashed_password, full_name, 1, 1)  # is_active=1, is_superuser=1
        )

        conn.commit()
        print(f"Superadmin user with email '{email}' created successfully!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
