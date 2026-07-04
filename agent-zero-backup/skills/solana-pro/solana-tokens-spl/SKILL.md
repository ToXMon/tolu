---
name: solana-tokens-spl
description: Build SPL Token and Token-2022 flows including mints, ATAs, extensions, metadata, transfer hooks, fees, and confidential balances.
version: 1.0.1
---

# Solana Tokens: SPL and Token-2022

## When to Use

Use this skill when the task involves:

- creating fungible tokens, mints, and token accounts
- using Token-2022 extensions
- deriving ATAs for SPL Token versus Token-2022
- managing mint, freeze, permanent delegate, transfer hook, and confidential authorities
- debugging token account, mint, authority, or program ID issues

Trigger phrases: `solana-tokens-spl`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- ATA SDK deprecates `get_associated_token_address` in favor of `get_associated_token_address_with_program_id`
- Token-2022 Confidential Balances are newly highlighted
- RPC 2.0 improves token supply and largest-account coverage

## Primary Workflow

1. Choose SPL Token or Token-2022 before initializing mint/account state
2. Select extensions before mint creation because many extensions cannot be added later
3. Derive ATAs with explicit token program ID using `get_associated_token_address_with_program_id`
4. Model all authorities and decide which should be revoked, retained, or moved to multisig
5. Test wrong mint, wrong owner, wrong token program, frozen account, insufficient funds, and extension-specific failures
6. Verify mint, token accounts, supply, metadata, and transfers on devnet

## Production Design Notes

The token program ID is part of ATA derivation. SPL Token and Token-2022 mints with the same wallet can have different associated token accounts.

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

- `references/spl-token-guide.md` — SPL Token guide
- `references/token-2022-extensions.md` — Token-2022 extensions
- `references/ata-program.md` — Associated Token Account program

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-client` | Kit-based token transactions |
| `solana-anchor-programs` | Token CPI inside programs |
| `solana-zk-confidential` | Confidential balances |
| `solana-nft-metaplex` | NFT and metadata flows |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

