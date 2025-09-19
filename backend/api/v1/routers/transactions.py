from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
import io
from openpyxl import Workbook
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from backend.dependencies import get_db, get_current_user
from backend.services.transaction_service import TransactionService
from backend.schemas import TransactionRead, TransactionCreate
from backend.models import User
from backend.shared_enums import UserRole

router = APIRouter(tags=["transactions"])

@router.get("/", response_model=List[TransactionRead])
def read_transactions(db: Session = Depends(get_db)):
    """Retrieve all transactions."""
    transaction_service = TransactionService(db)
    return transaction_service.get_all()

@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new transaction."""
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and superadmins can create transactions."
        )
    transaction_service = TransactionService(db)
    return transaction_service.create(transaction_in=transaction)


@router.get("/export")
def export_transactions(
    start: Optional[str] = Query(None, description="Start datetime ISO8601 (inclusive)"),
    end: Optional[str] = Query(None, description="End datetime ISO8601 (inclusive)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Export transactions within a date range as an Excel (.xlsx) file.

    If no range is provided, defaults to the last 7 days.
    Accessible to any authenticated user.
    """
    try:
        if start:
            start_dt = datetime.fromisoformat(start)
        else:
            start_dt = datetime.now(timezone.utc) - timedelta(days=7)
        if end:
            end_dt = datetime.fromisoformat(end)
        else:
            end_dt = datetime.now(timezone.utc)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO8601, e.g. 2025-09-05T12:00:00+00:00")

    service = TransactionService(db)
    transactions = service.get_by_date_range(start_dt, end_dt)

    # Prepare Excel workbook in-memory
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"
    ws.append([
        "id", "item_id", "item_unique_id", "user_id", "username", "action", "state", "timestamp", "notes", "image_url",
    ])
    for t in transactions:
        ws.append([
            t.id,
            getattr(t, 'item_id', ''),
            getattr(getattr(t, 'item', None), 'unique_id', '') if getattr(t, 'item', None) else '',
            getattr(t, 'user_id', ''),
            getattr(getattr(t, 'user', None), 'username', '') if getattr(t, 'user', None) else '',
            getattr(t, 'action', ''),
            getattr(t, 'state', ''),
            t.timestamp.isoformat() if getattr(t, 'timestamp', None) else '',
            getattr(t, 'notes', ''),
            getattr(t, 'image_url', ''),
        ])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = f"transactions_{start_dt.date()}_{end_dt.date()}.xlsx"
    headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\""
    }
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
