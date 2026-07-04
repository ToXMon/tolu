---
name: solana-advanced
description: Advanced Solana engineering: Pinocchio, Token-2022, confidential transfers, compute budget, compression, crypto verification, and high-performance patterns.
version: 1.0.1
---

# Solana Advanced

## When to Use

Use this skill when the task involves:

- optimizing compute units, bytecode size, or account layout
- using Pinocchio or native programs for high performance
- building Token-2022 extension-heavy or confidential flows
- working with account compression, compressed NFTs, or ZK primitives
- adding secp256k1 verification or cryptographic helpers
- debugging sbpf-level behavior

Trigger phrases: `solana-advanced`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- Token-2022 Confidential Balances are back in ecosystem focus
- secp256k1-verify Rust crate provides reusable verification helpers
- sbpf CFG and graph engines enable deeper bytecode analysis
- Agave and Alpenglow updates may affect runtime assumptions over time

## Primary Workflow

1. Confirm the problem requires advanced patterns; prefer Anchor and standard SPL when sufficient
2. Measure baseline CU, account sizes, transaction sizes, latency, and failure rate
3. Choose the advanced tool: Pinocchio, Token-2022, compression, compute budget, or ZK
4. Prototype on local/devnet with tight logs and regression tests
5. Review with solana-security before production
6. Document migration, fallback, and user-facing limitations

## Production Design Notes

Advanced features should earn their complexity. If a standard Anchor + SPL flow works, use it. Move to Pinocchio, compression, or ZK only for measured needs.

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

- `references/pinocchio-and-performance.md` — Pinocchio and performance
- `references/token-2022-advanced.md` — Advanced Token-2022 extensions
- `references/compression-and-crypto.md` — Compression and crypto

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-native-programs` | Raw Rust or Pinocchio implementation |
| `solana-tokens-spl` | Token-2022 extension recipes |
| `solana-zk-confidential` | Confidential balances and ZK proofs |
| `solana-security` | Advanced feature audit |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

