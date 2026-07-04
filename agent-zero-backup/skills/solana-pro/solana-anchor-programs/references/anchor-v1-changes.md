# Anchor v1.x Migration Guide

Complete guide to migrating from Anchor v0.31.x to v1.x (v1.1.2 target).

## Overview

Anchor v1.0 was a major release with breaking changes. This guide covers what changed, why, and how to migrate.

## Breaking Changes Summary

| Area | v0.31.x | v1.x | Migration Effort |
|------|---------|------|-----------------|
| Dependencies | `anchor-lang = "0.31"` | `anchor-lang = "^1"`, `solana-* = "^3"` | Cargo.toml update |
| CPI Context | `CpiContext::new(account_info, ...)` | `CpiContext::new(pubkey, ...)` | Remove program account from struct |
| TypeScript | `@coral-xyz/anchor` | `@anchor-lang/core` | Package rename |
| IDL | Program-embedded | Off-program (mandatory) | Migration script required |
| Account init | `set_inner()` | Manual field assignment | Replace calls |
| Solana crates | `solana-program = "2"` | `solana-program = "^3"` | Version bump |

## 1. Dependency Updates

### Cargo.toml Changes

```toml
# Before (v0.31.x)
[dependencies]
anchor-lang = "0.31.0"
anchor-spl = "0.31.0"
solana-program = "2"

# After (v1.x)
[dependencies]
anchor-lang = "^1"
anchor-spl = "^1"
solana-program = "^3"
```

### Version Alignment

All `solana-*` crates must be aligned to v3:
```toml
solana-program = "^3"
solana-sdk = "^3"
solana-account-decoder = "^3"
```

## 2. CpiContext Changes

### The Change

`CpiContext::new` now takes a `Pubkey` (program ID) instead of an `AccountInfo`.

### Before (v0.31.x)

```rust
#[derive(Accounts)]
pub struct Make<'info> {
    // Program account was in the accounts struct
    pub token_program: Program<'info, Token>,
}

// CPI used the AccountInfo
let cpi_ctx = CpiContext::new(
    ctx.accounts.token_program.to_account_info(),  // AccountInfo
    cpi_accounts,
);
```

### After (v1.x)

```rust
#[derive(Accounts)]
pub struct Make<'info> {
    // Program account may be removed from struct if not needed for validation
    // OR kept as Program<'info, T> for validation but use .key() for CPI
}

// CPI uses the Pubkey (program ID)
let cpi_ctx = CpiContext::new(
    ctx.accounts.token_program.key(),  // Pubkey
    cpi_accounts,
);
```

### Migration Steps

1. Find all `CpiContext::new` calls
2. Replace `.to_account_info()` with `.key()` for the program argument
3. Remove the program account from the accounts struct if it's only used for CPI
4. Keep `Program<'info, T>` if you need Anchor's program validation

### PDA-Signed CPI (Unchanged Pattern)

```rust
// Still uses the same pattern, but with Pubkey for program
let cpi_ctx = CpiContext::new_with_signer(
    ctx.accounts.token_program.key(),  // Pubkey instead of AccountInfo
    cpi_accounts,
    signer,
);
```

## 3. Account Initialization

### set_inner() Removed

In v0.31.x, you could use `set_inner()` to initialize account data:

```rust
// v0.31.x (deprecated in v1.x)
ctx.accounts.escrow.set_inner(Escrow {
    seed,
    maker: ctx.accounts.maker.key(),
    mint_a: ctx.accounts.mint_a.key(),
    // ...
});
```

In v1.x, manually assign each field:

```rust
// v1.x
let escrow = &mut ctx.accounts.escrow;
escrow.seed = seed;
escrow.maker = ctx.accounts.maker.key();
escrow.mint_a = ctx.accounts.mint_a.key();
escrow.mint_b = ctx.accounts.mint_b.key();
escrow.receive = receive;
escrow.bump = ctx.bumps.escrow;
```

### Migration Steps

1. Search for `set_inner` in codebase
2. Replace each call with manual field assignment
3. Use `ctx.bumps.<field>` for bump seeds

## 4. IDL Off-Program Migration

### The Change

In v0.31.x, the IDL was embedded in the program binary. In v1.x, IDL management is moved off-program.

### Why

- Reduces program binary size
- Allows IDL updates without redeploying
- Cleaner separation of interface and implementation

### Migration Actions (Mandatory)

1. Run the Anchor IDL migration script
2. Store IDL externally (file system, registry, or on-chain account)
3. Update client code to load IDL from new location

### Anchor.toml Changes

```toml
# v1.x — IDL configuration
[IDL]
# IDL is no longer embedded in program
# Configure external IDL storage
```

### Client-Side IDL Loading

```typescript
// v0.31.x — IDL from program
const idl = await Program.fetchIdl(programId, provider);

// v1.x — IDL from external source
const idl = JSON.parse(fs.readFileSync('./idl/your_program.json', 'utf-8'));
const program = new Program(idl, provider);
```

## 5. TypeScript Package Changes

### Package Rename

```json
// Before (v0.31.x)
{
  "dependencies": {
    "@coral-xyz/anchor": "^0.31.0"
  }
}

// After (v1.x)
{
  "dependencies": {
    "@anchor-lang/core": "^1.0.0"
  }
}
```

### Import Changes

```typescript
// Before
import { Program, Provider, web3 } from "@coral-xyz/anchor";

// After
import { Program, Provider, web3 } from "@anchor-lang/core";
```

## 6. Codama Client Generation

### Preferred Workflow for v1.x

```bash
# 1. Build produces Anchor IDL
NO_DNA=1 anchor build

# 2. Convert to Codama
npx @codama/nodes-from-anchor idl/your_program.json

# 3. Render Kit-native TypeScript client
npx @codama/renderers codama/your_program.json
```

### Repository Structure

```
programs/<name>/        # Program source
idl/<name>.json         # Anchor IDL (generated)
codama/<name>.json      # Codama IDL (converted)
clients/ts/<name>/      # Generated TS client
```

## 7. Build Compatibility

### Anchor v0.32.0 Fixes (Still Apply)

If you encounter build conflicts:

```bash
cargo update base64ct --precise 1.6.0
cargo update constant_time_eq --precise 0.4.1
cargo update blake3 --precise 1.5.5
```

### solana-program Conflicts

If you see `solana-program` version conflicts, add to `[dependencies]`:
```toml
solana-program = "^3"
```

## 8. Migration Checklist

### Cargo.toml
- [ ] `anchor-lang` bumped to `^1`
- [ ] `anchor-spl` bumped to `^1`
- [ ] All `solana-*` crates bumped to `^3`
- [ ] No version conflicts in `Cargo.lock`

### Source Code
- [ ] All `CpiContext::new` calls use `.key()` not `.to_account_info()`
- [ ] All `set_inner()` calls replaced with manual field assignment
- [ ] No deprecated API usage

### IDL
- [ ] IDL migration script run
- [ ] IDL stored externally
- [ ] Client code loads IDL from new location

### TypeScript
- [ ] `@coral-xyz/anchor` replaced with `@anchor-lang/core`
- [ ] All imports updated
- [ ] Package.json updated

### Build & Test
- [ ] `NO_DNA=1 anchor build` succeeds
- [ ] `NO_DNA=1 anchor test` passes
- [ ] Program deploys to devnet
- [ ] Deployment verified on Explorer

## 9. Version Reference

| Component | v0.31.x | v1.x (Current) |
|-----------|---------|---------------|
| anchor-lang | 0.31.0 | 1.1.2 |
| anchor-spl | 0.31.0 | 1.1.2 |
| solana-program | 2.x | 3.x |
| @coral-xyz/anchor | 0.31.0 | (deprecated) |
| @anchor-lang/core | N/A | 1.x |
| Solana CLI | 2.x | 3.x+ |
| Agave | v2.x | v4.1.0 |

## 10. Alpenglow Consensus Context

Solana's Alpenglow consensus (Votor component, shipping in Agave v4.3) introduces changes to block production:

- Faster finality (sub-second)
- Modified leader schedule
- Potential impact on transaction confirmation patterns

**For program developers**: No code changes required, but be aware that:
- Transaction confirmation may be faster
- Block height references may behave differently
- Test on devnet with latest Agave version

## Cross-Reference

- For error debugging, load `solana-errors-and-compat` skill
- For testing migration, load `solana-testing` skill
- For security review post-migration, load `solana-security` skill
