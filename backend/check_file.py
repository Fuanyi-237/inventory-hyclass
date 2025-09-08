import os

def check_file():
    file_path = os.path.join(os.getcwd(), 'inventory_updated.db')
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    # Get file info
    file_size = os.path.getsize(file_path)
    print(f"✅ File found: {file_path}")
    print(f"File size: {file_size} bytes")
    
    # Try to read the first few bytes to check if it's a valid SQLite database
    try:
        with open(file_path, 'rb') as f:
            header = f.read(16)
            if header.startswith(b'SQLite format 3\000'):
                print("✅ Valid SQLite database header detected")
            else:
                print("❌ Not a valid SQLite database (invalid header)")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    check_file()
