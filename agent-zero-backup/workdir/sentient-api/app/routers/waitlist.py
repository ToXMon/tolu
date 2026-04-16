"""Public waitlist endpoints for the Sentient Waitlist API."""

import logging
from fastapi import APIRouter, Depends, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import WaitlistEntry
from app.schemas import (
    WaitlistSubmit,
    WaitlistSubmitResult,
    WaitlistCountResponse,
    QueuePositionResponse,
)
from app.utils.validation import is_valid_email
from app.utils.security import hash_ip, hash_email, sanitize_text

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/waitlist", tags=["waitlist"])


@router.post("", response_model=WaitlistSubmitResult, status_code=201)
async def submit_to_waitlist(
    payload: WaitlistSubmit,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Submit an email to the waitlist.

    Validates the email, checks for duplicates, and assigns a
    sequential queue position if the email is new.
    """
    # Validate email (syntax + optional MX check)
    is_valid, reason = is_valid_email(payload.email)
    if not is_valid:
        logger.warning("Invalid email rejected (position lookup failed): %s", reason)
        return WaitlistSubmitResult(
            success=False,
            message=reason,
            is_duplicate=False,
        )

    normalized_email = payload.email.strip().lower()

    # Check for existing entry
    existing = await db.execute(
        select(WaitlistEntry).where(WaitlistEntry.email == normalized_email)
    )
    existing_entry = existing.scalar_one_or_none()
    if existing_entry:
        logger.info(
            "Duplicate signup: queue_position=%d",
            existing_entry.queue_position,
        )
        return WaitlistSubmitResult(
            success=True,
            message="You are already on the waitlist!",
            queue_position=existing_entry.queue_position,
            is_duplicate=True,
        )

    # Assign next queue position
    max_pos_result = await db.execute(select(func.max(WaitlistEntry.queue_position)))
    max_pos = max_pos_result.scalar_one_or_none() or 0
    next_position = max_pos + 1

    # Hash client IP for privacy
    client_ip = request.client.host if request.client else "unknown"
    ip_hash = hash_ip(client_ip)

    # Sanitize user-supplied text fields to prevent XSS
    clean_name = sanitize_text(payload.name)
    clean_referral = sanitize_text(payload.referral_source)
    user_agent = sanitize_text(
        request.headers.get("user-agent", "")[:500], max_length=500
    )

    # Compute email hash for efficient lookups
    email_hash_val = hash_email(normalized_email)

    # Create and persist entry
    entry = WaitlistEntry(
        email=normalized_email,
        email_hash=email_hash_val,
        name=clean_name,
        referral_source=clean_referral,
        queue_position=next_position,
        ip_hash=ip_hash,
        user_agent=user_agent,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    logger.info("New signup: queue_position=%d", next_position)
    return WaitlistSubmitResult(
        success=True,
        message="You have been added to the waitlist!",
        queue_position=next_position,
        is_duplicate=False,
    )


@router.get("/count", response_model=WaitlistCountResponse)
async def get_waitlist_count(db: AsyncSession = Depends(get_db)):
    """Return the total number of signups on the waitlist."""
    result = await db.execute(select(func.count(WaitlistEntry.id)))
    total = result.scalar_one()
    return WaitlistCountResponse(
        total_signups=total,
        message=f"There are {total} people on the waitlist",
    )


@router.get("/position/{email_hash}", response_model=QueuePositionResponse)
async def get_queue_position(email_hash: str, db: AsyncSession = Depends(get_db)):
    """Look up queue position by SHA256 hash of the email.

    Uses pre-computed email_hash column for O(1) lookups.
    Hash must be exactly 64 hex characters (SHA256 output).
    """
    # Validate hash format to prevent abuse
    if len(email_hash) != 64 or not all(c in "0123456789abcdef" for c in email_hash.lower()):
        return QueuePositionResponse(
            found=False,
            email_hash=email_hash[:16] + "...",
            message="Invalid hash format",
        )

    # O(1) lookup via indexed email_hash column
    result = await db.execute(
        select(WaitlistEntry).where(WaitlistEntry.email_hash == email_hash.lower())
    )
    entry = result.scalar_one_or_none()

    if entry:
        return QueuePositionResponse(
            found=True,
            email_hash=email_hash.lower(),
            queue_position=entry.queue_position,
            signup_date=entry.created_at,
            message="Position found",
        )

    return QueuePositionResponse(
        found=False,
        email_hash=email_hash.lower(),
        message="Email not found on waitlist",
    )
