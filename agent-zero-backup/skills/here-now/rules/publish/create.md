# Create a Site

`POST /api/v1/publish` (alias: `POST /api/v1/artifact`)

## Request Body

```json
{
  "files": [
    { "path": "index.html", "size": 1234, "contentType": "text/html; charset=utf-8", "hash": "a1b2c3d4..." },
    { "path": "assets/app.js", "size": 999, "contentType": "text/javascript; charset=utf-8", "hash": "e5f6a7b8..." }
  ],
  "ttlSeconds": null,
  "spaMode": true,
  "forkable": true,
  "viewer": {
    "title": "My site",
    "description": "Published by an agent",
    "ogImagePath": "assets/cover.png"
  }
}
```

### Fields
- `files` (required): array of `{ path, size, contentType, hash }`
  - Paths must be relative to site root (no parent directory prefix)
  - `hash` (optional): SHA-256 hex digest for incremental deploys
- `ttlSeconds` (optional): expiry in seconds. Ignored for anonymous sites.
- `spaMode` (optional): enable SPA routing
- `forkable` (optional): enable fork button
- `viewer` (optional): metadata for auto-viewer pages

## Response (Authenticated)
```json
{
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "upload": {
    "versionId": "01J...",
    "uploads": [{ "path": "index.html", "method": "PUT", "url": "https://<presigned-url>", "headers": { "Content-Type": "text/html; charset=utf-8" } }],
    "skipped": ["assets/app.js"],
    "finalizeUrl": "https://here.now/api/v1/publish/bright-canvas-a7k2/finalize",
    "expiresInSeconds": 3600
  }
}
```

## Response (Anonymous) — additional fields
```json
{
  "claimToken": "abc123...",
  "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123...",
  "expiresAt": "2026-02-19T01:00:00.000Z",
  "anonymous": true,
  "warning": "IMPORTANT: Save the claimToken and claimUrl..."
}
```

**IMPORTANT**: `claimToken` and `claimUrl` are returned only once. Save immediately.
