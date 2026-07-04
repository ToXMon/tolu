---
name: solana-ecosystem-integration
description: Integrate major Solana ecosystem services: Jupiter, Pyth, Switchboard, Helius, Squads, Jito, DFlow, Phantom, wallets, and protocol SDKs.
version: 1.0.1
---

# Solana Ecosystem Integration

## When to Use

Use this skill when the task involves:

- adding swaps, prices, webhooks, multisig, MEV protection, or wallet features
- choosing Solana infrastructure providers and protocol SDKs
- integrating Jupiter, Pyth, Switchboard, Helius, Squads, Jito, DFlow, Phantom, or wallet standards
- building cross-program or composable workflows
- evaluating dependency and provider risk

Trigger phrases: `solana-ecosystem-integration`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- @solana/react and Kit separation enables more frontend framework options
- DFlow and Phantom CASH show richer wallet/DeFi integrations
- Jupiter, Helius, Squads, and Jito remain common production dependencies

## Primary Workflow

1. Identify integration boundary: client API, on-chain CPI, backend webhook, indexer, or wallet flow
2. Check official docs and pin package/API versions
3. Model trust assumptions: oracle freshness, provider uptime, route slippage, admin keys, rate limits, custody, and fallback
4. Build devnet or sandbox proof first
5. Add tests/mocks for provider failure, stale data, rejected wallet signatures, API limits, and bad routes/prices
6. Document monitoring and fallback for production

## Production Design Notes

Ecosystem integrations trade speed for dependency risk. Every provider or protocol call needs versioning, failure behavior, and monitoring.

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

- `references/jupiter-integration.md` — Jupiter integration
- `references/pyth-switchboard.md` — Pyth and Switchboard
- `references/helius-squads-jito.md` — Helius, Squads, and Jito

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-defi-patterns` | DeFi protocol design |
| `solana-rpc-data` | RPC/indexing providers |
| `solana-deployment-devops` | Squads and ops |
| `solana-client` | SDK integration code |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

