# Upload Files

For each entry in `upload.uploads[]`, PUT the file to the presigned URL:

```bash
curl -X PUT "<presigned-url>" \
  -H "Content-Type: <content-type>" \
  --data-binary @<local-file>
```

## Notes
- Uploads can run in parallel
- Presigned URLs are valid for 1 hour
- Files in `upload.skipped[]` don't need uploading (hash matched previous version)
- Use `Content-Type` from the upload entry headers
