# Patch Metadata

`PATCH /api/v1/publish/:slug/metadata` (alias: `PATCH /api/v1/artifact/:slug/metadata`)

Requires `Authorization: Bearer <API_KEY>`.

## Request Body (all fields optional)
```json
{
  "ttlSeconds": 604800,
  "viewer": {
    "title": "Updated title",
    "description": "New description",
    "ogImagePath": "assets/cover.png"
  },
  "password": "secret123",
  "price": {"amount": "0.50", "currency": "USD"},
  "forkable": true,
  "spaMode": true
}
```

## Fields
- `ttlSeconds`: expiry in seconds
- `viewer`: metadata for auto-viewer. `ogImagePath` must reference an image within the site.
- `password`: string to set, `null` to remove
- `price`: object to set, `null` to remove. Requires wallet address.
- `forkable`: boolean
- `spaMode`: boolean

## Mutual Exclusivity
- Password and price are mutually exclusive
- Forkable is mutually exclusive with both password and price
