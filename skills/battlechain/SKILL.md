---
name: battlechain
description: >
  Work with BattleChain, the pre-mainnet L2 for battle-testing smart contracts with real funds.
  Covers deploying contracts via battlechain-lib, creating Safe Harbor agreements, whitehat
  attack workflows, contract lifecycle management, verification, and on-chain APIs.
  Trigger: battlechain, battle chain, safe harbor, whitehat, attack mode, pre-mainnet,
  smart contract deployment, bounty, cyfrin.
license: MIT
metadata:
  author: Cyfrin
  version: "1.0.0"
  source: https://github.com/Cyfrin/solskill
  argument-hint: <battlechain-task-description>
---

# BattleChain Development Standards

Instructions for working with [BattleChain](https://docs.battlechain.com/), from the [Cyfrin security team](https://www.cyfrin.io/).

## What is BattleChain

BattleChain is a ZKSync-based L2 blockchain that inserts a battle-testing phase between testnet and mainnet: **Dev → Testnet → BattleChain → Mainnet**. Protocols deploy audited contracts with real funds, whitehats legally attack them for bounties under Safe Harbor agreements, and surviving contracts promote to production.

## Full Documentation

For up-to-date contract addresses, function signatures, struct definitions, enums, state transitions, bounty calculation rules, Safe Harbor agreement details, and all other technical reference material, fetch the full docs:

**https://docs.battlechain.com/llms-full.txt**

Always fetch this URL when you need BattleChain technical details. The docs are the single source of truth and stay current as the protocol evolves.

---

## Deployment

Projects deploying to BattleChain (or any EVM chain) should use `cyfrin/battlechain-lib`:

```bash
forge install cyfrin/battlechain-lib
```

Add the remapping to `foundry.toml`:
```toml
remappings = ["battlechain-lib/=lib/battlechain-lib/src/"]
```

## Inheritance Hierarchy

| Contract | Use when you need |
|----------|-------------------|
| `BCScript` | Full lifecycle: deploy + agreement + attack mode |
| `BCDeploy` | Deploy only (via CreateX on any chain, BattleChainDeployer on BC) |
| `BCSafeHarbor` | Agreement creation only |

## Key Helpers

| Helper | What it does |
|--------|-------------|
| `bcDeployCreate(bytecode)` | Deploy via BattleChainDeployer on BC, CreateX on 190+ other chains |
| `bcDeployCreate2(salt, bytecode)` | Deterministic deploy — same address across chains |
| `bcDeployCreate3(salt, bytecode)` | Address depends only on salt, not bytecode |
| `defaultAgreementDetails(name, contacts, contracts, recovery)` | Builds agreement with correct scope and URI per chain |
| `createAndAdoptAgreement(details, owner, salt)` | Create + 14-day commitment + adopt in one call |
| `requestAttackMode(agreement)` | Enter attack mode (BattleChain only — reverts on other chains) |
| `_isBattleChain()` | Runtime check: `true` on chain IDs 626, 627, 624 |
| `getDeployedContracts()` | All addresses deployed this session via `bcDeploy*` |

## Cross-chain Behavior

| | BattleChain (626/627/624) | Other EVM chains (190+) |
|---|---|---|
| `bcDeployCreate*` | BattleChainDeployer (CreateX + AttackRegistry) | CreateX (`0xba5Ed...`) directly |
| `defaultAgreementDetails` | BattleChain scope + `BATTLECHAIN_SAFE_HARBOR_URI` | Current chain CAIP-2 scope + `SAFE_HARBOR_V3_URI` |
| `requestAttackMode` | Works | Reverts with `BCSafeHarbor__NotBattleChain` |
| `createAndAdoptAgreement` | Works | Works (requires registry/factory on that chain) |

Only `requestAttackMode` is BattleChain-specific. Everything else works on any supported chain.

---

## Foundry

When working with foundry scripts, you need to pass a flag to skip simulations:

```bash
forge script scripts/Deploy.s.sol --skip-simulation
```

Combine with `-g` if issues persist:

```bash
forge script scripts/Deploy.s.sol --skip-simulation -g 300
```

Add these flags to `justfile` or `makefile` targets.

## Verification

BattleChain uses a custom block explorer API. The `battlechain-lib` ships a reusable justfile module.

### Install verification targets

Add to your `justfile`:

```just
import "lib/battlechain-lib/battlechain.just"
```

| Target | Usage |
|--------|-------|
| `bc-verify <addr> <path:name>` | Verify a single contract |
| `bc-verify-broadcast <script>` | Verify all contracts from a broadcast file |
| `bc-deploy <script> <account> <sender>` | Deploy with standard BC flags |
| `bc-deploy-verify <script> <account> <sender>` | Deploy + verify in one step |

### Verify manually

```bash
forge verify-contract <ADDRESS> src/MyVault.sol:MyVault \
    --chain-id 627 \
    --verifier-url https://block-explorer-api.testnet.battlechain.com/api \
    --verifier custom \
    --etherscan-api-key "1234" \
    --rpc-url https://testnet.battlechain.com
```

The API key is not validated — any non-empty string works.

### Verify during deployment

```bash
forge script script/Deploy.s.sol \
    --rpc-url https://testnet.battlechain.com \
    --broadcast --skip-simulation -g 300 \
    --verify \
    --verifier-url https://block-explorer-api.testnet.battlechain.com/api \
    --verifier custom \
    --etherscan-api-key 1234
```

For factory-deployed contracts (via CreateX/BCDeploy), use `bc-verify-broadcast` after deployment.

---

## Troubleshooting

### `AnyTxType(2) transaction can't be built due to missing keys: ["gas_limit"]`

Contract exceeds the EVM size limit (24,576 bytes).

**Diagnose:**
```bash
forge build --sizes
```

**Fix options:**
1. Split into smaller contracts (libraries, separate contracts)
2. Enable optimizer: `optimizer = true`, `optimizer_runs = 200` in `foundry.toml`
3. Use `--via-ir` for deeper optimization
4. Extract constants and large strings into separate libraries

### BattleChain does not support EIP-1559

Every `forge script` and `cast send` call must include `--legacy`. Without it, transactions are rejected.

---

## BattleChain Testnet Constants

```
BATTLECHAIN_CHAIN_ID  = 627
BATTLECHAIN_DEPLOYER  = 0x74269804941119554460956f16Fe82Fbe4B90448
AGREEMENT_FACTORY     = 0x2BEe2970f10FDc2aeA28662Bb6f6a501278eBd46
SAFE_HARBOR_REGISTRY  = 0x0A652e265336a0296816ac4D8400880E3e537c24
ATTACK_REGISTRY       = 0xdD029a6374095EEb4c47a2364Ce1D0f47f007350
BATTLECHAIN_CAIP2     = "eip155:627"
```
