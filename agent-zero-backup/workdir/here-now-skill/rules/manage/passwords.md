# Password Protection

Add a password to any site so visitors must authenticate before viewing. Server-side enforcement — content is never sent to the browser until the password is verified.

## Set/Change Password
```bash
curl -sS -X PATCH https://here.now/api/v1/publish/$SLUG/metadata \
  -H "Authorization: Bearer $API_KEY" \
  -H "content-type: application/json" \
  -d '{"password": "secret"}'
```

## Remove Password
```bash
d '{"password": null}'
```

## Notes
- Password protection survives redeploys (it's metadata, not content)
- Changing/removing password immediately invalidates all existing sessions
- Requires an authenticated site (anonymous sites cannot be password-protected)
- Mutually exclusive with payment gating and forkable
