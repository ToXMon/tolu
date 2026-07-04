# Solana Pro Skills Suite — Shared Build Context

## SKILL.md Standard
Every SKILL.md must follow this structure:

```markdown
---
name: solana-<skill-name>
description: <one-line description for skill search/matching>
version: 1.0.0
---

# <Skill Title>

## When to Use
- Trigger phrases and scenarios (bullet list)

## Core Operating Behaviors
- Safety guardrails
- Verification requirements

## <Domain Content Sections>
[Progressive disclosure: main skill covers workflow, references/ has deep material]

## Cross-Skill References
| Related Skill | When to Switch |
|--------------|----------------|

## Verification Checklist
- [ ] Verification items
```

## Mandatory Protocol References
ALL skills must include these in their content:

1. **NO_DNA=1 CLI Protocol**: All Solana CLI commands use `NO_DNA=1` prefix
   - Example: `NO_DNA=1 anchor build`, `NO_DNA=1 solana config set --url devnet`
   - This prevents DNA (Do Not Assume) errors in Solana CLI

2. **Solana MCP Server**: Reference `https://mcp.solana.com/mcp` for live docs
   - Skills should instruct: "Use MCP tools before falling back to training data"

3. **Devnet Default**: All work targets devnet unless explicitly stated
   - `NO_DNA=1 solana config set --url devnet`

4. **Explorer Verification**: Always verify on https://explorer.solana.com

## Modern Ecosystem Context (from Solana Changelog)
These version updates MUST be reflected in relevant skills:

| Update | Version | Skills Affected |
|--------|---------|---------------|
| Agave | v4.1.0 | foundations, native-programs, rpc-data |
| Anchor | v1.1.2 | anchor-programs, errors-and-compat |
| Solana Kit | v7.0.0 | client, frontend |
| @solana/react | Decoupled from Kit | frontend |
| @solana/transaction-introspection | NEW package | client |
| Token-2022 Confidential Balances | NEW | tokens-spl, advanced, zk-confidential |
| Alpenglow consensus | Votor in v4.3 | foundations, architecture-patterns |
| RPC 2.0 methods | getTokenSupply, getVoteAccounts, getTokenLargestAccounts | rpc-data |
| Superbank gRPC streaming | NEW | rpc-data |
| secp256k1-verify crate | NEW | native-programs, advanced |
| ATA deprecation | get_associated_token_address → get_associated_token_address_with_program_id | tokens-spl |
| Transaction versions | Legacy, v0, v1 | client, rpc-data, foundations |
| sbpf CFG analyses | NEW tooling | native-programs, security |
| Mollusk | v0.13.4 | testing |

## Source Material Paths

### Existing Skills (to enhance/reference)
- `/a0/usr/skills/solana-anchor-programs/SKILL.md` (471 lines)
- `/a0/usr/skills/solana-client/SKILL.md` (563 lines)
- `/a0/usr/skills/solana-errors-and-compat/SKILL.md` (906 lines)
- `/a0/usr/skills/solana-frontend/SKILL.md` (239 lines)
- `/a0/usr/skills/solana-security/SKILL.md` (712 lines)
- `/a0/usr/skills/solana-testing/SKILL.md` (589 lines)
- `/a0/usr/skills/solana-advanced/SKILL.md` (374 lines)

### SignalForge Skills (phase-based patterns)
- `/a0/usr/projects/solana_bootcamp/skills/signalforge-*/SKILL.md`

### Bootcamp Exercises (working code)
- `/a0/usr/projects/solana_bootcamp/exercises/hello-solana/`
- `/a0/usr/projects/solana_bootcamp/exercises/counter-pda/`
- `/a0/usr/projects/solana_bootcamp/exercises/first-token/`
- `/a0/usr/projects/solana_bootcamp/exercises/token-2022/`
- `/a0/usr/projects/solana_bootcamp/exercises/escrow-program/`
- `/a0/usr/projects/solana_bootcamp/exercises/defi-cli/`
- `/a0/usr/projects/solana_bootcamp/exercises/nft-collection/`
- `/a0/usr/projects/solana_bootcamp/exercises/full-dapp-flow/`

### Bootcamp Decks (extracted text)
- `/a0/usr/projects/solana_bootcamp/resources/extracted/deck-01-foundations.txt` (if exists)
- `/a0/usr/projects/solana_bootcamp/resources/extracted/deck-02-first-deployments.txt` (if exists)
- `/a0/usr/projects/solana_bootcamp/resources/extracted/deck-03-tokens.txt`
- `/a0/usr/projects/solana_bootcamp/resources/extracted/deck-04-programs-frontend.txt`
- `/a0/usr/projects/solana_bootcamp/resources/extracted/deck-05-escrow-defi-nfts.txt`

### Ecosystem Analysis
- `/a0/usr/projects/solana_bootcamp/resources/solana-skills-ecosystem-analysis.md`

### Repo Analysis (5 repos)
- `/a0/usr/projects/solana_bootcamp/resources/repo-analysis/crypto-primitives-examples/`
- `/a0/usr/projects/solana_bootcamp/resources/repo-analysis/solana-ai-kit/`
- `/a0/usr/projects/solana_bootcamp/resources/repo-analysis/SpecterAI/`
- `/a0/usr/projects/solana_bootcamp/resources/repo-analysis/megapredict/`
- `/a0/usr/projects/solana_bootcamp/resources/repo-analysis/solana-bootcamp-2026/`

### Solana Dev-Skill References
- `/a0/usr/projects/solana_bootcamp/resources/solana-dev-skill/skill/references/`

## Suite Architecture (8 Layers, 19 Skills)

| Layer | Skill | Status | Output Path |
|-------|-------|--------|------------|
| 1 Foundations | solana-foundations | NEW | /a0/usr/skills/solana-pro/solana-foundations/ |
| 1 Foundations | solana-environment-setup | NEW | .../solana-environment-setup/ |
| 2 Program Dev | solana-anchor-programs | ENHANCE | .../solana-anchor-programs/ |
| 2 Program Dev | solana-native-programs | NEW | .../solana-native-programs/ |
| 2 Program Dev | solana-errors-and-compat | ENHANCE | .../solana-errors-and-compat/ |
| 3 Client/Frontend | solana-client | ENHANCE | .../solana-client/ |
| 3 Client/Frontend | solana-frontend | ENHANCE | .../solana-frontend/ |
| 4 Testing/Security | solana-testing | ENHANCE | .../solana-testing/ |
| 4 Testing/Security | solana-security | ENHANCE | .../solana-security/ |
| 5 Advanced | solana-advanced | ENHANCE | .../solana-advanced/ |
| 6 Domain | solana-tokens-spl | NEW | .../solana-tokens-spl/ |
| 6 Domain | solana-defi-patterns | NEW | .../solana-defi-patterns/ |
| 6 Domain | solana-nft-metaplex | NEW | .../solana-nft-metaplex/ |
| 7 Infrastructure | solana-rpc-data | NEW | .../solana-rpc-data/ |
| 7 Infrastructure | solana-deployment-devops | NEW | .../solana-deployment-devops/ |
| 7 Infrastructure | solana-verification | NEW | .../solana-verification/ |
| 8 Architecture | solana-architecture-patterns | NEW | .../solana-architecture-patterns/ |
| 8 Architecture | solana-ecosystem-integration | NEW | .../solana-ecosystem-integration/ |
| 8 Architecture | solana-zk-confidential | NEW | .../solana-zk-confidential/ |

## Output Rules
- Each skill writes to: `/a0/usr/skills/solana-pro/<skill-name>/SKILL.md`
- Reference files write to: `/a0/usr/skills/solana-pro/<skill-name>/references/<file>.md`
- SKILL.md should be 200-500 lines (use references/ for deep material)
- Reference files should be 100-400 lines each
- Write production-grade content — this is for building ANY Solana app
