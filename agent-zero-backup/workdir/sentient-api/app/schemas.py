"""Pydantic v2 schemas for Sentient Waitlist API."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ── Request schemas ──

class WaitlistSubmit(BaseModel):
    email: EmailStr
    name: Optional[str] = Field(None, max_length=255)
    referral_source: Optional[str] = Field(None, max_length=255)


# ── Response schemas ──

class WaitlistResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    referral_source: Optional[str] = None
    queue_position: int
    verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class WaitlistSubmitResult(BaseModel):
    success: bool
    message: str
    queue_position: Optional[int] = None
    is_duplicate: bool = False


class WaitlistCountResponse(BaseModel):
    total_signups: int
    message: str = ""


class QueuePositionResponse(BaseModel):
    found: bool
    email_hash: str
    queue_position: Optional[int] = None
    signup_date: Optional[datetime] = None
    message: str = ""


class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    uptime_seconds: float = 0.0


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int = 500
