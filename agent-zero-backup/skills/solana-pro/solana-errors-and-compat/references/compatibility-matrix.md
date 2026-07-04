---
title: Version Compatibility Matrix
description: Reference table for matching Anchor, Solana CLI, Rust, Kit, and Node.js versions to avoid toolchain conflicts. Updated for Anchor v1.1.2, Kit v7.0.0, Agave v4.1.0.
---

# Solana Version Compatibility Matrix

> **Protocol**: All CLI commands use `NO_DNA=1` prefix. All work targets devnet unless stated otherwise.

## Master Compatibility Table

| Anchor Version | Release Date | Solana CLI | Rust Version | Platform Tools | GLIBC Req | Node.js | Key Notes |
|---|---|---|---|---|---|---|---|
| **1.1.x** | Q2 2026 | 4.x (Agave) | 1.85–1.96+ | v1.52 | ≥2.39 | ≥20 | Minor fixes over v1.0; Kit v7 compat; `@anchor-lang/core ^1.1.0` |
| **1.0.x** | Q1 2026 | 3.x–4.x | 1.85–1.96+ | v1.52 | ≥2.39 | ≥20 | TS pkg → `@anchor-lang/core`; `anchor test` defaults to surfpool; IDL in Program Metadata; no `solana` CLI shell-out; all `solana-*` deps must be `^3`; `solana-program` removed as project dep; `solana-signer` replaces `solana-sdk` for signing |
| **0.32.x** | Oct 2025 | 2.1.x+ | 1.79–1.85+ | v1.50+ | ≥2.39 | ≥17 | Replaces `solana-program` with smaller crates; IDL builds on stable Rust; removes Solang |
| **0.31.1** | Apr 2025 | 2.0.x–2.1.x | 1.79–1.83 | v1.47+ | ≥2.39 ⚠️ | ≥17 | New Docker image `solanafoundation/anchor`; published under solana-foundation org. **Tested: binary requires GLIBC 2.39, not 2.38** |
| **0.31.0** | Mar 2025 | 2.0.x–2.1.x | 1.79–1.83 | v1.47+ | ≥2.39 ⚠️ | ≥17 | Solana v2 upgrade; dynamic discriminators; `LazyAccount`; `declare_program!` improvements. **Pre-built binary needs GLIBC 2.39** |
| **0.30.1** | Jun 2024 | 1.18.x (rec: 1.18.8+) | 1.75–1.79 | v1.43 | ≥2.31 | ≥16 | `declare_program!` macro; legacy IDL conversion; `RUSTUP_TOOLCHAIN` override |
| **0.30.0** | Apr 2024 | 1.18.x (rec: 1.18.8) | 1.75–1.79 | v1.43 | ≥2.31 | ≥16 | New IDL spec; token extensions; `cargo build-sbf` default; `idl-build` feature required |
| **0.29.0** | Oct 2023 | 1.16.x–1.17.x | 1.68–1.75 | v1.37–v1.41 | ≥2.28 | ≥16 | Account reference changes; `idl build` compilation method; `.anchorversion` file |

## Solana CLI Version Mapping (Agave)

| Solana CLI | Agave Version | Era | solana-program Crate | Platform Tools | Status |
|---|---|---|---|---|---|
| **4.1.x** | v4.1.0 | Jul 2026 | N/A (validator only) | v1.52 | Latest stable |
| **4.0.x** | v4.0.x | Q2 2026 | N/A (validator only) | v1.52 | Stable |
| **3.1.x** | v3.1.x | Jan 2026 | N/A (validator only) | v1.52 | Legacy stable |
| **3.0.x** | v3.0.x | Late 2025 | N/A (validator only) | v1.52 | Legacy |
| **2.1.x** | v2.1.x | Mid 2025 | 2.x | v1.47–v1.51 | Legacy |
| **2.0.x** | v2.0.x | Early 2025 | 2.x | v1.44–v1.47 | Legacy |
| **1.18.x** | N/A (pre-Anza) | 2024 | 1.18.x | v1.43 | Deprecated |
| **1.17.x** | N/A | 2023 | 1.17.x | v1.37–v1.41 | Deprecated |
| **1.16.x** | N/A | 2023 | 1.16.x | v1.35–v1.37 | Deprecated |

### Important: Solana CLI v4.x (Agave v4.1.0)
As of Agave v4.0.0+, Anza **no longer publishes the `agave-validator` binary**. Operators must build from source. The CLI tools (for program development) remain available via `agave-install` or the install script.

```bash
# Install latest Solana CLI (Agave v4)
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"
NO_DNA=1 solana --version  # should show 4.1.0+
```

## Platform Tools → Rust Toolchain Mapping

| Platform Tools | Bundled Rust | Bundled Cargo | LLVM/Clang | Target Triple | Notes |
|---|---|---|---|---|---|
| **v1.52** | ~1.85 (solana fork) | ~1.85 | Clang 20 | `sbpf-solana-solana` | Latest; used by Solana CLI 3.x–4.x; required for Anchor v1+ |
| **v1.51** | ~1.84 (solana fork) | ~1.84 | Clang 19 | `sbpf-solana-solana` | |
| **v1.50** | ~1.83 (solana fork) | ~1.83 | Clang 19 | `sbpf-solana-solana` | |
| **v1.49** | ~1.82 (solana fork) | ~1.82 | Clang 18 | `sbpf-solana-solana` | |
| **v1.48** | rustc 1.84.1-dev | cargo 1.84.0 | Clang 19 | `sbpf-solana-solana` | **Verified.** Used by Solana CLI 2.2.16. ⚠️ Cargo does NOT support `edition2024` |
| **v1.47** | ~1.80 (solana fork) | ~1.80 | Clang 17 | `sbpf-solana-solana` | Used by Anchor 0.31.x |
| **v1.46** | ~1.79 (solana fork) | ~1.79 | Clang 17 | `sbf-solana-solana` | |
| **v1.45** | ~1.79 (solana fork) | ~1.79 | Clang 17 | `sbf-solana-solana` | |
| **v1.44** | ~1.78 (solana fork) | ~1.78 | Clang 16 | `sbf-solana-solana` | |
| **v1.43** | ~1.75 (solana fork) | ~1.75 | Clang 16 | `sbf-solana-solana` | Used by Anchor 0.30.x/Solana 1.18.x. ❌ Incompatible with CLI 2.2.16 (`sbpf-solana-solana` target not found) |

**Note:** Platform Tools ship a **forked** Rust compiler from [anza-xyz/rust](https://github.com/anza-xyz/rust). The version numbers approximate the upstream Rust equivalent. The forked compiler includes SBF/SBPF target support.

**⚠️ CRITICAL (Jan 2026):** Platform-tools v1.48 bundles `cargo 1.84.0` which does NOT support `edition = "2024"`. Multiple crates now require it. Pin to safe versions: `blake3=1.8.2`, `constant_time_eq=0.3.1`, `base64ct=1.7.3`, `indexmap=2.11.4`. **Always commit Cargo.lock files.** Platform-tools v1.52+ may resolve this with a newer cargo.

## GLIBC Requirements by OS

| OS / Distro | GLIBC Version | Compatible Anchor |
|---|---|---|
| **Ubuntu 24.04 (Noble)** | 2.39 | All (0.29–v1.1+) |
| **Ubuntu 22.04 (Jammy)** | 2.35 | 0.29–0.30.x only (build 0.31+ from source) |
| **Ubuntu 20.04 (Focal)** | 2.31 | 0.29–0.30.x only (build 0.31+ from source) |
| **Debian 12 (Bookworm)** | 2.36 | 0.29–0.30.x only ⚠️ **Tested: 0.31.1 and 0.32.1 pre-built binaries fail.** Build from source works for Anchor CLI, but `litesvm` 0.5.0 native binary also needs GLIBC 2.38+ |
| **Debian 13 (Trixie)** | 2.40 | All |
| **Fedora 39+** | ≥2.38 | All |
| **Arch Linux (rolling)** | Latest | All |
| **macOS 14+ (Sonoma)** | N/A (no GLIBC) | All |
| **macOS 12-13** | N/A | All |
| **Windows WSL2 (Ubuntu)** | Depends on distro | See Ubuntu version |

### Why GLIBC matters
Anchor 0.31+ and v1+ binaries are compiled against newer GLIBC. If your system's GLIBC is too old:
```
anchor: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.39' not found
```

**Solutions:**
1. Upgrade your OS (recommended)
2. Build Anchor from source: `NO_DNA=1 cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli`
3. Use Docker

## Anchor ↔ Solana Crate Versions

| Anchor | anchor-lang Crate | Project-level solana-* | Notes |
|---|---|---|---|
| **1.1.x** | 1.1.x | `^3` (granular crates) | Same as v1.0 with minor fixes; Kit v7 compatible |
| **1.0.x** | 1.0.x | `^3` (granular crates) | `solana-program` removed from project deps; use `solana-signer` instead of `solana-sdk` for signing; all `solana-*` must be `^3` |
| **0.32.x** | 0.32.x | `2` (still `solana-program` or granular v2) | anchor-lang internals use granular crates; `solana-program` still valid in user Cargo.toml |
| **0.31.x** | 0.31.x | 2.x | Upgraded to Solana v2 crate ecosystem |
| **0.30.x** | 0.30.x | 1.18.x | Last version using Solana v1 crates |
| **0.29.x** | 0.29.x | 1.16.x–1.17.x | |

### Solana Granular Crate Ecosystem (Anchor 0.31+)
Anchor 0.31+ uses the Solana v2+ crate structure. The monolithic `solana-program` crate is being split into smaller crates:
- `solana-pubkey` / `solana-address`
- `solana-instruction`
- `solana-account-info`
- `solana-msg`
- `solana-invoke`
- `solana-entrypoint`
- `solana-signer` (use instead of `solana-sdk` in v1+)
- etc.

Anchor 0.32+ fully replaces `solana-program` in its own internals. **Anchor v1.0+** goes further: user-facing `Cargo.toml` files must also drop `solana-program` and bump any remaining `solana-*` crates to `^3`. The `anchor build` command warns on mismatched versions.

## Anchor CLI ↔ anchor-lang Crate Compatibility

The Anchor CLI checks version compatibility with the `anchor-lang` crate. **Mismatched versions will produce a warning.** Always keep these in sync:

```toml
# Cargo.toml (Anchor v1.1.x)
[dependencies]
anchor-lang = "1.1.2"

# Must match CLI:
# NO_DNA=1 anchor --version → anchor-cli 1.1.2
```

## SPL Token Crate Versions

| Anchor | anchor-spl | spl-token | spl-token-2022 | spl-associated-token-account |
|---|---|---|---|---|
| **1.1.x / 1.0.x** | 1.x | Latest compatible (7.x) | Latest compatible (7.x) | Latest compatible (6.x) |
| **0.32.x** | 0.32.x | Latest compatible | Latest compatible | Latest compatible |
| **0.31.x** | 0.31.x | 6.x | 5.x | 4.x |
| **0.30.x** | 0.30.x | 4.x–6.x | 3.x–4.x | 3.x |
| **0.29.x** | 0.29.x | 4.x | 1.x–3.x | 2.x–3.x |

### Anchor v1: SPL Interface Crates
Anchor v1 prefers interface crates over the legacy `spl-token` crates:

| Legacy Crate | Interface Crate (v1) | Version |
|---|---|---|
| `spl-token` | `spl-token-interface` | 2.0 |
| `spl-token-2022` | `spl-token-2022-interface` | 2.1 |
| `spl-associated-token-account` | `spl-associated-token-account-interface` | 2.0 |

## Node.js / TypeScript Requirements

| Anchor | TS Package | Node.js | TypeScript | Notes |
|---|---|---|---|---|
| **1.1.x** | `@anchor-lang/core ^1.1.0` | ≥20 | 5.x | Kit v7 compatible; `@solana/react` decoupled from Kit |
| **1.0.x** | `@anchor-lang/core ^1.0.0` | ≥20 | 5.x | Renamed from `@coral-xyz/anchor`. IDL types at root of `@anchor-lang/core` |
| **0.32.x** | `@coral-xyz/anchor ^0.32.x` | ≥17 | 5.x | |
| **0.31.x** | `@coral-xyz/anchor ^0.31.x` | ≥17 | 5.x | |
| **0.30.x** | `@coral-xyz/anchor ^0.30.x` | ≥16 | 4.x–5.x | |
| **0.29.x** | `@coral-xyz/anchor ^0.29.x` | ≥16 | 4.x | |

### Anchor v1 TypeScript Package Rename

The npm package moved from `@coral-xyz/anchor` to `@anchor-lang/core`. Update `package.json` and all imports:

```bash
# Find all occurrences to update
NO_DNA=1 grep -r "@coral-xyz" --include="*.ts" --include="*.js" --include="package.json" .
NO_DNA=1 grep -r "dist/cjs/idl" --include="*.ts" --include="*.js" .
```

```typescript
// Before (0.32.x)
import * as anchor from "@coral-xyz/anchor";
import { Program, AnchorProvider, BN } from "@coral-xyz/anchor";
import { Idl } from "@coral-xyz/anchor/dist/cjs/idl";

// After (v1+)
import * as anchor from "@anchor-lang/core";
import { Program, AnchorProvider, BN } from "@anchor-lang/core";
import { Idl } from "@anchor-lang/core";
```

## Solana Kit (web3.js v2) Versions

| Kit Version | Node.js | Key Changes |
|---|---|---|
| **v7.0.0** | ≥20 | `@solana/react` decoupled from Kit; `@solana/transaction-introspection` is NEW package; transaction versions Legacy/v0/v1; requires Node 20+ |
| **v6.x** | ≥18 | Previous stable |
| **v5.x** | ≥18 | |

### Kit v7.0.0 Key Changes
- **`@solana/react` decoupled**: React hooks now in separate package, not bundled with Kit
- **`@solana/transaction-introspection`**: New package for transaction analysis
- **Transaction versions**: Supports Legacy, v0, and v1 transaction formats
- **Node.js 20+**: Required minimum

### Transaction Versions (Kit v7)

| Version | Description | Use Case |
|---|---|---|
| **Legacy** | Original Solana transaction format | Backward compatibility |
| **v0** | Versioned transactions with Address Lookup Tables | Alt support, compressed accounts |
| **v1** | Latest versioned transaction format | Future features |

## Testing Tools Compatibility

### LiteSVM / Bankrun / Mollusk

| Tool | Version | GLIBC Req | Node.js | Notes |
|---|---|---|---|---|
| **Mollusk** | v0.13.4 | N/A (Rust) | N/A | Rust-native testing; latest compatible with Anchor v1 |
| **LiteSVM 0.5.0+** (npm) | 0.5.x+ | ≥2.38 ⚠️ | ≥18 | Native binary fails on Debian 12 (GLIBC 2.36). Works on Ubuntu 24.04+, macOS |
| **LiteSVM 0.3.x** (npm) | 0.3.x | ≥2.31 | ≥16 | Older API, may work on older systems |
| **solana-bankrun** (npm) | — | ≥2.28 | ≥16 | Legacy — being replaced by LiteSVM |
| **anchor-litesvm** (npm) | — | Same as litesvm | ≥18 | Anchor wrapper for LiteSVM |
| **Surfpool** | latest | N/A | N/A | Default test runner in Anchor v1 `anchor test` |

### LiteSVM Rust Crate — Version Selection

Use the row that matches your workspace's resolved `solana-*` granular crate versions:

| litesvm (Rust) | solana-* era | Key markers | anchor-litesvm |
|---|---|---|---|
| **0.8.2** | `~3.0` | `solana-hash ~3.0`, `solana-vote-interface 4.0`, `solana-system-interface 2.0` | `0.3` (requires `anchor-lang ^1.0.0`, `litesvm ^0.8.2`) |
| **0.9.1** | `~3.1`–`~3.3` | `solana-hash 4.0`, `solana-vote-interface 5.0`, `solana-system-interface 3.0` | TBD |
| **>0.10.0** | `3.3+` | follow latest releases | follow litesvm/anchor-litesvm release |

**Diagnostic:** run `cargo tree -d` — duplicate `solana-*` minor versions in the tree means the selected `litesvm` version is mismatched.

## Known Working Combinations (Tested)

### 🟢 Anchor v1.1.x (Recommended for new projects)
```
Anchor CLI: 1.1.2
anchor-lang: 1.1.2
anchor-spl: 1.1.2
solana-* crates: ^3
litesvm (dev): 0.8.2
anchor-litesvm (dev): 0.3
Mollusk (dev): 0.13.4
TS: @anchor-lang/core ^1.1.0
Kit: @solana/kit ^7.0.0
Solana CLI: 4.1.0 (Agave v4.1.0)
Platform Tools: v1.52
Rust: 1.85+
Node.js: 20.x LTS+
OS: Ubuntu 24.04+ (GLIBC ≥2.39) or macOS 14+
Test runner: surfpool (default in anchor test)
```

### 🟢 Anchor v1.0.x
```
Anchor CLI: 1.0.0
anchor-lang: 1.0.0
anchor-spl: 1.0.0
solana-* crates: ^3
litesvm (dev): 0.8.2
anchor-litesvm (dev): 0.3
TS: @anchor-lang/core ^1.0.0
Solana CLI: 3.x
Platform Tools: v1.52
Rust: 1.79–1.85+
Node.js: 20.x LTS
OS: Ubuntu 24.04+ (GLIBC ≥2.39) or macOS 14+
Test runner: surfpool (default in anchor test)
```

### 🟢 Modern 0.32.x (Cutting edge pre-v1)
```
Anchor CLI: 0.32.1
Solana CLI: 2.1.7+
Rust: 1.84.0+
Platform Tools: v1.52
Node.js: 20.x LTS
OS: Ubuntu 24.04+ (GLIBC ≥2.39) or macOS 14+
```

### 🟡 Legacy Compatible (For older systems)
```
Anchor CLI: 0.30.1
Solana CLI: 1.18.26
Rust: 1.79.0
Platform Tools: v1.43
Node.js: 18.x LTS
OS: Ubuntu 20.04+ or macOS 12+
```

### Verified Test Environment (Jan 2026)
```
✅ Works: Anchor CLI 0.30.1 (built from source) + Solana CLI 2.2.16 + Rust 1.93.0 + Debian 12
❌ Fails: litesvm 0.5.0 native binary on Debian 12 (GLIBC 2.36)
❌ Fails: Anchor 0.31.1/0.32.1 pre-built binaries on Debian 12 (GLIBC 2.36)
✅ Works: cargo build-sbf (Solana 2.2.16, platform-tools v1.48) on Debian 12
✅ Works: Anchor 0.30.1 built from source with Rust 1.93.0 on Debian 12
✅ Works: solana-bankrun on Debian 12 (GLIBC 2.36)
```

## Quick Version Check Commands

```bash
# Check all tool versions
NO_DNA=1 anchor --version
NO_DNA=1 solana --version
NO_DNA=1 rustc --version
NO_DNA=1 cargo --version
NO_DNA=1 node --version
NO_DNA=1 solana config get

# Check GLIBC version
ldd --version | head -1

# Check platform-tools version
ls ~/.cache/solana/v*/platform-tools/version.md 2>/dev/null && cat ~/.cache/solana/v*/platform-tools/version.md
```
