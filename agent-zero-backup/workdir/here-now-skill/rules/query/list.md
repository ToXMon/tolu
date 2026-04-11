# List Sites

`GET /api/v1/publishes` (alias: `GET /api/v1/artifacts`)

Requires `Authorization: Bearer <API_KEY>`.

## Response
```json
{
  "publishes": [
    {
      "slug": "bright-canvas-a7k2",
      "siteUrl": "https://bright-canvas-a7k2.here.now/",
      "updatedAt": "2026-02-18T...",
      "expiresAt": null,
      "status": "active",
      "currentVersionId": "01J...",
      "pendingVersionId": null
    }
  ]
}
```
