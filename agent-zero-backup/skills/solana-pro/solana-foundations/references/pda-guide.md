# Program Derived Addresses (PDAs) — Deep Reference

## Overview

PDAs are deterministically derived addresses that have no private key. Only the owning program can sign for them. They are the primary mechanism for program-owned accounts with deterministic addresses, enabling composable account architectures without trusting off-chain key management.

## What Makes a PDA

A PDA is a public key that **falls off the ed25519 curve**. Normal public keys are points on the elliptic curve; PDAs are valid-looking addresses that are NOT on the curve — meaning no private key can sign for them.

### Derivation Process

```
PDA = findProgramAddress(seeds, programId)

Internal algorithm:
1. Start with bump seed = 255
2. Compute: hash(seeds ++ programId ++ bump_seed)
3. Check if result is on the ed25519 curve
4. If on curve: decrement bump (254, 253, ...) and retry
5. If off curve: return as PDA (with that bump value)
```

### Canonical Bump

The **canonical bump** is the highest bump seed (starting from 255, decrementing) that produces a valid PDA. Anchor's `bump` constraint automatically uses the canonical bump.

```rust
// Anchor automatically finds canonical bump
#[account(seeds = [b"counter", user.key().as_ref()], bump)]
pub counter: Account<'info, Counter>,
```

**Security note**: Always use the canonical bump. Non-canonical bumps can lead to PDA collision vulnerabilities and are flagged by security auditors.

## Seeds

Seeds are the inputs that deterministically derive a PDA. They can be any byte slices.

### Common Seed Patterns

| Pattern | Seeds | Use Case |
|---------|-------|----------|
| Constant | `[b"config"]` | Singleton config accounts |
| User-scoped | `[b"counter", user.key().as_ref()]` | Per-user state |
| Mint-scoped | `[b"vault", mint.key().as_ref()]` | Per-token vaults |
| Composite | `[b"pool", token_a.as_ref(), token_b.as_ref()]` | AMM pools |
| Hierarchical | `[b"escrow", maker.key().as_ref(), &escrow_id.to_le_bytes()]` | Multi-instance escrows |

### Seed Types

```rust
// Bytes literal
seeds = [b"counter"]

// Public key (32 bytes)
seeds = [user.key().as_ref()]

// Integer (must be little-endian bytes)
seeds = [b"item", &item_id.to_le_bytes()]

// String (convert to bytes)
seeds = [b"pool", token_a.key().as_ref(), token_b.key().as_ref()]

// Multiple seeds combined
seeds = [b"escrow", maker.key().as_ref(), &escrow_id.to_le_bytes()]
```

### Passing Seeds from Client

```typescript
// @solana/kit — derive PDA on client
import { getProgramAddressSync } from '@solana/kit';

const [counterPda] = getProgramAddressSync(
  [Buffer.from('counter'), userPublicKey.toBytes()],
  programId
);
```

## Anchor PDA Patterns

### Initialization with `init`

```rust
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        seeds = [b"counter", user.key().as_ref()],
        bump,
        payer = user,
        space = 8 + 8
    )]
    pub counter: Account<'info, Counter>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}
```

### Reading Existing PDA with `seeds` + `bump`

```rust
#[derive(Accounts)]
pub struct Increment<'info> {
    #[account(
        mut,
        seeds = [b"counter", user.key().as_ref()],
        bump = counter.bump  // Store bump in account for re-derivation
    )]
    pub counter: Account<'info, Counter>,
    #[account(mut)]
    pub user: Signer<'info>,
}
```

### Storing the Bump

Store the bump seed in the account data so you can re-derive the PDA without recomputing:

```rust
#[account]
pub struct Counter {
    pub count: u64,
    pub bump: u8,  // Store canonical bump here
}

// In initialize handler:
ctx.accounts.counter.bump = ctx.bumps.counter;
```

### Using `seeds` with Computed Values

```rust
// Dynamic seeds computed from instruction arguments
#[account(
    seeds = [
        b"pool",
        ctx.accounts.token_a.key().as_ref(),
        ctx.accounts.token_b.key().as_ref()
    ],
    bump
)]
pub pool: Account<'info, Pool>,
```

## Debugging Seed Mismatches

Seed mismatches are the #1 source of PDA errors. Symptoms:
- `Transaction failed: unknown signer` (PDA doesn't match)
- `IncorrectProgramId` errors
- Client-derived address doesn't match on-chain account

### Debug Protocol

#### Step 1: Print Seeds on Both Sides

```rust
// On-chain: print seeds
msg!("Seeds: b'counter', user: {}", ctx.accounts.user.key());
```

```typescript
// Client: print seeds
console.log('Seeds:', [
  Buffer.from('counter'),
  userPublicKey.toBytes()
]);
```

#### Step 2: Compare Byte Representations

Do NOT compare string representations. Compare raw bytes:

```typescript
// WRONG: string comparison
const seedStr = 'counter';
// This hides encoding issues

// RIGHT: byte comparison
const seedBytes = Buffer.from('counter', 'utf8');
console.log('Seed bytes:', [...seedBytes]);
```

#### Step 3: Check for Common Confusion

| Bug | Wrong | Right |
|-----|-------|-------|
| Empty vs null | `b""` (empty, 0 bytes) | `b"\0"` (1 null byte) — different! |
| String encoding | `'counter'` (16 bytes UTF-16) | `b"counter"` (7 bytes UTF-8) |
| Integer endianness | `&n.to_be_bytes()` (big-endian) | `&n.to_le_bytes()` (little-endian) |
| Public key format | `user.to_string().as_bytes()` (32-44 chars) | `user.key().as_ref()` (32 bytes) |
| Hash vs direct | `hash(user).as_ref()` | `user.key().as_ref()` |

#### Step 4: Verify Canonical Bump

```typescript
// Client: derive with canonical bump (same algorithm as on-chain)
const [pda, bump] = getProgramAddressSync(seeds, programId);
console.log('PDA:', pda.toBase58());
console.log('Bump:', bump);

// Verify against on-chain account
const accountInfo = await rpc.getAccountInfo(pda).send();
if (!accountInfo.value) {
  console.error('PDA does not exist on-chain');
}
```

#### Step 5: Use `findProgramAddressSync` for Debugging

```typescript
import { getProgramAddressSync, getAddressFromPublicKey } from '@solana/kit';

// Test different seed combinations
const seeds1 = [Buffer.from('counter'), user.toBytes()];
const seeds2 = [Buffer.from('Counter'), user.toBytes()]; // Wrong case!
const seeds3 = [user.toBytes(), Buffer.from('counter')]; // Wrong order!

const [pda1] = getProgramAddressSync(seeds1, programId);
const [pda2] = getProgramAddressSync(seeds2, programId);
const [pda3] = getProgramAddressSync(seeds3, programId);

console.log('pda1 (correct):', pda1.toBase58());
console.log('pda2 (wrong case):', pda2.toBase58());
console.log('pda3 (wrong order):', pda3.toBase58());
```

### Common Seed Mismatch Scenarios

#### Scenario 1: Case Sensitivity
```rust
// On-chain uses lowercase
seeds = [b"counter"]

// Client uses uppercase (typo)
Buffer.from('Counter')  // WRONG
```

#### Scenario 2: Wrong Endianness
```rust
// On-chain uses little-endian
seeds = [b"item", &item_id.to_le_bytes()]

// Client uses big-endian
const itemIdBytes = BigInt(itemId).toString(16).padStart(8, '0');
// WRONG: this is big-endian representation
```

#### Scenario 3: Public Key as String vs Bytes
```rust
// On-chain: 32 raw bytes
seeds = [user.key().as_ref()]

// Client: accidentally uses base58 string bytes (44 chars)
user.toBase58().encode()  // WRONG: 44 bytes, not 32
```

#### Scenario 4: Missing Seed
```rust
// On-chain: two seeds
seeds = [b"vault", mint.key().as_ref()]

// Client: only one seed
[Buffer.from('vault')]  // WRONG: missing mint
```

## PDA Signing

### Program Signing for CPI

When a program needs to sign for its PDA in a CPI call:

```rust
// Anchor: PDA signs automatically when declared with seeds
#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(
        mut,
        seeds = [b"vault", mint.key().as_ref()],
        bump
    )]
    pub vault: Account<'info, Vault>,
    // ...
}

// In handler: CPI call where vault PDA needs to sign
let cpi_accounts = Transfer {
    from: ctx.accounts.vault.to_account_info(),
    to: ctx.accounts.user.to_account_info(),
};
let signer_seeds = &[
    b"vault".as_ref(),
    ctx.accounts.mint.to_account_info().key.as_ref(),
    &[ctx.bumps.vault],
];
let cpi_ctx = CpiContext::new_with_signer(
    ctx.accounts.token_program.to_account_info(),
    cpi_accounts,
    &[signer_seeds],
);
token::transfer(cpi_ctx, amount)?;
```

### Signer Seeds Format

The `signer_seeds` array must contain:
1. All seeds used to derive the PDA
2. The bump seed as the last element

```rust
let signer_seeds = &[
    b"vault".as_ref(),           // seed 1
    mint.key().as_ref(),         // seed 2
    &[bump],                     // bump seed (must be &[u8])
];
```

## PDA Security Considerations

### 1. Always Verify PDA Derivation

Anchor's `seeds` constraint verifies that the account at the given address was derived from the specified seeds. But if you use `AccountInfo` directly (no Anchor constraints), you MUST verify manually:

```rust
// Manual verification (when not using Anchor constraints)
let (expected_pda, bump) = Pubkey::find_program_address(seeds, program_id);
if account.key() != expected_pda {
    return Err(MyError::InvalidPda);
}
```

### 2. Canonical Bump Enforcement

Always use the canonical bump (highest valid bump). Non-canonical bumps can cause:
- Multiple valid PDAs for the same logical entity (collision)
- Security vulnerabilities where attackers provide a different bump

```rust
// Store bump and use it for re-derivation
#[account(seeds = [b"vault", mint.key().as_ref()], bump = vault.bump)]
pub vault: Account<'info, Vault>,
```

### 3. Seed Collision Avoidance

Choose seeds that won't collide across different account types within your program:

```rust
// BAD: "config" used for multiple account types
seeds = [b"config"]  // Could collide if two account types use this

// GOOD: Include account type in seed
seeds = [b"pool_config"]
seeds = [b"global_config"]
```

### 4. Forward-Compatible Seeds

If you might need to migrate account structures, consider including a version byte:

```rust
seeds = [b"counter", b"v1", user.key().as_ref()]
```

This allows v2 accounts to coexist without conflicting with v1 addresses.

## CLI PDA Tools

```bash
# Derive a PDA from seeds
NO_DNA=1 solana address -k <program_id> --seeds "counter" --seeds <user_pubkey>

# Find PDA with canonical bump
NO_DNA=1 solana find-program-derived-address <program_id> <seed1> <seed2>
```

## Cross-Skill References

- `solana-anchor-programs` — Anchor `#[account]` constraints, `init` pattern
- `solana-architecture-patterns` — PDA-based account architectures, CPI patterns
- `solana-security` — PDA collision attacks, signer verification
- `solana-client` — Client-side PDA derivation with @solana/kit

## Verification Checklist

- [ ] PDA seeds match exactly between client and program (byte comparison)
- [ ] Canonical bump used (highest valid bump, starting from 255)
- [ ] Bump stored in account data for re-derivation
- [ ] Signer seeds format correct for CPI (all seeds + bump as last element)
- [ ] No seed collisions across account types
- [ ] Empty string `b""` vs null byte `b"\0"` confusion eliminated
- [ ] Integer seeds use little-endian encoding on both sides
- [ ] Public key seeds use 32-byte representation, not base58 string
