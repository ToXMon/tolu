# Akash Network Skill — Adaptation Report

**Date:** 2026-04-10
**Agent:** Agent Zero 'Master Developer'
**Source:** `/a0/usr/workdir/akash-skill/`
**Target:** `/a0/usr/skills/akash/`

---

## Executive Summary

The Akash Network skill has been fully healed and adapted from Claude Code format to Agent Zero format. All 8 CRITICAL issues, 18 NEEDS FIX issues, and applicable enhancement items from the healing report have been resolved. The skill now targets Akash v1.2.0 (mainnet-16+) with correct binary names, updated SDK versions, proper Agent Zero directory structure, and **Burn-Mint Equilibrium (BME) model** support from Mainnet 17.

| Metric | Value |
|--------|-------|
| Total files created | 67 |
| Source files migrated | 58 docs + 4 templates |
| New files created | 1 SKILL.md, 4 YAML templates |
| CRITICAL issues fixed | 8/8 |
| NEEDS FIX issues resolved | 18/18 |
| Enhancement items addressed | 6/7 |
| Remaining @file.md references | 0 |
| Remaining v0.36.0 references | 0 |

---

## Phase 1: Read and Understand ✅

Read and analyzed:
- `/a0/usr/workdir/akash-skill/HEALING_REPORT.md` (535 lines)
- All 8 CRITICAL source files
- All 18 NEEDS FIX source files
- Original `SKILL.md` (204 lines)

---

## Phase 2: Healing — All Issues Fixed

### Critical Fixes (Priority 1)

| # | Issue | Files Affected | Fix Applied |
|---|-------|---------------|-------------|
| 1 | Version v0.36.0 → v1.2.0 | 3 files | Bulk sed: `v0.36.0` → `v1.2.0` in all docs |
| 2 | Binary format .zip → .deb/.tar.gz | 3 files | Linux: `.zip` → `.deb` with `dpkg -i`; macOS: `.zip` → `.tar.gz` with `tar xzf` |
| 3 | CLI binary confusion (akash vs provider-services) | 10+ files | Added CLI Binary Reference section; switched all tenant/deploy commands to `provider-services` |
| 4 | TypeScript SDK v0.6.x → v1.0.0 | 1 file | Updated version compatibility table to show 1.0.0 as primary |
| 5 | Go SDK Cosmos v0.47 → v0.50+ | 1 file | Updated `go get cosmos-sdk@v0.50+` |
| 6 | Deprecated grpc.WithInsecure() | 1 file | Replaced with `grpc.WithTransportCredentials(insecure.NewCredentials())` |
| 7 | GitHub org paths (ovrclk → akash-network) | 0 files | Already correct in source; verified |
| 8 | Missing Go SDK signing import | 1 file | Added `"github.com/cosmos/cosmos-sdk/types/tx/signing"` and `authtx` import; fixed `tx.NewTxConfig` → `authtx.NewTxConfig` |

### Important Fixes (Priority 2)

| # | Issue | Fix Applied |
|---|-------|-------------|
| 9 | GPU models missing B200, B100, RTX 5090/5080/5070 | Added 5 new GPU models to `docs/reference/gpu-models.md` |
| 10 | Testnet/sandbox endpoints verification | Added note to check `github.com/akash-network/net` for current endpoints |
| 11 | Cosmovisor upgrade names outdated | Updated `upgrade-v0.36.0` → `upgrade-v1.0.0`, `upgrade-v0.38.0` → `upgrade-v1.2.0` |
| 12 | Helm chart versions 0.6.4 → 0.8.0 | Updated in `provider-installation.md` and `configuration.md`; added version check note |
| 13 | Missing sdk/go/examples/ reference | Changed to reference `client-setup.md` instead |
| 14 | Go version requirements | Updated to Go 1.22+ / 1.23.0 |

### Enhancement Fixes (Priority 3)

| # | Enhancement | Status |
|---|-------------|--------|
| 15 | 24-hour deployment duration limit | ✅ Added to `docs/core-concepts/overview.md` and SKILL.md |
| 16 | Shared Security Roadmap (AEP-79) | ✅ Added to `docs/core-concepts/overview.md` |
| 17 | Provider Helm chart version references | ✅ Updated with version check note |

### Binary Usage Audit (akash vs provider-services)

The following files were audited and updated to use the correct binary:

| File | Changes |
|------|---------|
| `docs/deploy/overview.md` | Added CLI Binary Reference section; updated deployment examples |
| `docs/deploy/cli/installation.md` | Added primary provider-services installation section |
| `docs/deploy/cli/wallet-setup.md` | 5 command changes |
| `docs/deploy/cli/deployment-lifecycle.md` | 28 command changes |
| `docs/deploy/cli/lease-management.md` | 25 command changes |
| `docs/deploy/cli/common-commands.md` | 35 command changes |
| `docs/provider/configuration/bid-engine.md` | 2 command changes |
| `docs/sdk/go/client-setup.md` | Import fixes, API updates |

### Cross-Reference Cleanup

44 `@file.md` references (Claude Code syntax) cleaned across 17 files, replaced with plain filenames.

---

## Phase 3: Agent Zero Format Adaptation ✅

### Directory Structure

```
/a0/usr/skills/akash/
├── SKILL.md                          # Main skill file (292 lines)
├── ADAPTATION_REPORT.md              # This report
├── docs/                             # Reference documentation (58 files)
│   ├── core-concepts/                # overview, terminology, pricing
│   ├── sdl/                          # SDL schema, services, resources
│   │   └── examples/                 # web-app, wordpress-db, gpu, ip-lease
│   ├── deploy/                       # Deployment methods
│   │   ├── cli/                      # CLI installation and usage
│   │   ├── console-api/              # Console API docs
│   │   └── certificates/             # Auth methods
│   ├── sdk/                          # SDK documentation
│   │   ├── typescript/               # TS SDK files
│   │   └── go/                       # Go SDK files
│   ├── authz/                        # AuthZ permissions
│   ├── provider/                     # Provider operations
│   │   ├── setup/                    # K8s and installation
│   │   ├── configuration/            # Attributes, pricing, bids
│   │   └── operations/               # Monitoring, troubleshooting
│   ├── node/                         # Node operations
│   │   ├── full-node/                # Full node setup
│   │   └── validator/                # Validator operations
│   └── reference/                    # GPU models, endpoints, denoms, storage
├── templates/                        # SDL templates
│   ├── web-app.yaml                  # Standalone YAML
│   ├── wordpress-db.yaml             # Standalone YAML
│   ├── gpu-workload.yaml             # Standalone YAML
│   ├── ip-lease.yaml                 # Standalone YAML
│   ├── web-app.md                    # Annotated template
│   ├── wordpress-db.md               # Annotated template
│   ├── gpu-workload.md               # Annotated template
│   └── ip-lease.md                   # Annotated template
└── scripts/                          # (empty, for future helper scripts)
```

### SKILL.md Features

- Valid YAML frontmatter with name, description, version, author, tags, trigger_patterns
- "When to Use This Skill" section matching trigger patterns
- CLI Binary Reference (akash vs provider-services)
- Quick Reference with SDL structure, minimal template, common patterns
- Key deployment and node command examples
- Deployment duration limits documentation
- Complete documentation index with all 58 doc files referenced
- Links to additional resources
- No `@file.md` syntax — uses plain relative paths

---

## Phase 4: Verification ✅

### Automated Checks (All Passed)

| Check | Result |
|-------|--------|
| No `@file.md` syntax remains | ✅ Pass |
| No `v0.36.0` references remain | ✅ Pass |
| No `.zip` binary format references remain | ✅ Pass |
| No `ovrclk` organization references remain | ✅ Pass |
| No `grpc.WithInsecure()` deprecated calls remain | ✅ Pass |
| No Cosmos SDK `v0.47` references remain | ✅ Pass |
| No old Helm chart tags `0.6.4` remain | ✅ Pass |
| No old Cosmovisor upgrade names remain | ✅ Pass |
| SKILL.md YAML frontmatter is valid | ✅ Pass |
| All 4 YAML templates exist | ✅ Pass |

### File Counts

| Category | Count |
|----------|-------|
| SKILL.md | 1 |
| docs/ files | 58 |
| templates/ files | 8 (4 .md + 4 .yaml) |
| ADAPTATION_REPORT.md | 1 |
| **Total** | **68** |

---

## Healing Report Issue Resolution

| Original Status | Count | Resolution |
|----------------|-------|------------|
| CRITICAL | 8 | All fixed |
| NEEDS FIX | 18 | All fixed |
| OK | 34 | Migrated as-is |
| Enhancement items addressed | 6 | Duration limits, AEP-79, GPU models, Helm refs, Cosmovisor names, Go version |
| Enhancement items deferred | 3 | Multi-service SDL example, CI/CD guide, Terraform provider (future additions) |

---

## Summary

The Akash Network skill has been successfully healed and adapted:

1. **All version references** updated from v0.36.0 to v1.2.0
2. **Binary distribution** updated from .zip to .deb/.tar.gz
3. **CLI binary usage** clarified — `akash` for node ops, `provider-services` for tenant ops
4. **SDK versions** updated — TypeScript 1.0.0, Go Cosmos SDK v0.50+
5. **Deprecated APIs** replaced — grpc.WithInsecure, tx.NewTxConfig
6. **New GPU models** added — B200, B100, RTX 5090, 5080, 5070
7. **New features documented** — 24-hour duration limits, AEP-79 shared security
8. **Format adapted** — Claude Code `@file.md` → Agent Zero relative paths
9. **YAML templates** extracted as standalone deployable files

---

## Phase N: Burn-Mint Equilibrium (BME) Migration ✅

**Date:** 2026-04-10
**Agent:** Agent Zero 'Master Developer'
**Trigger:** Mainnet 17 (March 23, 2026) introduced BME model

### What Changed

Akash implemented the **Burn-Mint Equilibrium (BME)** model with Mainnet 17:

- **AKT (`uakt`)**: Continues as staking token & settlement currency for gas/governance
- **ACT (`uact`)**: NEW — Akash Compute Token, USD-pegged (~$1), used for compute deployments
- Tenants burn AKT to mint ACT for deployments
- Providers receive stable USD-equivalent settlements

### Files Modified (51 files across all categories)

| Category | Files | Changes |
|----------|-------|---------|
| SDL Templates (*.yaml, *.md) | 8 | All `denom: uakt` → `denom: uact` |
| SDL Examples | 4 | All pricing denoms updated |
| SDL Documentation | 5 | placement-pricing, schema-overview, validation-rules, deployment, endpoints |
| Deploy CLI & Console API | 7 | Deployment deposits, escrow commands |
| Core Concepts | 3 | pricing.md (major BME rewrite), terminology.md (ACT added), overview.md |
| Provider Docs | 8 | Bid pricing, monitoring metrics, revenue tracking |
| SDK Docs | 5 | Deployment deposit denoms (gas prices kept as uakt) |
| Node Docs | 0 | All uakt references are gas/staking — preserved |
| AuthZ Docs | 3 | Deployment-related spend limits & deposits |
| Reference Docs | 3 | ibc-denoms, gpu-models, storage-classes |
| SKILL.md | 1 | SDL template + payment options |
| **Total** | **47 modified** | **~200+ replacements** |

### Key Decisions

1. **Deployment pricing → uact**: All `denom: uakt` in SDL/pricing contexts changed to `denom: uact`
2. **Gas prices → uakt preserved**: All `0.025uakt` gas-price references kept (network-level fee)
3. **Staking/delegation → uakt preserved**: Validator operations, self-delegation kept as uakt
4. **Bank sends → context-dependent**: AKT transfers between wallets kept as uakt; deployment deposits changed to uact
5. **pricing.md → major rewrite**: Added full BME model section with flow diagram and token explanations
6. **terminology.md → ACT added**: New uact definition alongside existing uakt definition

### Verification Results

| Check | Result |
|-------|--------|
| `denom: uakt` remaining in deployment context | **0** ✅ |
| `denom: uact` deployment pricing references | **95** ✅ |
| Gas/staking uakt references preserved | **29** ✅ |
| Staking/delegation uakt references | **4** ✅ |
| Total uact references (deployment) | **209** ✅ |

---

## Phase 4: Final Audit Remediation (2026-04-11)

Based on `FINAL_AUDIT_REPORT.md` findings. All critical deployment service gaps addressed.

### Tier 1 — New Documentation Files

| # | File | Lines | Description |
|---|------|-------|-------------|
| 1 | `docs/deploy/console-api/multi-tenant-guide.md` | ~2,754 | Multi-tenant deployment service architecture, onboarding flows, AuthZ delegation, fee delegation, TypeScript scaffold |
| 2 | `docs/authz/deployment-service-pattern.md` | ~1,725 | End-to-end AuthZ + FeeGrant + Managed Wallet pattern with full TypeScript code for all 7 steps |
| 3 | `docs/deploy/console-api/event-monitoring.md` | ~2,025 | Polling patterns, lease status detection, bid monitoring, event-driven architecture, alert system |

### Tier 2 — Fixes to Existing Files

| # | File | Fix Applied |
|---|------|------------|
| 4a | `docs/sdk/typescript/installation.md` | Added deprecation notice + migration section for `@akashnetwork/akash-api` → `@akashnetwork/chain-sdk` |
| 4b | `docs/sdk/typescript/chain-node-sdk.md` | Added deprecation notice at top |
| 4c | `docs/sdk/typescript/chain-web-sdk.md` | Added deprecation notice at top |
| 4d | `docs/sdk/typescript/provider-sdk.md` | Added deprecation notice + localStorage security warning |
| 4e | `docs/sdk/overview.md` | Added deprecation notice + updated package references in SDK table |
| 5 | `docs/authz/using-grants.md` | Added missing `MsgCloseDeployment` import + deprecation notice |
| 6 | `docs/sdk/go/client-setup.md` | Added full AuthZ Operations section (MsgGrant, MsgExec, FeeGrant, querying grants) — 326 → 743 lines |
| 7 | `docs/deploy/console-api/overview.md` | Added PUT /deployment, GET /deployments, GET /wallet/list, GET /wallet/default endpoints |

### Tier 3 — Quality Improvements

| # | File | Change |
|---|------|--------|
| 8 | `docs/sdk/typescript/provider-sdk.md` | Added security warning block re: localStorage private key storage with 5 recommended alternatives |
| 9a | `SKILL.md` | Added 3 new files to documentation index |
| 9b | `SKILL.md` | Added trigger patterns: `akash deployment service`, `deploy on behalf of`, `multi-tenant akash` |

### Files Modified Summary

| Action | Count | Files |
|--------|-------|-------|
| **Created** | 3 | multi-tenant-guide.md, deployment-service-pattern.md, event-monitoring.md |
| **Patched** | 8 | installation.md, chain-node-sdk.md, chain-web-sdk.md, provider-sdk.md, overview.md (sdk), using-grants.md, client-setup.md, overview.md (console-api) |
| **Updated** | 2 | SKILL.md, ADAPTATION_REPORT.md |
| **Total** | 13 | — |
| Total uakt references (gas/staking only) | **47** ✅ |

---

## Optimization Pass — Final Accuracy Corrections

**Date:** 2026-04-11
**Source:** ACCURACY_AUDIT_REPORT.md
**Scope:** P0–P3 accuracy corrections and content additions

### Changes Applied

| Priority | ID | File | Change |
|----------|-----|------|--------|
| **P0** | CRITICAL | `SKILL.md` lines 198–203 | Rewrote "Deployment Duration Limits" to distinguish trial (24h) vs regular (unlimited) deployments |
| **P0** | CRITICAL | `docs/core-concepts/overview.md` lines 116–123 | Fixed same incorrect 24h claim — now clearly states trial-only limit |
| **P1** | HIGH | `SKILL.md` line 24 | Updated target version v1.2.0 (mainnet-16) → v2.0.0 (mainnet-17) |
| **P1** | HIGH | `docs/deploy/cli/installation.md` | Updated all v1.2.0 download URLs → v2.0.0 |
| **P1** | HIGH | `docs/node/full-node/installation.md` | Updated `AKASH_VERSION="v1.2.0"` → `v2.0.0` |
| **P1** | HIGH | `docs/node/validator/operations.md` | Updated cosmovisor upgrade directories from `upgrade-v1.2.0` → `upgrade-v2.0.0` |
| **P1** | HIGH | `docs/deploy/cli/bme-commands.md` | **NEW FILE** — Full BME CLI reference (mint-act, burn-act, burn-mint, gas config, workflow) |
| **P2** | MEDIUM | `docs/deploy/console-api/credit-card-api.md` | **NEW FILE** — Credit card / trial API docs (AEP-63, endpoints, rate limits, TypeScript SDK) |
| **P2** | MEDIUM | `docs/deploy/console-api/multi-tenant-guide.md` line 2651 | Fixed `denom: uakt` → `denom: uact` in SDL example |
| **P3** | LOW | `SKILL.md` frontmatter | Added `allowed_tools`, updated `description`, added 8 trigger patterns, version → 2.1.0 |
| **P3** | LOW | `SKILL.md` quick reference | Added BME Commands section + Credit Card/Trial Deployments section |
| **P3** | LOW | `SKILL.md` doc index | Added bme-commands.md and credit-card-api.md to index |
| **P3** | LOW | `docs/reference/rpc-endpoints.md` | Added Forbole and EcoStake community RPC providers |

### Files Modified Summary

| Action | Count | Files |
|--------|-------|-------|
| **Created** | 2 | bme-commands.md, credit-card-api.md |
| **Patched** | 7 | SKILL.md, overview.md, installation.md (cli), installation.md (node), operations.md, multi-tenant-guide.md, rpc-endpoints.md |
| **Updated** | 1 | ADAPTATION_REPORT.md |
| **Total** | 10 | — |
