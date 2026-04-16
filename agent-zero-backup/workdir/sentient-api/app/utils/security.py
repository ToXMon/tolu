"""API key authentication, IP hashing, and input sanitization utilities."""

import os
import re
import html
import hashlib
import secrets
import logging
from fastapi import Header, HTTPException, Request

logger = logging.getLogger(__name__)

ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "")

# ── HTML/XSS sanitization ──────────────────────────────────────────
_DANGEROUS_PATTERNS = re.compile(
    r"<(script|iframe|object|embed|form|input|textarea|select|button|"
    r"svg|math|style|link|meta|base|applet|body|html|head)[^>]*>",
    re.IGNORECASE | re.DOTALL,
)
_EVENT_HANDLERS = re.compile(
    r"\bon\w+\s*=", re.IGNORECASE
)
_JS_PROTOCOL = re.compile(
    r"(javascript|vbscript|data)\s*:", re.IGNORECASE
)


def sanitize_text(value: str | None, max_length: int = 255) -> str | None:
    """Sanitize user-supplied text to prevent XSS and injection.

    Strips HTML tags, removes event handlers, escapes HTML entities,
    and truncates to max_length.
    """
    if value is None:
        return None
    value = str(value).strip()
    # Remove dangerous HTML tags
    value = _DANGEROUS_PATTERNS.sub("", value)
    # Remove event handler attributes
    value = _EVENT_HANDLERS.sub("", value)
    # Remove javascript:/data: URLs
    value = _JS_PROTOCOL.sub("", value)
    # HTML-escape remaining content
    value = html.escape(value, quote=True)
    # Truncate
    return value[:max_length]


# ── Hashing ────────────────────────────────────────────────────────

def hash_ip(ip_address: str) -> str:
    """Hash an IP address with SHA256 for GDPR compliance.

    Requires IP_HASH_SALT env var — will raise if not set.
    """
    salt = os.environ.get("IP_HASH_SALT")
    if not salt:
        logger.error("IP_HASH_SALT environment variable not set — cannot hash IPs")
        raise ValueError("IP_HASH_SALT environment variable must be set")
    return hashlib.sha256(f"{salt}:{ip_address}".encode()).hexdigest()


def hash_email(email: str) -> str:
    """Hash an email address with SHA256."""
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()


# ── API key verification ───────────────────────────────────────────

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Dependency to verify admin API key."""
    if not ADMIN_API_KEY:
        logger.error("ADMIN_API_KEY environment variable not set")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable"
        )
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key


def get_client_ip(request: Request) -> str:
    """Extract client IP from request.

    Only trusts X-Forwarded-For from the first hop (proxy).
    Falls back to direct connection IP.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Only trust the last entry (set by our immediate proxy)
        return forwarded.split(",")[-1].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "unknown"
