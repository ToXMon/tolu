---
name: solana-rpc-data
description: Use Solana RPC, RPC 2.0, subscriptions, gRPC streams, DAS APIs, webhooks, and indexing patterns for production data access.
version: 1.0.1
---

# Solana RPC and Data

## When to Use

Use this skill when the task involves:

- querying transactions, accounts, tokens, NFTs, validators, or program events
- choosing RPC providers or indexing architecture
- building subscriptions, webhooks, gRPC streams, or data backends
- handling commitment levels, pagination, rate limits, and transaction versions
- debugging getTransaction, getProgramAccounts, or token supply issues

Trigger phrases: `solana-rpc-data`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- Cloudbreak adds getTokenSupply, getVoteAccounts, and getTokenLargestAccounts coverage
- Superbank is adding gRPC streaming and getEpochInfo support
- getTransaction responses must surface Legacy, v0, and v1 transaction versions
- Solana Go supports getTransactionsForAddress and sysvar parsing

## Primary Workflow

1. Define data need: real-time UX, historical indexing, asset metadata, validator state, token supply, or transaction inspection
2. Choose API: native RPC, WebSocket, Helius DAS/enhanced APIs, webhooks, or gRPC streaming
3. Set commitment/finality rules explicitly
4. Handle pagination, rate limits, null results, versioned transactions, and retries
5. Store indexed data idempotently using signature+slot or account+slot
6. Verify fund-relevant data with multiple calls or Explorer

## Production Design Notes

RPC is not a database. For historical or user-facing product data, design indexing, idempotency, retries, and backfills.

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

- `references/rpc-methods.md` — RPC methods
- `references/helius-das-api.md` — Helius DAS and enhanced APIs
- `references/indexing-patterns.md` — Indexing patterns

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-client` | Kit RPC client code |
| `solana-frontend` | UI subscriptions and query caching |
| `solana-verification` | Explorer/RPC proof workflows |
| `solana-ecosystem-integration` | Provider-specific APIs |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

