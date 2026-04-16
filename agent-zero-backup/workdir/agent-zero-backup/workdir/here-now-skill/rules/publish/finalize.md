# Finalize a Publish

`POST /api/v1/publish/:slug/finalize` (alias: `POST /api/v1/artifact/:slug/finalize`)

## Request Body
```json
{ "versionId": "01J..." }
```

## Auth
- Owned sites: requires `Authorization: Bearer <API_KEY>`
- Anonymous sites: no auth needed

## Response
```json
{
  "success": true,
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "previousVersionId": null,
  "currentVersionId": "01J..."
}
```
