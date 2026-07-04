---
title: Anchor v0.32 → v1 Migration Guide (Enhanced)
description: Step-by-step checklist for upgrading an Anchor program workspace from v0.32.x to v1.1.x. Covers dependency bumps, CPI context changes, duplicate mutable account errors, legacy IDL account closure, declare_program! renames, interface-instructions removal, CLI commands, borsh 1.x, SDK 3.x, v1.0→v1.1 notes, and Kit v7 changes.
---

# Anchor v0.32 → v1 Migration (Enhanced)

Full upgrade checklist for an Anchor workspace from v0.32.x to v1.1.x. Triage which items apply, then work through them in order.

> **Protocol**: All CLI commands use `NO_DNA=1` prefix. All work targets devnet unless stated otherwise. Verify on https://explorer.solana.com.

Items marked **[COMPILE]** will prevent the program from building if not addressed. Items marked **[TS]** affect TypeScript clients. Items marked **[CLI]** affect developer workflow. Items marked **[DEPLOY]** must happen in the right order relative to deployment. Items marked **[CLIENT]** affect the Rust `anchor-client` crate.

---

## Applying the Migration (order matters)

IDL housekeeping and the program code upgrade are **independent tracks** that can be done in parallel, but have one hard constraint: legacy IDL accounts must be closed with the **v0.32 CLI before deploying v1**.

### Before deploying v1 (old program still live)

A1. **Re-publish IDL to the new v1 location** *(v1 CLI)* — `NO_DNA=1 anchor idl init` / `NO_DNA=1 anchor idl upgrade`, or use `program-metadata` CLI directly (see §5).
A2. **Update and publish clients** — update any clients that fetch the on-chain IDL to read from the new v1 location, then deploy them.
A3. **Close legacy IDL accounts** *(v0.32 CLI)* on every cluster (see §5). Deploying the v1 binary or upgrading the CLI first makes this impossible.
> **Client notice:** for minimal downtime, follow this order — new IDL first, then clients, then close legacy accounts.

### Program code upgrade (requires v1 CLI)

0. **Update toolchain** — bring Anchor CLI, AVM, and Solana CLI to the required versions first (see §0).
1. **Audit** — run `cargo check` with bumped deps and collect all errors before fixing anything.
2. **Fix compile errors in order** — deps → CPI context → duplicate accounts → `declare_program!` renames → multiple `#[error_code]` blocks → `Context` lifetime annotations.
3. **`anchor build`** — confirms Rust is clean: `NO_DNA=1 anchor build`
4. **Update TS** — rename package imports, rerun `yarn install` / `npm install`.
5. **Run tests** — `NO_DNA=1 anchor test` (surfpool) or `NO_DNA=1 anchor test -- --features some-feature`.
6. **Deploy** — `NO_DNA=1 anchor deploy`.

---

## 0. Check and update toolchain [CLI]

Verify your current versions before touching any code:

```bash
NO_DNA=1 anchor --version   # target: 1.1.2
NO_DNA=1 avm --version
NO_DNA=1 solana --version   # recommended: 4.1.0 (Agave v4.1.0)
NO_DNA=1 rustc --version    # must support edition 2021; 1.85+ recommended for v1+
```

**Update AVM and Anchor CLI:**

If your current `avm` supports `self-update`:
```bash
NO_DNA=1 avm self-update
NO_DNA=1 avm install 1.1.2
NO_DNA=1 avm use 1.1.2
```

Otherwise bootstrap via `cargo`:
```bash
NO_DNA=1 cargo install avm --git https://github.com/solana-foundation/anchor --tag v1.1.2 --locked
NO_DNA=1 avm install 1.1.2
NO_DNA=1 avm use 1.1.2
```

**Without AVM** — install `anchor-cli` directly:
```bash
NO_DNA=1 cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli --locked
```

**Update Solana CLI** (if below 4.x):
```bash
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"
NO_DNA=1 solana --version   # confirm 4.1.0+
```

---

## 1. Update dependencies [COMPILE]

**`Cargo.toml` (workspace root and program crate):**

```toml
# Before
anchor-lang = "0.32.1"
anchor-spl  = "0.32.1"
solana-program = "2"

# After
anchor-lang = "1.1.2"
anchor-spl  = "1.1.2"
solana-program = "^3"   # and any other solana-* crate that appears directly
```

- All `solana-*` crates that appear in `[dependencies]` must be `^3` or higher.

**Add `resolver = "2"` to the workspace root `Cargo.toml`:**

```toml
[workspace]
members = ["programs/*"]
resolver = "2"          # required for edition 2021 members
```

- The `cargo update` workarounds for 0.32 (`base64ct --precise 1.6.0`, `constant_time_eq --precise 0.4.1`, `blake3 --precise 1.5.5`) are no longer needed — remove them.
- If you transitively depended on `solana-sdk` for signing, use `solana-signer` directly.

See [compatibility-matrix.md](../compatibility-matrix.md) for the full Anchor v1 ↔ Solana CLI version table.

**Dev dependencies — `litesvm` / `anchor-litesvm`:**

When you bump `solana-*` crates to `^3`, also bump `litesvm` in `[dev-dependencies]`:

| litesvm | Solana granular crates era | Key markers |
|---------|---------------------------|-------------|
| `0.8.2` | `~3.0` | `solana-hash ~3.0`, `solana-vote-interface 4.0`, `solana-system-interface 2.0` |
| `0.9.1` | `~3.1`–`~3.3` | `solana-hash 4.0`, `solana-vote-interface 5.0`, `solana-system-interface 3.0` |
| `>0.10.0` | `3.3+` | follow latest releases |

```toml
# [dev-dependencies] — pick the row that matches your solana-* versions
litesvm = "0.8.2"   # solana-* ~3.0
anchor-litesvm = "0.3"   # requires anchor-lang ^1.0.0 and litesvm ^0.8.2
```

> **Tip:** run `cargo tree -d` after bumping — duplicate `solana-*` in the tree means wrong `litesvm` version.

**`package.json` [TS] — full package rename table:**

| Before (`@coral-xyz/…`) | After (`@anchor-lang/…`) |
|-------------------------|--------------------------|
| `@coral-xyz/anchor` | `@anchor-lang/core` |
| `@coral-xyz/spl-token` | `@anchor-lang/spl-token` |
| `@coral-xyz/anchor-errors` | `@anchor-lang/errors` |
| `@coral-xyz/borsh` | `@anchor-lang/borsh` |
| `@coral-xyz/anchor-cli` | `@anchor-lang/cli` |

```json
// Before
{
  "@coral-xyz/anchor": "^0.32.1",
  "@coral-xyz/spl-token": "^0.32.1"
}

// After
{
  "@anchor-lang/core": "^1.1.0",
  "@anchor-lang/spl-token": "^1.1.0"
}
```

```typescript
// Before
import * as anchor from "@coral-xyz/anchor";
import { Program, AnchorProvider, BN } from "@coral-xyz/anchor";
import { Idl } from "@coral-xyz/anchor/dist/cjs/idl";  // deep import

// After
import * as anchor from "@anchor-lang/core";
import { Program, AnchorProvider, BN } from "@anchor-lang/core";
import { Idl } from "@anchor-lang/core";  // IDL types live at root now
```

Find all occurrences:
```bash
NO_DNA=1 grep -r "@coral-xyz" --include="*.ts" --include="*.js" --include="package.json" .
NO_DNA=1 grep -r "dist/cjs/idl" --include="*.ts" --include="*.js" .
```

---

## 2. Fix CPI context construction [COMPILE]

`CpiContext::new` and `CpiContext::new_with_signer` no longer accept a program `AccountInfo` as the first argument. Pass the program's **`Pubkey`** (program ID) directly instead. Remove the program account from the accounts struct.

```rust
// Before (v0.32)
#[derive(Accounts)]
pub struct TransferTokens<'info> {
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    #[account(mut)]
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,  // <-- needed to pass AccountInfo
}

pub fn transfer_tokens(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
    let cpi_accounts = Transfer {
        from: ctx.accounts.from.to_account_info(),
        to: ctx.accounts.to.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };
    let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    token::transfer(cpi_ctx, amount)
}

// After (v1) — program ID as first argument; program field removed from struct
#[derive(Accounts)]
pub struct TransferTokens<'info> {
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    #[account(mut)]
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    // token_program no longer needed for CPI
}

pub fn transfer_tokens(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
    let cpi_accounts = Transfer {
        from: ctx.accounts.from.to_account_info(),
        to: ctx.accounts.to.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };
    let cpi_ctx = CpiContext::new(Token::id(), cpi_accounts);
    token::transfer(cpi_ctx, amount)
}

// PDA-signed CPI
// Before
let cpi_ctx = CpiContext::new_with_signer(ctx.accounts.token_program.to_account_info(), cpi_accounts, signer_seeds);
// After
let cpi_ctx = CpiContext::new_with_signer(Token::id(), cpi_accounts, signer_seeds);
```

Well-known IDs: `Token::id()`, `System::id()`, `system_program::ID`. For external programs declared with `declare_program!`, use `my_program::ID`.

---

## 3. Resolve duplicate mutable account errors [COMPILE]

Anchor now rejects instructions where the same account appears more than once as mutable.

```
error: duplicate mutable account `vault` — use `dup` constraint if intentional
```

**Option A — prevent aliasing with a constraint (accidental duplication):**
```rust
#[account(
    mut,
    constraint = token_b.key() != token_a.key() @ MyError::SameAccount
)]
pub token_b: Account<'info, TokenAccount>,
```

**Option B — allow intentional duplication:**
```rust
#[account(mut, dup)]
pub destination: Account<'info, TokenAccount>,
```

Checked types: `Account`, `LazyAccount`, `InterfaceAccount`, `Migration`. Read-only types and `UncheckedAccount` are not checked. Accounts under `init_if_needed` are now included in the check.

---

## 4. Update `declare_program!` usages [COMPILE]

**Rename `utils` module to `parsers`:**
```rust
// Before
use my_external_program::utils::*;
// After
use my_external_program::parsers::*;
```

```bash
NO_DNA=1 grep -r "::utils::" --include="*.rs" .
```

**Remove `interface-instructions` feature and `#[interface]` attribute:**

Use `#[instruction(discriminator = <const>)]` instead.

```toml
# Before (Cargo.toml)
anchor-lang = { version = "0.32.1", features = ["interface-instructions"] }
# After — feature removed entirely
anchor-lang = "1.1.2"
```

```rust
// Before
#[interface(spl_transfer_hook_interface::execute)]
pub fn transfer_hook(ctx: Context<TransferHook>, amount: u64) -> Result<()> { Ok(()) }

// After
#[instruction(discriminator = spl_transfer_hook_interface::instruction::ExecuteInstruction::SPL_DISCRIMINATOR)]
pub fn transfer_hook(ctx: Context<TransferHook>, amount: u64) -> Result<()> { Ok(()) }
```

---

## 5. Close legacy IDL accounts and re-publish [DEPLOY]

> **⚠️ Do this just before deploying the v1 binary.** Once a v1 binary is live, the legacy IDL instructions are gone.

**Step 1 — close the legacy IDL account on every cluster (with Anchor CLI v0.32):**

```bash
# with anchor-cli 0.32.x still installed
NO_DNA=1 anchor idl close --provider.cluster devnet <PROGRAM_ID>
NO_DNA=1 anchor idl close --provider.cluster mainnet-beta <PROGRAM_ID>
```

**Step 2** — deploy the v1 binary: `NO_DNA=1 anchor deploy`.

**Step 3 — re-publish the IDL via Program Metadata.**

**Option A: Anchor CLI:**
```bash
NO_DNA=1 anchor idl init --filepath target/idl/my_program.json      # first publish
NO_DNA=1 anchor idl upgrade --filepath target/idl/my_program.json   # subsequent updates
```

**Option B: `program-metadata` CLI:**
```bash
npm install -g @solana-program/program-metadata
program-metadata upload idl target/idl/my_program.json --program-id <PROGRAM_ID>
```

---

## 6. Update `AccountInfo` usage [WARNING]

Using raw `AccountInfo<'info>` in `#[derive(Accounts)]` now emits a compile-time warning.

| Old | New |
|-----|-----|
| `AccountInfo<'info>` (unknown data) | `UncheckedAccount<'info>` + `/// CHECK:` comment |
| `AccountInfo<'info>` (token account) | `InterfaceAccount<'info, TokenAccount>` |
| `AccountInfo<'info>` (executable program) | `Program<'info, MyProgram>` or `Interface<'info, T>` |

### `UncheckedAccount::clone()` vs `.to_account_info()`

In anchor v1, `.clone()` on `UncheckedAccount<'info>` returns `UncheckedAccount<'info>`, not `AccountInfo<'info>`.

```rust
// Error: mismatched types
let ctx_accounts = MyCpiAccounts {
    some_account: ctx.accounts.some_unchecked.clone(),
    ..
};

// Fix: use .to_account_info() explicitly
let ctx_accounts = MyCpiAccounts {
    some_account: ctx.accounts.some_unchecked.to_account_info(),
    ..
};
```

---

## 7. Suppress `unexpected_cfgs` warnings from macros [WARNING]

**Option A — declare them as features in each program's `[features]`:**

```toml
[features]
anchor-debug = []
custom-heap = []
custom-panic = []
```

**Option B — suppress workspace-wide via lints:**

```toml
[workspace.lints.rust]
unexpected_cfgs = { level = "allow" }
```

```toml
# programs/my_program/Cargo.toml
[lints]
workspace = true
```

> Do not use the `check-cfg` list form — cfg names with hyphens are rejected.

---

## 8. Handle IDL external account exclusion [IDL]

External account types are no longer inlined in the generated IDL.

```typescript
// Before — type came from your program's IDL
const mintAccount = await program.account.mint.fetch(mintAddress);

// After — use the token program's own client
import { getMint } from "@solana/spl-token";
const mintAccount = await getMint(connection, mintAddress);
```

---

## 9. Switch the test runner [CLI]

`anchor test` and `anchor localnet` now use **surfpool** by default.

```toml
# Anchor.toml — opt out to standard validator
[tooling]
validator = "solana"

# Or configure surfpool
[surfpool]
startup_wait = 5000
log_level = "info"
block_production_mode = "clock"
datasource_rpc_url = "https://api.mainnet-beta.solana.com"
```

Add to `.gitignore`:
```
.surfpool/
```

CI — surfpool must be installed explicitly:
```yaml
- name: Install surfpool
  run: curl -sL https://run.surfpool.run/ | bash
```

---

## 10. Remove external `solana` CLI dependency [CLI]

Anchor no longer shells out to `solana`. Update CI pipelines and scripts.

| Before | After |
|--------|-------|
| `NO_DNA=1 solana address` | `NO_DNA=1 anchor address` |
| `NO_DNA=1 solana balance` | `NO_DNA=1 anchor balance` |
| `NO_DNA=1 solana airdrop` | `NO_DNA=1 anchor airdrop` |
| `NO_DNA=1 solana program deploy` | `NO_DNA=1 anchor deploy` |
| `NO_DNA=1 solana logs` | `NO_DNA=1 anchor logs` |

---

## 11. Clean up `Anchor.toml` and removed CLI commands [CLI]

**Remove `[registry]` from `Anchor.toml`:**
```toml
# Before — remove this entire section
[registry]
url = "https://anchor.projectserum.com"
```

**Remove `arch` build options** (`arch = "sbf"` etc. are no longer recognised).

**`anchor login` is removed.** Remove it from CI scripts and `Makefile` targets.

---

## 12. Disallow multiple `#[error_code]` blocks [COMPILE]

Having more than one `#[error_code]` block is now a compile-time error. Merge all error enums into one.

```rust
// Before — two separate blocks compiled fine
#[error_code]
pub enum InitError { AlreadyInitialized }

#[error_code]
pub enum UpdateError { InvalidAmount }

// After — single merged enum
#[error_code]
pub enum MyProgramError {
    AlreadyInitialized,
    InvalidAmount,
}
```

```bash
NO_DNA=1 grep -r "#\[error_code\]" --include="*.rs" .
```

---

## 13. Update `Context` lifetime annotations [COMPILE]

`Context` was simplified from four lifetime parameters (`'a, 'b, 'c, 'info`) to one (`'info`).

```rust
// Before (v0.32)
pub fn my_handler<'a, 'b, 'c, 'info>(
    ctx: Context<'a, 'b, 'c, 'info, MyAccounts<'info>>,
) -> Result<()> { ... }

// After (v1)
pub fn my_handler<'info>(ctx: Context<'info, MyAccounts<'info>>) -> Result<()> { ... }
// or simply
pub fn my_handler(ctx: Context<MyAccounts<'_>>) -> Result<()> { ... }
```

---

## 14. Update Borsh 1.x serialization usage [COMPILE]

### `try_to_vec()` removed

Replace every call with `borsh::to_vec(&value)?`.

```rust
// Before
let data = my_struct.try_to_vec()?;
// After
let data = borsh::to_vec(&my_struct)?;
```

```bash
NO_DNA=1 grep -rn "try_to_vec" --include="*.rs" .
```

### Enum explicit discriminants conflict with anchor derive macros

If explicit discriminants match default ordinal values (0, 1, 2, …), remove them:

```rust
// Before — conflicts with anchor derive macros
#[derive(AnchorSerialize, AnchorDeserialize)]
pub enum MyType {
    Variant1 = 0,
    Variant2 = 1,
}

// After — remove explicit discriminants
#[derive(AnchorSerialize, AnchorDeserialize)]
pub enum MyType {
    Variant1,
    Variant2,
}
```

If discriminant values don't match ordinal order, implement borsh serialization manually.

---

## 15. Update Solana SDK 3.x API changes [COMPILE]

### `anchor_lang::solana_program` re-export gaps

| Module | Old import | New import |
|--------|-----------|------------|
| `keccak` | `anchor_lang::solana_program::keccak` | `solana_program::keccak` |
| `hash` | `anchor_lang::solana_program::hash` | `solana_program::hash` |
| `ed25519_program` | `anchor_lang::solana_program::ed25519_program` | `solana_program::ed25519_program` |
| `sysvar::instructions` | `anchor_lang::solana_program::sysvar::instructions` | `solana_program::sysvar::instructions` |
| `instruction::Instruction` | `anchor_lang::solana_program::instruction::Instruction` | `solana_program::instruction::Instruction` |
| `program::invoke_signed` | `anchor_lang::solana_program::program::invoke_signed` | `solana_program::program::invoke_signed` |

**Fix:** Add `solana-program = { workspace = true }` to the program's `Cargo.toml` and import directly.

```bash
NO_DNA=1 grep -rn "anchor_lang::solana_program" --include="*.rs" programs/
```

### `AccountInfo::realloc` renamed to `resize`

```rust
// Before
account_info.realloc(new_len, false)?;
// After
account_info.resize(new_len)?;
```

```bash
NO_DNA=1 grep -rn "\.realloc(" --include="*.rs" .
```

### `MAX_PERMITTED_DATA_INCREASE` path change

```rust
// Before
use solana_program::entrypoint::MAX_PERMITTED_DATA_INCREASE;
// After
use solana_program::account_info::MAX_PERMITTED_DATA_INCREASE;
```

---

## 16. Audit external program CPI crates [COMPILE]

Any external CPI crate compiled against **anchor 0.31** will produce trait-bound errors.

**Symptoms:**
```
error[E0277]: the trait bound `Noop: anchor_lang::Id` is not satisfied
```

**Step 1 — identify affected crates:**
```bash
cargo tree 2>&1 | grep -E "anchor-lang|anchor-spl" | sort -u
```

**Step 2 — check for an updated release:**
```bash
cargo search <crate-name>
```

**Step 3 — update the crate yourself** (if you own the repo)

**Step 4 (last resort) — vendor the crate locally** using `declare_program!` against the program's IDL JSON.

---

## 17. Migrate `spl-token` / `spl-token-2022` / `spl-associated-token-account` direct dependencies [COMPILE]

`spl-token 7.x`, `spl-token-2022 7.x`, and `spl-associated-token-account 6.x` depend on `solana-program 2.x`.

### Preferred fix — migrate to the interface crates

| Legacy Crate | Interface Crate (v1) | Version |
|---|---|---|
| `spl-token` | `spl-token-interface` | 2.0 |
| `spl-token-2022` | `spl-token-2022-interface` | 2.1 |
| `spl-associated-token-account` | `spl-associated-token-account-interface` | 2.0 |

```toml
# Cargo.toml
spl-token-interface = "2.0"   # replaces spl-token = "7.x"
```

### Fallback — use `anchor_spl` re-exports

```rust
use anchor_spl::token::ID as TOKEN_PROGRAM_ID;
use anchor_spl::token_2022::ID as TOKEN_2022_PROGRAM_ID;
use anchor_spl::associated_token::ID as ATA_PROGRAM_ID;
```

```bash
NO_DNA=1 grep -rn "spl_token::\|spl_token_2022::\|spl_associated_token_account::" --include="*.rs" programs/
```

---

## v1.0 → v1.1 Migration Notes (NEW)

Anchor v1.1.x is a minor release over v1.0.x with compatibility fixes:

### Dependency Updates
```toml
# Bump from v1.0 to v1.1
anchor-lang = "1.1.2"
anchor-spl = "1.1.2"
```

```json
// package.json
"@anchor-lang/core": "^1.1.0"
```

### Verification
```bash
NO_DNA=1 anchor --version  # should show 1.1.2
NO_DNA=1 anchor build       # verify compilation
NO_DNA=1 anchor test        # verify tests pass
```

### Key Changes in v1.1
- Minor bug fixes and compatibility improvements over v1.0
- Ensure `solana-*` crates are compatible with v1.1.x
- Kit v7.0.0 compatibility improvements
- No breaking changes from v1.0 — drop-in upgrade

---

## Kit v7.0.0 Changes (NEW)

When upgrading to Anchor v1.1.x with Solana Kit v7.0.0:

### Node.js Requirement
- Kit v7.0.0 requires **Node.js 20+**
- Verify: `node --version`

### `@solana/react` Decoupled
- React hooks are now in a separate `@solana/react` package
- No longer bundled with `@solana/kit`
- Install separately if using React:
  ```bash
  npm install @solana/react
  ```

### `@solana/transaction-introspection` (NEW Package)
- New package for transaction analysis and introspection
- Install if needed:
  ```bash
  npm install @solana/transaction-introspection
  ```

### Transaction Versions (Legacy, v0, v1)
- Kit v7 supports three transaction versions: Legacy, v0, and v1
- Use appropriate version handling:
  ```typescript
  import { assertIsTransactionWithBlockhashLifetime } from '@solana/transactions';
  ```

### Package.json Updates
```json
{
  "@solana/kit": "^7.0.0",
  "@solana/react": "^7.0.0",
  "@solana/transaction-introspection": "^7.0.0"
}
```

> See `references/kit/gotchas.md` for full Kit v7.0.0 gotchas and type errors.

---

## What's New in v1

Worth adopting during migration:

- **`Migration<'info, From, To>`** — safe account schema migrations between layouts.
- **`LazyAccount`** — heap-allocated read-only access, auto-optimized for unit-variant enums and empty arrays.
- **Relaxed seeds syntax** — PDA seeds accept richer Rust expressions beyond literals and `.as_ref()`.
- **`FnMut` event closures** — event listeners now accept `FnMut`, allowing mutable captures.
- **Generic `Program<'info>`** — usable without a type parameter for executable-only validation.
- **`declare_program!` without `anchor_lang`** — `anchor_client` alone is sufficient for client-side usage.
- **Owner re-checked on `.reload()`** — `account.reload()` now re-validates the account owner.
- **`common::close` accepts references** — no need to call `.to_account_info()` at every call site.
- **`Owners` in prelude** — `anchor_lang::prelude::Owners` is re-exported.
- **Borsh 1.5.7** — both Rust and TypeScript Borsh implementations upgraded.
- **Lifecycle hooks** — add a `[hooks]` section to `Anchor.toml` to run shell commands at `pre_build`, `post_build`, `pre_test`, `post_test`, `pre_deploy`, `post_deploy`.
