---
name: solana-defi-patterns
description: Design and build Solana DeFi protocols: escrow, AMMs, oracles, lending, Jupiter integrations, flash loans, vaults, and composable CPI flows.
version: 1.0.1
---

# Solana DeFi Patterns

## When to Use

Use this skill when the task involves:

- building escrow, swap, lending, vault, prediction-market, yield, or oracle-dependent programs
- integrating Jupiter, Pyth, Switchboard, DFlow, or liquidity protocols
- designing CPI-heavy DeFi architecture
- reviewing token-flow safety and economic invariants
- testing liquidation, slippage, oracle, and replay conditions

Trigger phrases: `solana-defi-patterns`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- DFlow and Phantom CASH show deeper institutional DeFi integration
- World prediction-market analysis highlights program/API/on-chain composition
- Jupiter ecosystem skills cover swap and product endpoints; check official docs

## Primary Workflow

1. Map token movement before code: source, vault, authority PDA, destination, fees, and close path
2. Define economic invariants: conservation, slippage, oracle freshness, collateralization, fee math, and liquidation rules
3. Use PDA-owned vaults for protocol custody
4. Verify external program IDs, oracle accounts, mint identities, and pool authorities
5. Test wrong mint, stale oracle, bad price, double take, cancel after take, unauthorized authority, and slippage exceeded
6. Monitor TVL, failed transaction rate, oracle staleness, and admin actions

## Production Design Notes

DeFi correctness is economic as much as technical. A transaction can pass constraints and still violate a protocol invariant.

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

- `references/escrow-and-cpi.md` — Escrow and CPI
- `references/amm-patterns.md` — AMM patterns
- `references/oracle-integration.md` — Oracle integration

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-architecture-patterns` | Protocol/account design |
| `solana-ecosystem-integration` | Jupiter/Pyth/Helius/Squads details |
| `solana-security` | Economic and CPI audit |
| `solana-testing` | Invariant and failure tests |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

