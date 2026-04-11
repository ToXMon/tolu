# here.now Platform Knowledge

## What is here.now?
here.now is free, instant web hosting for agents. Publish any file or folder and get a live URL at `<slug>.here.now`.

## Key Concepts

### Publishing Flow
1. **Create** (`POST /api/v1/publish`) — declare files, get presigned upload URLs
2. **Upload** (`PUT <presigned-url>`) — upload each file to its presigned URL
3. **Finalize** (`POST /api/v1/publish/:slug/finalize`) — activate the site

### Authentication Modes
- **Anonymous**: No auth header. Sites expire in 24h. Response includes `claimToken`/`claimUrl`.
- **Authenticated**: `Authorization: Bearer <API_KEY>`. Sites are permanent.

### API Key Storage
- Recommended: `~/.herenow/credentials` file (chmod 600)
- Alt: `$HERENOW_API_KEY` env var
- Alt: `--api-key` flag

### Incremental Deploys
Include SHA-256 `hash` on each file. Unchanged files appear in `skipped[]` — no re-upload needed.

### Site Features
- **Password protection**: Server-side enforcement, survives redeploys
- **Payment gating**: Stablecoin payments via Tempo network
- **SPA routing**: Unknown paths serve `index.html`
- **Forkable**: Others can download and remix your site
- **Duplicate**: Server-side copy to new slug
- **Custom domains**: Bring your own domain with CNAME/ALIAS DNS
- **Handles**: Stable subdomain like `yourname.here.now`
- **Proxy routes**: `.herenow/proxy.json` for server-side API proxying with secret variables
- **Service variables**: Store API keys securely, reference as `${VAR_NAME}` in proxy manifests

### Limits
| Feature | Anonymous | Authenticated |
|---------|-----------|---------------|
| Max file size | 250 MB | 5 GB |
| Expiry | 24 hours | Permanent |
| Sites | — | 500 free |
| Rate limit | 5/hour/IP | 60/hour free |

## Critical Rules
1. **Always save `claimToken` and `claimUrl` immediately** — returned only once
2. **Paths must be relative to site root** — no parent directory prefix
3. **Password, payment, and forkable are mutually exclusive**
4. **Proxy routes require authenticated sites**

## API Endpoints Quick Reference
- `POST /api/v1/publish` — create site
- `PUT /api/v1/publish/:slug` — update site
- `POST /api/v1/publish/:slug/finalize` — finalize
- `DELETE /api/v1/publish/:slug` — delete
- `POST /api/v1/publish/:slug/claim` — claim anonymous
- `POST /api/v1/publish/:slug/duplicate` — duplicate
- `PATCH /api/v1/publish/:slug/metadata` — patch metadata
- `GET /api/v1/publishes` — list sites
- `GET /api/v1/publish/:slug` — get site details
- `PUT /api/v1/me/variables/:name` — create/update variable
- `POST /api/v1/handle` — create handle
- `POST /api/v1/domains` — add custom domain
- `POST /api/v1/links` — create link

## Skill Location
`/a0/usr/workdir/tolu/skills/here-now/` — SKILL.md with 24 rule files
