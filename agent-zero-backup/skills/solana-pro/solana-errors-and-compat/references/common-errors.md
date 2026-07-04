---
title: Common Errors & Solutions
description: Diagnose and fix common errors in Solana development — GLIBC, Anchor version conflicts, build failures, deployment errors, transaction simulation errors, account constraint errors, Kit v7 gotchas, and toolchain compatibility.
---

# Common Solana Development Errors & Solutions

> **Protocol**: All CLI commands use `NO_DNA=1` prefix. Verify deployments on https://explorer.solana.com. All work targets devnet unless stated otherwise.

## GLIBC Errors

### `GLIBC_2.39 not found` / `GLIBC_2.38 not found`
```
anchor: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.39' not found (required by anchor)
```

**Cause:** Anchor 0.31+ binaries require GLIBC ≥2.38. Anchor 0.32+ and v1+ require ≥2.39.

**Solutions:**
1. **Upgrade OS** (best): Ubuntu 24.04+ has GLIBC 2.39
2. **Build from source:**
   ```bash
   NO_DNA=1 cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli
   # For 0.31.x:
   NO_DNA=1 cargo install --git https://github.com/solana-foundation/anchor --tag v0.31.1 anchor-cli
   ```
3. **Use Docker:**
   ```bash
   docker run -v $(pwd):/workspace -w /workspace solanafoundation/anchor:0.31.1 anchor build
   ```
4. **Use AVM with source build:**
   ```bash
   NO_DNA=1 avm install 1.1.2 --from-source
   ```

---

## Rust / Cargo Errors

### `anchor-cli` fails to install with Rust 1.80 (`time` crate issue)
```
error[E0635]: unknown feature `proc_macro_span_shrink`
```

**Cause:** Anchor 0.30.x uses a `time` crate version incompatible with Rust ≥1.80.

**Solutions:**
1. **Use AVM** — auto-selects `rustc 1.79.0` for Anchor < 0.31
2. **Pin Rust version:**
   ```bash
   rustup install 1.79.0 && rustup default 1.79.0
   NO_DNA=1 cargo install --git https://github.com/coral-xyz/anchor --tag v0.30.1 anchor-cli --locked
   ```
3. **Upgrade to Anchor 0.31+** which fixes this issue

### `unexpected_cfgs` warnings flooding build output
**Solution:** Add to `Cargo.toml`:
```toml
[lints.rust]
unexpected_cfgs = { level = "allow" }
```
Or upgrade to Anchor 0.31+ which handles this.

### `error[E0603]: module inner is private`
**Cause:** Version mismatch between `anchor-lang` crate and Anchor CLI.
**Solution:** Ensure `anchor-lang` in Cargo.toml matches your `anchor --version`.

---

## Build Errors

### `cargo build-sbf` not found
**Solutions:**
1. Install Solana CLI: `sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"`
2. Add to PATH: `export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"`
3. Verify: `NO_DNA=1 solana --version`

### `cargo build-bpf` is deprecated
**Solution:** Use `NO_DNA=1 cargo build-sbf` (Anchor 0.30+ handles this automatically).

### Platform tools download failure
**Solutions:**
1. Clear cache and retry:
   ```bash
   rm -rf ~/.cache/solana/
   NO_DNA=1 cargo build-sbf
   ```
2. Manual platform tools install from https://github.com/anza-xyz/platform-tools/releases
3. Check disk space (see "No space left" error)

### `anchor build` IDL generation fails
**Solutions:**
1. Ensure `idl-build` feature is enabled (required since 0.30.0):
   ```toml
   [features]
   default = []
   idl-build = ["anchor-lang/idl-build", "anchor-spl/idl-build"]
   ```
2. Set ANCHOR_LOG for debugging: `NO_DNA=1 ANCHOR_LOG=1 anchor build`
3. Skip IDL generation: `NO_DNA=1 anchor build --no-idl`
4. Check for nightly Rust interference: `NO_DNA=1 RUSTUP_TOOLCHAIN=stable anchor build`

### `anchor build` error with `proc_macro2` / `local_file` method not found
**Solutions:**
1. Upgrade to Anchor 0.31.1+ (fixed in [#3663](https://github.com/solana-foundation/anchor/pull/3663))
2. Use stable Rust: `NO_DNA=1 RUSTUP_TOOLCHAIN=stable anchor build`
3. Pin proc-macro2: `cargo update -p proc-macro2 --precise 1.0.86`

---

## Installation Errors

### `No space left on device` during Solana install
**Cause:** Solana CLI + platform tools can use 2-5 GB.

**Solutions:**
1. Clean old versions:
   ```bash
   ls ~/.local/share/solana/install/releases/
   rm -rf ~/.local/share/solana/install/releases/1.16.*
   rm -rf ~/.local/share/solana/install/releases/1.17.*
   rm -rf ~/.cache/solana/
   ```
2. Clean Cargo/Rust caches:
   ```bash
   cargo cache --autoclean  # if installed
   rm -rf ~/.cargo/registry/cache/
   rm -rf target/
   ```
3. Clean AVM: `ls ~/.avm/bin/` and remove unused anchor versions

### `agave-install` not found
**Cause:** Anchor CLI 0.31+ migrates to `agave-install` for Solana versions ≥1.18.19.
**Solution:**
```bash
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"
```

---

## Testing Errors

### `solana-test-validator` crashes or hangs
**Solutions:**
1. Kill existing validators:
   ```bash
   pkill -f solana-test-validator
   # or
   NO_DNA=1 solana-test-validator --kill
   ```
2. Clean ledger: `rm -rf test-ledger/`
3. Check port availability: `lsof -i :8899` and `lsof -i :8900`
4. Consider Surfpool as alternative:
   ```bash
   curl --proto '=https' --tlsv1.2 -LsSf https://github.com/txtx/surfpool/releases/latest/download/surfpool-installer.sh | sh
   ```

### Anchor test fails with `Connection refused` / IPv6 issue
```
Error: connect ECONNREFUSED ::1:8899
```
**Cause:** Node.js 17+ resolves `localhost` to IPv6 `::1`, but validator binds to `127.0.0.1`.

**Solutions:**
1. Use Anchor 0.30+ (defaults to `127.0.0.1`)
2. Set NODE_OPTIONS: `NO_DNA=1 NODE_OPTIONS="--dns-result-order=ipv4first" anchor test`
3. Edit Anchor.toml:
   ```toml
   [provider]
   cluster = "http://127.0.0.1:8899"
   ```

---

## Anchor Version Migration Issues

### Anchor 0.29 → 0.30 Migration Errors

**`.accounts()` method type errors:**
Change `.accounts({...})` to `.accountsPartial({...})` or remove auto-resolved accounts.

**Missing `idl-build` feature:**
Add to each program's Cargo.toml:
```toml
[features]
idl-build = ["anchor-lang/idl-build"]
```

**`overflow-checks` not specified:**
Add to workspace `Cargo.toml`:
```toml
[profile.release]
overflow-checks = true
```

### Anchor 0.30 → 0.31 Migration Errors

**Solana v1 → v2 crate conflicts:**
Remove direct `solana-program` and `solana-sdk` dependencies. Use through `anchor-lang`:
```rust
use anchor_lang::prelude::*;
// NOT: use solana_program::pubkey::Pubkey;
```

**`Discriminator` trait changes:**
Ensure you derive `#[account]` on structs. The discriminator is now dynamically sized.

### Anchor 0.31 → 0.32 Migration Errors

**`solana-program` dependency removed:**
```rust
// Before (0.31):
use solana_program::pubkey::Pubkey;
// After (0.32):
use solana_pubkey::Pubkey;
// Or use anchor's re-export:
use anchor_lang::prelude::*;
```

**Duplicate mutable accounts error:**
Anchor 0.32+ disallows duplicate mutable accounts by default. Use the `dup` constraint:
```rust
#[derive(Accounts)]
pub struct MyInstruction<'info> {
    #[account(mut)]
    pub account_a: Account<'info, MyAccount>,
    #[account(mut, dup = account_a)]
    pub account_b: Account<'info, MyAccount>,
}
```

### Anchor 0.32 → v1 Migration Errors

**TS package renamed:** `@coral-xyz/anchor` → `@anchor-lang/core`
```typescript
// Before
import * as anchor from "@coral-xyz/anchor";
// After
import * as anchor from "@anchor-lang/core";
```

**`CpiContext::new` takes `Pubkey` not `AccountInfo`:**
```rust
// Before (v0.32)
let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
// After (v1)
let cpi_ctx = CpiContext::new(Token::id(), cpi_accounts);
```

**All `solana-*` crates must be `^3`:**
```toml
# Before
solana-program = "2"
# After
solana-program = "^3"
```

**`try_to_vec()` removed (borsh 1.x):**
```rust
// Before
let data = my_struct.try_to_vec()?;
// After
let data = borsh::to_vec(&my_struct)?;
```

**`AccountInfo::realloc` renamed to `resize`:**
```rust
// Before
account_info.realloc(new_len, false)?;
// After
account_info.resize(new_len)?;
```

> Full migration guide: `references/anchor/migrating-v0.32-to-v1.md`

### Anchor v1.0 → v1.1 Migration Notes
- Ensure `solana-*` crates are compatible with v1.1.x (check for any breaking minor version bumps)
- Kit v7.0.0 changes: `@solana/react` decoupled, `@solana/transaction-introspection` is new package
- Update `@anchor-lang/core` to `^1.1.0` in package.json
- Run `NO_DNA=1 anchor build` to verify compatibility

---

## Program Deployment Errors (NEW)

### `Program failed to deploy: account already exists`
**Cause:** A program with the same program ID already exists on-chain.
**Solutions:**
1. Close existing program: `NO_DNA=1 solana program close <PROGRAM_ID>`
2. Use a new keypair: `NO_DNA=1 solana program deploy target/deploy/my_program.so --program-id new-keypair.json`

### `Program failed to deploy: account data size mismatch`
**Cause:** Deploying to an existing program with different data size.
**Solution:** Redeploy with `--program-id` matching the original, or close and redeploy:
```bash
NO_DNA=1 solana program close <PROGRAM_ID>
NO_DNA=1 solana program deploy target/deploy/my_program.so
```

### `Upgrade authority mismatch`
**Cause:** The wallet signing the upgrade is not the upgrade authority.
**Solution:** Verify authority and use the correct wallet:
```bash
NO_DNA=1 solana program show <PROGRAM_ID>
# Check "Upgrade Authority" field
```

### `Program data account not found`
**Cause:** The program was never deployed or was closed.
**Solution:** Deploy the program first:
```bash
NO_DNA=1 solana program deploy target/deploy/my_program.so
```

### `Insufficient funds for deployment`
**Cause:** Program deployment requires SOL for rent-exempt minimum.
**Solution:**
```bash
NO_DNA=1 solana airdrop 2
# Verify balance
NO_DNA=1 solana balance
```

---

## Transaction Simulation Errors (NEW)

### `Transaction simulation failed: Blockhash not found`
**Cause:** Blockhash expired before transaction was processed.
**Solutions:**
1. Fetch fresh blockhash before signing
2. Check RPC connectivity: `NO_DNA=1 solana config get`
3. Use ` commitment: 'confirmed'` for faster processing

### `Transaction simulation failed: Instruction error`
**Cause:** An instruction in the transaction failed during simulation.
**Solution:** Check the instruction error code and trace logs. Run with `ANCHOR_LOG=1` for detailed logs.

### `Error: custom program error: 0x1` (InsufficientFunds)
**Cause:** The account doesn't have enough SOL/lamports.
**Solution:** Fund the account: `NO_DNA=1 solana airdrop 2 <WALLET_ADDRESS>`

### `Error: custom program error: 0x0` (Generic failure)
**Cause:** Program returned a generic error (code 0).
**Solution:** Check program logic — this is often an `Err(())` return or a custom error with offset 0.

### `Transaction too large` (exceeds 1232 bytes)
**Cause:** Transaction exceeds the 1232-byte limit.
**Solutions:**
1. Use Address Lookup Tables (ALTs) to compress account references
2. Split into multiple transactions
3. Reduce instruction data size

### `Compute budget exceeded`
**Cause:** Transaction consumed more CUs than the default limit (200,000).
**Solution:** Add compute budget instruction:
```rust
use anchor_lang::solana_program::compute_budget;
// In instruction:
compute_budget::ComputeBudgetInstruction::set_compute_unit_limit(400_000)
```

---

## Account Constraint Errors (NEW)

### `Constraint has been violated: raw_constraint`
**Cause:** A constraint defined in `#[derive(Accounts)]` doesn't match runtime state.
**Solution:** Verify the constraint logic matches the account's actual state. Check:
```rust
#[account(
    mut,
    constraint = token_b.key() != token_a.key() @ MyError::SameAccount
)]
pub token_b: Account<'info, TokenAccount>,
```

### `Account not initialized`
**Cause:** Trying to read/write an account that hasn't been created via `init`.
**Solution:** Call the initialization instruction first, or use `init_if_needed`.

### `Account discriminator mismatch`
**Cause:** Account was initialized by a different program or different program version.
**Solution:** Ensure the account was created by the correct program. Check:
```bash
NO_DNA=1 solana account <ACCOUNT_ADDRESS> --output json
```
Verify the `owner` field matches your program ID.

### `Account did not deserialize`
**Cause:** Account data layout doesn't match the expected struct.
**Solutions:**
1. Check account owner matches expected program
2. Verify struct field types and order match serialization
3. Ensure account has enough data for the struct

### `Insufficient funds for rent`
**Cause:** Account doesn't have minimum rent-exempt balance.
**Solution:** Fund account with minimum rent-exempt lamports:
```bash
NO_DNA=1 solana rent <DATA_SIZE_BYTES>
# Then transfer:
NO_DNA=1 solana transfer <ACCOUNT_ADDRESS> <LAMPORTS>
```

### `Owner mismatch`
**Cause:** Account owner doesn't match the expected program.
**Solution:** Verify account owner:
```bash
NO_DNA=1 solana account <ACCOUNT_ADDRESS> --output json | jq .owner
```
If wrong, the account was created by a different program.

### `Address not in PDA range`
**Cause:** The provided address is not a valid PDA for the given seeds and program ID.
**Solution:** Verify PDA derivation:
```bash
NO_DNA=1 solana find-program-derived-address <PROGRAM_ID> <SEED_1> <SEED_2>
```
Ensure seeds match exactly what the program uses in `find_program_address`.

---

## LiteSVM Errors

### `undefined symbol: __isoc23_strtol` (litesvm native binary)
**Cause:** LiteSVM 0.5.0+ requires GLIBC 2.38+.
**Solutions:**
1. Upgrade OS to Ubuntu 24.04+ or Debian 13+
2. Use Docker: `FROM ubuntu:24.04`
3. Fall back to `solana-bankrun`:
   ```bash
   pnpm remove litesvm anchor-litesvm
   pnpm add -D solana-bankrun anchor-bankrun
   ```
4. Try litesvm 0.3.x on older GLIBC

### `Cannot find module './litesvm.linux-x64-gnu.node'`
**Cause:** pnpm hoisting issue with native optional dependencies.
**Solutions:**
1. `rm -rf node_modules && pnpm install`
2. Add `node-linker=hoisted` to `.npmrc`
3. `pnpm add -D litesvm-linux-x64-gnu`

---

## Platform Tools Errors

### `The Solana toolchain is corrupted` after fresh install
**Cause:** Platform-tools extraction failed (insufficient disk space, ~3GB needed).

**Solutions:**
1. Run with force reinstall:
   ```bash
   NO_DNA=1 cargo build-sbf --force-tools-install
   ```
2. Ensure sufficient disk space:
   ```bash
   df -h ~/.cache/solana/
   # If too small, symlink to bigger disk:
   rm -rf ~/.cache/solana/v1.52/platform-tools
   mkdir -p /mnt/data/solana-cache/v1.52/platform-tools
   ln -sf /mnt/data/solana-cache/v1.52/platform-tools ~/.cache/solana/v1.52/platform-tools
   ```
3. Manual extraction (if cycling):
   ```bash
   wget https://github.com/anza-xyz/platform-tools/releases/download/v1.52/platform-tools-linux-x86_64.tar.bz2
   mkdir -p /mnt/data/solana-platform-tools/v1.52
   cd /mnt/data/solana-platform-tools/v1.52
   tar xjf /path/to/platform-tools-linux-x86_64.tar.bz2
   ln -sf /mnt/data/solana-platform-tools/v1.52 ~/.cache/solana/v1.52/platform-tools
   ```

**Note:** The `version.md` file is the last file extracted. Its presence confirms successful extraction.

### Anchor CLI version mismatch warnings (non-fatal)
```
WARNING: `anchor-lang` version(0.32.1) and the current CLI version(0.30.1) don't match.
```
**Solutions:**
1. Match versions via AVM: `NO_DNA=1 avm install 0.32.1 && avm use 0.32.1`
2. Or downgrade crate in Cargo.toml
3. Ignore if just building — mismatch is cosmetic for `anchor build`

---

## edition2024 Crate Incompatibility (Cargo 1.84.0)

### `feature edition2024 is required` during `cargo build-sbf`
**Cause:** Platform-tools v1.48 bundles Cargo 1.84.0 which doesn't support `edition2024`.

#### Known edition2024 Crates (Updated Jan 31, 2026)

| Crate | Breaking Version | Safe Version | Pulled By |
|---|---|---|---|
| `blake3` | ≥1.8.3 | **1.8.2** | `solana-blake3-hasher` → `solana-program` |
| `constant_time_eq` | ≥0.4.2 | **0.3.1** | `blake3` |
| `base64ct` | ≥1.8.3 | **1.7.3** | `pkcs8`, `spki` → crypto crates |
| `indexmap` | ≥2.13.0 | **2.11.4** | `toml_edit` → `proc-macro-crate` → `borsh-derive` → `anchor-lang` |

**New crates may ship edition2024 at any time.** Pin to previous version if you see this error with a new crate.

#### Solutions

**1. Pin all known problematic crates (recommended for CI):**
```bash
cargo generate-lockfile
cargo update -p blake3 --precise 1.8.2
cargo update -p constant_time_eq --precise 0.3.1
cargo update -p base64ct --precise 1.7.3
cargo update -p indexmap --precise 2.11.4
```

**2. Pin via workspace Cargo.toml:**
```toml
[workspace.dependencies]
blake3 = "=1.8.2"
base64ct = "=1.7.3"
```

**3. Always commit Cargo.lock:**
```bash
git add -f Cargo.lock
```
This is the single most effective prevention.

**4. For monorepos with per-project Cargo.lock files:**
```bash
for dir in $(find . -path "*/anchor/Cargo.toml" -exec dirname {} \;); do
  cd "$dir"
  cargo generate-lockfile
  cargo update -p blake3 --precise 1.8.2 2>/dev/null
  cargo update -p constant_time_eq --precise 0.3.1 2>/dev/null
  cargo update -p base64ct --precise 1.7.3 2>/dev/null
  cargo update -p indexmap --precise 2.11.4 2>/dev/null
  cd -
done
git add -f **/Cargo.lock
```

### `Could not find specification for target "sbpf-solana-solana"` with `--tools-version`
**Cause:** Using `--tools-version v1.43` with CLI 2.2.16. Target rename happened between v1.43 and v1.48.
**Solution:** Don't downgrade platform-tools below your CLI's default version.

---

## Miscellaneous Errors

### `solana airdrop` fails
**Cause:** Rate limiting on devnet/testnet.
**Solutions:**
1. Wait and retry
2. Use web faucet: https://faucet.solana.com
3. Use localnet for unlimited airdrops

### Anchor IDL account authority mismatch
**Solution:** The IDL authority is the program's upgrade authority:
```bash
NO_DNA=1 solana program show <PROGRAM_ID>
```

### `declare_program!` not finding IDL file
**Solution:** Place IDL JSON in `idls/` directory at workspace root (filename must match program name in snake_case):
```
workspace/
├── idls/
│   └── my_program.json
├── programs/
│   └── my_program/
└── Anchor.toml
```

---

## Verified Test Results (Debian 12, Jan 2026)

Environment: Rust 1.93, Solana CLI 2.2.16, Anchor CLI 0.30.1, Node 22.22.0, GLIBC 2.36

| Test | Result | Notes |
|------|--------|-------|
| Anchor CLI/crate mismatch (0.30.1 / 0.32.1) | ⚠️ PASS with warnings | Builds succeed; version mismatch warnings only |
| cargo build-sbf (native) | ✅ PASS | All build after platform-tools v1.48 installed |
| solana-bankrun (GLIBC 2.36) | ✅ PASS | Works on GLIBC 2.36 |
| litesvm npm (GLIBC 2.36) | ❌ FAIL | `undefined symbol: __isoc23_strtol` — requires GLIBC ≥2.38 |
| @solana/web3.js CJS/ESM | ✅ PASS | Full support on Node 22 |
| @solana/kit (web3.js v2) ESM | ✅ PASS | ESM-only, works on Node 22 |
| @coral-xyz/anchor CJS/ESM | ✅ PASS | Full support on Node 22 |
| IDL generation | ✅ PASS | Valid JSON IDL with CLI 0.30.1 |
| Platform tools corruption | ❌→✅ PASS | Fixed with `--force-tools-install` on adequate disk |

### Key Findings
1. **litesvm 0.5.0+ is BROKEN on Debian 12** (GLIBC 2.36) — use `solana-bankrun`
2. **solana-bankrun works** on GLIBC 2.36 — recommended for older systems
3. **Platform-tools needs ~2GB disk** for extraction
4. **Anchor CLI 0.30.1 builds anchor-lang 0.32.1** — warnings only, no errors
5. **Node 22 has full ESM+CJS support** for all Solana JS packages
6. **Cargo duplicate dependencies are normal** in Solana monorepos
