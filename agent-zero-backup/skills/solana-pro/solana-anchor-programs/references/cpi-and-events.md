# CPI and Events Reference

Complete guide to Cross-Program Invocation (CPI) patterns, event emission, and program-to-program calls in Anchor.

## CPI Overview

Cross-Program Invocation allows one program to call instructions on another program. Anchor provides two patterns:

| Pattern | Who Signs | Use Case |
|---------|-----------|----------|
| `CpiContext::new` / `invoke` | User (signer in transaction) | User transfers their own funds |
| `CpiContext::new_with_signer` / `invoke_signed` | PDA (program provides seeds + bump) | Vault PDA sends funds out |

## Anchor CPI (CpiContext)

### Basic CPI (User Signs)

From escrow exercise — maker transfers tokens to vault:

```rust
use anchor_spl::token::{self, TransferChecked};

let cpi_accounts = TransferChecked {
    from: ctx.accounts.maker_ata_a.to_account_info(),
    mint: ctx.accounts.mint_a.to_account_info(),
    to: ctx.accounts.vault.to_account_info(),
    authority: ctx.accounts.maker.to_account_info(),
};
let cpi_ctx = CpiContext::new(
    ctx.accounts.token_program.to_account_info(),
    cpi_accounts,
);
token::transfer_checked(cpi_ctx, amount, ctx.accounts.mint_a.decimals)?;
```

### PDA-Signed CPI

From escrow exercise — vault PDA sends tokens to taker:

```rust
let signer_seeds = &[
    b"escrow".as_ref(),
    ctx.accounts.maker.to_account_info().key.as_ref(),
    &ctx.accounts.escrow.seed.to_le_bytes(),
    &[ctx.accounts.escrow.bump],
];
let signer = &[&signer_seeds[..]];

let cpi_accounts_a = TransferChecked {
    from: ctx.accounts.vault.to_account_info(),
    mint: ctx.accounts.mint_a.to_account_info(),
    to: ctx.accounts.taker_ata_a.to_account_info(),
    authority: ctx.accounts.escrow.to_account_info(),
};
let cpi_ctx_a = CpiContext::new_with_signer(
    ctx.accounts.token_program.to_account_info(),
    cpi_accounts_a,
    signer,
);
token::transfer_checked(cpi_ctx_a, vault_amount, ctx.accounts.mint_a.decimals)?;
```

### Closing Accounts via CPI

From escrow exercise — close vault and return rent:

```rust
use anchor_spl::token::{self, CloseAccount};

let close_accounts = CloseAccount {
    account: ctx.accounts.vault.to_account_info(),
    destination: ctx.accounts.maker.to_account_info(),
    authority: ctx.accounts.escrow.to_account_info(),
};
let close_ctx = CpiContext::new_with_signer(
    ctx.accounts.token_program.to_account_info(),
    close_accounts,
    signer,
);
token::close_account(close_ctx)?;
```

### System Program CPI

Create accounts via System Program:

```rust
use anchor_lang::system_program;

system_program::create_account(
    CpiContext::new(
        ctx.accounts.system_program.to_account_info(),
        system_program::CreateAccount {
            from: ctx.accounts.authority.to_account_info(),
            to: ctx.accounts.mint.to_account_info(),
        },
    ),
    lamports,
    space as u64,
    &ctx.accounts.token_program.key(),
)?;
```

> **v1.x change**: `CpiContext::new` takes `Pubkey` (program ID), not `AccountInfo`. See `anchor-v1-changes.md`.

## Raw invoke / invoke_signed

For programs without Anchor wrappers (e.g., calling SPL instructions directly):

```rust
use anchor_lang::solana_program::program::{invoke, invoke_signed};
```

### invoke (User Signs)

From SignalForge production code — user transfers their tokens:

```rust
let transfer_ix = spl_token::instruction::transfer(
    &ctx.accounts.token_program.key(),
    &ctx.accounts.from.key(),
    &ctx.accounts.to.key(),
    &ctx.accounts.authority.key(),
    &[],
    amount,
)?;

invoke(
    &transfer_ix,
    &[
        ctx.accounts.from.to_account_info(),
        ctx.accounts.to.to_account_info(),
        ctx.accounts.authority.to_account_info(),
        ctx.accounts.token_program.to_account_info(),
    ],
)?;
```

### invoke_signed (PDA Signs)

From SignalForge — PDA mints tokens:

```rust
let bump = ctx.bumps.signal_token_mint;
let seeds = &[
    b"signal_token".as_ref(),
    &[bump],
];
let signer = &[&seeds[..]];

let mint_to_ix = spl_token::instruction::mint_to(
    &ctx.accounts.token_program.key(),
    &ctx.accounts.mint.key(),
    &ctx.accounts.destination.key(),
    &ctx.accounts.signal_token_mint.key(),
    &[],
    amount,
)?;

invoke_signed(
    &mint_to_ix,
    &[
        ctx.accounts.mint.to_account_info(),
        ctx.accounts.destination.to_account_info(),
        ctx.accounts.signal_token_mint.to_account_info(),
        ctx.accounts.token_program.to_account_info(),
    ],
    signer,
)?;
```

## Token-2022 CPI

From SignalForge — minting NonTransferable badges:

```rust
let mint_to_ix = spl_token_2022::instruction::mint_to(
    &ctx.accounts.token_2022_program.key(),
    &ctx.accounts.mint.key(),
    &ctx.accounts.destination.key(),
    &ctx.accounts.badge_mint_config.key(),
    &[],
    1, // Mint 1 badge
)?;

invoke_signed(
    &mint_to_ix,
    &[
        ctx.accounts.mint.to_account_info(),
        ctx.accounts.destination.to_account_info(),
        ctx.accounts.badge_mint_config.to_account_info(),
        ctx.accounts.token_2022_program.to_account_info(),
    ],
    signer,
)?;
```

## CPI Safety Rules

### 1. Validate CPI Targets

Always use `Program<'info, T>` to validate CPI targets:

```rust
// GOOD — program is validated by Anchor
pub token_program: Program<'info, Token>,

// BAD — no validation, allows arbitrary CPI
/// CHECK: Not validated
pub token_program: AccountInfo<'info>,
```

### 2. Never Pass Extra Privileges

Only pass the minimum required accounts to CPI callees.

### 3. Prefer Anchor CPI Helpers

Use `anchor_spl` helpers over raw `invoke` when possible:

```rust
// PREFERRED — Anchor helper
use anchor_spl::token::{self, Transfer};
token::transfer(cpi_ctx, amount)?;

// FALLBACK — raw invoke (for programs without Anchor wrappers)
invoke(&transfer_ix, &[...])?;
```

## CPI Debugging (from deck-04)

Most CPI failures are metadata failures, not logic errors:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Missing required signature | Using `invoke` where PDA signer needed | Switch to `new_with_signer` + correct seeds |
| Insufficient account keys | System Program or transfer accounts omitted | Pass sender, recipient, and system program |
| Invalid seeds | Derivation and signer seed bytes differ | Unify seed order/encoding across init and withdraw |
| Vault disappears | Balance dropped below rent-exempt threshold | Check min balance or close account intentionally |

### Debugging Steps

1. Check signer pattern — does the CPI need user or PDA signature?
2. Verify all required accounts are passed
3. Compare seed bytes between PDA derivation and signer construction
4. Check rent-exempt balances

## Events

### Defining Events

```rust
#[event]
pub struct EscrowCreated {
    pub maker: Pubkey,
    pub seed: u64,
    pub mint_a: Pubkey,
    pub mint_b: Pubkey,
    pub receive: u64,
    pub amount: u64,
}

#[event]
pub struct TakeCompleted {
    pub taker: Pubkey,
    pub maker: Pubkey,
}
```

### Emitting Events

```rust
use anchor_lang::prelude::*;

pub fn make(ctx: Context<Make>, seed: u64, receive: u64, amount: u64) -> Result<()> {
    // ... logic ...

    emit!(EscrowCreated {
        maker: ctx.accounts.maker.key(),
        seed,
        mint_a: ctx.accounts.mint_a.key(),
        mint_b: ctx.accounts.mint_b.key(),
        receive,
        amount,
    });

    Ok(())
}
```

### Event vs msg!

| Approach | Purpose | Queryable |
|----------|---------|-----------|
| `emit!` | Structured event emission | Yes — via `getProgramAccounts` or log parsing |
| `msg!` | Debug logging | No — terminal output only |

Use `msg!` for debugging:

```rust
msg!("Escrow created by maker {} — seed={}, receive={}, amount={}",
    ctx.accounts.maker.key(), seed, receive, amount);
```

### Reading Events from Client

Events are written to transaction logs. Parse them client-side:

```typescript
import { Program } from "@anchor-lang/core";

const tx = await program.methods
    .make(seed, receive, amount)
    .accounts({...})
    .rpc();

// Parse events from transaction logs
const txInfo = await connection.getTransaction(tx, {
    maxSupportedTransactionVersion: 0,
});

// Events appear in txInfo.meta.logMessages
```

## Program-to-Program Architecture

### Two-Program Pattern (Tip Jar from deck-04)

Program A (Tip Jar) calls System Program:

```rust
// Deposit — user signs
let cpi_ctx = CpiContext::new(
    ctx.accounts.system_program.to_account_info(),
    system_program::Transfer {
        from: ctx.accounts.user.to_account_info(),
        to: ctx.accounts.vault.to_account_info(),
    },
);
system_program::transfer(cpi_ctx, amount)?;

// Withdraw — PDA signs
let seeds = &[b"vault", owner.key().as_ref(), &[bump]];
let signer = &[&seeds[..]];

let cpi_ctx = CpiContext::new_with_signer(
    ctx.accounts.system_program.to_account_info(),
    system_program::Transfer {
        from: ctx.accounts.vault.to_account_info(),
        to: ctx.accounts.owner.to_account_info(),
    },
    signer,
);
system_program::transfer(cpi_ctx, amount)?;
```

### PDA Design for CPI

From deck-04 — vault seeds design:

```rust
// Use vault seeds like ["vault", owner_wallet]
// so each owner has deterministic storage and withdraw authority
#[account(
    init,
    payer = owner,
    space = 8 + Vault::INIT_SPACE,
    seeds = [b"vault", owner.key().as_ref()],
    bump
)]
pub vault: Account<'info, Vault>,
```

## CPI Error Propagation

CPI errors bubble up automatically with `?`:

```rust
token::transfer_checked(cpi_ctx, amount, decimals)?;
// If CPI fails, error propagates to caller
```

For custom error handling:

```rust
match token::transfer_checked(cpi_ctx, amount, decimals) {
    Ok(_) => Ok(()),
    Err(_) => Err(MyError::TransferFailed.into()),
}
```

## Cross-Reference

- For testing CPIs, load `solana-testing` skill (Mollusk, LiteSVM)
- For security audit of CPI patterns, load `solana-security` skill
- For error debugging, load `solana-errors-and-compat` skill
