# Claim an Anonymous Site

`POST /api/v1/publish/:slug/claim` (alias: `POST /api/v1/artifact/:slug/claim`)

Requires `Authorization: Bearer <API_KEY>`.

## Request Body
```json
{ "claimToken": "abc123..." }
```

Transfers ownership and removes the expiration. Users can also claim by visiting the `claimUrl` and signing in.
