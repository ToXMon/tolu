# Forkable Sites

Allow others to download and remix your site.

## Enable Forking
```bash
curl -sS -X PATCH https://here.now/api/v1/publish/$SLUG/metadata \
  -H "Authorization: Bearer $API_KEY" \
  -H "content-type: application/json" \
  -d '{"forkable": true}'
```

Or pass `forkable: true` in the create/update request body.

## How Forking Works
1. Fork button appears on live site
2. Visitor copies a prompt into their AI agent
3. Prompt includes manifest URL (`/.herenow/manifest.json`) and download pattern (`/.herenow/raw/{path}`)
4. Agent fetches manifest, downloads files, asks user what to change
5. Publishes modified version

## Proxy Route Forking
Forked sites get `.herenow/proxy.json` with variable references (e.g. `${RESEND_API_KEY}`), not actual secrets. Forker sets up their own variables.

## Defaults
- Forked sites inherit `forkable: true` by default
- Mutually exclusive with password protection and payment gating
