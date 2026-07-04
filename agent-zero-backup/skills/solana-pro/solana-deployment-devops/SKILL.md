---
name: solana-deployment-devops
description: Deploy, upgrade, host, monitor, and operate Solana programs and dApps across devnet, testnet, and mainnet with CI/CD and multisig safety.
version: 1.0.1
---

# Solana Deployment and DevOps

## When to Use

Use this skill when the task involves:

- deploying Anchor or native programs
- managing program IDs, upgrade authorities, IDLs, and cluster configs
- preparing mainnet launch checklists
- setting up CI/CD for programs and frontends
- hosting dApps on Cloudflare, Vercel, Akash, or similar platforms
- moving authority to Squads multisig

Trigger phrases: `solana-deployment-devops`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- Cloudflare and Akash are viable hosting options for Solana dApps
- Alpenglow rollout and Agave versions reinforce pinned runtime/toolchain assumptions
- Upgrade authority is a high-risk production asset

## Primary Workflow

1. Build and test locally before deploy
2. Deploy to devnet with pinned program ID and recorded keypair path
3. Verify program, IDL, accounts, and smoke transactions on Explorer/RPC
4. For mainnet, require human gate, audit status, rent/funding plan, monitoring, rollback, and upgrade authority plan
5. Transfer upgrade authority to Squads or multisig where risk justifies it
6. Deploy frontend with environment-separated RPC URLs, program IDs, feature flags, and observability

## Production Design Notes

Deployment is not done when the CLI prints success. Done means verified program, verified IDL, smoke transaction, monitoring, and rollback path.

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

- `references/devnet-workflow.md` — Devnet workflow
- `references/mainnet-deployment.md` — Mainnet deployment
- `references/squads-multisig.md` — Squads multisig

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-verification` | Post-deploy proof |
| `solana-environment-setup` | Toolchain and cluster config |
| `solana-frontend` | dApp hosting and env vars |
| `solana-security` | Production launch gates |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

