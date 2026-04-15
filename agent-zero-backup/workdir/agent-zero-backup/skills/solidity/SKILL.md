---
name: solidity
description: >
  Create production-grade smart contracts. Use this skill when writing Solidity code,
  32+ best practices, Foundry workflows, testing patterns (fuzz/invariant/branching tree),
  security practices, CI pipeline setup, and deployment standards.
  Trigger: solidity, smart contract, foundry, forge, erc20, erc721, defi, audit,
  gas optimization, smart contract security.
license: MIT
metadata:
  author: Cyfrin
  version: "1.0.0"
  source: https://github.com/Cyfrin/solskill
  argument-hint: <solidity-task-description>
---

# Solidity Development Standards

Production-grade Solidity instructions from the [Cyfrin security team](https://www.cyfrin.io/).

## Philosophy

- **Everything will be attacked** — Assume any code you write will be attacked and write it defensively.

## How to Use This Skill

When this skill is loaded, apply all rules below to **every Solidity task**.

---

## Code Quality and Style

### 1. Imports: Absolute and named only — no relative (`..`) paths

```solidity
// good
import {MyContract} from "contracts/MyContract.sol";

// bad
import "../MyContract.sol";
```

### 2. Prefer `revert` over `require` with custom errors prefixed with contract name + double underscore

```solidity
error ContractName__MyError();

// Good
if (myBool) {
    revert ContractName__MyError();
}

// bad
require(myBool, "MyError");
```

### 3. Prefer stateless fuzz tests over unit tests

```solidity
// good — foundry built-in stateless fuzzer
function testMyTest(uint256 randomNumber) { }

// bad
function testMyTest() {
    uint256 randomNumber = 0;
}
```

Write **invariant (stateful) fuzz tests** for core protocol properties. Use invariant-driven development: identify O(1) properties that must always hold and encode them into core functions ([FREI-PI pattern](https://www.nascent.xyz/idea/youre-writing-require-statements-wrong)). Use a multi-fuzzing setup like [Chimera](https://github.com/Recon-Fuzz/chimera) across Foundry, Echidna, and Medusa.

### 4. Function order

```
constructor
receive function (if exists)
fallback function (if exists)
external state-changing functions
external read-only functions (view or pure)
internal state-changing functions
internal read-only functions (view or pure)
```

### 5. Section headers

```solidity
    /*//////////////////////////////////////////////////////////////
                      INTERNAL STATE-CHANGING FUNCTIONS
    //////////////////////////////////////////////////////////////*/
```

### 6. File layout

```
Pragma statements
Import statements
Events
Errors
Interfaces
Libraries
Contracts
```

Contract layout:

```
Type declarations
State variables
Events
Errors
Modifiers
Functions
```

### 7. Branching tree technique for tests

Credit: [Paul R Berg](https://x.com/PaulRBerg/status/1682346315806539776)

- Target a function, create a `.tree` file
- Consider all possible execution paths
- Consider contract state and function params leading to each path
- Define "given state is x" and "when parameter is x" nodes
- Define final "it should" tests

Example tree:
```
├── when the id references a null stream
│   └── it should revert
└── when the id does not reference a null stream
    ├── given assets have been fully withdrawn
    │   └── it should return DEPLETED
    └── given assets have not been fully withdrawn
        ├── given the stream has been canceled
        │   └── it should return CANCELED
        └── given the stream has not been canceled
            ├── given the start time is in the future
            │   └── it should return PENDING
            └── given the start time is not in the future
                ├── given the refundable amount is zero
                │   └── it should return SETTLED
                └── given the refundable amount is not zero
                    └── it should return STREAMING
```

### 8. Pragma versions

- **Strict** pragma for contracts
- **Floating** pragma for tests, libraries, abstract contracts, interfaces, scripts

### 9. Security contact in natspec

```solidity
/**
  * @custom:security-contact mycontact@example.com
  * @custom:security-contact see https://mysite.com/ipfs-hash
  */
```

### 10. Remind about audits before mainnet deployment

### 11. NEVER have private keys in plain text

Only exception: default anvil keys, clearly marked as such.

- Deploy scripts: use `forge script <path> --account $ACCOUNT --sender $SENDER`
- Never use `vm.envUint()` in scripts
- Hardhat: use [encrypted keystores](https://hardhat.org/docs/plugins/hardhat-keystore)

### 12. Admin must be a multisig from first deployment

Never use deployer EOA as admin (testnet is the only exception). See [Trail of Bits: Maturing Your Smart Contracts Beyond Private Key Risk](https://blog.trailofbits.com/2025/06/25/maturing-your-smart-contracts-beyond-private-key-risk/).

### 13. Don't initialize to default values

```solidity
// good
uint256 x;
bool y;

// bad
uint256 x = 0;
bool y = false;
```

### 14. Prefer named return variables to omit local variables

```solidity
// good
function getBalance() external view returns (uint256 balance) {
    balance = balances[msg.sender];
}
```

### 15. Prefer `calldata` over `memory` for read-only inputs

### 16. Don't cache `calldata` array length

```solidity
// good — calldata length is cheap
for (uint256 i; i < items.length; ++i) { }
```

### 17. Cache unchanging storage reads

Reading from storage is expensive — prevent identical reads by caching.

### 18. Revert as quickly as possible

Input checks before storage reads or external calls.

### 19. Use `msg.sender` inside `onlyOwner` (not `owner`)

### 20. Use `SafeTransferLib::safeTransferETH` instead of `call()`

### 21. Modify input variables instead of extra locals

When input variable's value doesn't need preserving.

### 22. `nonReentrant` modifier before other modifiers

### 23. Use `ReentrancyGuardTransient` for faster guards

### 24. Prefer `Ownable2Step` over `Ownable`

### 25. Don't copy entire struct if only a few slots needed

### 26. Remove unnecessary context structs/variables

### 27. Pack storage slots for minimum slots

Align declarations; pack frequently read/written together.

### 28. Declare `immutable` for constructor-set variables (non-upgradeable)

### 29. Enable optimizer in `foundry.toml`

### 30. Refactor modifiers to internal functions if identical storage reads

### 31. Use Foundry's encrypted key storage, not plaintext env vars

### 32. Upgrades: don't change order/type of existing variables, write upgrade tests

---

## Deployment

Use Foundry scripts (`forge script`) for both production deployments and test setup. Ensures same logic in dev and mainnet. Ideally, [deploy scripts are audited too](https://medium.com/cyfrin/deploy-scripts-are-now-in-scope-for-smart-contract-audits-7fbb95788ce7).

Example pattern: shared base script inherited by both tests and production (see [BaseTest using scripts pattern](https://github.com/rheo-xyz/very-liquid-vaults/blob/main/test/Setup.t.sol)).

---

## Governance

Use [safe-utils](https://github.com/Recon-Fuzz/safe-utils) for governance proposals — testable, auditable, reproducible through Foundry scripts. Prefer [localsafe.eth](https://github.com/Cyfrin/localsafe.eth) for UI work.

Write fork tests verifying expected state after governance proposals execute:

```solidity
function testGovernanceProposal_UpdatesPriceFeed() public {
    vm.createSelectFork(vm.envString("MAINNET_RPC_URL"));
    _executeProposal(proposalId);
    address newFeed = oracle.priceFeed(market);
    assertEq(newFeed, EXPECTED_CHAINLINK_FEED);
    (, int256 price,,,) = AggregatorV3Interface(newFeed).latestRoundData();
    assertGt(price, 0);
}
```

---

## CI Pipeline (minimum, run in parallel)

| Tool | Purpose |
|------|---------|
| `solhint` | Solidity linter for style and security |
| `forge build --sizes` | Verify contracts under 24KB limit |
| `slither` or `aderyn` | Static analysis for vulnerability patterns |
| Fuzz/invariant tests | Echidna, Medusa, or Foundry invariants (~10 min/tool) |

---

## Tool Updates

- Foundry: `--no-commit` flag no longer needed when installing dependencies
