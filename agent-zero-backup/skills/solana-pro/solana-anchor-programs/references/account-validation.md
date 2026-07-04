# Account Validation Reference

Complete guide to Anchor account validation patterns, constraints, and types.

## Account Types

| Type | Purpose | Auto-Validates |
|------|---------|----------------|
| `Signer<'info>` | Verifies account signed the transaction | Signature |
| `SystemAccount<'info>` | Confirms System Program ownership | Owner = System |
| `Program<'info, T>` | Validates executable program accounts | Executable, owner |
| `Account<'info, T>` | Typed program account | Owner = program, discriminator |
| `InterfaceAccount<'info, T>` | Dual Token/Token2022 compatibility | Owner = Token or Token2022 |
| `UncheckedAccount<'info>` | Raw account (AVOID) | Nothing — manual validation required |
| `LazyAccount<'info, T>` | Heap-allocated read-only (v0.31+) | Same as Account, lazy deserialization |
| `AccountInfo<'info>` | Raw account info | Nothing |
| `Sysvar<'info, T>` | System variables (Clock, Rent, etc.) | Sysvar address |

## Constraint Reference

### Initialization

```rust
#[account(
    init,
    payer = payer,
    space = 8 + CustomAccount::INIT_SPACE,
    seeds = [b"vault", owner.key().as_ref()],
    bump
)]
pub account: Account<'info, CustomAccount>,
```

- `init` — Creates account via System Program, transfers rent-exempt lamports
- `payer` — Account paying for rent (must be `mut` and `Signer`)
- `space` — Must include 8-byte discriminator + account data size
- Use `INIT_SPACE` derive macro for automatic calculation

### InitSpace Derive

```rust
#[account]
#[derive(InitSpace)]
pub struct Escrow {
    pub seed: u64,      // 8
    pub maker: Pubkey,  // 32
    pub mint_a: Pubkey, // 32
    pub mint_b: Pubkey, // 32
    pub receive: u64,   // 8
    pub bump: u8,       // 1
}
// INIT_SPACE = 8 + 32 + 32 + 32 + 8 + 1 = 113

// Usage
#[account(
    init,
    payer = maker,
    space = 8 + Escrow::INIT_SPACE,
)]
```

**String space**: 4-byte length prefix + max bytes
```rust
#[derive(InitSpace)]
pub struct Proposal {
    pub title: String,  // 4 + max_length
}

#[account]
#[derive(InitSpace)]
pub struct Proposal {
    #[max_len(50)]
    pub title: String,  // 4 + 50 = 54 bytes
}
```

### PDA Validation

```rust
// Init with PDA
#[account(
    init,
    payer = payer,
    space = 8 + CustomAccount::INIT_SPACE,
    seeds = [b"counter", user.key().as_ref()],
    bump
)]
pub counter: Account<'info, Counter>,

// Validate existing PDA
#[account(
    mut,
    seeds = [b"counter", user.key().as_ref()],
    bump
)]
pub counter: Account<'info, Counter>,

// Store bump for PDA-signed CPI
#[account(
    init,
    seeds = [b"escrow", maker.key().as_ref(), seed.to_le_bytes().as_ref()],
    bump
)]
pub escrow: Account<'info, Escrow>,
// In handler: escrow.bump = ctx.bumps.escrow;
```

### Ownership and Relationships

```rust
#[account(
    has_one = authority @ CustomError::InvalidAuthority,
    has_one = mint @ CustomError::InvalidMint,
    constraint = account.is_active @ CustomError::AccountInactive
)]
pub account: Account<'info, CustomAccount>,
```

- `has_one` — Checks `account.field == given_account.key()`
- `constraint` — Arbitrary boolean expression
- `@` — Attach custom error to constraint failure

### Signer Constraint

```rust
#[account(
    mut,
    constraint = vault.authority == maker.key() @ EscrowError::InvalidMaker,
)]
pub vault: Account<'info, TokenAccount>,

// Or use Signer wrapper
pub maker: Signer<'info>,
```

### Mint Constraints

```rust
#[account(
    mint::decimals = 9,
    mint::authority = authority,
    mint::freeze_authority = authority
)]
pub mint: Account<'info, Mint>,
```

### Token Account Constraints

```rust
#[account(
    mut,
    associated_token::mint = mint,
    associated_token::authority = owner,
    token::mint = mint,
    token::authority = owner,
)]
pub token_account: Account<'info, TokenAccount>,
```

### Associated Token Account Creation

```rust
use anchor_spl::associated_token::AssociatedToken;

#[account(
    init,
    payer = maker,
    associated_token::mint = mint_a,
    associated_token::authority = escrow  // PDA as authority
)]
pub vault: Account<'info, TokenAccount>,

pub associated_token_program: Program<'info, AssociatedToken>,
pub token_program: Program<'info, Token>,
pub system_program: Program<'info, System>,
```

### Reallocation

```rust
#[account(
    mut,
    realloc = new_space,
    realloc::payer = payer,
    realloc::zero = true  // Clear old data when shrinking
)]
pub account: Account<'info, CustomAccount>,
```

### Closing Accounts

```rust
#[account(
    mut,
    close = destination  // Rent lamports sent to destination
)]
pub account: Account<'info, CustomAccount>,
```

- Account data zeroed
- Lamports transferred to destination
- Account marked closed

### init_if_needed (USE WITH CAUTION)

```rust
#[account(
    init_if_needed,
    payer = taker,
    associated_token::mint = mint_a,
    associated_token::authority = taker
)]
pub taker_ata_a: Account<'info, TokenAccount>,
```

**WARNING**: `init_if_needed` can permit reinitialization attacks. Always pair with `require` guards:

```rust
require!(
    ctx.accounts.account.field == 0 || ctx.accounts.account.is_initialized,
    MyError::AlreadyInitialized
);
```

## Account Discriminators

### Default Discriminator

`sha256("account:<StructName>")[0..8]` — first 8 bytes of SHA256 hash.

### Custom Discriminator (v0.31+)

```rust
#[account(discriminator = 1)]
pub struct Escrow { ... }
```

**Constraints:**
- Must be unique across your program
- Using `[1]` prevents `[1, 2, ...]` which also start with `1`
- `[0]` conflicts with uninitialized accounts

## Zero-Copy Accounts

For accounts exceeding stack/heap limits (>10KB):

```rust
#[account(zero_copy)]
pub struct LargeAccount {
    pub data: [u8; 10000],
    pub owner: Pubkey,
}

// Access via deref
let large_account: &mut LargeAccount = &mut ctx.accounts.account;
large_account.data[0] = 42;
```

Accounts under 10,240 bytes use `init`; larger accounts require external creation then `zero` constraint:

```rust
#[account(
    zero,  // Assumes account already exists with correct lamports
    seeds = [...],
    bump
)]
pub large_account: AccountLoader<'info, LargeAccount>,
```

## LazyAccount (v0.31+)

Heap-allocated, read-only account access for efficient memory usage:

```rust
// Cargo.toml
anchor-lang = { version = "0.31.1", features = ["lazy-account"] }

// Usage
pub account: LazyAccount<'info, CustomAccountType>,

pub fn handler(ctx: Context<MyInstruction>) -> Result<()> {
    let value = ctx.accounts.account.get_value()?;
    Ok(())
}
```

**Note:** LazyAccount is read-only. After CPIs, use `unload()` to refresh cached values.

## Remaining Accounts

Pass dynamic accounts beyond fixed instruction structure:

```rust
pub fn batch_operation(ctx: Context<BatchOp>, amounts: Vec<u64>) -> Result<()> {
    let remaining = &ctx.remaining_accounts;
    require!(remaining.len() % 2 == 0, BatchError::InvalidSchema);

    for (i, chunk) in remaining.chunks(2).enumerate() {
        process_pair(&chunk[0], &chunk[1], amounts[i])?;
    }
    Ok(())
}
```

## Instruction Data Access

Access instruction arguments in account validation:

```rust
#[derive(Accounts)]
#[instruction(seed: u64)]
pub struct Make<'info> {
    #[account(
        init,
        seeds = [b"escrow", maker.key().as_ref(), seed.to_le_bytes().as_ref()],
        bump
    )]
    pub escrow: Account<'info, Escrow>,
    // ...
}
```

## Token2022 Compatibility

Use `InterfaceAccount` for dual Token/Token2022 compatibility:

```rust
use anchor_spl::token_interface::{Mint, TokenAccount, TokenInterface};

pub mint: InterfaceAccount<'info, Mint>,
pub token_account: InterfaceAccount<'info, TokenAccount>,
pub token_program: Interface<'info, TokenInterface>,
```

## Common Validation Patterns

### Vault Pattern (Escrow)

```rust
#[derive(Accounts)]
pub struct Take<'info> {
    #[account(
        mut,
        close = maker,
        has_one = maker @ EscrowError::InvalidMaker,
        has_one = mint_a @ EscrowError::InvalidMintA,
        has_one = mint_b @ EscrowError::InvalidMintB,
        seeds = [b"escrow", maker.key().as_ref(), escrow.seed.to_le_bytes().as_ref()],
        bump = escrow.bump
    )]
    pub escrow: Account<'info, Escrow>,

    #[account(
        mut,
        associated_token::mint = mint_a,
        associated_token::authority = escrow
    )]
    pub vault: Account<'info, TokenAccount>,
}
```

### Counter PDA Pattern

```rust
#[derive(Accounts)]
pub struct Increment<'info> {
    #[account(
        mut,
        seeds = [b"counter", user.key().as_ref()],
        bump
    )]
    pub counter: Account<'info, Counter>,

    pub user: Signer<'info>,
}
```

### Multiple PDAs with Instruction Data

```rust
#[derive(Accounts)]
#[instruction(proposal_id: u64, voter: Pubkey)]
pub struct Vote<'info> {
    #[account(
        mut,
        seeds = [b"proposal", proposal_id.to_le_bytes().as_ref()],
        bump
    )]
    pub proposal: Account<'info, Proposal>,

    #[account(
        init,
        payer = voter_signer,
        space = 8 + VoteRecord::INIT_SPACE,
        seeds = [b"vote", proposal_id.to_le_bytes().as_ref(), voter.as_ref()],
        bump
    )]
    pub vote_record: Account<'info, VoteRecord>,

    #[account(mut)]
    pub voter_signer: Signer<'info>,

    pub system_program: Program<'info, System>,
}
```
