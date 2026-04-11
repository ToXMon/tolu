# Custom Domains

Bring your own domain and serve sites from it.

## Endpoints
- `POST /api/v1/domains` — add domain
- `GET /api/v1/domains` — list domains
- `GET /api/v1/domains/:domain` — check status
- `DELETE /api/v1/domains/:domain` — remove domain

## Add Domain
```bash
curl -sS https://here.now/api/v1/domains \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

## DNS Configuration

**Subdomains** (e.g. `docs.example.com`):
- Add CNAME record pointing to `fallback.here.now`

**Apex domains** (e.g. `example.com`):
1. Add ALIAS record pointing to `fallback.here.now` (provider may call ANAME or CNAME flattening)
2. Add TXT record from `ownership_verification` object

## SSL
Provisioned automatically once DNS is verified. Status is `pending` until verified, then `active`.

## Limits
- Free plan: 1 domain
- Hobby plan: up to 5 domains
