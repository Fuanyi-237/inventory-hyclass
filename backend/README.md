# Inventory System Backend

This directory contains the backend API for the Inventory System, built with FastAPI and SQLite (upgradeable to PostgreSQL).

## Features
- User authentication and roles (Superadmin, Admin)
- Inventory item management
- Sign in/out tracking
- State and category management
- Audit logging
- Weekly Excel export
- In-app and email notifications (future)

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `uvicorn main:app --reload`

## Structure
- `main.py` - FastAPI entrypoint
- `models.py` - Database models
- `schemas.py` - Pydantic schemas
- `crud.py` - Database operations
- `auth.py` - Authentication and user management
- `utils.py` - Utility functions (Excel export, notifications)

---

Frontend will be in `/frontend`.
