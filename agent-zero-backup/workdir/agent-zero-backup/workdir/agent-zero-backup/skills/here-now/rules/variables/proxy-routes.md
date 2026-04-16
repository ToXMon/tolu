# Proxy Routes

Sites can make authenticated API calls to external services via a `.herenow/proxy.json` manifest.

## Manifest Structure
```json
{
  "proxies": {
    "/api/chat": {
      "upstream": "https://openrouter.ai/api/v1/chat/completions",
      "method": "POST",
      "headers": {
        "Authorization": "Bearer ${OPENROUTER_API_KEY}"
      }
    },
    "/api/db/*": {
      "upstream": "https://xyz.supabase.co/rest/v1",
      "headers": {
        "apikey": "${SUPABASE_KEY}"
      }
    }
  }
}
```

## Path Matching
- Exact paths (`/api/chat`) match that path only
- Prefix patterns (`/api/db/*`) match any path starting with that prefix — rest appended to upstream
- Query parameters forwarded automatically

## Variable Resolution
`${VAR_NAME}` references resolved from account's variables at request time.

## Headers
`Content-Type` and `Accept` forwarded from browser automatically. Manifest only needs auth headers.

## Requirements & Limits
- Requires authenticated site
- Rate limit: 100 requests/hour/IP (overridable per route with `"rateLimit": "20/hour/ip"`)
- Request body limit: 10 MB
- `.herenow/proxy.json` is never served to visitors
- Streaming (SSE) works out of the box
