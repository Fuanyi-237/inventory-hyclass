from sqlalchemy import create_engine, inspect

def test_database_connection():
    try:
        # Use the same database URL as in database.py
        db_url = "sqlite:///inventory_updated.db"
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        
        # Test connection
        with engine.connect() as conn:
            print("✅ Successfully connected to the database!")
            
            # Check if tables exist
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print("\nTables in the database:")
            for table in tables:
                print(f"- {table}")
                
                # Print columns for each table
                columns = inspector.get_columns(table)
                print(f"  Columns in {table}:")
                for column in columns:
                    print(f"  - {column['name']}: {column['type']}")
                
            # Check if transactions table has image_url column
            if 'transactions' in tables:
                print("\n✅ 'transactions' table exists!")
                transactions_columns = [col['name'] for col in inspector.get_columns('transactions')]
                if 'image_url' in transactions_columns:
                    print("✅ 'image_url' column exists in 'transactions' table!")
                else:
                    print("❌ 'image_url' column is missing from 'transactions' table!")
            else:
                print("❌ 'transactions' table does not exist!")
                
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")

if __name__ == "__main__":
    test_database_connection()
