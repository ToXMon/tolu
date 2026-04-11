---
name: "akash"
description: "Comprehensive Akash Network skill for deployers, providers, and node operators. Covers SDL generation, CLI deployments, Console API, TypeScript/Go SDKs, provider setup, and validator operations."
version: "2.0.0"
author: "baktun14 (adapted for Agent Zero)"
tags: ["akash", "cloud", "deployment", "blockchain", "kubernetes", "SDL", "decentralized"]
trigger_patterns:
  - "akash"
  - "deploy to akash"
  - "generate SDL"
  - "akash provider"
  - "akash CLI"
  - "akash SDK"
  - "akash validator"
  - "akash node"
  - "decentralized cloud"
---

# Akash Network Skill

Comprehensive skill for working with the Akash Network — the decentralized cloud computing marketplace. Current target version: **v1.2.0** (mainnet-16).

## When to Use This Skill

Use this skill when the user asks about or needs help with:
- Deploying applications to Akash (the decentralized cloud)
- Generating or validating SDL (Stack Definition Language) configurations
- Setting up Akash providers (becoming a host)
- Running Akash full nodes or validators
- Using the Akash TypeScript or Go SDKs
- Managing Akash certificates, leases, or deployments
- Provider operations, pricing, and bid engine configuration
- Understanding Akash terminology, pricing, or IBC denominations

## Critical Rules

**NEVER use `:latest` or omit image tags.** Always specify explicit version tags for reproducible deployments.

```yaml
# CORRECT
image: nginx:1.25.3
image: node:20-alpine
image: postgres:16

# WRONG - will cause deployment issues
image: nginx:latest
image: nginx          # implies :latest
```

**Always verify current versions.** Check https://github.com/akash-network/node/releases for the latest Akash release before following installation guides.

## CLI Binary Reference

Akash now has two separate binaries — use the correct one for your task:

| Binary | Purpose | Used For |
|--------|---------|----------|
| `akash` | Node operations | Validators, full nodes, chain queries, governance, staking |
| `provider-services` | Tenant/deploy operations | Deployments, leases, certificates, manifests, provider queries |

**Rule of thumb:** If you're deploying workloads or managing leases, use `provider-services`. If you're running a node or participating in governance, use `akash`.

## Quick Reference

### SDL Structure

Every SDL file has four required sections:

```yaml
version: "2.0"  # or "2.1" for IP endpoints

services:       # Container definitions
profiles:       # Compute resources & placement
deployment:     # Service-to-profile mapping
```

Optional section for IP endpoints:
```yaml
endpoints:      # IP lease endpoints (requires version 2.1)
```

### Minimal SDL Template

```yaml
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
```

### Common Patterns

**Environment Variables:**
```yaml
services:
  app:
    env:
      - "DATABASE_URL=postgres://..."
      - "NODE_ENV=production"
```

**Persistent Storage:**
```yaml
profiles:
  compute:
    app:
      resources:
        storage:
          - size: 10Gi
            attributes:
              persistent: true
              class: beta2
```

**GPU Workloads:**
```yaml
profiles:
  compute:
    ml:
      resources:
        gpu:
          units: 1
          attributes:
            vendor:
              nvidia:
                - model: a100
```

**Payment Options:**
- **uact**: Akash Compute Token (ACT, ~$1 peg). Used for deployment pricing since Mainnet 17 (BME model).
- **uakt**: Native Akash Token for staking, governance, and gas fees
- **USDC**: Via IBC denom (e.g., `denom: ibc/170C677610AC31DF0904FFE09CD3B5C657492170E7E52372E48756B71E56F2F1`)

### Key Deployment Commands (using provider-services)

```bash
# Create certificate
provider-services tx cert create client --from my-key

# Create deployment
provider-services tx deployment create deploy.yaml --dseq $DSEQ --from my-key

# Send manifest to provider
provider-services send-manifest deploy.yaml --dseq $DSEQ --provider $PROVIDER --from my-key

# Query deployment status
provider-services query deployment get --owner $ADDRESS --dseq $DSEQ

# Close deployment
provider-services tx deployment close --dseq $DSEQ --from my-key
```

### Key Node Commands (using akash)

```bash
# Check node status
akash status 2>&1 | jq '.SyncInfo'

# Query validators
akash query staking validators --status bonded

# Vote on governance
akash tx gov vote PROPOSAL_ID yes --from validator-wallet
```

## Deployment Duration Limits

Akash deployments have a **maximum duration of 24 hours** per bid order. For longer-running workloads:
- Use automation to re-deploy before expiration
- Consider using the Console API or SDKs for programmatic renewal
- The SDL `deployment` section does NOT have a `duration` field longer than 24h

## Documentation Index

### Core Concepts
- `docs/core-concepts/overview.md` — Akash Network introduction, architecture, and duration limits
- `docs/core-concepts/terminology.md` — Key terms (lease, bid, dseq, gseq, oseq)
- `docs/core-concepts/pricing.md` — Payment with uact (ACT, BME model), USDC, IBC denoms

### SDL Configuration
- `docs/sdl/schema-overview.md` — Version requirements and SDL structure
- `docs/sdl/services.md` — Service configuration (image, expose, env, credentials)
- `docs/sdl/compute-resources.md` — CPU, memory, storage, and GPU specifications
- `docs/sdl/placement-pricing.md` — Provider selection and pricing
- `docs/sdl/deployment.md` — Service-to-profile mapping
- `docs/sdl/endpoints.md` — IP endpoint configuration (v2.1)
- `docs/sdl/validation-rules.md` — All constraints and validation rules

### SDL Examples
- `docs/sdl/examples/web-app.md` — Simple web deployment
- `docs/sdl/examples/wordpress-db.md` — Multi-service with persistent storage
- `docs/sdl/examples/gpu-workload.md` — GPU deployment with NVIDIA
- `docs/sdl/examples/ip-lease.md` — IP endpoint configuration

### Deployment Methods
- `docs/deploy/overview.md` — Comparison of deployment options, CLI binary guide
- `docs/deploy/cli/installation.md` — Installing akash and provider-services CLIs
- `docs/deploy/cli/wallet-setup.md` — Wallet creation and funding
- `docs/deploy/cli/deployment-lifecycle.md` — Full deployment workflow
- `docs/deploy/cli/lease-management.md` — Managing active leases
- `docs/deploy/cli/common-commands.md` — Command reference
- `docs/deploy/console-api/overview.md` — Console API for programmatic deployments
- `docs/deploy/console-api/authentication.md` — Console API authentication
- `docs/deploy/console-api/managed-wallet.md` — Managed wallet documentation
- `docs/deploy/console-api/deployment-endpoints.md` — Deployment API endpoints
- `docs/deploy/certificates/jwt-auth.md` — JWT authentication (recommended)
- `docs/deploy/certificates/mtls-legacy.md` — Legacy mTLS authentication

### AuthZ (Delegated Permissions)
- `docs/authz/overview.md` — AuthZ concepts and use cases
- `docs/authz/granting-permissions.md` — Creating grants
- `docs/authz/using-grants.md` — Using granted permissions

### SDK Documentation
- `docs/sdk/overview.md` — SDK comparison and selection guide
- `docs/sdk/typescript/installation.md` — TypeScript SDK setup (v1.0.0+)
- `docs/sdk/typescript/chain-node-sdk.md` — Chain SDK for Node.js
- `docs/sdk/typescript/chain-web-sdk.md` — Chain SDK for browsers
- `docs/sdk/typescript/provider-sdk.md` — Provider communication SDK
- `docs/sdk/go/installation.md` — Go SDK setup
- `docs/sdk/go/client-setup.md` — Complete Go client configuration

### Provider Operations
- `docs/provider/overview.md` — Provider requirements and overview
- `docs/provider/requirements.md` — Hardware and software requirements
- `docs/provider/setup/kubernetes-cluster.md` — Kubernetes cluster setup
- `docs/provider/setup/provider-installation.md` — Provider Helm chart installation
- `docs/provider/setup/configuration.md` — Provider configuration
- `docs/provider/configuration/attributes.md` — Provider attributes
- `docs/provider/configuration/pricing.md` — Pricing strategies
- `docs/provider/configuration/bid-engine.md` — Bid engine configuration
- `docs/provider/operations/lease-management.md` — Lease lifecycle for providers
- `docs/provider/operations/monitoring.md` — Monitoring setup
- `docs/provider/operations/troubleshooting.md` — Troubleshooting guide

### Node Operations
- `docs/node/overview.md` — Running Akash nodes
- `docs/node/full-node/requirements.md` — Full node hardware requirements
- `docs/node/full-node/installation.md` — Full node installation guide
- `docs/node/full-node/state-sync.md` — State sync for fast bootstrap
- `docs/node/validator/becoming-validator.md` — Becoming a validator
- `docs/node/validator/operations.md` — Validator day-to-day operations
- `docs/node/validator/security.md` — Validator security best practices

### Reference
- `docs/reference/storage-classes.md` — beta2, beta3, ram storage classes
- `docs/reference/gpu-models.md` — Supported NVIDIA GPUs (incl. B200, RTX 5090)
- `docs/reference/ibc-denoms.md` — IBC payment denominations
- `docs/reference/rpc-endpoints.md` — Public RPC and API endpoints

## Templates

Standalone SDL templates are available in the `templates/` directory:
- `templates/web-app.md` — Basic web application SDL
- `templates/wordpress-db.md` — WordPress with MySQL SDL
- `templates/gpu-workload.md` — GPU workload SDL
- `templates/ip-lease.md` — IP lease endpoint SDL

## Additional Resources

- **[awesome-akash](https://github.com/akash-network/awesome-akash)** — 100+ production-ready SDL templates
- **[Akash Docs](https://akash.network/docs/)** — Official documentation
- **[GitHub](https://github.com/akash-network/node)** — Source code and releases
- **[Discord](https://discord.gg/akash)** — Community support
