"""Admin endpoints for the Sentient Waitlist API (API-key protected)."""

import csv
import io
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import WaitlistEntry
from app.schemas import WaitlistResponse
from app.utils.security import verify_api_key
from app.main import limiter

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/waitlist", response_model=list[WaitlistResponse])
@limiter.limit("30/minute")
async def list_signups(
    request: Request,
    limit: int = Query(100, ge=1, le=1000, description="Max results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: AsyncSession = Depends(get_db),
):
    """List all waitlist signups (paginated). Requires API key."""
    result = await db.execute(
        select(WaitlistEntry)
        .order_by(WaitlistEntry.queue_position.asc())
        .limit(limit)
        .offset(offset)
    )
    entries = result.scalars().all()
    return entries


@router.get("/waitlist/export")
@limiter.limit("10/minute")
async def export_signups(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Export all waitlist signups as CSV. Requires API key."""
    result = await db.execute(
        select(WaitlistEntry).order_by(WaitlistEntry.queue_position.asc())
    )
    entries = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "email", "name", "referral_source",
        "queue_position", "ip_hash", "user_agent",
        "created_at", "verified",
    ])
    for entry in entries:
        writer.writerow([
            entry.id,
            entry.email,
            entry.name or "",
            entry.referral_source or "",
            entry.queue_position,
            entry.ip_hash or "",
            entry.user_agent or "",
            entry.created_at.isoformat() if entry.created_at else "",
            entry.verified,
        ])

    output.seek(0)
    logger.info("CSV export requested: %d entries", len(entries))
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=waitlist_export.csv"},
    )


@router.delete("/waitlist/{signup_id}", status_code=200)
@limiter.limit("20/minute")
async def delete_signup(
    request: Request,
    signup_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Remove a signup by ID. Requires API key."""
    result = await db.execute(
        select(WaitlistEntry).where(WaitlistEntry.id == signup_id)
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Signup not found")

    await db.delete(entry)
    await db.commit()
    logger.info("Deleted signup id=%d queue_position=%d", signup_id, entry.queue_position)
    return {"success": True, "message": "Signup deleted"}
