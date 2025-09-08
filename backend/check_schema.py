from sqlalchemy import create_engine, inspect

def check_transactions_schema():
    # Connect to the database
    engine = create_engine('sqlite:///inventory.db')
    
    # Create an inspector
    inspector = inspect(engine)
    
    # Get columns in transactions table
    columns = inspector.get_columns('transactions')
    
    print("Columns in 'transactions' table:")
    for column in columns:
        print(f"- {column['name']}: {column['type']} (nullable: {column['nullable']}, default: {column.get('default', None)})")

if __name__ == "__main__":
    check_transactions_schema()
