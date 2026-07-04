---
name: solana-nft-metaplex
description: Create production NFT systems with Metaplex Umi, Token Metadata, MPL Core, Candy Machine, compressed NFTs, collections, and metadata workflows.
version: 1.0.1
---

# Solana NFT and Metaplex

## When to Use

Use this skill when the task involves:

- minting NFTs, collections, badges, or compressed assets
- using Metaplex Umi, Token Metadata, Candy Machine, MPL Core, or Bubblegum
- managing metadata, creators, royalties, collection verification, and update authority
- building wallet-connected mint UIs
- debugging collection, metadata, tree, or owner verification

Trigger phrases: `solana-nft-metaplex`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- MPL Core is increasingly used for simpler asset models
- Compressed NFTs remain the right choice for large collections or cost-sensitive mints

## Primary Workflow

1. Choose standard: Token Metadata, MPL Core, or Bubblegum compressed NFTs
2. Prepare metadata: name, symbol, URI, seller fee, creators, collection, and mutability
3. Configure mint, update, collection, candy machine, and guard authorities
4. Test minting on devnet and verify asset, metadata, collection, and owner
5. For drops, add guards, allowlists, mint limits, payment checks, and bot mitigation
6. Pin storage and document update/royalty policy

## Production Design Notes

NFT production work is mostly authority and metadata discipline. Decide who can update, verify, freeze, or mint before launching.

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

- `references/metaplex-umi.md` — Metaplex Umi
- `references/candy-machine.md` — Candy Machine
- `references/compressed-nfts.md` — Compressed NFTs

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-tokens-spl` | Mint and token account fundamentals |
| `solana-client` | Umi/Kit client flows |
| `solana-frontend` | Wallet mint UI |
| `solana-deployment-devops` | Launch hosting and monitoring |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

