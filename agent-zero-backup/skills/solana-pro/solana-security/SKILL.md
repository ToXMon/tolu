---
name: solana-security
description: Audit and harden Solana programs against PDA, CPI, signer, owner, lifecycle, oracle, Token-2022, and upgrade risks.
version: 1.0.1
---

# Solana Security

## When to Use

Use this skill when the task involves:

- reviewing Anchor or native programs for vulnerabilities
- hardening account validation, CPI boundaries, sysvars, token transfers, and admin paths
- preparing for audit or STRIDE-style review
- writing exploit regression tests
- assessing upgrade authority, multisig, oracle, and custody risks

Trigger phrases: `solana-security`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- Asymmetric Research STRIDE findings reinforce structured security review
- sbpf CFG analysis can inspect program bytecode and reachability
- ZK ElGamal Proof bugs show cryptographic assumptions need specialist review
- secp256k1-verify crate decouples verification helpers

## Primary Workflow

1. Inventory assets, authorities, external programs, token mints, upgrade keys, oracle dependencies, and user-controlled accounts
2. Validate accounts before business logic: owner, signer, writable, executable, PDA seeds, bumps, mint, token program, ATA, and sysvars
3. Review CPI boundaries: expected program IDs, account effects, PDA signer seeds, and arbitrary CPI risk
4. Review lifecycle: init, mutate, close, re-init, replay, double-spend, stale state, and rent reclaim
5. Turn each finding into a regression test
6. For production, require multisig upgrade authority, monitoring, incident runbook, and audit trail

## Production Design Notes

Security review must prove negative cases. Comments are not controls. If a constraint protects funds, there should be a test showing the exploit fails.

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

- `references/vulnerability-checklist.md` — Solana vulnerability checklist
- `references/audit-workflow.md` — Audit workflow
- `references/cpi-pda-security.md` — CPI and PDA security

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-testing` | Convert findings into regression tests |
| `solana-anchor-programs` | Fix Anchor constraints and account validation |
| `solana-native-programs` | Manual validation in raw programs |
| `solana-zk-confidential` | Confidential balance or ZK-specific risks |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

