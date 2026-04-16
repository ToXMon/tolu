"""Email validation utilities with regex and optional MX record verification."""

import re
import logging

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)


def validate_email_syntax(email: str) -> bool:
    """Validate email format using regex."""
    if not email or len(email) > 320:
        return False
    return bool(EMAIL_REGEX.match(email))


def verify_mx_records(domain: str) -> bool:
    """Check if domain has valid MX or A records."""
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX")
        return len(answers) > 0
    except ImportError:
        logger.warning("dnspython not installed, skipping MX verification")
        return True
    except Exception:
        try:
            import dns.resolver
            dns.resolver.resolve(domain, "A")
            return True
        except Exception:
            return False


def is_valid_email(email: str, check_mx: bool = True) -> tuple:
    """Full email validation. Returns (is_valid, reason)."""
    email = email.strip().lower()
    if not email:
        return False, "Email is required"
    if not validate_email_syntax(email):
        return False, "Invalid email format"
    if check_mx:
        domain = email.split("@")[1]
        if not verify_mx_records(domain):
            return False, "Email domain has no valid mail records"
    return True, "Valid"
