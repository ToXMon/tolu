"""Sentient Waitlist API — FastAPI application entry point."""

import logging
import time
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import init_db, shutdown_db
from app.routers import waitlist, admin
from app.schemas import HealthResponse

# ── Structured logging ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("sentient-api")

VERSION = "1.1.0"
START_TIME: float = 0.0

# ── Allowed CORS origins (locked down) ────────────────────────────
ALLOWED_ORIGINS = [
    "https://sentient.fyi",
    "https://www.sentient.fyi",
    "https://here.now",
]

# Dev-only origins (strip in production)
import os
if os.environ.get("ENABLE_DEV_CORS", "false").lower() == "true":
    ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://localhost:8000",
    ])

# ── Rate limiter (10 req/min per IP, stricter on admin) ─────────────
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10/minute"],
    headers_enabled=True,
)


# ── Lifespan (startup / shutdown) ──────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global START_TIME
    START_TIME = time.time()
    logger.info("Sentient Waitlist API v%s starting up", VERSION)
    await init_db()
    yield
    await shutdown_db()
    logger.info("Sentient Waitlist API shut down")


# ── App factory ────────────────────────────────────────────────────
app = FastAPI(
    title="Sentient Waitlist API",
    description="Waitlist management API for sentient.fyi",
    version=VERSION,
    lifespan=lifespan,
    docs_url=None,       # Disable /docs in production
    redoc_url=None,      # Disable /redoc in production
    openapi_url=None,    # Disable /openapi.json in production
)

# ── Re-enable docs only with explicit env flag ─────────────────────
if os.environ.get("ENABLE_DOCS", "false").lower() == "true":
    app.docs_url = "/docs"
    app.redoc_url = "/redoc"
    app.openapi_url = "/openapi.json"

# Rate-limit state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ── Security headers middleware ────────────────────────────────────
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "accelerometer=(), camera=(), geolocation=(), "
        "gyroscope=(), magnetometer=(), microphone=(), "
        "payment=(), usb=()"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; frame-ancestors 'none'"
    )
    # HSTS only if served over TLS (proxied via here.now)
    if request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https":
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )
    # Remove server identification
    response.headers["Server"] = "sentient-api"
    return response


# ── Request body size limit (1MB) ─────────────────────────────────
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 1_048_576:  # 1MB
        return JSONResponse(
            status_code=413,
            content={"error": "Request too large", "detail": "Maximum request size is 1MB"},
        )
    return await call_next(request)


# ── Production-safe error handler ──────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception on %s %s: %s",
        request.method, request.url.path, str(exc),
    )
    # Never leak stack traces to clients
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


# ── CORS (strict) ──────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Only needed methods
    allow_headers=["Content-Type", "X-API-Key"],  # Only needed headers
    max_age=3600,
)

# Routers
app.include_router(waitlist.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


# ── Health check ───────────────────────────────────────────────────
@app.get("/api/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Return service health, version, and uptime."""
    uptime = time.time() - START_TIME if START_TIME else 0.0
    return HealthResponse(
        status="healthy",
        version=VERSION,
        database="connected",
        uptime_seconds=round(uptime, 2),
    )
