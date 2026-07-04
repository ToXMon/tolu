# Account Model — Deep Reference

## Overview

Everything in Solana is an account. Accounts are the universal data structure — they hold lamports (SOL), store arbitrary byte data, have an owner, and can be executable (programs). This is fundamentally different from EVM where smart contracts have their own storage. In Solana, programs are stateless; all state lives in separate data accounts.

## Account Structure

Every account on Solana has this binary layout:

```
+-------------------+
| lamports (u64)    |  8 bytes — balance in lamports
+-------------------+
| data (vec<u8>)    |  variable — arbitrary state bytes
+-------------------+
| owner (Pubkey)    |  32 bytes — program that owns this account
+-------------------+
| executable (bool) |  1 byte — true if this is a program
+-------------------+
| rent_epoch (u64)  |  8 bytes — epoch when rent was last collected
+-------------------+
```

### Field Details

| Field | Size | Description |
|-------|------|-------------|
| `lamports` | 8 bytes | Balance in lamports. 1 SOL = 1,000,000,000 lamports. Only the owner can debit. |
| `data` | Variable | Byte array for state. Programs read/write this during execution. |
| `owner` | 32 bytes | Pubkey of the owning program. Only the owner can write data or debit lamports. |
| `executable` | 1 byte | `1` if account contains BPF bytecode (a program), `0` otherwise. |
| `rent_epoch` | 8 bytes | Epoch number when rent was last assessed. With rent exemption, this is largely historical. |

## Account Types

### 1. Data Accounts

Store application state. Created by programs via the System Program. Owned by the creating program.

```
Wallet Account (System-owned)
├── lamports: 2_500_000_000
├── data: [] (empty)
├── owner: System Program (11111111111111111111111111111111)
├── executable: false
└── rent_epoch: 0
```

### 2. Program Accounts

Contain compiled BPF bytecode. Owned by the BPF Loader. Marked `executable = true`.

```
Program Account (BPF Loader-owned)
├── lamports: 1_000_000_000
├── data: [compiled bytecode...]
├── owner: BPF Loader (BPFLoaderUpgradeab1e11111111111111111111111)
├── executable: true
└── rent_epoch: 0
```

### 3. Native Program Accounts

Built-in programs that ship with the validator. Their addresses are well-known:

| Program | Address | Purpose |
|---------|---------|---------|
| System Program | `1111...1111` | Account creation, transfers, assignment |
| BPF Loader (Upgradeable) | `BPFLoaderUpgradeab1e...` | Loading and upgrading custom programs |
| Vote Program | `Vote111111111111111111111111111111111111111` | Validator voting |
| Stake Program | `Stake11111111111111111111111111111111111111` | Staking operations |
| Config Program | `Config1111111111111111111111111111111111111` | Configuration storage |

### 4. Token Accounts (SPL)

Specialized data accounts owned by the SPL Token Program. Three sub-types:

| Type | Purpose | Key Fields |
|------|---------|------------|
| Mint Account | Defines a token | supply, decimals, mint_authority |
| Token Account | Holds one wallet's balance of one mint | amount, owner, mint, delegate |
| Associated Token Account (ATA) | Deterministic token account | Derived from wallet + mint |

**Critical distinction**: Your wallet does not "contain" tokens. Token accounts do. To read a balance, you must find the token account (or ATA) first.

## Ownership Model

Every account has exactly one owner. The owner is a program (Pubkey). This creates a strict permission hierarchy.

### Ownership Rules

1. **Only the owner can debit lamports** from an account
2. **Only the owner can write data** to an account
3. **Only the owner can assign a new owner** (via System Program, one-time, irreversible)
4. **Any program can credit lamports** to any account
5. **The System Program can create new accounts** and transfer ownership to other programs

### Common Ownership Patterns

```
System-owned account (e.g., wallet)
  → System Program can: debit, write (empty data), transfer ownership
  → Your custom program CANNOT touch this directly

Program-owned account (e.g., counter PDA)
  → Owning program can: debit lamports, write data
  → Any program can: credit lamports
  → System Program CANNOT write to this (ownership already transferred)
```

### Why This Matters

When a program receives an account in an instruction, it must verify:

1. **Is this account owned by my program?** (If writing data)
2. **Is this account writable?** (Passed in the instruction's `accounts` array)
3. **Is the expected signer present?**
4. **Does the account data match the expected type?** (Anchor handles this via discriminators)

Anchor automates most of this with `#[account]` and `Account<'info, T>` types, but understanding the underlying model prevents security mistakes.

## Rent and Rent Exemption

### Historical Context

Originally, Solana charged rent every epoch for storing data. Accounts that couldn't pay were garbage-collected. This created complexity — accounts could disappear.

### Modern: Rent Exemption Only

Current Solana requires **rent exemption**: accounts must maintain a minimum balance proportional to their data size. If the balance drops below the minimum, the account is closed and data is wiped.

### Calculation

```
rent_exempt_minimum = (account_data_length + 128) * lamports_per_byte_year
```

Where:
- `128` bytes: Account metadata overhead
- `lamports_per_byte_year`: Currently `3480` (set by network governance)
- For 2-year exemption: multiply by 2

**Simplified formula** (current network rates):
```
rent_exempt_minimum ≈ (data_length + 128) * 6960 lamports
```

### Checking Rent Exemption

```bash
# CLI: Check rent-exempt minimum for a data size
NO_DNA=1 solana rent 0  # Zero-lamport account minimum
NO_DNA=1 solana rent 32 # 32-byte data account
NO_DNA=1 solana rent 80 # Typical token account size
```

### Rent in Anchor

Anchor's `init` constraint handles rent automatically:
```rust
#[account(
    init,
    payer = user,
    space = 8 + 8,  // 8-byte discriminator + 8-byte u64
)]
pub counter: Account<'info, Counter>,
```

The `init` constraint:
1. Creates the account with zero lamports via System Program
2. Transfers ownership to the current program
3. Transfers enough lamports from `payer` to meet rent exemption
4. Sets the discriminator (first 8 bytes)

### Zero-Lamport Initialization

The `init` pattern creates accounts with zero lamports first, then funds them. This is safe because:
- The account is created atomically within the transaction
- If the transaction fails, the account doesn't exist
- The System Program handles the funding transfer

### Account Closing

To close an account and reclaim lamports:
```rust
// Anchor: close account and return funds to recipient
#[account(
    mut,
    close = recipient
)]
pub my_account: Account<'info, MyAccount>,
```

This drains lamports to `recipient` and clears the account data.

## Data Storage Patterns

### Anchor Discriminator

Anchor uses the first 8 bytes of every account as a discriminator — a unique identifier for the account type. This prevents type confusion attacks.

```rust
// Discriminator is automatically computed from:
// sha256("account:<ModuleName><StructName>")[..8]
```

When you use `Account<'info, T>`, Anchor checks that the first 8 bytes match the expected discriminator. If they don't, the instruction fails.

### Space Calculation

Common Rust types and their sizes:

| Type | Size (bytes) |
|------|-------------|
| `u8` / `i8` | 1 |
| `u16` / `i16` | 2 |
| `u32` / `i32` | 4 |
| `u64` / `i64` | 8 |
| `u128` / `i128` | 16 |
| `bool` | 1 |
| `Pubkey` | 32 |
| `Option<T>` | 1 + size(T) |
| `String` | 4 + length (Vec length prefix) |
| `Vec<T>` | 4 + (length * size(T)) |
| `Option<Pubkey>` | 1 + 32 = 33 |

**Always add 8 bytes for the Anchor discriminator.**

Example:
```rust
#[account]
pub struct Game {
    pub player: Pubkey,        // 32
    pub score: u64,            // 8
    pub is_active: bool,       // 1
    pub items: Vec<Item>,      // 4 + (count * item_size)
}
// space = 8 (discriminator) + 32 + 8 + 1 + (4 + items_count * item_size)
```

### Dynamic Data

For variable-length data (Vecs, Strings), you must allocate for the maximum expected size at initialization. You cannot resize accounts after creation (without closing and recreating).

**Pattern**: Allocate generously, or use a separate account for dynamic data.

### Account Resize

Accounts cannot be resized in-place. Options:
1. **Reallocate**: Close and recreate with larger space (loses data)
2. **Sub-accounts**: Store overflow in separate accounts keyed by index
3. **Pre-allocate**: Allocate maximum size at init

## Account Lookup and Resolution

### By Address (Direct)
```typescript
// @solana/kit
const accountInfo = await rpc.getAccountInfo(address).send();
```

### By PDA (Deterministic)
```typescript
const [pda] = await findProgramAddress(seeds, programId);
const accountInfo = await rpc.getAccountInfo(pda).send();
```

### By Filter (Program-Owned)
```typescript
// Get all accounts owned by a program
const accounts = await rpc.getProgramAccounts(programId, {
  filters: [
    { dataSize: 48 },              // Filter by size
    { memcmp: { offset: 8, bytes: owner.toBase58() } }  // Filter by field
  ]
}).send();
```

## Cross-Skill References

- `solana-anchor-programs` — Writing programs with `#[account]` types
- `solana-architecture-patterns` — Account layout design, PDA patterns
- `solana-errors-and-compat` — Debugging account-related errors

## Verification

- [ ] Account ownership verified before writing data
- [ ] Space calculation includes 8-byte discriminator
- [ ] Rent exemption calculated for account data size
- [ ] Account types distinguished (data vs program vs token)
- [ ] Anchor discriminator checked on deserialization
