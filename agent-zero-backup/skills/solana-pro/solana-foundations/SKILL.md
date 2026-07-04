---
name: solana-foundations
description: Core Solana mental models — account model, PDAs, transaction lifecycle, programs, consensus, rent, ownership, and transaction versions
version: 1.0.0
---

# Solana Foundations

## When to Use

- Learning Solana architecture for the first time
- Understanding the account model before writing programs
- Debugging PDA seed mismatches or address derivation errors
- Reasoning about transaction atomicity, composability, or confirmation levels
- Distinguishing programs from accounts, or system-owned from program-owned accounts
- Calculating rent exemption or choosing zero-lamport initialization
- Understanding Proof of History, stake delegation, or Alpenglow consensus
- Choosing between Legacy, v0, and upcoming v1 transaction formats
- Building mental models before touching Anchor, CLI, or client SDK code

## Core Operating Behaviors

### Safety Guardrails

1. **NO_DNA=1 CLI Protocol**: All Solana CLI commands must use the `NO_DNA=1` prefix to disable "Do Not Assume" mode. This prevents silent assumption errors in CLI output.
   ```bash
   NO_DNA=1 solana config set --url devnet
   NO_DNA=1 solana balance
   NO_DNA=1 anchor build
   ```

2. **MCP-First Documentation**: Use the Solana MCP server (`https://mcp.solana.com/mcp`) for live documentation before falling back to training data. Add it with:
   ```bash
   claude mcp add --transport http solana-mcp-server https://mcp.solana.com/mcp
   ```

3. **Devnet Default**: All work targets devnet unless explicitly stated otherwise.
   ```bash
   NO_DNA=1 solana config set --url devnet
   ```

4. **Explorer Verification**: Always verify deployments and transactions on https://explorer.solana.com (append `?cluster=devnet` for devnet). Never trust terminal output alone.

### Verification Requirements

- Verify account structures match expected layouts before reading data
- Confirm PDA derivations match on-chain addresses using `findProgramAddressSync`
- Check transaction confirmation status before reporting success
- Validate rent-exempt balances after account creation

## The Account Model

Everything in Solana is an account. Accounts store data, hold lamports, and have an owner. Programs are accounts too — they're just marked executable.

### Account Structure

Every account has these fields:

| Field | Description |
|-------|-------------|
| `lamports` | Balance in lamports (1 SOL = 1,000,000,000 lamports) |
| `data` | Byte array storing arbitrary state |
| `owner` | Public key of the program that owns this account |
| `executable` | Boolean — true if this account is a program |
| `rent_epoch` | Epoch when rent was last assessed |

### Key Principles

1. **Programs don't store state** — programs are stateless binaries. All state lives in data accounts.
2. **Only the owner can modify an account** — the System Program owns default accounts; custom programs own accounts they create.
3. **Only the owner can debit lamports** — but any program can credit lamports to any account.
4. **Accounts are rent-exempt or closed** — no partial rent collection anymore.

**Deep reference**: `references/account-model.md`

## Program Derived Addresses (PDAs)

PDAs are deterministic addresses derived from seeds + a program ID. They have no private key — only the owning program can sign for them.

### Core Concepts

- **Derivation**: `PDA = findProgramAddress(seeds, programId)`
- **Canonical bump**: The highest bump seed that produces a valid PDA (off-curve)
- **Signer authority**: Only the program that owns the PDA can sign transactions on its behalf
- **Deterministic**: Same seeds + same program = same PDA, every time

### Common Patterns

```rust
// Anchor: derive PDA with canonical bump
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

### Debugging Seed Mismatches

The #1 source of PDA errors is seed mismatches. Debug protocol:
1. Print the seeds you're using on both client and program side
2. Compare byte representations (not string representations)
3. Check for `b""` vs `b"\0"` confusion
4. Verify canonical bump vs custom bump usage
5. Use `findProgramAddressSync` on the client and compare to on-chain address

**Deep reference**: `references/pda-guide.md`

## Transaction Lifecycle

Transactions are the unit of state change in Solana. They contain one or more instructions, execute atomically, and are composable.

### Lifecycle Stages

```
Client constructs → Signs → Submits → Validator processes → Block inclusion → Confirmation
```

### Atomicity and Composability

- **Atomic**: All instructions in a transaction succeed or all fail. No partial state changes.
- **Composable**: Multiple instructions from different programs can be batched in one transaction, enabling CPI (Cross-Program Invocation) chains.

### Confirmation Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `processed` | Transaction landed in a block | Fast UI feedback |
| `confirmed` | Voted on by supermajority of stake | Most dApps |
| `finalized` | Cannot be rolled back | High-value transfers |

### Transaction Versions

- **Legacy**: Original format, no address lookup tables
- **v0**: Supports Address Lookup Tables (ALTs) for cheaper, larger transactions
- **v1**: Coming in coming months — next generation format

**Deep reference**: `references/transaction-lifecycle.md`

## Programs: Stateless Binaries

Programs are executable accounts containing compiled logic (BPF bytecode). They:

- Process instructions but store no state within themselves
- Are owned by the BPF Loader (System Program for native programs)
- Can be upgraded by their upgrade authority (if using the upgradeable loader)
- Interact with state through accounts passed in instructions

### Program vs Account Distinction

| Aspect | Program | Data Account |
|--------|---------|-------------|
| `executable` | `true` | `false` |
| `data` | BPF bytecode | Application state |
| `owner` | BPF Loader | Custom program |
| State | Stateless | Stateful |
| Upgrade | Replaceable (if upgradeable) | Immutable layout |

## Consensus: Proof of History and Alpenglow

Solana uses Proof of History (PoH) combined with Proof of Stake (PoS) for consensus.

### Proof of History (PoH)

PoH is a cryptographic clock — a verifiable delay function that encodes time passage into a hash sequence. It enables validators to process transactions in parallel without coordinating timestamps.

### Stake Delegation

- Validators stake SOL to participate in consensus
- Delegators stake SOL to validators, earning rewards
- Voting weight is proportional to stake

### Alpenglow (Coming in v4.3)

Alpenglow is Solana's next-generation consensus protocol. The **Votor** portion releases in Agave v4.3, with **Alpenswitch** already on testnet. Alpenglow aims to:
- Reduce block production latency
- Improve finality speed
- Maintain the high throughput that defines Solana

**Deep reference**: `references/consensus-and-poh.md`

## Rent and Rent Exemption

Solana charges rent for storing data on-chain. Modern Solana requires **rent exemption** — accounts must maintain a minimum balance or they're garbage-collected.

### Rent Exemption Calculation

```
rent-exempt minimum = (account_data_length + 128) * 6960 lamports
```

The `128` bytes account for account metadata. The `6960` is a per-byte rate set by the network.

### Zero-Lamport Initialization

In Anchor, `init` creates accounts with zero lamports, then the System Program transfers rent-exempt minimum. Use `space` to specify data size:

```rust
#[account(init, payer = user, space = 8 + 48)]
pub my_account: Account<'info, MyAccount>,
```

- `8` bytes: Anchor discriminator
- `48` bytes: Your data structure size

Always calculate space carefully — under-allocating causes runtime errors.

## Ownership Model

Every account has exactly one owner. The owner is a program (identified by public key).

### System-Owned Accounts

- Created by the System Program
- Default for new wallets and basic transfers
- Only the System Program can debit or modify them

### Program-Owned Accounts

- Created by custom programs (via `invoke` to System Program's `create_account`)
- Only the owning program can debit lamports or write data
- Any program can credit lamports to them

### Ownership Rules Summary

1. Only the owner can debit an account's lamports
2. Only the owner can modify an account's data
3. Only the owner can assign a new owner
4. Any program can credit lamports to any account
5. The System Program can transfer account ownership (one-time, irreversible)

## Cross-Skill References

| Related Skill | When to Switch |
|--------------|----------------|
| `solana-environment-setup` | Setting up Rust, Anchor CLI, Solana CLI, devnet config |
| `solana-anchor-programs` | Writing, building, and deploying Anchor programs |
| `solana-architecture-patterns` | Designing program architectures, account layouts, CPI patterns |
| `solana-errors-and-compat` | Debugging version mismatches, GLIBC errors, toolchain issues |
| `solana-client` | Building TypeScript clients with @solana/kit SDK |
| `solana-testing` | Testing programs with LiteSVM, Mollusk, Surfpool |

## Modern Ecosystem Context

| Component | Version | Notes |
|-----------|---------|-------|
| Agave | v4.1.0 | Current validator client release |
| Alpenglow | Votor in v4.3 | Next-gen consensus; Alpenswitch on testnet |
| Transaction versions | Legacy, v0, v1 coming | v0 enables ALTs; v1 coming in coming months |

## Verification Checklist

- [ ] NO_DNA=1 prefix used for all CLI commands
- [ ] MCP server (https://mcp.solana.com/mcp) referenced for live docs
- [ ] Devnet configuration confirmed (`solana config get` shows devnet)
- [ ] Account structures match expected layouts
- [ ] PDA derivations verified on both client and program side
- [ ] Rent exemption calculated correctly (8 + data_size for Anchor accounts)
- [ ] Transaction confirmation level appropriate for use case
- [ ] Ownership model understood: only owner can debit/modify
- [ ] Programs are stateless — state lives in data accounts
- [ ] Explorer verification: https://explorer.solana.com?cluster=devnet
- [ ] Transaction version (Legacy/v0) chosen appropriately
