"""SQLAlchemy models for Sentient Waitlist API."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.database import Base


def _utcnow() -> datetime:
    """Return timezone-aware UTC now (replaces deprecated datetime.utcnow)."""
    return datetime.now(timezone.utc)


class WaitlistEntry(Base):
    """Waitlist signup entry."""
    __tablename__ = "waitlist_entries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    email_hash = Column(String(64), unique=True, nullable=True, index=True)
    name = Column(String(255), nullable=True)
    referral_source = Column(String(255), nullable=True)
    queue_position = Column(Integer, unique=True, nullable=False)
    ip_hash = Column(String(64), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_utcnow, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
