# SPA Routing

For single-page applications (React, Vue, Svelte), enable SPA mode so unknown paths serve `index.html` instead of 404.

## Enable at Publish Time
```json
{"spaMode": true}
```

## Enable on Existing Site
```bash
curl -sS -X PATCH https://here.now/api/v1/publish/$SLUG/metadata \
  -H "Authorization: Bearer $API_KEY" \
  -H "content-type: application/json" \
  -d '{"spaMode": true}'
```

## Notes
- Static assets resolve normally — only unmatched paths fall through to index.html
- Use root-relative asset paths (`/assets/app.js`)
- Vite and Create React App do this by default
- Works with root `index.html` and subdirectory-based structures
