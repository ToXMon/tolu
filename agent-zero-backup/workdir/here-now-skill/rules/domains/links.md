# Links

Links connect a site to a location on your handle or custom domain.

## Endpoints
- `POST /api/v1/links` — create link
- `GET /api/v1/links` — list links
- `GET /api/v1/links/:location` — get link
- `PATCH /api/v1/links/:location` — update link
- `DELETE /api/v1/links/:location` — delete link

## Link to Handle
```json
{"location": "docs", "slug": "bright-canvas-a7k2"}
```

## Link to Custom Domain
```json
{"location": "", "slug": "bright-canvas-a7k2", "domain": "example.com"}
```

## Root Location
- Use `"location": ""` in request body
- Use `__root__` in path params: `/api/v1/links/__root__`

## Delete from Custom Domain
Add `?domain=example.com` as query parameter.

## Propagation
Updates written to Cloudflare KV — can take up to 60 seconds to propagate globally.
