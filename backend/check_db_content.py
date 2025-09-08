import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

def check_database():
    db_path = 'inventory_updated.db'
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' does not exist!")
        return False
    
    print(f"✅ Database file found at: {os.path.abspath(db_path)}")
    print(f"File size: {os.path.getsize(db_path)} bytes")
    
    try:
        # Create engine and inspect the database
        engine = create_engine(f'sqlite:///{db_path}')
        inspector = inspect(engine)
        
        # List all tables
        tables = inspector.get_table_names()
        print("\nTables in database:")
        for table in tables:
            print(f"- {table}")
            
            # List columns for each table
            columns = inspector.get_columns(table)
            for column in columns:
                print(f"  - {column['name']}: {column['type']}")
        
        # If no tables found, database might be empty
        if not tables:
            print("❌ No tables found in the database!")
            return False
            
        # Check if users table exists
        if 'users' not in tables:
            print("❌ 'users' table not found in the database!")
            return False
            
        # Check if admin user exists
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            from models import User
            admin = session.query(User).filter(User.username == 'admin').first()
            
            if admin:
                print("\n✅ Admin user found:")
                print(f"ID: {admin.id}")
                print(f"Username: {admin.username}")
                print(f"Email: {admin.email}")
                print(f"Role: {admin.role}")
                print(f"Is Active: {admin.is_active}")
                print(f"Is Superuser: {admin.is_superuser}")
            else:
                print("❌ Admin user not found in the database!")
                return False
                
        except Exception as e:
            print(f"❌ Error querying users table: {e}")
            return False
        finally:
            session.close()
            
        return True
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        return False

if __name__ == "__main__":
    print("Checking database...")
    success = check_database()
    sys.exit(0 if success else 1)
