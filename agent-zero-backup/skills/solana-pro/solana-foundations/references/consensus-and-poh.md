# Consensus and Proof of History — Deep Reference

## Overview

Solana's consensus mechanism combines Proof of History (PoH) with Proof of Stake (PoS). PoH provides a cryptographic clock that orders transactions before consensus, enabling validators to process transactions in parallel. The next generation, Alpenglow, begins rollout with the Votor component in Agave v4.3.

## Proof of History (PoH)

### What PoH Is

Proof of History is a verifiable delay function (VDF) that encodes the passage of time into a sequential hash chain. It is NOT a consensus algorithm itself — it's a clock that consensus builds on top of.

### How PoH Works

```
Block N-1
   │
   ▼
hash₁ = SHA256(hash₀ || data₁)
hash₂ = SHA256(hash₁ || data₂)
hash₃ = SHA256(hash₂ || data₃)
   ...
hashₙ = SHA256(hashₙ₋₁ || dataₙ)
   │
   ▼
Block N
```

Each hash incorporates the previous hash plus any transactions or events recorded at that step. The sequence is:

1. **Deterministic**: Anyone can verify the hash chain is correct by re-computing
2. **Time-ordered**: The position in the chain encodes temporal ordering
3. **Tamper-evident**: Changing any entry invalidates all subsequent hashes

### Why PoH Matters

Without PoH, validators must coordinate timestamps through messaging — slow and complex. With PoH:

- **Parallel processing**: Validators know the ordering of transactions without communicating
- **Fast confirmation**: The cryptographic clock enables sub-second block times
- **Throughput**: Validators process transactions simultaneously, then vote on results
- **Reduced overhead**: No need for timestamp consensus messages

### PoH vs PoS

| Aspect | Proof of History | Proof of Stake |
|--------|-----------------|----------------|
| Purpose | Cryptographic clock | Consensus / security |
| What it proves | Time ordering of events | Economic stake in network |
| Standalone? | No — needs consensus layer | Can be standalone (other chains) |
| On Solana | Enables parallel processing | Secures the network |

## Stake Delegation

### Validators

Validators are nodes that:
1. Process transactions and produce blocks (when they're the leader)
2. Vote on the validity of blocks produced by other leaders
3. Earn rewards proportional to their stake

### Delegators

Token holders who don't run validator infrastructure can delegate their SOL to validators:

```
Delegator stakes SOL → Validator → Validator earns rewards → Rewards split with delegator
```

### Stake Mechanics

- **Voting weight**: Proportional to total stake (own + delegated)
- **Rewards**: Distributed based on stake amount and validator performance
- **Lock-up**: Staked SOL has a warm-up and cool-down period (epochs)
- **Slashing**: Validators can be penalized for malicious behavior (double-signing, etc.)

### Epochs

Solana operates in epochs (~2-3 days each). Stake changes (delegating, undelegating) take effect at epoch boundaries.

```bash
# Check current epoch
NO_DNA=1 solana epoch

# Check epoch info
NO_DNA=1 solana epoch-info
```

### Validator Selection

Delegators should consider:
- **Commission rate**: Percentage of rewards the validator keeps
- **Uptime**: Reliability of block production
- **Vote success rate**: How often the validator votes correctly
- **Delinquent streaks**: Periods of inactivity

## Consensus Flow

### Tower BFT

Solana uses Tower BFT — a PoS consensus algorithm optimized for PoH:

```
Leader produces block
   │
   ▼
Validators vote on block
   │
   ▼
Votes propagate through network
   │
   ▼
Supermajority (66%+) reached
   │
   ▼
Block confirmed
   │
   ▼
More blocks built on top
   │
   ▼
Block finalized (after enough confirmations)
```

### Leader Schedule

Leaders are selected based on stake weight using a Verifiable Delay Function (VDF). The schedule is deterministic — all nodes can compute who the leader is for any given slot.

### Forks and Rollbacks

If validators disagree, forks can occur. Solana handles this with:
- **Heaviest fork rule**: Validators vote on the fork with the most stake
- **Rollback**: Transactions on abandoned forks are reverted
- **Finality**: After enough confirmations, blocks become immutable

This is why `processed` confirmation can be rolled back but `finalized` cannot.

## Alpenglow — Next Generation Consensus

### Overview

Alpenglow is Solana's next-generation consensus protocol, designed to improve on Tower BFT's latency and finality characteristics.

### Rollout Plan

| Component | Status | Version |
|-----------|--------|---------|
| **Votor** | Upcoming | Agave v4.3 |
| **Alpenswitch** | On testnet | Current testnet |

### Votor

Votor is the voting component of Alpenglow. It replaces the current Tower BFT voting mechanism with a faster, more efficient protocol.

Key improvements expected:
- **Faster finality**: Reduced time from confirmation to finality
- **Lower latency**: Quicker block confirmation
- **Better network utilization**: More efficient vote propagation

### Alpenswitch

Alpenswitch is already running on testnet. It handles the network switching logic — how validators transition between consensus states and recover from network partitions.

### Why Alpenglow Matters for Developers

For most dApp developers, Alpenglow is transparent — transactions still work the same way. But:

- **Confirmation times may decrease**: Applications can confirm transactions faster
- **Finality may come quicker**: Less waiting for `finalized` commitment
- **Network resilience improves**: Better handling of partitions and recovery

Monitor the Agave v4.3 release notes for specific performance characteristics.

## Practical Implications for Developers

### Choosing Confirmation Levels

```typescript
// For most dApps: 'confirmed' is sufficient
// With Alpenglow, this may become even faster
const commitment = 'confirmed';

// For critical operations (e.g., large transfers)
const commitment = 'finalized';
```

### Handling Network Conditions

```typescript
// Retry logic for transaction submission
async function submitWithRetry(tx, rpc, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const signature = await rpc.sendTransaction(tx).send();
      const status = await rpc.confirmTransaction(signature, 'confirmed');
      if (status) return signature;
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}
```

### Monitoring Validator Health

```bash
# Check cluster health
NO_DNA=1 solana cluster-version

# List validators
NO_DNA=1 solana validators

# Check vote accounts
NO_DNA=1 solana vote-accounts
```

## Agave Validator Client

Agave is the current validator client for Solana (replacing the original Solana Labs client).

### Version Context

| Component | Version |
|-----------|---------|
| Agave | v4.1.0 (current) |
| Alpenglow Votor | Coming in v4.3 |
| Alpenswitch | On testnet |

### Why This Matters

- **Agave v4.x** is the production validator software running mainnet
- **v4.3** will introduce Alpenglow Votor — monitor release notes
- Skills and tools should reference Agave versions, not legacy "Solana" versions

## Cross-Skill References

- `solana-environment-setup` — Installing and configuring Solana CLI tools
- `solana-anchor-programs` — How consensus affects program execution
- `solana-architecture-patterns` — Designing for confirmation levels and finality
- `solana-client` — Setting commitment levels in RPC calls

## Verification Checklist

- [ ] PoH understood as cryptographic clock, not standalone consensus
- [ ] Stake delegation mechanics understood (epochs, rewards, lock-up)
- [ ] Confirmation levels chosen appropriately (processed/confirmed/finalized)
- [ ] Alpenglow Votor tracked for Agave v4.3 release
- [ ] Alpenswitch awareness for testnet testing
- [ ] Retry logic implemented for transaction submission
- [ ] Agave v4.1.0 as current validator client baseline
