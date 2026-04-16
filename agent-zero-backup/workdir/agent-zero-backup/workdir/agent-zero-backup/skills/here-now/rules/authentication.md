# Authentication

Two modes of authentication:

## Anonymous
- Omit the Authorization header
- Sites expire in 24 hours with lower limits
- Response includes `claimToken` and `claimUrl` (save immediately!)

## Authenticated
- Include `Authorization: Bearer <API_KEY>` header
- Sites are permanent (or custom TTL)
- Higher limits (see limits reference)

## Getting an API Key

### Option A: Agent-assisted sign-up
```bash
# Request code to email
curl -sS https://here.now/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'

# Verify code, receive API key
curl -sS https://here.now/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```
New emails create accounts automatically.

### Option B: Dashboard sign-up
Sign in at https://here.now and copy the API key from the dashboard.

## Storing the API Key
```bash
mkdir -p ~/.herenow && echo "<API_KEY>" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

Key resolution order (first match wins):
1. `--api-key` flag (CI/scripting only)
2. `$HERENOW_API_KEY` environment variable
3. `~/.herenow/credentials` file (recommended)

## Attribution Header
Optional: `X-HereNow-Client: <agent>/<tool>` for debugging reliability.
