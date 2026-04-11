# Refresh Upload URLs

`POST /api/v1/publish/:slug/uploads/refresh` (alias: `POST /api/v1/artifact/:slug/uploads/refresh`)

Requires `Authorization: Bearer <API_KEY>`.

Returns fresh presigned URLs for a pending upload (same version). Use when URLs expire mid-upload.
