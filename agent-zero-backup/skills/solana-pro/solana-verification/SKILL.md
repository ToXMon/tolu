---
name: solana-verification
description: Verify Solana deployments, transactions, accounts, IDLs, token state, and program behavior with Explorer, RPC, logs, and reproducible evidence.
version: 1.0.1
---

# Solana Verification

## When to Use

Use this skill when the task involves:

- proving a deployment or transaction happened on-chain
- checking program ID, upgrade authority, IDL, account state, token supply, or NFT metadata
- creating devnet/mainnet evidence for assignments or launches
- debugging Explorer logs and instruction details
- preparing handoff reports with verifiable links

Trigger phrases: `solana-verification`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- Solana Explorer now shows logs next to instructions, account info from account lists, mobile pages, selected-instruction sharing, and native program IDLs
- Legacy, v0, and v1 transaction versions matter when inspecting transaction responses

## Primary Workflow

1. Identify what must be proven: deployment, instruction, account state, token mint, NFT creation, authority transfer, or frontend connection
2. Collect signatures, program IDs, accounts, mints, cluster, slot, and Explorer URLs
3. Query with CLI/RPC and compare with Explorer
4. Inspect logs next to instructions and account info from updated Explorer pages
5. Save evidence in progress notes or release docs
6. Never mark milestones complete from terminal output alone

## Production Design Notes

Verification is a product habit. If someone else cannot click or query your proof, the work is not operationally complete.

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

- `references/explorer-workflows.md` — Explorer workflows
- `references/verification-checklist.md` — Verification checklist

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-deployment-devops` | Before and after deployment |
| `solana-rpc-data` | RPC queries or indexing proof |
| `solana-foundations` | Interpreting accounts and transactions |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

