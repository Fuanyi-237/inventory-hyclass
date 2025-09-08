from sqlalchemy.orm import Session
from datetime import datetime

# Import models before schemas to ensure correct initialization order
import models
import schemas
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

# User CRUD

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Category CRUD

def create_category(db: Session, category: schemas.CategoryCreate, creator_id: int):
    db_category = models.Category(
        name=category.name,
        description=category.description,
        created_by=creator_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryCreate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db_category.name = category.name
        db_category.description = category.description
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

def get_categories(db: Session):
    return db.query(models.Category).all()

# Item CRUD

def create_item(db: Session, item: schemas.ItemCreate, creator_id: int):
    db_item = models.Item(
        unique_id=item.unique_id,
        name=item.name,
        description=item.description,
        category_id=item.category_id,
        state=item.state,
        location=item.location,
        purchase_date=item.purchase_date,
        expiry_date=item.expiry_date,
        created_by=creator_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# Transaction CRUD

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        item_id=transaction.item_id,
        user_id=transaction.user_id,
        action=transaction.action,
        timestamp=transaction.timestamp,
        notes=transaction.notes,
        state=transaction.state
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Notification CRUD

def create_notification(db: Session, notification: schemas.NotificationCreate):
    db_notification = models.Notification(
        user_id=notification.user_id,
        message=notification.message,
        sent_at=notification.sent_at,
        read=notification.read
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
