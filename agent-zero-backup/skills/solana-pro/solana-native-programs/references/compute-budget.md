# Compute Budget Reference

The Compute Budget program (`ComputeBudget111111111111111111111111111111`) controls transaction prioritization, compute unit allocation, and heap frame sizing on Solana.

## Core Concepts

### Compute Units (CU)

Every instruction consumes compute units. The default limit is 200,000 CU per instruction (1,400,000 per transaction). Exceeding the limit causes the transaction to fail.

### Fee Structure

```
Total fee = base fee + priority fee

base fee    = 5,000 lamports per signature
priority fee = CU consumed × price per CU (in micro-lamports)
```

Example: A transaction consuming 100,000 CU at 5,000 micro-lamports/CU:
```
base fee    = 5,000 lamports
priority fee = 100,000 × 5,000 / 1,000,000 = 500 lamports
total fee   = 5,500 lamports
```

---

## Compute Budget Instructions

### 1. SetComputeUnitLimit

Cap the compute units available for the transaction. Always set this based on simulation to avoid overpaying.

```rust
use solana_program::compute_budget::ComputeBudgetInstruction;

// Set limit to 50,000 CU
let ix = ComputeBudgetInstruction::set_compute_unit_limit(50_000);
```

**Best practice:** Simulate the transaction first, then set the limit to ~110% of simulated CU consumption.

### 2. SetComputeUnitPrice

Set the priority fee in micro-lamports per CU. Higher price = higher priority for validators.

```rust
// 5,000 micro-lamports per CU (= 0.005 lamports per CU)
let ix = ComputeBudgetInstruction::set_compute_unit_price(5_000);
```

**Conversion:**
- 1 micro-lamport = 0.000001 lamports
- 1,000,000 micro-lamports = 1 lamport
- Priority fee = CU_consumed × price / 1,000,000 (in lamports)

### 3. RequestHeapFrame

Increase the heap frame beyond the default 32KB. Useful for programs with large data structures.

```rust
// Request 256KB heap (must be multiple of 32KB)
let ix = ComputeBudgetInstruction::request_heap_frame(256 * 1024);
```

**When to use:**
- Large Vec allocations
- Complex deserialization requiring temporary buffers
- Programs processing large account data

**Cost:** Each heap frame increase costs additional CU.

---

## CU Estimation

### Method 1: Simulate and Read

```typescript
import { simulateTransaction } from '@solana/web3.js';

// Simulate the transaction
const simulation = await connection.simulateTransaction(transaction);
const unitsConsumed = simulation.value.unitsConsumed;

// Set limit to 110% of consumed
const limit = Math.ceil(unitsConsumed * 1.1);
```

### Method 2: Using Kit Helpers

```typescript
import { estimateComputeUnitLimitFactory } from '@solana/kit';

const estimateCU = estimateComputeUnitLimitFactory({ rpc });
const { units } = await estimateCU(transactionMessage);
```

### Method 3: Auto-Update Pattern

```typescript
import { estimateAndUpdateProvisoryComputeUnitLimitFactory } from '@solana/kit';

// Automatically estimates and adds SetComputeUnitLimit instruction
const updatedTx = await estimateAndUpdateProvisoryComputeUnitLimitFactory({
  rpc,
  sender,
})(transactionMessage);
```

**Important:** Always refresh the blockhash after simulation, as simulation consumes the blockhash window.

---

## Priority Fee Estimation

### Priority Fee APIs

| Provider | API | Use Case |
|----------|-----|----------|
| [Helius](https://docs.helius.dev/solana-apis/priority-fee-api) | `getPriorityFeeEstimate` | Recommended — percentile-based estimates |
| [QuickNode](https://marketplace.quicknode.com/add-on/solana-priority-fee) | Priority Fee API | Alternative |
| [Triton](https://docs.triton.one/chains/solana/improved-priority-fees-api) | Improved Priority Fees | Validator-side data |

### Helius Example

```typescript
const response = await fetch('https://mainnet.helius-rpc.com/?api-key=YOUR_KEY', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: '1',
    method: 'getPriorityFeeEstimate',
    params: [{
      transaction: serializedTransaction,
      options: { priority_level: 'high' }
    }]
  })
});

const { result } = await response.json();
const priorityFee = result.priorityFeeEstimate; // in micro-lamports
```

### Fee Strategy Guidelines

| Transaction Type | Priority Level | Strategy |
|-----------------|---------------|----------|
| Non-time-sensitive | None | 0 micro-lamports — let it land eventually |
| Normal | Medium | 50th percentile of recent fees |
| Time-sensitive | High | 75th-90th percentile |
| Arbitrage/MEV | Max | 95th+ percentile or fixed high value |

---

## Fee Market Dynamics

### How Validators Prioritize

Validators select transactions for blocks based on:
1. **Priority fee per CU** — higher micro-lamports/CU = more likely included
2. **Transaction size** — smaller transactions are more efficient to include
3. **Account contention** — transactions touching hot accounts may be delayed

### Priority Fee vs. Compute Unit Price

These terms are often confused:

- **Priority fee** = total extra fee paid (lamports)
- **Compute unit price** = rate (micro-lamports per CU)

```
priority_fee = compute_unit_price × CU_consumed / 1,000,000
```

### Overpaying Problem

Setting a high CU limit but consuming few CU means:
- You pay priority fee based on **consumed CU**, not the limit
- But validators see the **requested limit** when prioritizing
- Setting an accurate, tight CU limit improves inclusion probability

---

## Optimization Strategies

### 1. Reduce CU Consumption

| Technique | CU Savings |
|-----------|------------|
| Use Pinocchio instead of solana-program | 60-80% |
| Zero-copy account access (no borsh) | 20-40% |
| Batch CPI calls | ~1,000 CU per batched op |
| Remove unnecessary logging | 100 CU per byte of log |
| Use `checked_*` arithmetic | Avoids overflow handling overhead |
| Minimize account iterations | 100 CU per `iter()` call |
| Pre-compute PDA bumps (don't search at runtime) | ~1,500 CU per PDA |

### 2. Use `sol_log_compute_units` for Profiling

```rust
use solana_program::log::sol_log_compute_units;

pub fn process_instruction(...) -> ProgramResult {
    sol_log_compute_units(); // Baseline
    
    let accounts = parse_accounts(accounts)?;
    sol_log_compute_units(); // After parsing
    
    let data = CounterData::from_bytes(&accounts[0].data.borrow())?;
    sol_log_compute_units(); // After deserialization
    
    data.count += 1;
    sol_log_compute_units(); // After business logic
    
    data.save(&accounts[0])?;
    sol_log_compute_units(); // After serialization
    
    Ok(())
}
```

### 3. Optimize Instruction Data

- Use 1-byte discriminators (not 8-byte like Anchor)
- Pack data tightly — no padding
- Use `u8` instead of `u64` when values fit
- Pass data in instruction rather than accounts where possible

### 4. Heap Frame Management

Default heap: 32KB. If your program needs more:

```rust
// Request only what you need (multiples of 32KB)
ComputeBudgetInstruction::request_heap_frame(64 * 1024); // 64KB
```

**Avoid** requesting large heap frames unnecessarily — each KB costs CU.

---

## Program-Level CU Costs (Reference)

| Operation | Typical CU |
|-----------|-----------|
| `msg!()` (per call) | 100 + 100/byte |
| `Pubkey::find_program_address` | ~1,500 |
| `invoke` (CPI base) | 1,000 |
| `invoke` (per account) | 500 |
| `invoke_signed` (per signer) | 700 |
| `borsh::to_writer` | ~50/byte |
| `BorshDeserialize::try_from_slice` | ~50/byte |
| Zero-copy struct cast | ~10 |
| `u64` checked_add | ~5 |
| `Vec::push` | ~100 + alloc |
| Account data borrow | ~50 |
| Sysvar read (Clock::get) | ~100 |

---

## Common Mistakes

### 1. Not Setting CU Limit

If you don't set `SetComputeUnitLimit`, the transaction defaults to 200,000 CU per instruction. This means:
- Validators see a high requested limit
- You may be deprioritized compared to transactions with tight limits
- You still only pay for consumed CU, but inclusion probability drops

### 2. Setting CU Price Without CU Limit

Setting only `SetComputeUnitPrice` without `SetComputeUnitLimit` means:
- Priority fee = consumed CU × price (you pay for what you use — OK)
- But validators see the default 200K limit, reducing inclusion probability

**Always set both.**

### 3. Overpaying Priority Fees

For non-time-sensitive transactions:
- 0 micro-lamports is fine — transaction will land eventually
- Only use priority fees when latency matters

### 4. Not Refreshing Blockhash

After simulating a transaction to estimate CU, the blockhash may expire. Always:
1. Simulate → get CU consumption
2. Add `SetComputeUnitLimit` instruction
3. Get a fresh blockhash
4. Re-sign the transaction

---

## Client-Side Integration (TypeScript)

### Full Pattern: Estimate + Set CU + Priority Fee

```typescript
import {
  ComputeBudgetProgram,
  Connection,
  Transaction,
  TransactionInstruction,
  PublicKey,
} from '@solana/web3.js';

async function buildOptimizedTransaction(
  connection: Connection,
  payer: PublicKey,
  instructions: TransactionInstruction[],
  priorityLevel: 'none' | 'medium' | 'high' = 'medium',
): Promise<Transaction> {
  // 1. Add a placeholder CU limit for simulation
  const simInstructions = [
    ComputeBudgetProgram.setComputeUnitLimit({ units: 1_400_000 }),
    ...instructions,
  ];

  // 2. Get latest blockhash for simulation
  const { blockhash } = await connection.getLatestBlockhash();

  // 3. Simulate to get CU consumption
  const simulation = await connection.simulateTransaction(
    new Transaction({
      feePayer: payer,
      blockhash,
      instructions: simInstructions,
    }),
  );

  if (simulation.value.err) {
    throw new Error(`Simulation failed: ${simulation.value.err}`);
  }

  const unitsConsumed = simulation.value.unitsConsumed || 50_000;
  const cuLimit = Math.ceil(unitsConsumed * 1.1); // 110% buffer

  // 4. Get priority fee estimate
  let priorityFee = 0;
  if (priorityLevel !== 'none') {
    // Use Helius/Triton/QuickNode API here
    priorityFee = await estimatePriorityFee(priorityLevel);
  }

  // 5. Build final transaction with CU limit and priority fee
  const finalInstructions = [
    ComputeBudgetProgram.setComputeUnitLimit({ units: cuLimit }),
    ComputeBudgetProgram.setComputeUnitPrice({ microLamports: priorityFee }),
    ...instructions,
  ];

  // 6. Get fresh blockhash (simulation consumed the old one)
  const { blockhash: freshBlockhash, lastValidBlockHeight } =
    await connection.getLatestBlockhash();

  const tx = new Transaction({
    feePayer: payer,
    blockhash: freshBlockhash,
    lastValidBlockHeight,
    instructions: finalInstructions,
  });

  return tx;
}
```

---

## Runtime CU Limits (Agave)

| Scope | Default CU Limit |
|-------|-----------------|
| Per instruction | 200,000 |
| Per transaction | 1,400,000 |
| Per CPI (nested) | 200,000 (shares parent budget) |
| Heap frame | 32 KB |

CPI calls share the parent transaction's CU budget. A CPI call does not get a fresh 200K — it draws from the parent's remaining CU.

---

## See Also

- [Compute Budget Documentation](https://solana.com/docs/programs/runtime#compute-budget)
- [Priority Fees Guide](https://solana.com/docs/fees-and-prioritization)
- [Helius Priority Fee API](https://docs.helius.dev/solana-apis/priority-fee-api)
- [Triton Priority Fees](https://docs.triton.one/chains/solana/improved-priority-fees-api)
- Load skill `solana-advanced` for advanced compute optimization patterns
- Load skill `solana-client` for TypeScript CU estimation helpers
