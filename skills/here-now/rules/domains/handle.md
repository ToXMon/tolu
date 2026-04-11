# Handle Management

A handle gives you a stable subdomain like `yourname.here.now`.

## Endpoints
- `POST /api/v1/handle` — create handle
- `GET /api/v1/handle` — get current handle
- `PATCH /api/v1/handle` — update handle
- `DELETE /api/v1/handle` — delete handle

## Create Request
```json
{"handle": "yourname"}
```

## Create Response
```json
{
  "handle": "yourname",
  "hostname": "yourname.here.now"
}
```

## Rules
- Handle format: lowercase letters/numbers/hyphens, 2-30 chars, no leading/trailing hyphens
- Changing a handle keeps the same namespace, links move automatically
- Deleting a handle removes the namespace and its links
- Requires paid plan (Hobby or above)
