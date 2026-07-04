# Error Handling Reference

Complete guide to Anchor error codes, require macros, error propagation, and debugging.

## Custom Error Codes

### Defining Errors

```rust
#[error_code]
pub enum MyError {
    #[msg("Custom error message")]
    CustomError,

    #[msg("Value too large: {0}")]
    ValueError(u64),

    #[msg("Invalid amount: expected {0}, got {1}")]
    InvalidAmount(u64, u64),
}
```

### Real-World Example (Escrow)

From bootcamp `escrow-program` exercise:

```rust
#[error_code]
pub enum EscrowError {
    #[msg("Invalid amount")]
    InvalidAmount,
    #[msg("Invalid maker")]
    InvalidMaker,
    #[msg("Invalid mint a")]
    InvalidMintA,
    #[msg("Invalid mint b")]
    InvalidMintB,
}
```

### Real-World Example (SignalForge)

From production SignalForge program:

```rust
#[error_code]
pub enum ErrorCode {
    #[msg("Failed to calculate account space for Token-2022 extensions")]
    SpaceCalculationFailed,
    #[msg("Token-2022 badge is non-transferable")]
    BadgeNonTransferable,
}
```

## Require Macros

### Basic Require

```rust
require!(condition, ErrorName::ErrorVariant);
```

### Require with Context

```rust
require!(
    value > 0,
    MyError::CustomError
);
```

### Typed Require Macros

| Macro | Purpose | Equivalent |
|------|---------|------------|
| `require!` | Boolean condition | `if !cond { return Err(...) }` |
| `require_eq!` | Equality check | `require!(a == b, err)` |
| `require_keys_eq!` | Pubkey equality | `require!(a.key() == b.key(), err)` |
| `require_gt!` | Greater than | `require!(a > b, err)` |
| `require_gte!` | Greater than or equal | `require!(a >= b, err)` |
| `require_lt!` | Less than | `require!(a < b, err)` |
| `require_lte!` | Less than or equal | `require!(a <= b, err)` |
| `require_ne!` | Inequality | `require!(a != b, err)` |
| `require_keys_neq!` | Pubkey inequality | `require!(a.key() != b.key(), err)` |

### Usage Examples

```rust
// Amount validation
require_gt!(receive, 0, EscrowError::InvalidAmount);
require_gt!(amount, 0, EscrowError::InvalidAmount);

// Authority check
require_keys_eq!(
    ctx.accounts.proposal.creator,
    ctx.accounts.creator.key(),
    ProposalError::NotCreator
);

// State machine transition
require!(
    ctx.accounts.proposal.state == ProposalState::Draft,
    ProposalError::InvalidStateTransition
);

// Custom constraint
require!(
    remaining.len() % 2 == 0,
    BatchError::InvalidSchema
);
```

## Error Propagation with `?`

The `?` operator propagates errors automatically:

```rust
pub fn make(ctx: Context<Make>, seed: u64, receive: u64, amount: u64) -> Result<()> {
    require_gt!(receive, 0, EscrowError::InvalidAmount);

    let cpi_ctx = CpiContext::new(
        ctx.accounts.token_program.to_account_info(),
        cpi_accounts,
    );
    token::transfer_checked(cpi_ctx, amount, ctx.accounts.mint_a.decimals)?;

    Ok(())
}
```

## Error in Constraints

Attach errors to constraint failures using `@`:

```rust
#[account(
    mut,
    close = maker,
    has_one = maker @ EscrowError::InvalidMaker,
    has_one = mint_a @ EscrowError::InvalidMintA,
    has_one = mint_b @ EscrowError::InvalidMintB,
    constraint = vault.amount >= amount @ EscrowError::InsufficientFunds
)]
pub escrow: Account<'info, Escrow>,
```

## State Machine Error Pattern

From bootcamp deck-04 — proposal/voting state machine:

```rust
#[error_code]
pub enum ProposalError {
    #[msg("Invalid state transition")]
    InvalidStateTransition,
    #[msg("Not the proposal creator")]
    NotCreator,
    #[msg("Proposal is not active")]
    NotActive,
    #[msg("Already voted")]
    AlreadyVoted,
    #[msg("Voting is closed")]
    VotingClosed,
}

// Enforce transitions
pub fn vote(ctx: Context<Vote>, yes: bool) -> Result<()> {
    require!(
        ctx.accounts.proposal.state == ProposalState::Active,
        ProposalError::NotActive
    );
    // ... vote logic
    Ok(())
}

pub fn close(ctx: Context<Close>) -> Result<()> {
    require_keys_eq!(
        ctx.accounts.proposal.creator,
        ctx.accounts.creator.key(),
        ProposalError::NotCreator
    );
    require!(
        ctx.accounts.proposal.state == ProposalState::Active,
        ProposalError::InvalidStateTransition
    );
    ctx.accounts.proposal.state = ProposalState::Closed;
    Ok(())
}
```

**Critical**: AI usually writes the happy path. You must enforce invalid transition rejection:
- Vote in Draft should fail → `NotActive`
- Vote in Closed should fail → `VotingClosed`
- Non-creator activate/close should fail → `NotCreator`
- Duplicate vote should fail → `AlreadyVoted`

## Error Codes for Common Scenarios

### Token Operations

```rust
#[error_code]
pub enum TokenError {
    #[msg("Insufficient funds")]
    InsufficientFunds,
    #[msg("Invalid mint")]
    InvalidMint,
    #[msg("Invalid token account")]
    InvalidTokenAccount,
    #[msg("Decimals mismatch")]
    DecimalsMismatch,
}
```

### Access Control

```rust
#[error_code]
pub enum AccessError {
    #[msg("Unauthorized")]
    Unauthorized,
    #[msg("Not the authority")]
    NotAuthority,
    #[msg("Not the admin")]
    NotAdmin,
    #[msg("Operation not allowed")]
    NotAllowed,
}
```

### Validation

```rust
#[error_code]
pub enum ValidationError {
    #[msg("Invalid input")]
    InvalidInput,
    #[msg("Value out of range")]
    OutOfRange,
    #[msg("String too long")]
    StringTooLong,
    #[msg("Already initialized")]
    AlreadyInitialized,
}
```

## Error Handling Best Practices

### 1. Use Custom Errors Always

```rust
// BAD — generic error
if amount == 0 {
    return Err(ProgramError::InvalidArgument);
}

// GOOD — specific error
require_gt!(amount, 0, EscrowError::InvalidAmount);
```

### 2. Descriptive Messages

```rust
#[msg("Invalid amount: expected > 0, got {0}")]
InvalidAmount(u64),
```

### 3. Constraint Errors

Always attach errors to constraints:

```rust
#[account(
    constraint = account.is_active @ MyError::AccountInactive
)]
```

### 4. Early Validation

Validate inputs at the start of instruction handlers:

```rust
pub fn make(ctx: Context<Make>, seed: u64, receive: u64, amount: u64) -> Result<()> {
    require_gt!(receive, 0, EscrowError::InvalidAmount);
    require_gt!(amount, 0, EscrowError::InvalidAmount);
    // ... proceed with logic
}
```

## Debugging Errors

### Reading Program Logs

Use `msg!` for debugging:

```rust
msg!("Escrow created by maker {} — seed={}, receive={}, amount={}",
    ctx.accounts.maker.key(), seed, receive, amount);
```

### Common Error Codes

| Error | Code | Cause |
|-------|------|-------|
| `InsufficientFunds` | 301 | Not enough lamports |
| `InvalidAccountData` | 3001 | Account discriminator mismatch |
| `AccountNotEnoughKeys` | 3002 | Missing required accounts |
| `DeclinedInstruction` | 3003 | Constraint failed |
| `AccountDiscriminatorNotFound` | 3004 | Expected Anchor account, got raw |
| `AccountDiscriminatorMismatch` | 3005 | Wrong account type |
| `DeclaredProgramIdMismatch` | 3006 | declare_id! doesn't match |

See `solana-errors-and-compat` skill for comprehensive error reference.

### Error from CPI

CPI errors bubble up as `ProgramError`:

```rust
// CPI error propagation
token::transfer_checked(cpi_ctx, amount, decimals)?;
// If CPI fails, error propagates to caller
```

## Testing Error Cases

Always test both success AND failure:

```typescript
// Anchor test — failure case
it("Rejects vote in Draft state", async () => {
    try {
        await program.methods.vote({ yes: true })
            .accounts({ proposal, voter: voter.publicKey })
            .rpc();
        assert.fail("Should have rejected vote in Draft state");
    } catch (err) {
        assert.include(err.toString(), "NotActive");
    }
});
```

### Test Coverage Requirements (from deck-04)

- Happy path (valid transition, valid authority)
- Failure cases:
  - Vote in Draft should fail
  - Vote in Closed should fail
  - Non-creator activate/close should fail
  - Duplicate vote should fail
- Edge cases (boundary values, empty accounts)

## Cross-Reference

For comprehensive Solana error debugging and version compatibility, load the `solana-errors-and-compat` skill.
