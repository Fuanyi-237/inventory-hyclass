import typer
from getpass import getpass

from database import SessionLocal, init_db
from create_admin import create_superadmin_logic

app = typer.Typer()

@app.command()
def create_superadmin():
    """
    Creates a new superadmin user.
    """
    print("Initializing database...")
    init_db()
    db = SessionLocal()
    print("Creating new superadmin user...")

    username = typer.prompt("Enter username")
    email = typer.prompt("Enter email")
    full_name = typer.prompt("Enter full name")
    password = getpass("Enter password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match. Aborting.")
        raise typer.Exit()

    try:
        user = create_superadmin_logic(
            db=db,
            username=username,
            email=email,
            full_name=full_name,
            password=password
        )
        print(f"Superadmin user '{user.username}' created successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    app()
