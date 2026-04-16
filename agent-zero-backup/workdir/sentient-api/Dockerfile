# ── Stage 1: Builder ──────────────────────────────────────────────
FROM python:3.11-alpine AS builder

RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ──────────────────────────────────────────────
FROM python:3.11-alpine

RUN apk add --no-cache curl tini

COPY --from=builder /install /usr/local

WORKDIR /app
COPY app/ ./app/

RUN adduser -D -s /bin/sh sentient \
    && mkdir -p /data \
    && chown sentient:sentient /data

# Security: run as non-root
USER sentient

# Persistent data volume
VOLUME ["/data"]

EXPOSE 8000

# Security: health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Security: use tini as PID 1 to handle signals properly
ENTRYPOINT ["/sbin/tini", "--"]

# Security: resource-conscious uvicorn config
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--timeout-keep-alive", "5", \
     "--limit-max-header-size", "16384", \
     "--limit-concurrency", "50"]
