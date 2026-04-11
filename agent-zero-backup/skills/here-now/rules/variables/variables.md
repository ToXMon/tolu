# Service Variables

Store API keys and secrets on your account for use in proxy routes.

## Create or Update
`PUT /api/v1/me/variables/:name`

Requires `Authorization: Bearer <API_KEY>`.

```json
{
  "value": "sk-or-v1-abc123",
  "allowedUpstreams": ["openrouter.ai"]
}
```

- Names: uppercase letters, digits, underscores, starting with a letter
- Max 50 variables per account, 4 KB per value
- `allowedUpstreams`: restrict which upstream domains the variable can be sent to (optional)

## List Variables
`GET /api/v1/me/variables` — returns names, upstream pinning, timestamps. Values are never returned.

## Delete Variable
`DELETE /api/v1/me/variables/:name`
