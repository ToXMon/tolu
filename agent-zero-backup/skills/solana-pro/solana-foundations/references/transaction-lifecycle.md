# Transaction Lifecycle — Deep Reference

## Overview

Transactions are the unit of state change in Solana. Each transaction contains one or more instructions, executes atomically, and can compose across programs. Understanding the full lifecycle — from construction to finality — is essential for building reliable dApps.

## Transaction Structure

```
Transaction
├── Message
│   ├── Header
│   │   ├── num_required_signatures
│   │   ├── num_readonly_signed_accounts
│   │   └── num_readonly_unsigned_accounts
│   ├── Account Keys (compact array)
│   │   ├── Signed writable accounts
│   │   ├── Signed readonly accounts
│   │   ├── Unsigned writable accounts
│   │   └── Unsigned readonly accounts
│   ├── Recent Blockhash
│   └── Instructions (compact array)
│       └── Instruction
│           ├── program_id_index
│           ├── account_indexes
│           └── data (byte array)
└── Signatures (compact array)
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **Instructions** | One or more calls to programs with data and accounts |
| **Account Keys** | All accounts the transaction touches (deduplicated) |
| **Blockhash** | Recent blockhash for replay protection (valid ~60-90 seconds) |
| **Signatures** | Ed25519 signatures from required signers |

## Instructions

### Instruction Anatomy

```rust
pub struct Instruction {
    pub program_id: Pubkey,       // Which program to call
    pub accounts: Vec<AccountMeta>, // Accounts the instruction reads/writes
    pub data: Vec<u8>,            // Serialized instruction arguments
}

pub struct AccountMeta {
    pub pubkey: Pubkey,
    pub is_signer: bool,    // Must this account sign?
    pub is_writable: bool,  // Can the program modify this account?
}
```

### Single Instruction Example

```typescript
// Transfer 0.5 SOL from user to recipient
const transferIx = {
  programId: SystemProgram.programId,
  keys: [
    { pubkey: user, isSigner: true, isWritable: true },
    { pubkey: recipient, isSigner: false, isWritable: true }
  ],
  data: Buffer.concat([
    Buffer.from([2, 0, 0, 0]), // Transfer instruction discriminator
    new BN(500_000_000).toArray('le', 8) // 0.5 SOL in lamports
  ])
};
```

### Multi-Instruction Transactions (Composability)

```typescript
// Create token + mint to user in one atomic transaction
const tx = new Transaction().add(
  createMintIx,    // Instruction 1: Create mint account
  mintTokensIx     // Instruction 2: Mint tokens to user
);
```

**Key benefit**: If instruction 2 fails, instruction 1 is rolled back too. No partial state.

## Transaction Lifecycle Stages

```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Construct   │────▶│   Sign   │────▶│ Submit   │────▶│  Validate    │
│  (client)    │     │ (client) │     │ (RPC)    │     │  (validator) │
└─────────────┘     └──────────┘     └──────────┘     └──────┬───────┘
                                                                │
                                                                ▼
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Finalized   │◀────│ Confirm  │◀────│ Execute  │◀────│  Block       │
│  (network)   │     │ (network)│     │ (runtime)│     │  Inclusion   │
└─────────────┘     └──────────┘     └──────────┘     └──────────────┘
```

### Stage 1: Construction (Client)

1. Gather all required accounts for all instructions
2. Serialize instruction data (Anchor uses Borsh; raw programs use custom)
3. Fetch a recent blockhash from RPC
4. Assemble the transaction message

### Stage 2: Signing (Client)

1. All required signers sign the transaction
2. For PDA signers, the program signs during execution (not client-side)
3. Partial signing is supported for multi-signature workflows

### Stage 3: Submission (RPC)

```typescript
// Submit transaction
const signature = await rpc.sendTransaction(tx, {
  skipPreflight: false,
  preflightCommitment: 'confirmed',
  encoding: 'base64'
}).send();
```

### Stage 4: Validation (Validator)

The validator checks:
- All required signatures are present
- The blockhash is recent (not expired)
- No duplicate signatures
- Account limits respected (max accounts per transaction)
- Compute budget not exceeded

### Stage 5: Execution (Runtime)

1. Accounts are loaded into memory
2. Instructions execute in order
3. If any instruction fails, the entire transaction rolls back
4. Rent checks are performed
5. Account balances are updated atomically

### Stage 6: Block Inclusion

The transaction is included in a block proposed by the current leader.

### Stage 7: Confirmation

The transaction propagates through the network. Confirmation level determines how confident you can be.

## Atomicity

**All-or-nothing execution**: If any instruction in a transaction fails, ALL changes are rolled back. This includes:
- Data changes
- Lamport transfers
- Account creation

### What Gets Rolled Back

```rust
// If this fails at instruction 2:
//   Instruction 1: Create account (allocates space, transfers rent)
//   Instruction 2: Write data (fails: account too small)
//
// Result: Account creation is rolled back. No rent charged. No data written.
```

### Exception: Compute Units

Compute units consumed during execution are NOT refunded on failure. The transaction fee is charged regardless of success/failure.

## Composability and CPI

Cross-Program Invocation (CPI) allows programs to call other programs within a single transaction.

```
Transaction
└── Instruction 1 (My Program)
    └── CPI → Token Program (transfer)
        └── CPI → System Program (if needed)
```

### CPI Depth Limit

Solana enforces a maximum CPI depth of 4 (configurable, historically). Deep CPI chains must be carefully designed.

### CPI Signers

When a program invokes another program via CPI and needs its PDA to sign:

```rust
let signer_seeds = &[
    b"vault".as_ref(),
    mint.key().as_ref(),
    &[vault_bump],
];

let cpi_ctx = CpiContext::new_with_signer(
    token_program.to_account_info(),
    cpi_accounts,
    &[signer_seeds],
);
```

## Confirmation Levels

| Level | What It Means | Speed | Safety |
|-------|---------------|-------|--------|
| `processed` | Transaction landed in a block, voted on by 1+ validators | ~400ms | Can still be rolled back |
| `confirmed` | Voted on by supermajority (66%+) of stake | ~1-2s | Very unlikely to roll back |
| `finalized` | Built on top of by many blocks; cannot be rolled back | ~6-12s | Immutable |

### When to Use Each

```typescript
// Fast UI feedback (e.g., "Transaction sent!")
await rpc.confirmTransaction(signature, 'processed');

// Most dApp operations
await rpc.confirmTransaction(signature, 'confirmed');

// High-value transfers or critical state changes
await rpc.confirmTransaction(signature, 'finalized');
```

### Checking Status

```typescript
const status = await rpc.getSignatureStatuses([signature]).send();
const txStatus = status.value[0];
// txStatus.confirmationStatus === 'confirmed' | 'finalized' | 'processed'
```

## Transaction Fees

### Base Fee

Every transaction pays a base fee regardless of success:

```
base_fee = signatures_count * lamports_per_signature
```

Currently: 5000 lamports per signature.

### Priority Fee

For faster inclusion during congestion, add a priority fee:

```typescript
const computeBudgetIx = ComputeBudgetProgram.setComputeUnitPrice({
  microLamports: 1000 // Priority fee per compute unit
});

const tx = new Transaction().add(computeBudgetIx, mainIx);
```

### Compute Units

Each transaction consumes compute units during execution:
- Default limit: 200,000 compute units per transaction
- Max limit: 1,400,000 compute units (request with `setComputeUnitLimit`)

```typescript
const computeLimitIx = ComputeBudgetProgram.setComputeUnitLimit({
  units: 400_000
});
```

## Blockhash and Expiry

Transactions must reference a recent blockhash for replay protection. If the blockhash expires (~60-90 seconds), the transaction fails.

### Handling Expiry

```typescript
// Fetch fresh blockhash before signing
const { blockhash, lastValidBlockHeight } = await rpc.getLatestBlockhash().send();

// Set on transaction
tx.recentBlockhash = blockhash;

// Submit and confirm before expiry
const signature = await sendAndConfirm(rpc, tx, [signer], {
  commitment: 'confirmed',
  // Retry until this block height
  blockhash,
  lastValidBlockHeight
});
```

## Transaction Versions

### Legacy Transactions

The original transaction format. No address lookup tables.

- **Max accounts**: ~35 (due to 1232-byte transaction size limit)
- **Use case**: Simple transactions with few accounts

### Version 0 (v0) Transactions

Introduced Address Lookup Tables (ALTs), allowing more accounts per transaction.

- **Max accounts**: 256 (with full ALT)
- **Smaller size**: Account addresses referenced by index in ALT, not full pubkey
- **Use case**: Complex transactions, DeFi composability

```typescript
// Create v0 transaction
const messageV0 = new MessageV0.compile({
  payerKey: user,
  instructions: [ix1, ix2],
  addressLookupTables: [altKey],
  recentBlockhash
});

const txV0 = new VersionedTransaction(messageV0);
txV0.sign([signer]);
```

### Version 1 (v1) — Coming

Next-generation transaction format. Expected improvements:
- Enhanced features beyond v0
- Better composability
- Specifics pending Agave release

### Choosing a Version

| Scenario | Version |
|----------|---------|
| Simple transfer | Legacy |
| Single program call | Legacy |
| Multi-program with many accounts | v0 (with ALT) |
| DeFi composability (5+ accounts) | v0 |
| Future-proofing | Monitor v1 release notes |

## Address Lookup Tables (ALTs)

ALTs store account addresses on-chain, referenced by index in transactions.

```typescript
// Create an ALT
const createAltIx = AddressLookupTableProgram.createLookupTable({
  authority: user,
  payer: user,
  recentSlot: await rpc.getSlot().send()
});

// Extend with addresses
const extendIx = AddressLookupTableProgram.extendLookupTable({
  lookupTable: altAddress,
  authority: user,
  payer: user,
  newAddresses: [addr1, addr2, addr3]
});
```

## Common Transaction Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `BlockhashNotFound` | Blockhash expired | Fetch fresh blockhash, re-sign |
| `InsufficientFundsForRent` | Account can't pay rent | Add more SOL to payer |
| `InstructionError` | Program logic rejected | Check error code, fix logic |
| `TransactionTooLarge` | Too many accounts/bytes | Use v0 + ALTs |
| `ComputationalBudgetExceeded` | Too many compute units used | Optimize logic or raise limit |

## Cross-Skill References

- `solana-anchor-programs` — Building transactions with Anchor's `invoke` and CPI
- `solana-client` — Constructing and sending transactions with @solana/kit
- `solana-architecture-patterns` — CPI patterns, multi-instruction transactions
- `solana-errors-and-compat` — Debugging transaction failures

## Verification Checklist

- [ ] All required accounts included in transaction (signers + writable + readonly)
- [ ] Blockhash is recent (fetched within last 60 seconds)
- [ ] Payer has sufficient lamports for fees + rent
- [ ] Confirmation level matches use case (processed/confirmed/finalized)
- [ ] Compute budget set appropriately for complex instructions
- [ ] Transaction version (Legacy/v0) chosen based on account count
- [ ] Priority fee added if network is congested
- [ ] CPI signer seeds correct for PDA signing
