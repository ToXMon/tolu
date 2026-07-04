---
name: solana-architecture-patterns
description: Design production Solana systems: account models, PDA namespaces, state machines, multi-program composition, upgrades, migrations, and compute-aware architecture.
version: 1.0.1
---

# Solana Architecture Patterns

## When to Use

Use this skill when the task involves:

- designing a Solana app from scratch
- choosing accounts, PDAs, instructions, events, clients, and indexers
- splitting a system into one or more programs
- planning upgrades, migrations, and authority models
- optimizing account size, compute, contention, and transaction composition

Trigger phrases: `solana-architecture-patterns`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- Alpenglow changes consensus behavior over time but does not remove account/PDA discipline
- Transaction versions v0/v1 affect address lookup, client construction, and complex transaction architecture

## Primary Workflow

1. Start with domain entities and invariants, then decide what must be on-chain
2. Define account types, ownership, sizing, rent, PDA seeds, and lifecycle transitions
3. Define instructions as state transitions with explicit preconditions and postconditions
4. Decide off-chain components: client, indexer, backend, queue, webhook, cache, frontend
5. Design upgrade and migration path before mainnet
6. Review security, compute, data availability, indexing, UX, failure recovery, and cost

## Production Design Notes

Good Solana architecture minimizes hot writable accounts, keeps state explicit, and accepts that every byte of account data and every writable lock has a cost.

## Common Failure Modes

| Failure | Likely Cause | Fix |
|---|---|---|
| PDA mismatch | Client and program seeds differ | Centralize seed definitions, test derived address, store canonical bump where useful |
| Owner mismatch | Wrong program owns account | Check `owner`, token program ID, and system/SPL/Token-2022 boundaries |
| Missing signer | Authority omitted or PDA signer seeds wrong | Recheck account metas and signer seeds |
| Simulation failed | Bad account order, stale blockhash, compute cap, constraint error | Inspect logs, simulate locally, narrow the failing instruction |
| Devnet differs from local | Toolchain/RPC/cluster mismatch | Pin versions, verify cluster config, reproduce on devnet |
| Mainnet launch risk | Upgrade/admin/oracle/custody path not controlled | Use multisig, runbook, monitoring, and human gate |


## Reference Files

- `references/account-strategies.md` — Account strategies
- `references/pda-design-patterns.md` — PDA design patterns
- `references/upgrade-patterns.md` — Upgrade patterns

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-foundations` | Account/PDA/transaction mental models |
| `solana-anchor-programs` | Anchor implementation |
| `solana-defi-patterns` | DeFi-specific architecture |
| `solana-deployment-devops` | Operational architecture |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

