from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
import io
import csv
import json
try:
    from openpyxl import Workbook  # type: ignore
    HAS_OPENPYXL = True
except Exception:  # ImportError or other env issues
    HAS_OPENPYXL = False
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
    """Export transactions within a date range as an Excel (.xlsx) file when possible,
    otherwise fall back to CSV if Excel dependencies are not available.

    If no range is provided, defaults to the last 7 days.
    Accessible to any authenticated user.
    """
    def parse_iso(dt_str: Optional[str], default: datetime) -> datetime:
        if not dt_str:
            return default
        s = dt_str.strip()
        # Allow trailing 'Z' from browsers
        if s.endswith('Z'):
            s = s[:-1] + '+00:00'
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            # Try date-only (YYYY-MM-DD)
            try:
                d = datetime.strptime(s, '%Y-%m-%d')
                return d.replace(tzinfo=timezone.utc)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO8601, e.g. 2025-09-05T12:00:00+00:00")

    now_utc = datetime.now(timezone.utc)
    start_dt = parse_iso(start, now_utc - timedelta(days=7))
    end_dt = parse_iso(end, now_utc)

    service = TransactionService(db)
    transactions = service.get_by_date_range(start_dt, end_dt)

    def to_cell(val):
        # Convert complex types to JSON strings; keep primitives; None -> ''
        if val is None:
            return ''
        if isinstance(val, (dict, list)):
            try:
                return json.dumps(val, ensure_ascii=False)
            except Exception:
                return str(val)
        if isinstance(val, (str, int, float, bool)):
            return val
        # Fallback to string for other objects (e.g., UUID, Decimal)
        return str(val)

    headers_list = [
        "id", "item_id", "item_unique_id", "user_id", "username", "action", "state", "timestamp", "notes", "image_url",
    ]

    if HAS_OPENPYXL:
        # Prepare Excel workbook in-memory
        wb = Workbook()
        ws = wb.active
        ws.title = "Transactions"
        ws.append(headers_list)
        for t in transactions:
            ws.append([
                to_cell(t.id),
                to_cell(getattr(t, 'item_id', '')),
                to_cell(getattr(getattr(t, 'item', None), 'unique_id', '') if getattr(t, 'item', None) else ''),
                to_cell(getattr(t, 'user_id', '')),
                to_cell(getattr(getattr(t, 'user', None), 'username', '') if getattr(t, 'user', None) else ''),
                to_cell(getattr(t, 'action', '')),
                to_cell(getattr(t, 'state', '')),
                to_cell(t.timestamp.isoformat() if getattr(t, 'timestamp', None) else ''),
                to_cell(getattr(t, 'notes', '')),
                to_cell(getattr(t, 'image_url', '')),
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
    else:
        # Fallback to CSV if Excel library isn't available on the server
        sio = io.StringIO()
        writer = csv.writer(sio)
        writer.writerow(headers_list)
        for t in transactions:
            writer.writerow([
                to_cell(t.id),
                to_cell(getattr(t, 'item_id', '')),
                to_cell(getattr(getattr(t, 'item', None), 'unique_id', '') if getattr(t, 'item', None) else ''),
                to_cell(getattr(t, 'user_id', '')),
                to_cell(getattr(getattr(t, 'user', None), 'username', '') if getattr(t, 'user', None) else ''),
                to_cell(getattr(t, 'action', '')),
                to_cell(getattr(t, 'state', '')),
                to_cell(t.timestamp.isoformat() if getattr(t, 'timestamp', None) else ''),
                to_cell(getattr(t, 'notes', '')),
                to_cell(getattr(t, 'image_url', '')),
            ])
        sio.seek(0)
        filename = f"transactions_{start_dt.date()}_{end_dt.date()}.csv"
        headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}
        return StreamingResponse(iter([sio.getvalue()]), media_type="text/csv", headers=headers)
