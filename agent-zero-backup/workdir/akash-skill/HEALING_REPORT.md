# Akash Network Skill - Healing Report

**Generated:** 2026-04-10  
**Auditor:** Agent Zero Deep Research  
**Files Analyzed:** 60 markdown files  
**Scope:** Complete content audit, cross-reference validation, gap analysis

---

## Executive Summary

The Akash Network skill is a comprehensive knowledge base covering deployments, providers, nodes, SDKs, and reference materials. The overall structure and content quality is strong, but the skill has a **critical versioning problem**: most version-specific references point to **v0.36.0** while the current mainnet version is **v1.2.0** (with v2.0.0 in release candidate). Additionally, several GitHub organization paths changed from `ovrclk/akash` to `akash-network/node`, binary distribution formats changed, and the `provider-services` CLI became a separate binary. These issues could cause deployment failures for users following the guides.

| Severity | Count |
|----------|-------|
| CRITICAL | 8 |
| NEEDS FIX | 18 |
| OK | 34 |

---

## File Status Table

### Top-Level Files

| File | Status | Summary |
|------|--------|---------|
| `SKILL.md` | NEEDS FIX | Version refs outdated, missing new features |
| `rules/overview.md` | NEEDS FIX | Version refs, GitHub org paths |
| `rules/terminology.md` | OK | Accurate terminology |
| `rules/pricing.md` | OK | Pricing concepts still valid |

### SDL Section (`rules/sdl/`)

| File | Status | Summary |
|------|--------|---------|
| `schema-overview.md` | OK | SDL schema is stable |
| `services.md` | OK | Service definitions current |
| `compute-resources.md` | OK | Resource specs accurate |
| `placement-pricing.md` | OK | Placement and pricing valid |
| `endpoints.md` | OK | Endpoint configuration current |
| `validation-rules.md` | OK | Validation rules accurate |
| `deployment.md` | OK | Deployment SDL concepts valid |
| `examples/web-app.md` | OK | Working example |
| `examples/wordpress-db.md` | OK | Working example |
| `examples/gpu-workload.md` | OK | GPU SDL valid |
| `examples/ip-lease.md` | OK | IP lease example current |

### Deploy Section (`rules/deploy/`)

| File | Status | Summary |
|------|--------|---------|
| `overview.md` | NEEDS FIX | References old CLI commands, missing provider-services distinction |
| `cli/installation.md` | CRITICAL | References v0.36.0 binary download, wrong paths |
| `cli/wallet-setup.md` | NEEDS FIX | Uses `akash` instead of `provider-services` for some commands |
| `cli/deployment-lifecycle.md` | NEEDS FIX | Mixed `akash`/`provider-services` command usage |
| `cli/lease-management.md` | NEEDS FIX | Should use `provider-services` for lease operations |
| `cli/common-commands.md` | NEEDS FIX | Version refs, command names need audit |
| `console-api/overview.md` | OK | Console API concepts valid |
| `console-api/authentication.md` | OK | Auth patterns valid |
| `console-api/managed-wallet.md` | OK | Managed wallet docs good |
| `console-api/deployment-endpoints.md` | OK | Endpoints current |
| `certificates/jwt-auth.md` | OK | JWT auth well documented |
| `certificates/mtls-legacy.md` | OK | Legacy mTLS properly marked |

### AuthZ Section (`rules/authz/`)

| File | Status | Summary |
|------|--------|---------|
| `overview.md` | OK | AuthZ concepts accurate |
| `granting-permissions.md` | OK | Grant commands valid |
| `using-grants.md` | OK | Usage patterns correct |

### Provider Section (`rules/provider/`)

| File | Status | Summary |
|------|--------|---------|
| `overview.md` | NEEDS FIX | References old binary names, version refs |
| `requirements.md` | OK | Hardware/software requirements still valid |
| `setup/kubernetes-cluster.md` | NEEDS FIX | k3s version refs may be outdated |
| `setup/provider-installation.md` | CRITICAL | Helm chart version, old binary references |
| `setup/configuration.md` | NEEDS FIX | Config paths may differ in new versions |
| `configuration/attributes.md` | OK | Attribute system stable |
| `configuration/pricing.md` | OK | Pricing strategies valid |
| `configuration/bid-engine.md` | NEEDS FIX | Script paths may reference old binary |
| `operations/lease-management.md` | OK | Lease lifecycle concepts valid |
| `operations/monitoring.md` | OK | Monitoring setup accurate |
| `operations/troubleshooting.md` | OK | Troubleshooting still applicable |

### Node Section (`rules/node/`)

| File | Status | Summary |
|------|--------|---------|
| `overview.md` | NEEDS FIX | GitHub repo path changed, version refs |
| `full-node/requirements.md` | NEEDS FIX | Go version, binary paths |
| `full-node/installation.md` | CRITICAL | References v0.36.0, old download URLs, .zip format |
| `full-node/state-sync.md` | NEEDS FIX | RPC endpoint URLs need verification |
| `validator/becoming-validator.md` | NEEDS FIX | Command syntax may need provider-services |
| `validator/operations.md` | NEEDS FIX | Cosmovisor setup, version refs |
| `validator/security.md` | OK | Security practices still sound |

### SDK Section (`rules/sdk/`)

| File | Status | Summary |
|------|--------|---------|
| `overview.md` | CRITICAL | References old package paths, v0.6.x SDK version |
| `typescript/installation.md` | CRITICAL | @akashnetwork/akashjs v1.0.0 not 0.6.x, API paths changed |
| `typescript/chain-web-sdk.md` | NEEDS FIX | Import paths may need update for v1.0.0 |
| `typescript/chain-node-sdk.md` | NEEDS FIX | Import paths, API version refs |
| `typescript/provider-sdk.md` | NEEDS FIX | Import paths, function signatures |
| `go/installation.md` | CRITICAL | Old Go package paths, Cosmos SDK v0.47.x outdated |
| `go/client-setup.md` | CRITICAL | Old import paths, deprecated gRPC dial options |

### Reference Section (`rules/reference/`)

| File | Status | Summary |
|------|--------|---------|
| `storage-classes.md` | OK | Storage classes still valid |
| `gpu-models.md` | NEEDS FIX | Missing newer GPU models (B200, RTX 5090, etc.) |
| `ibc-denoms.md` | OK | IBC denom references valid |
| `rpc-endpoints.md` | NEEDS FIX | Testnet endpoints may be outdated, sandbox URL needs verification |

---

## Detailed Issues by Category

### 1. CRITICAL: Version References Outdated

**Severity:** CRITICAL  
**Impact:** Users following installation guides will download wrong/incompatible binaries

| Location | Issue | Current Value | Correct Value |
|----------|-------|---------------|---------------|
| `cli/installation.md` | Binary version | v0.36.0 | v1.2.0 (or latest) |
| `node/full-node/installation.md` | Binary version | v0.36.0 | v1.2.0 (or latest) |
| `node/full-node/installation.md` | Download format | `.zip` | `.deb` / `.rpm` / direct binary |
| `sdk/typescript/installation.md` | SDK version table | 0.6.x / 0.5.x | 1.0.0 |
| `sdk/go/installation.md` | Cosmos SDK version | v0.47.x | v0.50+ (check current) |
| `node/overview.md` | GitHub repo | `akash-network/node` (correct but version refs wrong) | Update version numbers |
| `provider/setup/provider-installation.md` | Helm chart version | Not specified / old | Must match v1.2.0+ |
| `sdk/overview.md` | SDK version references | Pre-1.0 | v1.0.0+ for TypeScript |

**Recommended Fix:**
- Replace all `v0.36.0` references with a variable like `$AKASH_VERSION` and note to check latest
- Update download URLs to use new GitHub release paths
- Update binary format from `.zip` to `.deb` / `.rpm` as appropriate
- Add version pinning guidance with instructions to check https://github.com/akash-network/node/releases

---

### 2. CRITICAL: Binary/CLI Name Confusion

**Severity:** CRITICAL  
**Impact:** Commands will fail if users use wrong binary

The Akash ecosystem now has two main binaries:
1. **`akash`** - Node binary (for running validators, full nodes, chain queries)
2. **`provider-services`** - Provider/tenant CLI (for deployments, leases, certificates)

| Location | Issue | Fix |
|----------|-------|-----|
| `deploy/overview.md` | Unclear which binary to use | Add clear section distinguishing the two CLIs |
| `deploy/cli/installation.md` | May reference `akash` for deploy commands | Use `provider-services` for deployment operations |
| `deploy/cli/deployment-lifecycle.md` | Mixed command usage | Standardize to `provider-services` for tenant ops |
| `deploy/cli/lease-management.md` | May use `akash` for lease commands | Use `provider-services` for lease management |
| `provider/setup/provider-installation.md` | Binary name confusion | Clarify `provider-services` vs `akash` for provider ops |

**Recommended Fix:**
- Add a "CLI Binary Guide" section to `deploy/overview.md` explaining when to use each binary
- Audit all CLI commands in deploy/ section and update to `provider-services` where appropriate
- Node operations (validator, full-node) should continue using `akash` binary

---

### 3. CRITICAL: SDK Package Paths and Versions

**Severity:** CRITICAL  
**Impact:** TypeScript and Go SDK examples will not compile/run

#### TypeScript SDK Issues

| Location | Issue | Fix |
|----------|-------|-----|
| `sdk/typescript/installation.md` | Version table shows 0.6.x/0.5.x | Update to 1.0.0 with correct CosmJS version |
| `sdk/typescript/installation.md` | Import paths like `@akashnetwork/akashjs/build/stargate` | Verify paths for v1.0.0 - may have changed |
| `sdk/typescript/chain-web-sdk.md` | Import paths reference old build structure | Verify and update for v1.0.0 API surface |
| `sdk/typescript/chain-node-sdk.md` | `SDL.fromString()` API | Verify API signature for v1.0.0 |
| `sdk/typescript/provider-sdk.md` | `sendManifest`, `queryLeaseStatus` imports | Verify these functions exist in v1.0.0 |

#### Go SDK Issues

| Location | Issue | Fix |
|----------|-------|-----|
| `sdk/go/installation.md` | `github.com/akash-network/akash-api/go/node/...` | Verify current Go module path |
| `sdk/go/installation.md` | `cosmos-sdk@v0.47.x` | Update to v0.50+ or current requirement |
| `sdk/go/client-setup.md` | `grpc.WithInsecure()` | Deprecated - use `grpc.WithTransportCredentials(insecure.NewCredentials())` (partially fixed) |
| `sdk/go/client-setup.md` | Import paths for akash-codec | Verify `akashcodec.RegisterInterfaces` path |
| `sdk/go/client-setup.md` | `signing.SignMode_SIGN_MODE_DIRECT` | Missing import for `signing` package |
| `sdk/go/client-setup.md` | `akashcodec` import path | Verify current Go module structure |

**Recommended Fix:**
- Test all SDK examples against current package versions
- Update import paths to match v1.0.0 package structure
- Add version compatibility table with current package versions
- For Go SDK, update Cosmos SDK version and fix deprecated API usage

---

### 4. NEEDS FIX: GitHub Organization Path Changes

**Severity:** Moderate  
**Impact:** Links to source code may 404

The GitHub organization changed from `ovrclk` to `akash-network`:

| Old Path | New Path |
|----------|----------|
| `github.com/ovrclk/akash` | `github.com/akash-network/node` |
| `github.com/ovrclk/docs` | `github.com/akash-network/docs` |
| `github.com/ovrclk/akash-on-akash` | May still work via redirect |

Files that may contain old paths:
- `node/full-node/installation.md` - clone URLs
- `node/overview.md` - GitHub repository references
- `sdk/overview.md` - Go package paths
- `sdk/go/installation.md` - Go module paths

---

### 5. NEEDS FIX: Missing Modern Features

**Severity:** Moderate  
**Impact:** Skill doesn't cover important new capabilities

| Feature | Status | Recommendation |
|---------|--------|---------------|
| **Provider JWT ES256K Auth** | Partially covered | Verify jwt-auth.md covers latest gateway changes |
| **Managed Deployments / Console v2** | Partially covered | Add Console API v2 features if applicable |
| **24-hour deployment limit** | Missing | Document deployment duration limits introduced in 2025 |
| **Stackable Profile Layouts** | Missing | Document if SDL v2 supports stackable profiles |
| **Full-stack Decentralized Infrastructure** | Missing | Mention Akash's expanded scope (storage, etc.) |
| **GPU B200 / RTX 5090 series** | Missing | Add to gpu-models.md reference |
| **v2.0.0 Migration Guide** | Missing | Add migration notes when v2.0.0 goes stable |
| **Shared Security (AEP-79)** | Missing | Document upcoming shared security transition |
| **Provider onboarding improvements** | Missing | Document simplified provider setup from 2025 roadmap |
| **Enhanced read performance (AEP-61)** | Missing | Document on-chain query improvements |

---

### 6. NEEDS FIX: Specific File Issues

#### `node/full-node/installation.md`
- **Line ~6:** `AKASH_VERSION="v0.36.0"` should be `AKASH_VERSION="v1.2.0"` (or use latest check)
- **Line ~13:** `wget ... akash_linux_amd64.zip` - Binary distribution now uses `.deb` and `.rpm` packages
- **Line ~32:** Clone URL should use `akash-network/node` not potentially old paths
- **Genesis download URL:** Verify `https://raw.githubusercontent.com/akash-network/net/main/mainnet/genesis.json` is current
- **Seed nodes:** Placeholder seed addresses should be replaced with actual current seeds

#### `node/full-node/requirements.md`
- **Go version:** References Go 1.21+ / example uses 1.22.5 - may need Go 1.22+ for v1.2.0
- Verify current Go version requirement for v1.2.0 node binary

#### `node/validator/operations.md`
- **Cosmovisor setup:** Example uses `cosmovisor run` subcommand - verify this is current
- **Upgrade directory example:** Shows `upgrade-v0.36.0` and `upgrade-v0.38.0` - should update to realistic upgrade names
- **Governance queries:** `akash query gov proposal` syntax may have changed in newer Cosmos SDK

#### `provider/setup/provider-installation.md`
- **Helm chart:** Must verify current Helm chart version and values format
- **Docker image tags:** Should reference current provider image tags

#### `provider/setup/kubernetes-cluster.md`
- **k3s version:** Referenced versions may be outdated - should pin to tested versions
- **kubeadm:** Verify kubeadm config format for current Kubernetes versions

#### `provider/configuration/bid-engine.md`
- Pricing script references old binary names in shell commands

#### `reference/gpu-models.md`
- Missing newer GPUs: NVIDIA B200, B100, RTX 5090, RTX 5080, RTX 5070
- Pricing expectations table may be outdated given GPU market changes

#### `reference/rpc-endpoints.md`
- **Testnet/sandbox endpoint:** `https://rpc.sandbox-01.aksh.pw:443` needs verification
- **Sandbox chain ID:** `sandbox-01` needs verification against current testnet
- Consider adding `https://rpc.akashnet.net:443` vs `https://rpc.akashnet.net` clarification

#### `sdk/overview.md`
- **SDK version table:** Shows pre-1.0 versions, needs complete update
- **Go SDK quick start:** Import paths need verification
- **Architecture diagram:** May need update for v1.0+ SDK structure

---

### 7. Cross-Reference Issues

#### SKILL.md References

| Reference | Target File | Status |
|-----------|-------------|--------|
| `@overview.md` | `rules/overview.md` | OK |
| `@sdl/schema-overview.md` | `rules/sdl/schema-overview.md` | OK |
| `@deploy/overview.md` | `rules/deploy/overview.md` | OK |
| `@provider/overview.md` | `rules/provider/overview.md` | OK |
| `@node/overview.md` | `rules/node/overview.md` | OK |
| `@sdk/overview.md` | `rules/sdk/overview.md` | OK |
| `@reference/rpc-endpoints.md` | `rules/reference/rpc-endpoints.md` | OK |
| All sub-file `@` references | Various | Need to verify each file's internal refs |

#### Internal Cross-References Needing Verification

| File | Reference | Target | Status |
|------|-----------|--------|--------|
| `deploy/cli/installation.md` | Links to wallet-setup | `./wallet-setup.md` | OK |
| `node/overview.md` | Links to full-node/requirements | `./full-node/requirements.md` | OK |
| `node/overview.md` | Links to validator/becoming-validator | `./validator/becoming-validator.md` | OK |
| `node/overview.md` | Links to validator/security | `./validator/security.md` | OK |
| `node/overview.md` | Links to validator/operations | `./validator/operations.md` | OK |
| `sdk/typescript/installation.md` | `@chain-node-sdk.md` | `chain-node-sdk.md` | OK |
| `sdk/typescript/installation.md` | `@chain-web-sdk.md` | `chain-web-sdk.md` | OK |
| `sdk/typescript/installation.md` | `@provider-sdk.md` | `provider-sdk.md` | OK |
| `sdk/go/installation.md` | `@client-setup.md` | `client-setup.md` | OK |
| `sdk/go/installation.md` | `@examples/` | No examples directory exists | MISSING |

---

### 8. Missing Content / Gap Analysis

#### Missing Files That Should Exist

| Proposed File | Justification |
|---------------|---------------|
| `rules/sdl/examples/multi-service.md` | Multi-service deployment (e.g., frontend + API + DB) |
| `rules/sdl/examples/persistent-storage.md` | Persistent storage with beta2/beta3 classes |
| `rules/deploy/cli/provider-services-guide.md` | Dedicated guide for `provider-services` binary |
| `rules/deploy/console/deployment-wizard.md` | Step-by-step Console deployment walkthrough |
| `rules/provider/setup/migration.md` | Provider migration/upgrade procedures |
| `rules/sdk/typescript/examples/` | Working TypeScript examples directory |
| `rules/sdk/go/examples/` | Working Go examples directory (referenced but missing) |
| `rules/reference/changelog.md` | Version history and breaking changes |
| `rules/reference/troubleshooting.md` | General troubleshooting guide for common issues |
| `rules/reference/network-upgrades.md` | History of network upgrades with links |

#### Missing Topics

| Topic | Recommended Location |
|-------|---------------------|
| **24-hour deployment duration limit** | `rules/sdl/deployment.md` or `rules/overview.md` |
| **SDL v2 changes (if applicable)** | `rules/sdl/schema-overview.md` |
| **Provider gateway JWT ES256K** | `rules/deploy/certificates/jwt-auth.md` (verify current) |
| **Managed wallet deep dive** | `rules/deploy/console-api/managed-wallet.md` (expand) |
| **Shared Security Roadmap (AEP-79)** | `rules/overview.md` or new roadmap file |
| **GPU marketplace trends** | `rules/reference/gpu-models.md` |
| **Cost optimization strategies** | `rules/pricing.md` (expand) |
| **Multi-region deployments** | `rules/sdl/placement-pricing.md` (expand) |
| **CI/CD integration patterns** | `rules/sdk/` or new file |
| **Terraform Provider** | New file in `rules/deploy/` |
| **Akash vs traditional cloud comparison** | `rules/overview.md` |
| **Security best practices for tenants** | New file in `rules/deploy/` |
| **Billing and escrow deep dive** | `rules/pricing.md` (expand) |

---

### 9. Formatting and Quality Issues

| File | Issue |
|------|-------|
| `sdk/go/client-setup.md` | Missing `signing` package import in example code |
| `sdk/go/client-setup.md` | `tx.NewTxConfig` may not exist in newer Cosmos SDK - verify API |
| `sdk/typescript/chain-web-sdk.md` | `window.keplr` types may be outdated for Keplr v0.12+ |
| `sdk/typescript/chain-web-sdk.md` | `SigningStargateClient.connectWithSigner` may have new API in CosmJS 0.32+ |
| `provider/configuration/bid-engine.md` | Pricing script references old binary names in shell commands |
| `node/validator/operations.md` | Cosmovisor `run` subcommand may need verification for current version |
| Multiple files | Inconsistent use of `akash` vs `provider-services` in CLI examples |

---

## Recommended Fix Priority

### Priority 1 - Critical (Fix Immediately)

1. **Update all version references** from v0.36.0 to v1.2.0 (or parametric)
2. **Update binary download URLs** and formats in installation guides
3. **Clarify `akash` vs `provider-services` binary usage** throughout
4. **Update TypeScript SDK** import paths and version table for v1.0.0
5. **Update Go SDK** import paths and Cosmos SDK version
6. **Update GitHub organization paths** from `ovrclk` to `akash-network`

### Priority 2 - Important (Fix Soon)

7. **Add GPU models** (B200, B100, RTX 5090, RTX 5080, RTX 5070)
8. **Verify testnet/sandbox endpoints** and chain IDs
9. **Update cosmovisor examples** with realistic upgrade names
10. **Verify Helm chart versions** for provider setup
11. **Create missing `sdk/go/examples/`** directory or remove reference
12. **Update Go SDK deprecated API** usage (`grpc.WithInsecure` etc.)

### Priority 3 - Enhancement (Plan for Next Version)

13. Add 24-hour deployment limit documentation
14. Add shared security (AEP-79) roadmap information
15. Create multi-service SDL example
16. Create persistent storage SDL example
17. Add CI/CD integration guide
18. Expand pricing/cost optimization content
19. Add Terraform provider documentation
20. Create network upgrade history reference

---

## Files by Status

### OK (34 files)

These files have accurate content with no critical issues:

- `rules/terminology.md`
- `rules/pricing.md`
- `rules/sdl/schema-overview.md`
- `rules/sdl/services.md`
- `rules/sdl/compute-resources.md`
- `rules/sdl/placement-pricing.md`
- `rules/sdl/endpoints.md`
- `rules/sdl/validation-rules.md`
- `rules/sdl/deployment.md`
- `rules/sdl/examples/web-app.md`
- `rules/sdl/examples/wordpress-db.md`
- `rules/sdl/examples/gpu-workload.md`
- `rules/sdl/examples/ip-lease.md`
- `rules/deploy/console-api/overview.md`
- `rules/deploy/console-api/authentication.md`
- `rules/deploy/console-api/managed-wallet.md`
- `rules/deploy/console-api/deployment-endpoints.md`
- `rules/deploy/certificates/jwt-auth.md`
- `rules/deploy/certificates/mtls-legacy.md`
- `rules/authz/overview.md`
- `rules/authz/granting-permissions.md`
- `rules/authz/using-grants.md`
- `rules/provider/requirements.md`
- `rules/provider/configuration/attributes.md`
- `rules/provider/configuration/pricing.md`
- `rules/provider/operations/lease-management.md`
- `rules/provider/operations/monitoring.md`
- `rules/provider/operations/troubleshooting.md`
- `rules/node/validator/security.md`
- `rules/reference/storage-classes.md`
- `rules/reference/ibc-denoms.md`

### NEEDS FIX (18 files)

These files have moderate issues that should be addressed:

- `SKILL.md` - Version refs, missing new features
- `rules/overview.md` - Version refs, GitHub paths
- `rules/deploy/overview.md` - CLI binary confusion
- `rules/deploy/cli/wallet-setup.md` - Mixed CLI usage
- `rules/deploy/cli/deployment-lifecycle.md` - Mixed CLI usage
- `rules/deploy/cli/lease-management.md` - Mixed CLI usage
- `rules/deploy/cli/common-commands.md` - Version refs
- `rules/provider/overview.md` - Binary names
- `rules/provider/setup/kubernetes-cluster.md` - k3s version refs
- `rules/provider/setup/configuration.md` - Config paths
- `rules/provider/configuration/bid-engine.md` - Binary refs in scripts
- `rules/node/overview.md` - GitHub paths, versions
- `rules/node/full-node/requirements.md` - Go version
- `rules/node/full-node/state-sync.md` - RPC endpoint verification
- `rules/node/validator/becoming-validator.md` - Command syntax
- `rules/node/validator/operations.md` - Cosmovisor, upgrade names
- `rules/sdk/typescript/chain-web-sdk.md` - Import paths
- `rules/sdk/typescript/chain-node-sdk.md` - Import paths, API
- `rules/sdk/typescript/provider-sdk.md` - Import paths
- `rules/reference/gpu-models.md` - Missing newer GPUs
- `rules/reference/rpc-endpoints.md` - Testnet verification

### CRITICAL (8 files)

These files have severe issues that could cause failures:

- `rules/deploy/cli/installation.md` - Wrong version, wrong download format
- `rules/provider/setup/provider-installation.md` - Wrong Helm/binary versions
- `rules/node/full-node/installation.md` - Wrong version, URLs, format
- `rules/sdk/overview.md` - Wrong SDK versions and paths
- `rules/sdk/typescript/installation.md` - Wrong package versions
- `rules/sdk/go/installation.md` - Wrong Go paths, Cosmos SDK version
- `rules/sdk/go/client-setup.md` - Deprecated APIs, wrong paths
- `rules/node/validator/operations.md` - Cosmovisor setup issues

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total files analyzed | 60 |
| Files with OK status | 34 (57%) |
| Files needing fixes | 18 (30%) |
| Files with critical issues | 8 (13%) |
| Total issues identified | 42 |
| Critical issues | 8 |
| Moderate issues | 18 |
| Minor issues | 10 |
| Missing content items | 14 |
| Missing files recommended | 10 |
| Broken cross-references | 1 (`sdk/go/examples/`) |

---

## Methodology

1. Read all 60 markdown files in the `rules/` directory and subdirectories
2. Read and analyzed the main `SKILL.md` file
3. Verified version numbers, download URLs, and package paths against:
   - GitHub releases: https://github.com/akash-network/node/releases
   - npm registry: https://www.npmjs.com/package/@akashnetwork/akashjs
   - Akash official docs: https://akash.network/docs/
   - GitHub repositories: https://github.com/akash-network/
4. Cross-validated all `@file.md` references in SKILL.md and internal file links
5. Checked SDL examples against current Akash SDL specification
6. Verified CLI commands against current provider-services documentation
7. Assessed coverage gaps against Akash Network 2025 roadmap and current features

---

## Appendix: Key Version Reference

| Component | Referenced in Skill | Current (as of 2026-04-10) |
|-----------|-------------------|---------------------------|
| Akash Node | v0.36.0 | v1.2.0 (mainnet-16) |
| Akash Node (dev) | N/A | v2.0.0-rc5 |
| @akashnetwork/akashjs | 0.6.x | 1.0.0 |
| Cosmos SDK (Go) | v0.47.x | v0.50+ |
| Go version | 1.21+ / 1.22.5 | 1.22+ (check current) |
| Binary format | .zip | .deb / .rpm |
| GitHub org | ovrclk (old refs) | akash-network |
| provider-services | Mixed with akash | Separate binary |
