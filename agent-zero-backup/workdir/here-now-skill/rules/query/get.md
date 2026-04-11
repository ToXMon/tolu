# Get Site Details

`GET /api/v1/publish/:slug` (alias: `GET /api/v1/artifact/:slug`)

Requires `Authorization: Bearer <API_KEY>` (owner only).

## Response
```json
{
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "status": "active",
  "createdAt": "2026-02-18T...",
  "updatedAt": "2026-02-18T...",
  "expiresAt": null,
  "currentVersionId": "01J...",
  "pendingVersionId": null,
  "manifest": [
    {"path": "index.html", "size": 1234, "contentType": "text/html; charset=utf-8", "hash": "a1b2c3d4..."},
    {"path": "assets/app.js", "size": 999, "contentType": "text/javascript; charset=utf-8", "hash": "e5f6a7b8..."}
  ]
}
```

File contents can be fetched from the live `siteUrl` (e.g. `https://bright-canvas-a7k2.here.now/index.html`).
