# Akash Network Skill — Final Accuracy Audit Report

**Date**: 2026-04-11
**Scope**: Full accuracy verification of `/a0/usr/skills/akash/` skill
**Methodology**: Cross-referenced all claims against official Akash documentation, GitHub releases, npm registry, and verified third-party sources

---

## Executive Summary

The Akash skill contains **3 critical inaccuracies**, **1 major omission**, and **1 structural deficiency** requiring correction. The most significant issues are: (1) version reference is one mainnet behind, (2) deployment duration limit is incorrectly stated as universal when it applies only to trial deployments, and (3) BME CLI commands are completely absent from the skill.

| Issue | Severity | Status |
|-------|----------|--------|
| Version outdated (v1.2.0 → should be v2.0.0) | HIGH | Needs correction |
| 24h duration limit misapplied to all deployments | CRITICAL | Needs correction |
| Missing BME CLI commands | HIGH | Needs addition |
| Missing Credit Card API (AEP-63) docs | MEDIUM | Needs addition |
| SKILL.md missing `allowed_tools` field | LOW | Needs correction |

---

## 1. CORRECT Version Number

### Finding

**SKILL.md line 24 states: "Current target version: v1.2.0 (mainnet-16)"** — This is REAL but OUTDATED.

### Verified Facts

| Attribute | Value | Source |
|-----------|-------|--------|
| **v1.2.0** | Mainnet-16, March 4, 2026, block 25,789,395 | CONFIRMED REAL |
| **v2.0.0** | Mainnet-17, March 21, 2026, block 26,063,777 | **CURRENT MAINNET** |
| **v2.0.1** | Stable patch, March 23, 2026 | **LATEST RECOMMENDED** |
| **v2.1.0-rc3** | Release candidate, April 1, 2026 | NOT for production |

### Versioning Scheme (Confirmed)

- Even minor = stable (v0.24.0, v0.36.0, v1.2.0, v2.0.0)
- Odd minor = dev/unstable (v0.9.0, v2.1.0)
- Stable cut from `mainnet/main` branch; dev from `main` branch

### Complete Recent Upgrade Chain

~~~text
v1.1.0 → v1.2.0 (Mainnet-16, Mar 4 2026) → v2.0.0 (Mainnet-17, Mar 21 2026)
~~~

### Correction Required

All references to "current target version" should be **v2.0.0 (mainnet-17)** or the latest patch **v2.0.1**.

### Sources

- https://github.com/akash-network/node/releases
- https://akash.network/docs/node-operators/network-upgrades/mainnet-17/
- https://akash.network/docs/node-operators/network-upgrades/mainnet-16/
- https://polkachu.com/upgrade_history/akash

---

## 2. CORRECT Deployment Duration Policy

### Finding

**SKILL.md line 200 states: "Akash deployments have a maximum duration of 24 hours per bid order"** — This is MISLEADING and INACCURATE.

**`docs/core-concepts/overview.md` lines 118-122 repeat this incorrect claim.**

### Verified Facts

| Deployment Type | Max Duration | Notes |
|----------------|-------------|-------|
| **Trial** (credit card / Console) | **24 hours per deployment** | 30-day trial period, $100 free credits, auto-closure after 24h, can redeploy |
| **Regular** (wallet-funded) | **NO LIMIT** | Runs indefinitely as long as escrow has funds, pay per block |

The 24-hour limit applies **EXCLUSIVELY** to trial/credit card deployments. Regular funded deployments have **no duration limit** and run as long as the deployment escrow account has sufficient funds.

### Mainnet-17 Impact

Mainnet-17 (BME model) changed pricing denomination from `uakt` to `uact` but did NOT change deployment duration rules. The 24h trial limit existed before BME and continues unchanged.

### Sources

- https://akash.network/docs/getting-started/what-is-akash/
- https://akash.network/blog/akash-2025-year-in-review/ (comparison table: "Trial Duration: Unlimited vs 30 days, Deployment Limits: No limits vs 24-hour auto-closure")

---

## 3. BME CLI Command Reference

### Finding

The skill contains **ZERO documentation** for `akash tx bme` commands despite the BME model being active since Mainnet-17 (March 2026). The skill mentions BME conceptually but provides no operational commands.

### Verified Commands

#### Mint ACT from AKT

~~~bash
# Burn AKT to receive ACT (epoch-based, ~1 min / 10 blocks)
akash tx bme mint-act 5000000uakt \
  --from "$AKASH_KEY_NAME" \
  --node "$AKASH_NODE" \
  --chain-id "$AKASH_CHAIN_ID" \
  -y
~~~

#### Burn ACT back to AKT

~~~bash
# Burn ACT to receive AKT
akash tx bme burn-act 5000000uact \
  --from "$AKASH_KEY_NAME" \
  --node "$AKASH_NODE" \
  --chain-id "$AKASH_CHAIN_ID" \
  -y
~~~

#### Generic Conversion

~~~bash
# AKT → ACT
akash tx bme burn-mint 1000000uakt uact --from "$AKASH_KEY_NAME"

# ACT → AKT
akash tx bme burn-mint 1000000uact uakt --from "$AKASH_KEY_NAME"
~~~

#### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `<amount><denom>` | Positional: amount + denom | `5000000uakt` or `5000000uact` |
| `--from` | Wallet name or address | `--from wallet` |
| `--node` | RPC node URL | `--node https://rpc.akashnet.net:443` |
| `--chain-id` | Network ID | `--chain-id akashnet-2` |
| `-y` | Skip confirmation prompt | `-y` |

#### Gas Configuration

~~~bash
export AKASH_GAS="auto"
export AKASH_GAS_PRICES="0.025uakt"
export AKASH_GAS_ADJUSTMENT="1.5"
~~~

### Key Notes

- ACT minting is **epoch-based** (~1 minute / 10 blocks), NOT instant
- SDL pricing MUST use `uact` (not `uakt`) since BME activation
- `uakt` = micro AKT (staking/gas token), `uact` = micro ACT (compute token, ~$1 USD peg)
- Providers receive ACT, then burn it to get AKT
- Circuit breaker exists to halt minting during extreme market conditions
- BME vault seeded with 300,000 AKT from community pool

### Sources

- https://akash.network/docs/developers/deployment/cli/act-mint-burn/
- https://github.com/akash-network/AEP/blob/main/spec/aep-76/README.md
- https://akash.network/blog/what-burn-mint-equilibrium-means-for-akash/

---

## 4. Credit Card API (AEP-63) Documentation

### Finding

The skill has no documentation for the Credit Card API despite it being a critical deployment pathway for non-crypto users.

### What Is AEP-63?

**AEP-63** = "Console API for Managed Wallet Users - v1"
- REST API allowing managed wallet (credit card) users to deploy and manage workloads
- Completion Date: May 27, 2025
- Eliminates need for crypto knowledge (no mnemonics, no Cosmos SDK)
- Designed for traditional Web2 developers
- Superseded by AEP-64 (JWT auth, July 2025)

### Architecture

~~~text
Credit Card User → Console API (REST) → Managed Wallet (auto-signing) → Akash Blockchain
                          |
                   Stripe Checkout API (payments)
~~~

### Base URL

~~~text
Base URL:  https://console-api.akash.network/v1
Swagger:   https://console-api.akash.network/v1/swagger
~~~

### Key Endpoints

| Category | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| Auth | POST/GET/PATCH/DELETE | `/v1/users/api-keys` | API key management |
| Certificates | POST/GET/DELETE | `/v1/certificates` | Auto-managed certs |
| Deployments | POST | `/v1/deployments` | Create deployment from SDL |
| Deployments | GET | `/v1/deployments` | List all deployments |
| Deployments | GET | `/v1/deployments/{dseq}` | Get deployment details + escrow |
| Deployments | DELETE | `/v1/deployments/{dseq}` | Close deployment |
| Deployments | POST | `/v1/deployments/deposit/{dseq}` | Add funds to escrow |
| Bids | GET | `/v1/bids/{dseq}` | List bids for deployment |
| Leases | POST | `/v1/leases` | Accept bid, create lease |
| Wallet | POST | `/v1/wallet/create` | Create managed wallet |
| Wallet | GET | `/v1/wallet/balance` | Get wallet balance |
| Wallet | POST | `/v1/wallet/deposit` | Get deposit address |
| SDL | POST | `/v1/sdl/validate` | Validate SDL syntax |
| SDL | POST | `/v1/sdl/price` | Estimate deployment cost |

### Rate Limits

| Tier | Requests/min | Deployments/day |
|------|-------------|----------------|
| Free | 60 | 10 |
| Pro | 300 | 100 |
| Enterprise | Unlimited | Unlimited |

### Sources

- https://akash.network/roadmap/aep-63/
- https://akash.network/roadmap/aep-64/
- https://github.com/akash-network/website/blob/main/src/content/Docs/api-documentation/console-api/index.md

---

## 5. Current Best Practices Summary

### SDL Version

| Aspect | Verified |
|--------|----------|
| **Default version** | SDL **v2.0** for standard deployments |
| **v2.1 addition** | IP endpoint leasing (`endpoints` section with `kind: ip`) |
| **v2.2+** | Does NOT exist — only v2.0 and v2.1 are defined |

### Authentication

| Aspect | Verified |
|--------|----------|
| **Recommended** | **JWT** (modern, per AEP-64) |
| **mTLS status** | Legacy but NOT yet deprecated — serves as fallback |
| **JWT migration** | Phase 1 (current): JWT alongside mTLS → Phase 2: migrate → Phase 3: deprecate mTLS |
| **JWT token lifetime** | ~24 hours |
| **JWT scopes** | `send-manifest`, `get-manifest`, `logs`, `shell`, `events`, `status`, `restart`, `hostname-migrate`, `ip-migrate` |

### SDK Packages

| Package | Version | Status |
|---------|---------|--------|
| `@akashnetwork/chain-sdk` | 1.0.0-alpha.30 | **ACTIVE (recommended)** |
| `@akashnetwork/akashjs` | 1.0.0 | Active (web/JS) |
| `@akashnetwork/akash-api` | 1.4.1 | **DEPRECATED** |

Migration path:
~~~text
OLD: import { MsgCreateDeployment } from "@akashnetwork/akash-api/akash/deployment/v1beta3";
NEW: import { MsgCreateDeployment } from "@akashnetwork/chain-sdk/build/akash/deployment/v1beta3";
~~~

### Minimum Account Balance

| Period | Minimum | Denom |
|--------|---------|-------|
| Pre-BME (before Mar 23, 2026) | 0.5 AKT minimum, 5 AKT recommended | `uakt` |
| Post-BME (Mainnet-17+) | Fund via ACT minted from AKT | `uact` |

### RPC Endpoints

| Service | URL | Type |
|---------|-----|------|
| RPC (Tendermint) | `https://rpc.akashnet.net:443` | Official |
| REST/LCD | `https://api.akashnet.net:443` | Official |
| gRPC | `grpc.akashnet.net:443` | Official |
| WebSocket | `wss://rpc.akashnet.net/websocket` | Official |
| Console API | `https://console-api.akash.network/v1` | Official |
| Forbole | `https://rpc.akash.forbole.com:443` | Community |
| EcoStake | `https://rpc-akash.ecostake.com:443` | Community |
| Polkachu | `https://akash-rpc.polkachu.com:443` | Community |
| Testnet | `https://rpc.sandbox-01.aksh.pw:443` (chain: `sandbox-01`) | Official |

Chain ID: `akashnet-2`

### Mainnet-17 Breaking Changes (v2.0.0)

| Area | Change |
|------|--------|
| Module removal | Legacy `x/take` module completely removed |
| Denom migration | All deployments: `axlUSDC`/`uakt` → `uact` (ACT only) |
| New modules | `x/bme`, `x/oracle`, `x/epochs`, CosmWasm runtime |
| API | Pagination encoding changed; new gRPC/REST endpoints for BME/oracle/epochs |
| CLI | New `akash tx bme` commands; unordered transactions enabled |
| SDL | No structural changes; pricing denom `uakt` → `uact` (auto-migrated) |

### Sources

- https://akash.network/docs/developers/deployment/akash-sdl/best-practices/
- https://akash.network/docs/node-operators/network-upgrades/mainnet-17/
- https://www.npmjs.com/~akashnetwork
- https://github.com/akash-network/docs/blob/master/akash-nodes/public-rpc-nodes.md

---

## 6. SKILL.md Optimization Recommendations

### 6.1 Missing `allowed_tools` Field

The SKILL.md frontmatter is missing the `allowed_tools` field per the Agent Zero skill format specification.

**Recommended addition to frontmatter:**

~~~yaml
allowed_tools:
  - "code_execution_tool"
  - "search_engine"
  - "document_query"
  - "text_editor"
  - "browser_agent"
  - "call_subordinate"
~~~

### 6.2 Version Update

**Current (WRONG):**
~~~yaml
version: "2.0.0"  # This is the skill version, not Akash version
~~~

Line 24 **needs update:**
~~~markdown
Current target version: **v1.2.0** (mainnet-16).  ← CHANGE TO: **v2.0.0** (mainnet-17)
~~~

### 6.3 Better Trigger Patterns

Current triggers are adequate but missing key patterns:

~~~yaml
trigger_patterns:
  # ... existing patterns ...
  - "akash act"               # BME/ACT token queries
  - "akash bme"               # Burn-Mint Equilibrium
  - "akash credit card"       # Console API / managed wallet
  - "akash console"           # Console deployments
  - "akash managed wallet"    # Managed wallet operations
  - "akash uact"              # Pricing denom queries
  - "akash certificate"       # Certificate management
  - "akash sdl"               # SDL-specific queries
~~~

### 6.4 Better Description

**Current:**
~~~yaml
description: "Comprehensive Akash Network skill for deployers, providers, and node operators. Covers SDL generation, CLI deployments, Console API, TypeScript/Go SDKs, provider setup, and validator operations."
~~~

**Recommended:**
~~~yaml
description: "Akash Network (decentralized cloud) skill covering SDL generation, CLI deployments (akash + provider-services binaries), Console API with credit card support, BME/ACT token management, TypeScript/Go SDKs, provider setup, and validator operations. Targets Mainnet-17 (v2.0.0+)."
~~~

### 6.5 Content Structure Improvements

1. **Add BME section to SKILL.md** — Currently missing entirely. Should include mint-act, burn-act, burn-mint commands directly in the Quick Reference section.

2. **Add Credit Card / Trial deployment section** — Document the trial deployment workflow with 24h limits distinct from regular deployments.

3. **Fix duration section** — Rewrite "Deployment Duration Limits" section to clearly distinguish trial vs. regular deployments.

4. **Delegate to docs/** — The SKILL.md is already well-structured with references to `docs/` subdirectory. New BME and Credit Card API content should be created as `docs/deploy/cli/bme-commands.md` and `docs/deploy/console-api/credit-card-api.md` with summaries in SKILL.md.

5. **Add breaking changes note** — Add a "Breaking Changes" or "Migration Notes" section linking to mainnet upgrade impacts.

---

## 7. Complete List of Files Needing Correction

### Files with WRONG Version (v1.2.0 → v2.0.0)

| # | File | Lines | Issue |
|---|------|-------|-------|
| 1 | `SKILL.md` | 24 | `v1.2.0 (mainnet-16)` → `v2.0.0 (mainnet-17)` |
| 2 | `docs/deploy/cli/installation.md` | 26, 31, 36, 46, 58 | All `v1.2.0` download URLs and version refs |
| 3 | `docs/node/full-node/installation.md` | 13, 36 | `AKASH_VERSION="v1.2.0"` |
| 4 | `docs/node/validator/operations.md` | 269, 272 | Cosmovisor `upgrade-v1.2.0/` directory references |
| 5 | `docs/sdl/services.md` | 32 | `image: myapp:v1.2.0` (example, LOW priority) |
| 6 | `ADAPTATION_REPORT.md` | 12, 43, 58, 191, 197 | Historical report — update or leave as-is |

### Files with WRONG Duration Claim (24h applies to trial ONLY)

| # | File | Lines | Issue |
|---|------|-------|-------|
| 7 | `SKILL.md` | 198-203 | "maximum duration of 24 hours" stated as universal |
| 8 | `docs/core-concepts/overview.md` | 118-122 | Repeats incorrect universal 24h claim |

### Files with WRONG Denom (uakt in deployment context)

| # | File | Lines | Issue |
|---|------|-------|-------|
| 9 | `docs/deploy/console-api/multi-tenant-guide.md` | 2651 | `denom: uakt` should be `denom: uact` |

### Files MISSING Content

| # | File | Issue |
|---|------|-------|
| 10 | `SKILL.md` | Missing `allowed_tools` in frontmatter |
| 11 | `SKILL.md` | Missing BME CLI commands in Quick Reference |
| 12 | `SKILL.md` | Missing Credit Card API / trial deployment info |
| 13 | (NEW) | Missing `docs/deploy/cli/bme-commands.md` |
| 14 | (NEW) | Missing `docs/deploy/console-api/credit-card-api.md` |

### Priority Summary

| Priority | Action | Files |
|----------|--------|-------|
| **P0 — CRITICAL** | Fix 24h duration claim (misleads all users) | SKILL.md, overview.md |
| **P1 — HIGH** | Update version to v2.0.0 | SKILL.md, installation.md (x2), operations.md |
| **P1 — HIGH** | Add BME CLI commands | SKILL.md + new doc |
| **P2 — MEDIUM** | Fix uakt→uact in multi-tenant guide | multi-tenant-guide.md |
| **P2 — MEDIUM** | Add Credit Card API docs | New doc + SKILL.md |
| **P3 — LOW** | Add allowed_tools to frontmatter | SKILL.md |
| **P3 — LOW** | Improve trigger patterns | SKILL.md |

---

## Appendix: Verification Methodology

All findings were cross-referenced against:

1. **GitHub Releases**: https://github.com/akash-network/node/releases
2. **Official Akash Docs**: https://akash.network/docs/
3. **Mainnet Upgrade Pages**: mainnet-16 and mainnet-17 upgrade guides
4. **Polkachu Upgrade History**: https://polkachu.com/upgrade_history/akash
5. **npm Registry**: https://www.npmjs.com/~akashnetwork
6. **AEP Specifications**: AEP-63, AEP-64, AEP-76
7. **Official Blog**: https://akash.network/blog/akash-2025-year-in-review/
8. **GitHub Source**: akash-network/node, akash-network/docs, akash-network/AEP

---

*Report generated 2026-04-11 by Agent Zero Deep Research. All findings verified with multiple independent sources.*
