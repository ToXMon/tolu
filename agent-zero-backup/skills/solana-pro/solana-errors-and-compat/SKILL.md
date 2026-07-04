---
name: solana-errors-and-compat
description: Diagnose and fix Solana development errors: GLIBC issues, Anchor version conflicts, build failures, deployment errors, transaction simulation errors, Kit v7 gotchas, and toolchain compatibility. Triggers: Solana error, Anchor build fails, GLIBC error, version mismatch, deploy fails, transaction simulation failed, account constraint violated, Kit gotcha, edition2024, platform tools corrupted, migrate Anchor.
version: 1.0.0
---

# Solana Errors & Compatibility

## When to Use

- "Solana error", "Anchor build fails", "GLIBC error", "version mismatch"
- "Anchor install fails", "Anchor upgrade", "migrate Anchor", "toolchain setup"
- "Program failed to deploy", "Transaction simulation failed"
- "Account constraint violated", "discriminator mismatch", "Account not initialized"
- "edition2024 is required", "platform tools corrupted", "custom program error"
- "Kit gotcha", "plugin ordering", "transaction message must be signed"
- Any GLIBC, Rust/Cargo, build, installation, testing, or deployment error on Solana

## Core Operating Behaviors

- **NO_DNA=1 CLI Protocol**: All Solana CLI commands use `NO_DNA=1` prefix to prevent DNA (Do Not Assume) errors. Example: `NO_DNA=1 anchor build`, `NO_DNA=1 solana config set --url devnet`, `NO_DNA=1 cargo build-sbf`, `NO_DNA=1 anchor test`
- **Solana MCP Server**: Reference `https://mcp.solana.com/mcp` for live docs. Use MCP tools before falling back to training data
- **Devnet Default**: All work targets devnet unless explicitly stated: `NO_DNA=1 solana config set --url devnet`
- **Explorer Verification**: Always verify deployments and transactions on https://explorer.solana.com
- **Safety guardrails**: Never deploy to mainnet without explicit human gate approval
- **Version pinning**: Pin all dependency versions explicitly; commit `Cargo.lock`

## Quick Error Classification

| Error Pattern | Category | Key Fix |
|---|---|---|
| `GLIBC_2.39 not found` | GLIBC | Upgrade OS to Ubuntu 24.04+, build Anchor from source, or use Docker |
| `unknown feature proc_macro_span_shrink` | Rust/Cargo | Pin Rust 1.79.0 or use AVM; upgrade to Anchor 0.31+ |
| `unexpected_cfgs` warnings | Rust/Cargo | Add `[lints.rust] unexpected_cfgs = { level = "allow" }` or upgrade Anchor |
| `module inner is private` | Version mismatch | Match `anchor-lang` crate version to CLI version |
| `no such command: build-sbf` | Build | Install Solana CLI; add to PATH |
| `cargo-build-bpf is deprecated` | Build | Use `NO_DNA=1 cargo build-sbf` (Anchor 0.30+ handles this) |
| `Failed to download platform-tools` | Build | Clear `~/.cache/solana/`, retry; check disk space |
| `IDL build failed` | Build | Add `idl-build` feature; set `ANCHOR_LOG=1` for debugging |
| `no method named local_file found` | Build | Upgrade to Anchor 0.31.1+, use stable Rust, or pin proc-macro2 |
| `No space left on device` | Installation | Clean old Solana/Cargo versions; remove `target/` |
| `agave-install not found` | Installation | Reinstall via Solana install script |
| `solana-test-validator` crashes | Testing | Kill existing validators, clean ledger, check ports |
| `connect ECONNREFUSED ::1:8899` | Testing | Use `127.0.0.1` instead of `localhost`; set `NODE_OPTIONS` |
| `feature edition2024 is required` | edition2024 | Pin crates: blake3=1.8.2, constant_time_eq=0.3.1, base64ct=1.7.3, indexmap=2.11.4 |
| `undefined symbol: __isoc23_strtol` (litesvm) | LiteSVM/GLIBC | Upgrade OS, use Docker, or fall back to `solana-bankrun` |
| `The Solana toolchain is corrupted` | Platform Tools | Run `NO_DNA=1 cargo build-sbf --force-tools-install`; ensure ~3GB disk free |
| Plugin ordering type error | Kit gotcha | Install `signer()` before `solanaRpc`/`litesvm` |
| `Program failed to deploy: account already exists` | Deployment | Close existing program or use `--program-id` with new keypair |
| `Transaction simulation failed: Blockhash not found` | Transaction | Fetch fresh blockhash before signing; check RPC connectivity |
| `custom program error: 0x1` | Transaction | InsufficientFunds — fund the account with more SOL |
| `Constraint has been violated: raw_constraint` | Account | Verify account constraints in `#[derive(Accounts)]` match runtime state |
| `Account discriminator mismatch` | Account | Ensure account was initialized by the correct program version |
| `Transaction too large` | Transaction | Exceeds 1232 bytes — split into multiple transactions or use LUTs |
| `@coral-xyz/anchor` not found (v1) | Anchor v1 | Rename to `@anchor-lang/core` in package.json and imports |

## Core Error Categories

> Full diagnostics and solutions in `references/common-errors.md`

### GLIBC Errors
Anchor 0.31+ binaries require GLIBC ≥2.38; 0.32+ requires ≥2.39; v1+ requires ≥2.39. Solutions: upgrade OS (Ubuntu 24.04+), build from source (`NO_DNA=1 cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli`), or use Docker.

### Rust/Cargo Errors
- `proc_macro_span_shrink`: Anchor 0.30.x + Rust ≥1.80 → use AVM (auto-selects Rust 1.79.0) or upgrade to Anchor 0.31+
- `unexpected_cfgs`: Add `[lints.rust] unexpected_cfgs = { level = "allow" }` to Cargo.toml
- `module inner is private`: Match `anchor-lang` crate version to CLI version

### Build Errors
- `cargo build-sbf` not found → install Solana CLI, add to PATH
- Platform tools download failure → clear `~/.cache/solana/`, retry
- IDL generation fails → ensure `idl-build` feature enabled, use `NO_DNA=1 ANCHOR_LOG=1 anchor build`
- `proc_macro2` / `local_file` → upgrade to Anchor 0.31.1+, use stable Rust

### Installation Errors
- `No space left on device` → clean old Solana/Cargo versions (~2-5GB needed)
- `agave-install not found` → reinstall via `sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"`

### Testing Errors
- `solana-test-validator` crashes → kill existing, clean ledger, check ports 8899/8900
- `ECONNREFUSED ::1:8899` → use `127.0.0.1` instead of `localhost`, set `NODE_OPTIONS="--dns-result-order=ipv4first"`
- LiteSVM GLIBC errors → upgrade OS or fall back to `solana-bankrun`

### Anchor Version Migration
- 0.29→0.30: `.accounts()` → `.accountsPartial()`, add `idl-build` feature
- 0.30→0.31: Remove direct `solana-program`/`solana-sdk` deps, use through `anchor-lang`
- 0.31→0.32: `solana-program` removed, use granular crates (`solana_pubkey`), `dup` constraint for duplicate mutable accounts
- 0.32→v1: TS package rename (`@coral-xyz/anchor` → `@anchor-lang/core`), `CpiContext::new` takes `Pubkey` not `AccountInfo`, IDL in Program Metadata, `anchor test` defaults to surfpool, all `solana-*` must be `^3`
- v1.0→v1.1: Minor fixes, ensure `solana-*` crates compatible with v1.1.x

### Kit Gotchas (v7.0.0)
> Full reference in `references/kit/gotchas.md`

- Plugin ordering: `signer()` before `solanaRpc`/`litesvm`
- Await async client: `const client = await createClient().use(signerFromFile(...))`
- `IInstruction` → `Instruction` from `@solana/kit`
- Transaction assertions: `assertTransactionMessageIsFullySigned`, `assertTransactionMessageHasBlockhashLifetime`
- Account existence: `assertAccountExists(account)` before decode
- Fee payer: use `setTransactionMessageFeePayerSigner` (not address)
- Blockhash: refresh after CU estimation
- Kit v7.0.0: requires Node 20+, `@solana/react` decoupled, `@solana/transaction-introspection` is new package, transaction versions Legacy/v0/v1

### edition2024 Crate Issues
Platform-tools v1.48 bundles Cargo 1.84.0 which doesn't support `edition2024`. Pin: `blake3=1.8.2`, `constant_time_eq=0.3.1`, `base64ct=1.7.3`, `indexmap=2.11.4`. Always commit `Cargo.lock`.

### Platform Tools Errors
- `The Solana toolchain is corrupted` → `NO_DNA=1 cargo build-sbf --force-tools-install` (~3GB disk needed)
- Anchor CLI version mismatch warnings → match CLI and crate versions via AVM

### Program Deployment Errors (NEW)
- `account already exists` → close existing program or use new keypair
- `account data size mismatch` → redeploy with `--program-id` matching original
- `Upgrade authority mismatch` → verify with `NO_DNA=1 solana program show <ID>`
- `Insufficient funds for deployment` → airdrop more SOL: `NO_DNA=1 solana airdrop 2`

### Transaction Simulation Errors (NEW)
- `Blockhash not found` → fetch fresh blockhash, check RPC connectivity
- `Instruction error` / `custom program error: 0x1` → InsufficientFunds
- `Transaction too large` → exceeds 1232 bytes, use Address Lookup Tables
- `Compute budget exceeded` → add `ComputeBudgetInstruction::setComputeUnitLimit`

### Account Constraint Errors (NEW)
- `Constraint has been violated: raw_constraint` → verify account constraints match runtime state
- `Account not initialized` → call init instruction first
- `Account discriminator mismatch` → ensure correct program version initialized account
- `Account did not deserialize` → check account owner and data layout
- `Insufficient funds for rent` → fund account with minimum rent-exempt balance
- `Owner mismatch` → verify account owner matches expected program
- `Address not in PDA range` → verify PDA seeds derivation

## Version Compatibility

> Full matrix in `references/compatibility-matrix.md`

### Summary Table

| Anchor Version | Solana CLI | Rust Version | Platform Tools | GLIBC Req | Node.js |
|---|---|---|---|---|---|
| **1.1.x** | 4.x (Agave) | 1.85–1.96+ | v1.52 | ≥2.39 | ≥20 |
| **1.0.x** | 3.x–4.x | 1.85–1.96+ | v1.52 | ≥2.39 | ≥20 |
| **0.32.x** | 2.1.x+ | 1.79–1.85+ | v1.50+ | ≥2.39 | ≥17 |
| **0.31.1** | 2.0.x–2.1.x | 1.79–1.83 | v1.47+ | ≥2.39 | ≥17 |
| **0.30.1** | 1.18.x (rec: 1.18.8+) | 1.75–1.79 | v1.43 | ≥2.31 | ≥16 |
| **0.29.0** | 1.16.x–1.17.x | 1.68–1.75 | v1.37–v1.41 | ≥2.28 | ≥16 |

### Kit & Ecosystem Versions (Latest)

| Component | Version | Notes |
|---|---|---|
| **Anchor** | v1.1.2 | TS pkg: `@anchor-lang/core`; `anchor test` defaults to surfpool |
| **Solana Kit** | v7.0.0 | Requires Node 20+; `@solana/react` decoupled; `@solana/transaction-introspection` NEW |
| **Agave** | v4.1.0 | Solana CLI 4.1.0+; `agave-validator` build-from-source only |
| **Platform Tools** | v1.52 | Bundles Rust ~1.85 fork, Clang 20, target `sbpf-solana-solana` |
| **Rust** | 1.85+ | Required for Anchor v1+ |
| **Node.js** | 20+ | Required for Kit v7.0.0 |
| **Mollusk** | v0.13.4 | Testing tool compatibility |
| **Transaction versions** | Legacy, v0, v1 | Kit v7 supports all three |

### GLIBC Requirements by OS

| OS / Distro | GLIBC | Compatible Anchor |
|---|---|---|
| Ubuntu 24.04 (Noble) | 2.39 | All (0.29–v1+) |
| Ubuntu 22.04 (Jammy) | 2.35 | 0.29–0.30.x only (build 0.31+ from source) |
| Debian 12 (Bookworm) | 2.36 | 0.29–0.30.x only (build 0.31+ from source) |
| Debian 13 (Trixie) | 2.40 | All |
| macOS 14+ (Sonoma) | N/A | All |

## Progressive Disclosure

Full reference documents available via `skills_tool` action `read_file`:

| File | Contents |
|------|----------|
| `references/common-errors.md` | Complete error reference: GLIBC, Rust/Cargo, Build, Installation, Testing, LiteSVM, Platform Tools, edition2024, Deployment, Transaction Simulation, Account Constraint errors with full diagnostics and solutions |
| `references/compatibility-matrix.md` | Full version compatibility matrix, platform-tools mapping, SPL crate versions, TS package versions, testing tool compatibility, known working combinations, transaction versions |
| `references/anchor/migrating-v0.32-to-v1.md` | Complete Anchor v0.32→v1 migration guide: dependency bumps, CPI context changes, duplicate accounts, declare_program! renames, IDL migration, borsh 1.x, SDK 3.x, v1.0→v1.1 notes, Kit v7 changes |
| `references/kit/gotchas.md` | Full Kit gotchas reference: plugin ordering, async client, type errors, runtime errors, Kit v7.0.0 specific gotchas, @solana/react decoupling, transaction versions |

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| solana-environment-setup | Environment setup, toolchain installation, devnet configuration |
| solana-anchor-programs | Writing, building, deploying Anchor programs (not error fixing) |
| solana-client | @solana/kit client SDK, transactions, accounts (not gotcha fixing) |
| solana-testing | Testing with LiteSVM, bankrun, test validator, Mollusk |
| solana-security | Security audit, vulnerability review for program code |
| solana-frontend | dApp UI, wallet connection, framework-kit |
| solana-advanced | Pinocchio, Token-2022, compute budget optimization |

## CLI Usage (NO_DNA)

This skill is a reference knowledge base. Use it to:

1. **Look up errors** by matching error messages to the tables and sections above
2. **Read the full compatibility matrix** for detailed version planning
3. **Read the migration guide** before upgrading Anchor versions
4. **Verify solutions** on Solana Explorer after applying fixes

All CLI commands in this skill use `NO_DNA=1` prefix:
```bash
NO_DNA=1 solana config set --url devnet
NO_DNA=1 anchor build
NO_DNA=1 cargo build-sbf
NO_DNA=1 anchor test
NO_DNA=1 solana program deploy target/deploy/my_program.so
```

## Verification Checklist

- [ ] Error matched to correct category
- [ ] Version compatibility verified against matrix
- [ ] NO_DNA=1 prefix used for all CLI commands
- [ ] Solution verified on Solana Explorer (if deployment related)
- [ ] Cross-skill reference checked if error spans domains
- [ ] Cargo.lock committed after version pinning
- [ ] All `solana-*` crates at correct major version for Anchor version
- [ ] TS package matches Anchor version (`@anchor-lang/core` for v1+, `@coral-xyz/anchor` for 0.x)
- [ ] Node.js version meets minimum (≥20 for Kit v7, ≥17 for Anchor v1)
- [ ] Platform tools version matches Solana CLI version
