# Duplicate a Site

`POST /api/v1/publish/:slug/duplicate`

Creates a complete server-side copy under a new slug. All files copied server-side — no client upload or finalize needed. Immediately live.

Requires `Authorization: Bearer <API_KEY>` (must own the source site).

## Optional Request Body
```json
{
  "viewer": {
    "title": "My Copy",
    "description": "Copy of bright-canvas-a7k2"
  }
}
```

`viewer` is shallow-merged with source. Only provided fields are overridden.

## Response
```json
{
  "slug": "warm-lake-f3k9",
  "siteUrl": "https://warm-lake-f3k9.here.now/",
  "sourceSlug": "bright-canvas-a7k2",
  "status": "active",
  "currentVersionId": "01J...",
  "filesCount": 36
}
```

## Notes
- Copies all files and viewer metadata
- Does NOT copy password, handle/domain links, or TTL
