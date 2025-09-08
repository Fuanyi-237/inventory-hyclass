import sqlite3
import json
from pathlib import Path

def export_database():
    # Connect to the old database
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    # Get list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
    
    # Dictionary to hold all data
    data = {}
    
    # Export data from each table
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        data[table] = [dict(row) for row in rows]
    
    # Save to JSON file
    export_path = Path('database_export.json')
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    
    conn.close()
    return export_path

if __name__ == "__main__":
    export_path = export_database()
    print(f"Database exported to {export_path}")
