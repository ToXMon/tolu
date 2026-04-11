# Credit Card / Trial Deployment API (AEP-63)

## Overview

The Akash Console Credit Card API (AEP-63) provides a REST API for **managed wallet** users who deploy using credit card payments via Stripe. This API abstracts away all blockchain complexity — no mnemonics, no Cosmos SDK knowledge, and no command-line tools required.

### Architecture

```
User → Console API (REST) → Managed Wallet (auto-signing) → Akash Blockchain + Stripe Payments
```

- **User**: Interacts via REST API with API key authentication
- **Console API**: Translates REST calls into blockchain transactions
- **Managed Wallet**: Console holds and manages the user's wallet (auto-signing)
- **Akash Blockchain**: Executes deployment transactions
- **Stripe**: Handles credit card payments for funding

### Base URL

| Environment | URL |
|-------------|-----|
| **Mainnet** | `https://console-api.akash.network/v1` |
| **Swagger Docs** | `https://console-api.akash.network/v1/swagger` |
| **Sandbox** | `https://console-api.sandbox-01.aksh.pw/v1` |

## Authentication

All requests require an API key in the `Authorization` header:

```bash
curl -H "Authorization: Bearer <your-api-key>" \
  https://console-api.akash.network/v1/deployments
```

### API Key Management

```bash
# Create API key
POST /v1/users/api-keys

# List API keys
GET /v1/users/api-keys

# Update API key
PATCH /v1/users/api-keys/{keyId}

# Delete API key
DELETE /v1/users/api-keys/{keyId}
```

## Key Endpoints

### Certificates

```bash
# Create certificate
POST /v1/certificates
{
  "cert": "<PEM-encoded certificate>",
  "publicKey": "<PEM-encoded public key>"
}

# List certificates
GET /v1/certificates

# Delete certificate
DELETE /v1/cificates/{certSerial}
```

### Deployments

```bash
# Create deployment
POST /v1/deployments
{
  "sdl": "<base64-encoded SDL YAML>",
  "deposit": "5000000uact"
}

# List deployments
GET /v1/deployments

# Get deployment details
GET /v1/deployments/{dseq}

# Close/delete deployment
DELETE /v1/deployments/{dseq}

# Deposit funds to deployment escrow
POST /v1/deployments/deposit/{dseq}
{
  "amount": "5000000uact"
}
```

### Bids

```bash
# Get bids for a deployment
GET /v1/bids/{dseq}
```

### Leases

```bash
# Create/accept lease (select winning bid)
POST /v1/leases
{
  "dseq": "12345",
  "provider": "akash1provider..."
}
```

### Wallet

```bash
# Create managed wallet
POST /v1/wallet/create

# Get wallet balance
GET /v1/wallet/balance

# Deposit funds via Stripe
POST /v1/wallet/deposit
{
  "amount": "1000",
  "currency": "usd"
}
```

### SDL Utilities

```bash
# Validate SDL
POST /v1/sdl/validate
{
  "sdl": "<base64-encoded SDL YAML>"
}

# Estimate deployment price
POST /v1/sdl/price
{
  "sdl": "<base64-encoded SDL YAML>"
}
```

## Rate Limits

| Tier | Requests/Min | Deploys/Day | Notes |
|------|-------------|-------------|-------|
| **Free** | 60 | 10 | Default tier |
| **Pro** | 300 | 100 | Paid subscription |
| **Enterprise** | Unlimited | Unlimited | Custom arrangement |

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1712899200
```

## Trial Deployment Constraints

Credit card / trial deployments have specific limitations:

| Constraint | Value |
|-----------|-------|
| **Max deployment duration** | 24 hours (auto-closure) |
| **Trial period** | 30 days from signup |
| **Free credits** | $100 USD equivalent |
| **Auto-closure** | Deployments close after 24h; can redeploy |
| **SDL denom** | `uact` (same as regular deployments) |

### Differences from Regular Deployments

| Feature | Credit Card (Trial) | Regular (Wallet) |
|---------|---------------------|------------------|
| Duration limit | 24 hours per deployment | None |
| Funding | Stripe credit card | Blockchain escrow (uact) |
| Wallet management | Console managed (auto-sign) | User-controlled |
| Certificate management | Console managed | User creates/imports |
| Mnemonic required | No | Yes |
| Cosmos SDK knowledge | Not needed | Required |
| Gas fees | Included in pricing | User pays separately |

## Full Deployment Example

```bash
export API_URL="https://console-api.akash.network/v1"
export API_KEY="your-api-key-here"

# Step 1: Create certificate
curl -X POST "$API_URL/certificates" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sdl": ""}'  # Console auto-generates cert

# Step 2: Create deployment from SDL
SDL_BASE64=$(base64 -w 0 <<'EOF'
version: "2.0"
services:
  web:
    image: nginx:1.25.3
    expose:
      - port: 80
        as: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    dcloud:
      pricing:
        web:
          denom: uact
          amount: 1000
deployment:
  web:
    dcloud:
      profile: web
      count: 1
EOF
)

curl -X POST "$API_URL/deployments" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"sdl\": \"$SDL_BASE64\", \"deposit\": \"5000000uact\"}"

# Step 3: Get bids
curl "$API_URL/bids/{dseq}" \
  -H "Authorization: Bearer $API_KEY"

# Step 4: Accept bid / create lease
curl -X POST "$API_URL/leases" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dseq": "12345", "provider": "akash1..."}'

# Step 5: Check deployment status
curl "$API_URL/deployments/{dseq}" \
  -H "Authorization: Bearer $API_KEY"

# Step 6: Close deployment
curl -X DELETE "$API_URL/deployments/{dseq}" \
  -H "Authorization: Bearer $API_KEY"
```

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| `400` | Invalid request / SDL validation error | Fix request body or SDL |
| `401` | Missing or invalid API key | Check authentication |
| `403` | Rate limit exceeded or insufficient credits | Wait or upgrade tier |
| `404` | Resource not found | Verify dseq/cert serial |
| `429` | Rate limited | Respect rate limits, retry after `Retry-After` header |
| `500` | Server error | Retry with backoff |

## SDK Integration

### TypeScript Example

```typescript
const API_URL = "https://console-api.akash.network/v1";
const API_KEY = process.env.AKASH_API_KEY;

async function createDeployment(sdlYaml: string) {
  const sdl = Buffer.from(sdlYaml).toString("base64");

  const response = await fetch(`${API_URL}/deployments`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sdl, deposit: "5000000uact" }),
  });

  if (!response.ok) {
    throw new Error(`Deployment failed: ${response.status} ${await response.text()}`);
  }

  return response.json();
}
```

## Sources

- [Akash Console API Documentation](https://akash.network/docs/developers/console-api/)
- [AEP-63: Credit Card API Proposal](https://github.com/akash-network/akash-node-mainnet/tree/main/proposals)
- [Akash Console](https://console.akash.network/)
