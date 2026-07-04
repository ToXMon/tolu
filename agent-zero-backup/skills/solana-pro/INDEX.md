# Solana Pro Skills Suite

A general-purpose Solana skill suite for building production-grade applications from scratch. It is not tied to SignalForge. It combines bootcamp references, existing Solana skills, repo analysis, and current Solana Changelog context.

## Quick Start

| Developer goal | Start here | Then use |
|---|---|---|
| New to Solana | `solana-foundations` | `solana-environment-setup`, `solana-anchor-programs` |
| Build an Anchor program | `solana-anchor-programs` | `solana-testing`, `solana-security`, `solana-verification` |
| Build without Anchor | `solana-native-programs` | `solana-security`, `solana-testing`, `solana-advanced` |
| Build a dApp frontend | `solana-client` | `solana-frontend`, `solana-rpc-data`, `solana-deployment-devops` |
| Build tokens/NFTs | `solana-tokens-spl` | `solana-nft-metaplex`, `solana-zk-confidential` |
| Build DeFi | `solana-defi-patterns` | `solana-ecosystem-integration`, `solana-security` |
| Ship to production | `solana-deployment-devops` | `solana-verification`, `solana-security` |

## 8-Layer Architecture

| Layer | Skills |
|---|---|
| 1. Foundations | `solana-foundations`, `solana-environment-setup` |
| 2. Program Development | `solana-anchor-programs`, `solana-native-programs`, `solana-errors-and-compat` |
| 3. Client and Frontend | `solana-client`, `solana-frontend` |
| 4. Testing and Security | `solana-testing`, `solana-security` |
| 5. Advanced Topics | `solana-advanced` |
| 6. Domain Patterns | `solana-tokens-spl`, `solana-defi-patterns`, `solana-nft-metaplex` |
| 7. Infrastructure and Operations | `solana-rpc-data`, `solana-deployment-devops`, `solana-verification` |
| 8. Architecture and Ecosystem | `solana-architecture-patterns`, `solana-ecosystem-integration`, `solana-zk-confidential` |

## Skill Routing Matrix

| Task | Skill |
|---|---|
| Learn account model, PDAs, transactions | `solana-foundations` |
| Install Rust/Solana/Anchor/Node and configure devnet | `solana-environment-setup` |
| Write Anchor programs | `solana-anchor-programs` |
| Write native Rust/BPF or Pinocchio programs | `solana-native-programs` |
| Debug versions, GLIBC, build/deploy errors | `solana-errors-and-compat` |
| Build Kit clients and transaction flows | `solana-client` |
| Build wallet-connected UIs | `solana-frontend` |
| Test programs with LiteSVM/Mollusk/Anchor | `solana-testing` |
| Audit or harden programs | `solana-security` |
| Use high-performance, compression, crypto, advanced Token-2022 | `solana-advanced` |
| Create SPL/Token-2022 tokens | `solana-tokens-spl` |
| Build escrow, AMM, lending, oracle, Jupiter flows | `solana-defi-patterns` |
| Build NFTs, Metaplex, Candy Machine, compressed NFTs | `solana-nft-metaplex` |
| Query RPC, streams, webhooks, indexers | `solana-rpc-data` |
| Deploy programs/frontends and manage upgrades | `solana-deployment-devops` |
| Prove on-chain work with Explorer/RPC | `solana-verification` |
| Design system architecture and account models | `solana-architecture-patterns` |
| Integrate Jupiter/Pyth/Helius/Squads/Jito | `solana-ecosystem-integration` |
| Build confidential/ZK token flows | `solana-zk-confidential` |

## Shared Rules

- Use Solana MCP docs: `https://mcp.solana.com/mcp`.
- Prefix Solana/Anchor CLI commands with `NO_DNA=1`.
- Default to devnet unless explicitly told otherwise.
- Verify deployments and transactions on Explorer.
- Pin versions and record cluster/program IDs.
- Treat mainnet, upgrade authority, custody, and secrets as human-gated operations.

## Modern Context Integrated

- Agave v4.1.0
- Anchor v1.1.2
- Solana Kit v7.0.0
- @solana/react decoupled from Kit
- @solana/transaction-introspection
- Token-2022 Confidential Balances
- Alpenglow Votor in v4.3
- RPC 2.0 coverage additions
- Superbank gRPC streaming
- secp256k1-verify crate
- ATA `get_associated_token_address_with_program_id`
- Legacy, v0, and v1 transaction versions
- sbpf CFG analysis tooling
- Mollusk v0.13.4

## Files

Each skill lives at `/a0/usr/skills/solana-pro/<skill-name>/SKILL.md` with deeper guides in `references/`.
