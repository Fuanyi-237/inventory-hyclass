from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Generator

# Import models first to ensure tables are created
from backend import models
from backend.database import engine, SessionLocal
from backend.dependencies import get_db, get_current_user

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Import routers
from backend.api.v1.routers import auth, categories, items, transactions, users, uploads

# Create uploads directory
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Create FastAPI app
app = FastAPI(
    title="Inventory Management System API",
    description="API for managing inventory, items, and transactions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600  # Cache preflight request for 10 minutes
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(uploads.router, prefix="/api/v1/uploads", tags=["uploads"])

# Mount static files directory for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Inventory Management System API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Dependency
def get_db() -> Generator:
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["backend"])
