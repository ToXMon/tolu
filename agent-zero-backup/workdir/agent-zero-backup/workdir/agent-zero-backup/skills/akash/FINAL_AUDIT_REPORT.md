# Akash Network Skill — Final Comprehensive Audit Report

**Date:** 2026-04-10
**Auditor:** Agent Zero (Agent 1)
**Scope:** Full skill audit with focus on "deploy-on-behalf-of" service use case
**Skill Version:** 2.0.0 (post-BME migration)

---

## Executive Summary

The Akash Network skill provides **strong foundational coverage** for building a deployment service, with comprehensive Console API documentation, AuthZ delegation guides, managed wallet operations, and SDK examples in both TypeScript and Go. However, several critical gaps exist for production-grade "deploy-on-behalf-of" services, most notably the absence of multi-tenant architecture patterns, webhook/event handling, combined AuthZ + Console API integration, and migration guidance from the deprecated `@akashnetwork/akash-api` to the new `@akashnetwork/chain-sdk`.

| Metric | Score |
|--------|-------|
| **Overall SDK/API Coverage** | **7.5/10** |
| Console API Completeness | 8/10 |
| AuthZ Delegation Coverage | 8/10 |
| SDK Documentation | 7/10 |
| Certificate/Auth Coverage | 8/10 |
| Deployment Service Use Case | 6/10 |
| Code Quality | 7/10 |
| Currency Accuracy (BME) | 10/10 |

---

## 1. SDK/API Coverage Score — Deployment Service Use Case

### Score: 7.5/10

The skill covers the **individual building blocks** needed for a deployment service well:

| Component | Covered? | Quality | Notes |
|-----------|----------|---------|-------|
| Console API CRUD | ✅ | High | Full deployment lifecycle via REST |
| AuthZ Delegation | ✅ | High | CLI + TypeScript SDK examples |
| Managed Wallets | ✅ | High | Create, fund, deploy workflow |
| Fee Grants | ✅ | Medium | CLI examples only, no SDK code |
| JWT Authentication | ✅ | High | Full challenge-response flow |
| Provider Communication | ✅ | High | Manifest send, status, logs |
| Certificate Management | ✅ | High | Create, broadcast, store |

**What's missing for a complete deployment service:**

| Component | Covered? | Priority |
|-----------|----------|----------|
| Multi-tenant architecture patterns | ❌ | CRITICAL |
| AuthZ + Console API integration | ❌ | CRITICAL |
| Webhook/event handling | ❌ | HIGH |
| chain-sdk migration guide | ❌ | HIGH |
| Credit Card API (AEP-63) | ❌ | MEDIUM |
| Combined AuthZ + FeeGrant + Managed Wallet pattern | ❌ | HIGH |
| Go SDK AuthZ examples | ❌ | MEDIUM |
| Rate limit handling best practices | ⚠️ Partial | MEDIUM |

---

## 2. Missing Content — Critical Gaps

### 2.1 CRITICAL: Multi-Tenant Architecture Guide

**Gap:** No documentation exists for building a multi-tenant deployment service where a single platform manages deployments for many users.

**What's needed:**
- Service architecture overview (platform wallet + per-user AuthZ grants)
- User onboarding flow (user grants permissions to platform)
- Deployment isolation patterns
- Resource quota management per user
- Billing/settlement patterns (how to charge users)
- Monitoring multiple users' deployments

**Recommended file:** `docs/deploy/console-api/multi-tenant-guide.md`

### 2.2 CRITICAL: AuthZ + Console API Integration

**Gap:** AuthZ is documented exclusively for CLI and direct SDK usage. There is no guidance on combining AuthZ delegation with the Console API's managed wallet system.

**Key question unanswered:** Can the Console API execute deployments on behalf of a user who has granted AuthZ to the platform's wallet? Or must the platform use the direct chain SDK for AuthZ operations?

**What's needed:**
- Clear architecture decision: Console API vs. Direct SDK for AuthZ
- If Console API supports AuthZ: endpoint examples with `walletId` + delegation
- If not: explicit note that AuthZ requires direct SDK, with a combined pattern

**Recommended:** Add section to `docs/authz/using-grants.md` or create `docs/authz/console-api-integration.md`

### 2.3 HIGH: Webhook/Event Handling

**Gap:** No documentation for monitoring deployment status changes programmatically.

**What's needed:**
- Polling vs. webhook patterns
- Deployment state transition reference (open → active → closed)
- Lease state monitoring
- Provider health monitoring
- Recommended polling intervals
- Event-driven architecture patterns

**Recommended file:** `docs/deploy/console-api/event-monitoring.md`

### 2.4 HIGH: chain-sdk Migration Guide

**Gap:** All TypeScript SDK examples use `@akashnetwork/akash-api` which is **deprecated**. The replacement `@akashnetwork/chain-sdk` (v1.0.0-alpha.30 on GitHub) is not mentioned anywhere.

**What's needed:**
- Migration guide from `@akashnetwork/akash-api` to `@akashnetwork/chain-sdk`
- Updated import paths
- Breaking changes documentation
- Version pinning guidance (npm lags behind GitHub)

**Recommended file:** `docs/sdk/typescript/migration-guide.md`

### 2.5 HIGH: Combined AuthZ + FeeGrant + Managed Wallet Pattern

**Gap:** The three key primitives for a deployment service (AuthZ, FeeGrants, Managed Wallets) are documented separately but never combined into a single end-to-end pattern.

**What's needed:**
- Complete architecture pattern combining all three
- Example: User grants AuthZ → Platform creates managed wallet → Platform executes deployment → Platform pays fees via FeeGrant
- Code examples for the full flow

**Recommended file:** `docs/authz/deployment-service-pattern.md`

### 2.6 MEDIUM: Go SDK AuthZ Examples

**Gap:** AuthZ examples exist for CLI and TypeScript SDK only. No Go examples for MsgExec, MsgGrant, or FeeGrant operations.

**Recommended:** Add AuthZ section to `docs/sdk/go/client-setup.md`

### 2.7 MEDIUM: Credit Card API (AEP-63)

**Gap:** Akash introduced a Credit Card API allowing deployments without crypto wallets. Not documented.

**Recommended file:** `docs/deploy/console-api/credit-card-api.md`

---

## 3. Code Quality Issues

### 3.1 Deprecated Package References

**Severity:** HIGH
**Files:** All TypeScript SDK files + AuthZ files

All TypeScript imports reference the deprecated package:
```typescript
// Current (deprecated)
import { MsgCreateDeployment } from "@akashnetwork/akash-api/akash/deployment/v1beta3";

// Should also document
import { MsgCreateDeployment } from "@akashnetwork/chain-sdk/...";
```

**Fix:** Add deprecation notice + migration note to all affected files.

**Affected files:**
- `docs/sdk/typescript/chain-node-sdk.md`
- `docs/sdk/typescript/provider-sdk.md`
- `docs/sdk/typescript/installation.md` (Available Modules section)
- `docs/authz/using-grants.md`
- `docs/authz/granting-permissions.md`
- `docs/deploy/certificates/mtls-legacy.md`

### 3.2 Unverified Package: `@akashnetwork/console-api-client`

**Severity:** MEDIUM
**File:** `docs/deploy/console-api/overview.md` (line 235)

```typescript
import { ConsoleApiClient } from "@akashnetwork/console-api-client";
```

This package could not be verified on npm. If it doesn't exist, this example will confuse users.

**Fix:** Verify the package exists. If not, remove or replace with `fetch`-based examples.

### 3.3 Missing Import in AuthZ Example

**Severity:** MEDIUM
**File:** `docs/authz/using-grants.md`

The `AkashAutomation` class uses `MsgCloseDeployment` but never imports it:
```typescript
const innerMsg = MsgCloseDeployment.fromPartial({  // Used but not imported
```

**Fix:** Add `import { MsgCloseDeployment } from "@akashnetwork/akash-api/akash/deployment/v1beta3";` to the example.

### 3.4 Go gRPC Uses Insecure Credentials for Production

**Severity:** LOW (documented for examples only)
**File:** `docs/sdk/go/client-setup.md`

```go
grpc.WithTransportCredentials(insecure.NewCredentials())
```

While this is technically correct for TLS-enabled endpoints (the `grpc.akashnet.net:443` endpoint handles TLS at the load balancer), it could be confusing. Should add a note explaining that production deployments should use TLS.

### 3.5 Certificate Storage in localStorage

**Severity:** LOW (browser context only)
**File:** `docs/sdk/typescript/provider-sdk.md`

```typescript
localStorage.setItem(`akash-cert-${address}`, JSON.stringify({
  cert: cert.cert,
  privateKey: cert.privateKey,
  publicKey: cert.publicKey
}));
```

Storing private keys in localStorage is a security risk (accessible via XSS). Should recommend IndexedDB with encryption or server-side storage.

**Fix:** Add security warning note after the example.

### 3.6 Console API overview.md Missing Endpoints

**Severity:** LOW
**File:** `docs/deploy/console-api/overview.md`

1. **Missing `PUT /deployment/{dseq}`** (Update Deployment) in the endpoint table (line 39-46)
2. **Missing `/wallet/list` and `/wallet/default`** in Managed Wallet table (line 73-78)
3. **Only 2 auth methods listed** (line 30-31) — missing Anonymous

All these are documented in their respective detail files but missing from the overview.

### 3.7 Console API Quick Start Section

**Severity:** LOW
**File:** `docs/deploy/console-api/overview.md` (line 82-87)

The "Get API Key" section is just a comment — no actual instructions:
```bash
# Register at console.akash.network and generate API key
# Or use JWT from authenticated session
```

**Fix:** Add step-by-step instructions or link to `authentication.md`.

### 3.8 JWT Auth CLI Sign Challenge

**Severity:** LOW
**File:** `docs/deploy/certificates/jwt-auth.md`

The CLI sign challenge section is incomplete:
```bash
# Sign message
akash tx auth sign-msg "challenge-string" --from wallet
```

The `sign-msg` subcommand syntax is unverified and may not exist in the current CLI.

---

## 4. Recommended Additions

### New Files (Priority Order)

| # | File | Description | Priority |
|---|------|-------------|----------|
| 1 | `docs/deploy/console-api/multi-tenant-guide.md` | Multi-tenant deployment service architecture | CRITICAL |
| 2 | `docs/authz/deployment-service-pattern.md` | Combined AuthZ + FeeGrant + Managed Wallet pattern | CRITICAL |
| 3 | `docs/authz/console-api-integration.md` | AuthZ integration with Console API (or clarification that direct SDK is required) | CRITICAL |
| 4 | `docs/sdk/typescript/migration-guide.md` | Migration from deprecated akash-api to chain-sdk | HIGH |
| 5 | `docs/deploy/console-api/event-monitoring.md` | Deployment status monitoring patterns | HIGH |
| 6 | `docs/sdk/go/authz-operations.md` | Go SDK AuthZ examples (MsgGrant, MsgExec, FeeGrant) | MEDIUM |
| 7 | `docs/deploy/console-api/credit-card-api.md` | Credit Card API (AEP-63) documentation | MEDIUM |
| 8 | `docs/deploy/console-api/rate-limits.md` | Detailed rate limit handling and best practices | LOW |

### Updates to Existing Files

| # | File | Update | Priority |
|---|------|--------|----------|
| 1 | `docs/sdk/typescript/installation.md` | Add deprecation notice for akash-api, mention chain-sdk | HIGH |
| 2 | `docs/sdk/overview.md` | Add chain-sdk to comparison table | HIGH |
| 3 | `docs/authz/using-grants.md` | Fix missing MsgCloseDeployment import | MEDIUM |
| 4 | `docs/deploy/console-api/overview.md` | Add missing endpoints (PUT, /wallet/list, /wallet/default, Anonymous auth) | MEDIUM |
| 5 | `docs/sdk/typescript/provider-sdk.md` | Add localStorage security warning | LOW |
| 6 | `docs/deploy/console-api/authentication.md` | Complete Quick Start / API Key generation instructions | LOW |

---

## 5. Priority Fixes — Ordered List

### Tier 1: Must Fix (Blocks Deployment Service Use Case)

1. **Create `multi-tenant-guide.md`** — Without this, a developer has no architectural guidance for building a multi-user deployment service
2. **Create `deployment-service-pattern.md`** — The combined AuthZ + FeeGrant + Managed Wallet pattern is essential
3. **Clarify AuthZ + Console API integration** — Whether the Console API supports AuthZ or requires direct SDK is a fundamental architecture decision

### Tier 2: Should Fix (Quality & Accuracy)

4. **Add chain-sdk deprecation notices** — All files using `@akashnetwork/akash-api` should note the deprecation
5. **Create `migration-guide.md`** — Guide developers from deprecated to new SDK
6. **Create `event-monitoring.md`** — Polling/webhook patterns for deployment status
7. **Fix missing import in `using-grants.md`** — MsgCloseDeployment import

### Tier 3: Nice to Have (Completeness)

8. **Add missing Console API overview endpoints** — PUT deployment, wallet/list, wallet/default
9. **Add Go AuthZ examples** — MsgGrant/MsgExec in Go SDK
10. **Document Credit Card API** — AEP-63 feature
11. **Verify `@akashnetwork/console-api-client` package** — Remove if non-existent
12. **Add localStorage security warning** — In provider-sdk.md
13. **Complete API Key generation instructions** — In overview.md

---

## 6. Full File-by-File Status

### Console API (`docs/deploy/console-api/`)

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| `overview.md` | 245 | ✅ GOOD | Missing PUT /deployment in table; missing /wallet/list, /wallet/default; only 2 auth methods listed; Quick Start is placeholder comment; references unverified `@akashnetwork/console-api-client` package |
| `authentication.md` | 323 | ✅ GOOD | Comprehensive auth coverage; Go example ignores errors (cosmetic); JWT refresh logic stub |
| `deployment-endpoints.md` | 400+ | ✅ GOOD | Complete CRUD reference with SDL, bids, leases, providers; proper error codes table |
| `managed-wallet.md` | 300+ | ✅ GOOD | Full wallet lifecycle; funding methods; automation example; troubleshooting |

### AuthZ (`docs/authz/`)

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| `overview.md` | ~120 | ✅ GOOD | Clear use cases; grant types; fee grants; architecture diagram |
| `granting-permissions.md` | ~150 | ✅ GOOD | All deployment + market + cert message types; query/revoke commands; security best practices |
| `using-grants.md` | ~200 | ⚠️ MINOR | Missing `MsgCloseDeployment` import; no AuthZ + Console API integration; no Go examples |

### Certificates (`docs/deploy/certificates/`)

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| `jwt-auth.md` | ~120 | ✅ GOOD | Full challenge-response flow; browser + CLI methods; token lifecycle; security practices |
| `mtls-legacy.md` | ~150 | ✅ GOOD | Clearly marked legacy; creation/broadcast/storage; migration guide to JWT |

### SDK — TypeScript (`docs/sdk/typescript/`)

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| `installation.md` | ~180 | ⚠️ MINOR | References deprecated `@akashnetwork/akash-api` in imports; no mention of `chain-sdk` |
| `chain-node-sdk.md` | ~300 | ⚠️ MINOR | Comprehensive server-side SDK; deprecated akash-api imports; no AuthZ coverage |
| `chain-web-sdk.md` | ~300 | ✅ GOOD | Browser wallet integration (Keplr, Leap, Cosmostation); React hooks; testing mocks |
| `provider-sdk.md` | ~350 | ⚠️ MINOR | Full provider interaction; localStorage cert storage security risk; deprecated imports; complete deployment class example |

### SDK — Go (`docs/sdk/go/`)

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| `installation.md` | ~150 | ✅ GOOD | Dependencies, setup, query/tx examples, error handling |
| `client-setup.md` | ~250 | ✅ GOOD | Full client struct; deployment/market operations; tx broadcasting; **no AuthZ examples** |

### SDK Overview

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| `overview.md` | ~120 | ⚠️ MINOR | Missing chain-sdk from comparison table; Go SDK package reference should note chain-sdk migration |

### Top-Level Files

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| `SKILL.md` | ~290 | ✅ GOOD | Complete trigger patterns; CLI binary reference; quick reference; BME model correctly documented; full doc index |
| `ADAPTATION_REPORT.md` | ~200 | ✅ GOOD | Comprehensive migration record; BME migration documented |

---

## 7. Research Verification Results

### Current Akash Ecosystem State (as of 2026-04-10)

| Item | Skill Documents | Current Reality | Gap |
|------|----------------|-----------------|-----|
| Console API Base URL | `https://console-api.akash.network/v1` | ✅ Correct | None |
| Console API Swagger | `https://console-api.akash.network/v1/swagger` | ✅ Correct | None |
| akashjs version | v1.0.0 | v1.0.0 (2025-10-29) | ✅ Current |
| akash-api package | Documented as primary | **DEPRECATED** — replaced by chain-sdk | ⚠️ Needs update |
| chain-sdk | Not mentioned | v1.0.0-alpha.30 (GitHub) | ❌ Missing |
| AuthZ message types | v1beta3 deployment, v1beta4 market | Current | ✅ Correct |
| Managed Wallet denom | uact (BME model) | Correct for deployments | ✅ Correct |
| Gas denom | uakt | Correct for gas | ✅ Correct |
| Rate limits | Free: 60/min, Pro: 300/min | Correct | ✅ Current |
| Credit Card API | Not mentioned | Available (AEP-63) | ❌ Missing |
| Terraform provider | Not mentioned | Stale (May 2024) | N/A |
| Console API version | Not mentioned | v3.59.0 | N/A |

### Key External References Found

| Resource | URL |
|----------|-----|
| Console API Swagger | https://console-api.akash.network/v1/swagger |
| Console API OpenAPI JSON | https://console-api.akash.network/v1/doc |
| akashjs GitHub | https://github.com/akash-network/akashjs |
| chain-sdk GitHub | https://github.com/akash-network/chain-sdk |
| chain-sdk npm | https://www.npmjs.com/package/@akashnetwork/chain-sdk |
| Console GitHub | https://github.com/akash-network/console |
| Official AuthZ Docs | https://akash.network/docs/developers/deployment/authz/ |
| AuthZ SDK Docs | https://akash.network/docs/api-documentation/sdk/authz-feegrant/ |
| DeepWiki Console Routes | https://deepwiki.com/akash-network/console/2.1.1-api-routes-and-endpoints |
| DeepWiki Auth System | https://deepwiki.com/akash-network/console/3.5-authorization-system |
| Credit Card API Blog | https://akash.network/blog/console-api-for-credit-card-users/ |

---

## 8. Deployment Service — Use Case Coverage Matrix

For each of the 10 critical use case requirements:

### 1. Service Account Setup — ⚠️ PARTIAL (5/10)

- ✅ AuthZ overview explains granter/grantee model
- ✅ Granting permissions documented
- ❌ No dedicated "service account setup" guide
- ❌ No key management best practices for service accounts
- ❌ No service account lifecycle documentation

### 2. AuthZ Delegation — ✅ GOOD (8/10)

- ✅ Complete CLI grant/revoke workflow
- ✅ TypeScript SDK grant creation with MsgGrant
- ✅ TypeScript SDK execution with MsgExec
- ✅ All deployment + market + cert message types listed
- ❌ No Go SDK AuthZ examples
- ❌ No AuthZ + Console API integration

### 3. Wallet Management — ✅ GOOD (9/10)

- ✅ Complete managed wallet CRUD (create, list, balance, deposit, default)
- ✅ Funding methods (exchange, IBC, direct send)
- ✅ Deployment with managed wallet workflow
- ✅ Troubleshooting (insufficient balance, wallet not found)
- ❌ No multi-wallet management patterns

### 4. Deployment Lifecycle via API — ✅ GOOD (9/10)

- ✅ Complete CRUD (Create, Get, List, Update, Close, Deposit)
- ✅ SDL validation and pricing endpoints
- ✅ Pagination support
- ✅ Full request/response examples
- ❌ No webhook/notification for state changes

### 5. Lease Management — ✅ GOOD (8/10)

- ✅ List bids, create lease, get lease, close lease
- ✅ Lease status with service URIs
- ✅ Lease logs streaming
- ❌ No bid selection strategy guidance
- ❌ No lease renewal automation pattern

### 6. Manifest Submission — ✅ GOOD (8/10)

- ✅ Basic manifest send via provider SDK
- ✅ Retry logic with exponential backoff
- ✅ Complete deployment class with manifest step
- ❌ No manifest validation before send
- ❌ No Console API manifest endpoint documented

### 7. Fee Delegation — ⚠️ PARTIAL (6/10)

- ✅ FeeGrant CLI commands documented
- ✅ Spending limits and expiration supported
- ✅ FeeGrant + AuthZ combined use mentioned
- ❌ No TypeScript SDK FeeGrant examples
- ❌ No Go SDK FeeGrant examples
- ❌ No programmatic FeeGrant creation guide

### 8. Multi-tenant Patterns — ❌ MISSING (2/10)

- ✅ AuthZ model theoretically supports multi-tenancy
- ❌ No multi-tenant architecture guide
- ❌ No user isolation patterns
- ❌ No resource quota management
- ❌ No billing/settlement patterns
- ❌ No per-user deployment tracking

### 9. Webhook/Event Handling — ❌ MISSING (1/10)

- ✅ Polling for bids is shown in examples (30-second wait)
- ❌ No webhook documentation
- ❌ No event subscription patterns
- ❌ No recommended polling intervals
- ❌ No state transition reference

### 10. Error Handling — ⚠️ PARTIAL (6/10)

- ✅ Console API error codes table documented
- ✅ AuthZ error scenarios (not found, expired, unauthorized)
- ✅ Provider error handling in provider-sdk.md
- ✅ Retry logic examples (exponential backoff)
- ❌ No comprehensive error recovery patterns
- ❌ No common failure scenarios guide
- ❌ No circuit breaker patterns for provider communication

---

## 9. Currency Accuracy (BME Model) — Verification

The skill **correctly** implements the Burn-Mint Equilibrium (BME) model from Mainnet 17:

| Context | Denom Used | Correct? |
|---------|-----------|----------|
| SDL deployment pricing | `uact` | ✅ |
| Deployment deposits | `uact` | ✅ |
| Escrow operations | `uact` | ✅ |
| Fee grants (spend limits) | `uact` | ✅ |
| Gas prices | `uakt` | ✅ |
| Staking/delegation | `uakt` | ✅ |
| Bank sends (AKT transfers) | `uakt` | ✅ |

**No currency accuracy issues found.** The BME migration was applied correctly.

---

## 10. Summary of Recommendations

### Immediate Actions (Before Using for Deployment Service)

1. **Create multi-tenant architecture guide** — This is the single biggest gap
2. **Clarify AuthZ + Console API integration** — Architecture decision needed
3. **Create combined AuthZ + FeeGrant + Managed Wallet pattern guide** — End-to-end example

### Short-Term Improvements

4. Add deprecation notices for `@akashnetwork/akash-api` across all SDK files
5. Create chain-sdk migration guide
6. Add event monitoring / polling best practices
7. Fix missing `MsgCloseDeployment` import in `using-grants.md`

### Long-Term Enhancements

8. Add Go SDK AuthZ examples
9. Document Credit Card API (AEP-63)
10. Verify `@akashnetwork/console-api-client` package exists
11. Add localStorage security warning in provider-sdk.md
12. Complete API Key generation instructions in overview.md

---

## Appendix A: Complete File Inventory

### Files Audited: 60 markdown files + 4 YAML templates + 1 SKILL.md + 1 ADAPTATION_REPORT.md = 66 total

### Critical Path Files (Read Line-by-Line)

- `docs/deploy/console-api/overview.md` (245 lines)
- `docs/deploy/console-api/authentication.md` (323 lines)
- `docs/deploy/console-api/deployment-endpoints.md` (400+ lines)
- `docs/deploy/console-api/managed-wallet.md` (300+ lines)
- `docs/authz/overview.md` (~120 lines)
- `docs/authz/granting-permissions.md` (~150 lines)
- `docs/authz/using-grants.md` (~200 lines)
- `docs/deploy/certificates/jwt-auth.md` (~120 lines)
- `docs/deploy/certificates/mtls-legacy.md` (~150 lines)
- `docs/sdk/overview.md` (~120 lines)
- `docs/sdk/typescript/installation.md` (~180 lines)
- `docs/sdk/typescript/chain-web-sdk.md` (~300 lines)
- `docs/sdk/typescript/chain-node-sdk.md` (~300 lines)
- `docs/sdk/typescript/provider-sdk.md` (~350 lines)
- `docs/sdk/go/installation.md` (~150 lines)
- `docs/sdk/go/client-setup.md` (~250 lines)
- `SKILL.md` (~290 lines)
- `ADAPTATION_REPORT.md` (~200 lines)

### Research Sources Verified

- Console API Swagger and OpenAPI endpoints
- npm packages: @akashnetwork/akashjs, @akashnetwork/akash-api, @akashnetwork/chain-sdk
- GitHub repos: akashjs, akash-api, chain-sdk, console
- Official docs: AuthZ, FeeGrants, Console API
- Community: DeepWiki, HackerNoon

---

**Report completed:** 2026-04-10 21:18 EDT
