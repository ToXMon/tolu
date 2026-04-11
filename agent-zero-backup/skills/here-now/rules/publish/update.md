# Update an Existing Site

`PUT /api/v1/publish/:slug` (alias: `PUT /api/v1/artifact/:slug`)

Same request body as create. Returns new presigned upload URLs and a new `finalizeUrl`.

## Auth
- **Owned sites**: requires `Authorization: Bearer <API_KEY>`
- **Anonymous sites**: include `claimToken` in the request body

## Incremental Deploys
Include `hash` (SHA-256 hex) on each file. Files whose hash matches the previous version appear in `upload.skipped[]` instead of `upload.uploads[]` — no upload needed. The server copies them at finalize.

## Note
Updates do not extend the expiration for anonymous sites.
