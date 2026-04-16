# Sentient Waitlist API

Production-ready waitlist management API for [sentient.fyi](https://sentient.fyi). Built with FastAPI, async SQLAlchemy, and designed for decentralized deployment on Akash Network with here.now reverse proxy.

## Architecture

```
                          ┌──────────────────┐
                          │   here.now proxy  │
                          │  (reverse proxy)  │
                          └────────┬──────────┘
                                   │
                          ┌────────▼──────────┐
                          │   Akash Network    │
                          │  ┌──────────────┐  │
                          │  │ sentient-api  │  │
                          │  │  (FastAPI)    │  │
                          │  │              │  │
                          │  │ ┌──────────┐ │  │
                          │  │ │  SQLite   │ │  │
                          │  │ │ (/data)   │ │  │
                          │  │ └──────────┘ │  │
                          │  └──────────────┘  │
                          └────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                     │
     ┌────────▼───────┐  ┌────────▼───────┐  ┌─────────▼──────┐
     │  /api/waitlist  │  │  /api/admin/*  │  │ /api/health     │
     │  (public)       │  │  (API key)     │  │ (public)        │
     └────────────────┘  └────────────────┘  └────────────────┘
```

### Stack

| Layer       | Technology                    |
|-------------|-------------------------------|
| Framework   | FastAPI 0.109                 |
| Database    | SQLite via aiosqlite          |
| ORM         | SQLAlchemy 2.0 (async)        |
| Validation  | Pydantic v2 + email + DNS     |
| Rate Limit  | slowapi (10 req/min per IP)   |
| Deployment  | Docker → Akash Network        |
| Proxy       | here.now → Akash endpoint     |

## Quick Start (Local Development)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ADMIN_API_KEY="your-secret-key-here"
export DB_DIR="/tmp"  # Optional: defaults to /data

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API will be available at `http://localhost:8000`. Interactive docs at `/docs`.

## Docker

### Build

```bash
docker build -t sentient-api:1.0.0 .
```

### Run

```bash
docker run -d \
  --name sentient-api \
  -p 8000:8000 \
  -e ADMIN_API_KEY="your-secret-key" \
  -v sentient-data:/data \
  sentient-api:1.0.0
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

## Akash Deployment

### Prerequisites

- [Akash CLI](https://docs.akash.network/guides/install) installed and configured
- Sufficient AKT/USDC in wallet
- Docker image pushed to a registry accessible by Akash

### Deploy Steps

1. **Push image to registry** (example with Docker Hub):
   ```bash
   docker tag sentient-api:1.0.0 youruser/sentient-api:1.0.0
   docker push youruser/sentient-api:1.0.0
   ```

2. **Update `deploy.yaml`** — Change the image reference and set `ADMIN_API_KEY`:
   ```yaml
   services:
     sentient-api:
       image: youruser/sentient-api:1.0.0
       env:
         - "ADMIN_API_KEY=<your-strong-random-key>"
   ```

3. **Create deployment**:
   ```bash
   akash tx deployment create deploy.yaml --from your-key
   ```

4. **Get the Akash endpoint** from the lease:
   ```bash
   akash provider lease-status --from your-key
   ```

5. **Update here.now proxy** — Replace `AKASH_ENDPOINT` in `.herenow/proxy.json` with the actual Akash provider URI.

## Environment Variables

| Variable        | Required | Default                     | Description                        |
|-----------------|----------|-----------------------------|------------------------------------|
| `ADMIN_API_KEY` | Yes      | —                           | API key for admin endpoints        |
| `DB_DIR`        | No       | `/data`                     | Directory for SQLite database file |
| `IP_HASH_SALT`  | No       | `sentient-waitlist-2024`    | Salt for IP address hashing        |

## API Reference

### Public Endpoints

#### `POST /api/waitlist`
Submit an email to the waitlist.

```bash
curl -X POST http://localhost:8000/api/waitlist \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "Alice", "referral_source": "twitter"}'
```

**Response** (`201 Created`):
```json
{
  "success": true,
  "message": "You have been added to the waitlist!",
  "queue_position": 42,
  "is_duplicate": false
}
```

#### `GET /api/waitlist/count`
Get total signup count.

```bash
curl http://localhost:8000/api/waitlist/count
```

**Response**:
```json
{
  "total_signups": 1500,
  "message": "There are 1500 people on the waitlist"
}
```

#### `GET /api/waitlist/position/{email_hash}`
Look up queue position by SHA256 hash of the email.

```bash
# First compute the hash
EMAIL_HASH=$(echo -n "user@example.com" | openssl dgst -sha256 | cut -d' ' -f2)
curl http://localhost:8000/api/waitlist/position/$EMAIL_HASH
```

**Response**:
```json
{
  "found": true,
  "email_hash": "a3c2b...",
  "queue_position": 42,
  "signup_date": "2024-01-15T10:30:00",
  "message": "Position found"
}
```

#### `GET /api/health`
Service health check.

```bash
curl http://localhost:8000/api/health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "uptime_seconds": 3600.0
}
```

### Admin Endpoints (API Key Required)

All admin endpoints require the `X-API-Key` header.

#### `GET /api/admin/waitlist`
List all signups (paginated).

```bash
curl -H "X-API-Key: your-secret-key" \
  "http://localhost:8000/api/admin/waitlist?limit=50&offset=0"
```

#### `GET /api/admin/waitlist/export`
Export all signups as CSV.

```bash
curl -H "X-API-Key: your-secret-key" \
  -o waitlist.csv \
  "http://localhost:8000/api/admin/waitlist/export"
```

#### `DELETE /api/admin/waitlist/{signup_id}`
Remove a signup by ID.

```bash
curl -X DELETE -H "X-API-Key: your-secret-key" \
  "http://localhost:8000/api/admin/waitlist/5"
```

## here.now Proxy Setup

The `.herenow/proxy.json` file configures the here.now reverse proxy to route traffic from `here.now/api/waitlist` and `here.now/api/health` to the Akash deployment.

### Setup

1. Deploy to Akash and obtain the provider endpoint URI
2. Edit `.herenow/proxy.json` — replace `AKASH_ENDPOINT` with the real URI
3. Deploy the proxy configuration to here.now

Example with resolved endpoint:
```json
{
  "routes": [
    {
      "path": "/api/waitlist",
      "target": "http://provider.akash.world:8000/api/waitlist",
      "methods": ["GET", "POST"]
    },
    {
      "path": "/api/health",
      "target": "http://provider.akash.world:8000/api/health",
      "methods": ["GET"]
    }
  ]
}
```

## Security Notes

- **IP hashing**: Client IPs are SHA256-hashed with a configurable salt before storage (GDPR-friendly)
- **Email position lookup**: Uses SHA256 hash of email — emails are never exposed by the position endpoint
- **Admin protection**: All `/api/admin/*` endpoints require a valid `X-API-Key` header, verified with constant-time comparison
- **Rate limiting**: 10 requests per minute per IP to prevent abuse
- **CORS**: Restricted to known origins (localhost, sentient.fyi, here.now)
- **Non-root container**: Docker image runs as `sentient` user, not root
- **API key**: Must be set via `ADMIN_API_KEY` environment variable; admin endpoints return 503 if not configured
- **No sensitive logging**: Emails are logged only in edge cases (duplicate, invalid); IPs are never logged

## Project Structure

```
sentient-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, rate limit, lifespan
│   ├── database.py           # Async SQLAlchemy engine + sessions
│   ├── models.py             # WaitlistEntry model
│   ├── schemas.py            # Pydantic v2 request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── waitlist.py       # Public waitlist endpoints
│   │   └── admin.py          # Admin CRUD endpoints
│   └── utils/
│       ├── __init__.py
│       ├── validation.py     # Email validation (regex + MX)
│       └── security.py       # API key auth, IP/email hashing
├── .herenow/
│   └── proxy.json            # here.now reverse proxy config
├── Dockerfile                # Multi-stage production build
├── deploy.yaml               # Akash Network SDL
├── requirements.txt          # Python dependencies
└── README.md
```

## License

Proprietary — sentient.fyi
