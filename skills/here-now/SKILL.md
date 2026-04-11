---
name: here-now
description: >
  Publish static sites instantly via the here.now hosting platform.
  Covers creating, uploading, finalizing, updating, and managing sites
  with authentication, password protection, payment gating, custom domains,
  proxy routes, service variables, forking, and SPA routing.
  Use for "publish site", "deploy static", "here.now", "instant hosting",
  "herenow", or "quick deploy".
license: MIT
metadata:
  author: baktun14
  version: "1.0.0"
  argument-hint: <task-description>
---

# here.now Skill

Instant web hosting for agents. Publish any file or folder and get a live URL at `<slug>.here.now`.

## Capabilities

| Area | Description |
|------|-------------|
| **Publish** | Create, upload, and finalize static sites |
| **Update** | Incremental deploys with SHA-256 hash-based file skipping |
| **Auth** | Anonymous (24h expiry) or authenticated (permanent) sites |
| **Manage** | Password protection, payment gating, duplicate, delete |
| **Domains** | Handles, custom domains, and links |
| **Proxy** | Server-side proxy routes with secret variable injection |
| **Variables** | Store API keys securely for proxy route use |
| **Forks** | Enable remixing with forkable sites |
| **SPA** | Single-page application routing support |

## Critical Rules

**Always save `claimToken` and `claimUrl` for anonymous sites.** They are returned only once and cannot be recovered.

```python
# CORRECT - save claim info immediately
response = create_site(files)
save_claim(response["claimToken"], response["claimUrl"])

# WRONG - losing the claim token means the site expires in 24h with no recovery
```

**Use `~/.herenow/credentials` for API keys.** Never hardcode keys in scripts.

```bash
# CORRECT
mkdir -p ~/.herenow && echo "$API_KEY" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials

# WRONG
curl -H "Authorization: Bearer sk-hardcoded-key-in-script"
```

**Paths must be relative to site root.** Do not prefix with parent directories.

```json
// CORRECT
{"path": "index.html"}
{"path": "assets/app.js"}

// WRONG
{"path": "my-project/index.html"}
```

## Quick Reference

### Three-Step Publish

```bash
# 1. Create site (get presigned URLs)
curl -sS https://here.now/api/v1/publish \
  -H "X-HereNow-Client: agent-zero/skill" \
  -H "content-type: application/json" \
  -d '{"files": [{"path":"index.html","size":1234,"contentType":"text/html; charset=utf-8"}]}'

# 2. Upload file to presigned URL
curl -X PUT "$UPLOAD_URL" \
  -H "Content-Type: text/html; charset=utf-8" \
  --data-binary @index.html

# 3. Finalize
curl -sS -X POST "$FINALIZE_URL" \
  -H "content-type: application/json" \
  -d '{"versionId":"$VERSION_ID"}'
```

### Authentication Header

```bash
# Authenticated (permanent sites)
-H "Authorization: Bearer $API_KEY"

# Anonymous (24h expiry, no header needed)
# Response includes claimToken + claimUrl
```

### API Key Retrieval

```bash
# Step 1: Request code to email
curl -sS https://here.now/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com"}'

# Step 2: Verify code, get API key
curl -sS https://here.now/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```

## Documentation Structure

### Core Concepts
- **@rules/overview.md** - Platform overview, URL structure, serving rules
- **@rules/authentication.md** - Auth modes, API key management, storage

### Publishing
- **@rules/publish/create.md** - Create site, request body, response fields
- **@rules/publish/upload.md** - Upload files to presigned URLs
- **@rules/publish/finalize.md** - Finalize a publish/version
- **@rules/publish/update.md** - Update existing sites, incremental deploys
- **@rules/publish/delete.md** - Delete sites

### Site Management
- **@rules/manage/claim.md** - Claim anonymous sites
- **@rules/manage/passwords.md** - Password protection
- **@rules/manage/payment.md** - Payment gating with stablecoins
- **@rules/manage/duplicate.md** - Server-side site duplication
- **@rules/manage/forks.md** - Forkable sites and remixing
- **@rules/manage/spa.md** - SPA routing for React/Vue/Svelte
- **@rules/manage/metadata.md** - Patch metadata (title, description, TTL)

### Querying
- **@rules/query/list.md** - List owned sites
- **@rules/query/get.md** - Get site details and manifest
- **@rules/query/refresh.md** - Refresh expired upload URLs

### Variables & Proxy
- **@rules/variables/variables.md** - Create, list, delete service variables
- **@rules/variables/proxy-routes.md** - Proxy route manifest and configuration

### Domains & Links
- **@rules/domains/handle.md** - Handle subdomain management
- **@rules/domains/custom-domains.md** - Bring your own domain
- **@rules/domains/links.md** - Link sites to handle/domain locations

### Reference
- **@rules/reference/limits.md** - Anonymous vs authenticated limits
- **@rules/reference/endpoints.md** - Full API endpoint reference

## Common Patterns

### Incremental Deploy (skip unchanged files)
```bash
# Include SHA-256 hash for each file
curl -sS https://here.now/api/v1/publish \
  -H "Authorization: Bearer $API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "files": [
      {"path":"index.html","size":1234,"contentType":"text/html; charset=utf-8","hash":"a1b2c3d4..."},
      {"path":"assets/app.js","size":999,"contentType":"text/javascript; charset=utf-8","hash":"e5f6a7b8..."}
    ]
  }'
# Unchanged files appear in upload.skipped[] — no upload needed
```

### Proxy Route with Secret Variables
```json
// .herenow/proxy.json
{
  "proxies": {
    "/api/chat": {
      "upstream": "https://openrouter.ai/api/v1/chat/completions",
      "method": "POST",
      "headers": {
        "Authorization": "Bearer ${OPENROUTER_API_KEY}"
      }
    }
  }
}
```

### Password Protect a Site
```bash
curl -sS -X PATCH https://here.now/api/v1/publish/$SLUG/metadata \
  -H "Authorization: Bearer $API_KEY" \
  -H "content-type: application/json" \
  -d '{"password": "secret123"}'
```

## Additional Resources

- **[here.now docs](https://here.now/docs)** - Official documentation
- **[Skill repo](https://github.com/heredotnow/skill)** - Official agent skill
