---
name: solana-zk-confidential
description: Build and review Solana ZK and privacy features including ZK ElGamal Proofs, Token-2022 confidential balances/transfers, and compression privacy tradeoffs.
version: 1.0.1
---

# Solana ZK and Confidential

## When to Use

Use this skill when the task involves:

- using confidential balances or confidential transfers
- reviewing ZK ElGamal Proof program usage
- designing private payment or token flows
- integrating Token-2022 confidential extensions
- assessing cryptographic bug risk or proof verification assumptions
- exploring Light Protocol or ZK compression patterns

Trigger phrases: `solana-zk-confidential`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

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
- zksecurity reported a bug in Solana ZK ElGamal Proof program, reinforcing audit-first discipline
- secp256k1-verify crate reflects decoupled crypto helper patterns

## Primary Workflow

1. Treat cryptography as high-risk: check official docs, advisories, and audited examples
2. Define privacy goal: hidden balances, hidden transfer amounts, selective disclosure, compression, or proof verification
3. Choose Token-2022 confidential extensions only when UX, compliance, and audit complexity are justified
4. Model key management: auditor keys, decryptable balances, proof generation, and recovery
5. Test proof generation, verification, failed proofs, invalid authority, and extension layout
6. Require security review before mainnet

## Production Design Notes

Confidential systems fail at the seams: keys, proofs, account extension layout, client generation, and recovery. Design those seams first.

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

- `references/zk-elgamal-proof.md` — ZK ElGamal Proof
- `references/confidential-balances.md` — Confidential balances
- `references/token-2022-confidential.md` — Token-2022 confidential integration

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-tokens-spl` | Token-2022 extension setup |
| `solana-advanced` | Advanced cryptographic patterns |
| `solana-security` | Audit and bug-risk review |
| `solana-client` | Proof-generation client flows |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

