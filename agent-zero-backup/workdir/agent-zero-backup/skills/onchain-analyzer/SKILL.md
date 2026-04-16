---
name: "onchain-analyzer"
description: "Analyze and explain blockchain transactions, wallet activity, contract interactions, and token flows in plain English. Requires raw transaction data as input."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["research", "blockchain", "crypto", "onchain", "transactions", "web3"]
trigger_patterns:
  - "analyze transaction"
  - "onchain analysis"
  - "wallet trace"
  - "decode transaction"
  - "blockchain analysis"
  - "token flow"
---

# Onchain Transaction Analyzer

## When to Use
Activate when asked to analyze, decode, or explain blockchain transactions, wallet activity, smart contract interactions, or token flows. Requires raw transaction data, hashes, or blockchain data as input.

## The Process

### Step 1: Parse the Transaction Data
Given raw transaction data, extract:
- **Hash:** Transaction identifier
- **From/To:** Sender and receiver addresses
- **Value:** Amount transferred (native token)
- **Token Transfers:** ERC-20/ERC-721 movements
- **Gas:** Gas used, gas price, total fee
- **Method:** Function called (if contract interaction)
- **Events:** Logs emitted by the transaction
- **Block:** Block number and timestamp

### Step 2: Classify the Transaction
- **Type:** Transfer, Swap, Mint, Burn, Stake, Governance, NFT, Contract Deploy, Multisig
- **Direction:** Who initiated? Who benefited?
- **Complexity:** Simple transfer vs multi-step DeFi operation

### Step 3: Trace the Flow
- Map the path of funds
- Identify intermediate contracts
- Note any routing through DEXes, bridges, or aggregators

### Step 4: Generate Plain-English Report

```markdown
## Transaction Analysis

**Hash:** `0x...`
**Type:** [Classification]
**Network:** [Chain name]
**Status:** [Success/Failed]

### What Happened
[1-3 sentence plain English explanation]

### Flow
`[Address A]` > [Action] > `[Address B]`
- [Step 1 detail]
- [Step 2 detail]

### Token Movements
| Token | Amount | From | To |
|-------|--------|------|----| |
| [Token] | [Amount] | [Address] | [Address] |

### Gas Cost
- Gas Used: [amount]
- Gas Price: [price]
- Total Fee: [fee in native token + USD]

### Notes
- [Any suspicious patterns, MEV, or notable observations]
```

## Constraints
- This skill interprets data — it does not query the blockchain directly
- Always note when data is incomplete or uncertain
- Flag potential red flags (mixer interactions, unusual patterns)
- Never provide financial advice based on analysis

