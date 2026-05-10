---
name: "defi-scanner"
description: "Scan DeFi markets for profitable opportunities using Alchemy MCP on-chain data. Identifies arbitrage, liquidation, yield shifts, stablecoin peg disruptions, momentum plays, and cross-chain disparities. Generates risk-adjusted trade plans with entry/stop/target and MEV assessment. Triggers on: scan for opportunities, find arbitrage, defi opportunities, trading edge, market scan, find profitable trades, defi scan, defi scanner, crypto trades, token analysis for profit."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["defi", "trading", "arbitrage", "opportunity", "profitability", "risk"]
trigger_patterns:
  - "scan for opportunities"
  - "find arbitrage"
  - "defi opportunities"
  - "trading edge"
  - "market scan"
  - "find profitable trades"
  - "defi scanner"
---

# DeFi Opportunity Scanner

## When to Use
Activate when asked to scan for DeFi trading opportunities, identify arbitrage, evaluate market edges, or generate actionable trade plans from on-chain data. Requires Alchemy MCP tools for live data.

## Data Requirements

Before scanning, gather these inputs using Alchemy MCP tools:

| Data Point | Alchemy Tool | Purpose |
|------------|-------------|----------|
| Token prices | `fetchTokenPriceBySymbol` | Current market prices |
| Price history | `fetchTokenPriceHistoryByTimeFrame` | Trend analysis |
| ERC-20 transfers | `fetchTransfers` category=erc20 | Flow analysis |
| ETH transfers | `fetchTransfers` category=external | Whale detection |
| NFT sales | `getNFTSales` | Market sentiment |
| Token balances | `getTokenBalances` | Position tracking |
| Floor prices | `getFloorPrice` | NFT market health |

## Opportunity Types & Detection

### 1. Cross-DEX Arbitrage
Price differences between DEXs for the same token pair.

```
Opportunity = (Price_DexA - Price_DexB) × Size - Gas - Slippage
```

**Detection steps:**
1. Fetch prices for the same token pair on multiple DEXs (use price history for proxy)
2. Calculate price differential as percentage: `(diff / avg_price) × 100`
3. Subtract estimated gas costs (check `getMaxPriorityFeePerGas`)
4. Subtract estimated slippage (0.1-1% depending on liquidity)
5. If result > 0, opportunity exists

**Minimum threshold**: Price differential must exceed gas + slippage by at least 0.3% to be profitable.

### 2. Cross-Chain Bridge Disparities
Wrapped token price deviations across chains.

```
Opportunity = (Price_Native - Price_Wrapped) × Size - Bridge_Fee - Gas_Both_Chains - Time_Risk
```

**Detection steps:**
1. Compare token prices across chains using `fetchTokenPriceByAddress` with different networks
2. Identify wrapped versions trading at discount/premium
3. Factor in bridge fees (Stargate ~0.06%, Across ~0.05%)
4. Factor in bridge latency risk (price movement during transfer)
5. Net positive = tradeable

### 3. Stablecoin Peg Disruptions
USDC/USDT/DAI deviations from $1.00.

```
Opportunity = (1.00 - Peg_Price) × Size - Gas - Slippage - Time_To_Repeg
```

**Detection steps:**
1. Fetch stablecoin prices via `fetchTokenPriceBySymbol`
2. Flag any stablecoin >1.005 or <0.995 (50bp deviation)
3. Check `fetchTransfers` for large stablecoin movements (redemption pressure)
4. Direction: if below peg, buy + hold for repeg; if above peg, sell/borrow against
5. Risk: peg may not restore quickly

### 4. Liquidation Opportunities
Underwater positions in lending protocols (Aave, Compound).

```
Profit = (Liquidation_Bonus_Percent × Position_Size) - Gas - Price_Impact
```

**Detection steps:**
1. Identify tokens with sharp price drops (>10% in 24h) from price history
2. These drops may create underwater collateral positions
3. Liquidation bonuses typically 5-15% of position
4. Must execute quickly before others liquidate
5. Requires flash loan for capital efficiency

### 5. Yield Farming Shifts
Incentive changes creating arbitrage windows.

```
Yield_Arbitrage = (New_APR - Old_APR) × TVL_Capture - Migration_Cost - Impermanent_Loss_Risk
```

**Detection steps:**
1. Monitor token price surges in governance/reward tokens (often signal new incentives)
2. Check for large inflows to specific protocols via transfer analysis
3. Early movers capture highest yields before dilution
4. Factor in lockup periods and withdrawal penalties

### 6. Momentum Continuation (from Price Data)
Tokens with accelerating price trends.

```
Edge = (7d_Momentum / 7d_Volatility) × Volume_Confirmation
```

**Detection steps:**
1. Fetch 7-day price history for target tokens
2. Calculate momentum: `(current - 7d_ago) / 7d_ago`
3. Rank by momentum strength
4. Confirm with volume (check transfer counts from `fetchTransfers`)
5. Filter out tokens with negative hourly trend (fading momentum)

---

## Profitability Framework

Every opportunity must pass through this scoring system:

### Step 1: Gross Profit Calculation
```
Gross_Profit = (Price_Differential × Position_Size)
```

### Step 2: Cost Deduction
```
Total_Cost = Gas_Cost + Slippage_Cost + Bridge_Fee + Time_Value
```
Where:
- **Gas_Cost**: Use `getMaxPriorityFeePerGas` × estimated gas units
- **Slippage_Cost**: `Position_Size × Expected_Slippage_Percent`
- **Bridge_Fee**: Only for cross-chain (0.05-0.10%)
- **Time_Value**: Opportunity cost during execution delay

### Step 3: Net Profit
```
Net_Profit = Gross_Profit - Total_Cost
```

### Step 4: Risk-Adjusted Return
```
RAR = Net_Profit / (Execution_Risk + Smart_Contract_Risk + Market_Risk)
```

Risk scoring (1-5 each):
| Risk Type | Score 1 (Low) | Score 3 (Medium) | Score 5 (High) |
|-----------|---------------|------------------|----------------|
| Execution | Single tx | 2-3 tx, same chain | Multi-chain, time-sensitive |
| Contract | Audited protocol | Established, minor concerns | Unaudited or new |
| Market | Deep liquidity, low vol | Medium liquidity | Thin book, high vol |

**Minimum RAR threshold**: 1.5 (net profit must exceed risk by 50%)

### Step 5: MEV Risk Assessment
```
MEV_Risk = (Your_Tx_Position) × (Builder_Incentive) × (Potential_Interference)
```
- **Tx Position**: Are you front-of-line? Backrun risk?
- **Builder Incentive**: Would block builders profit from front-running you?
- **Interference**: Can others replicate your trade faster?

Mitigation:
- Use private mempool (Flashbots Protect)
- Set tight slippage limits
- Execute during low-competition blocks

---

## Trade Plan Template

For every scored opportunity, generate:

```markdown
## Trade Plan: [Opportunity Type]

### Opportunity
- **Type**: [Arbitrage / Liquidation / Momentum / Yield]
- **Token(s)**: [Symbols]
- **Network(s)**: [Chains]
- **Edge**: [Why this works in 1-2 sentences]

### Numbers
| Metric | Value |
|--------|-------|
| Position Size | $[amount] |
| Expected Gross Profit | $[amount] (+[X]%) |
| Gas Cost | $[amount] |
| Slippage Cost | $[amount] |
| Net Profit | $[amount] (+[X]%) |
| Risk-Adjusted Return | [RAR score] |

### Execution
1. [Step-by-step transaction sequence]
2. [Include contract addresses if interacting with specific protocols]
3. [Set slippage limits]
4. [MEV protection measures]

### Risk Management
- **Stop Loss**: [Exit condition]
- **Invalidation**: [What kills this thesis]
- **Time Limit**: [How long opportunity persists]
- **Max Position**: [Size limit]

### Monitoring
- [What to watch during execution]
- [How to detect if conditions change]
```

---

## Scanning Workflow

### Quick Scan (5 minutes)
1. Fetch 15 token prices via `fetchTokenPriceBySymbol`
2. Fetch 7-day history for top movers via `fetchTokenPriceHistoryByTimeFrame`
3. Check large ERC-20 transfers via `fetchTransfers`
4. Apply momentum scoring (Opportunity Type 6)
5. Output: Top 3 opportunities with RAR scores

### Deep Scan (15 minutes)
1. Run Quick Scan first
2. For each top opportunity, run full profitability framework
3. Check cross-chain prices via `fetchTokenPriceByAddress` with multiple networks
4. Analyze NFT market sentiment via `getNFTSales`
5. Generate full trade plans for opportunities with RAR > 1.5
6. Output: Ranked opportunity list with trade plans

### Emergency Scan (1 minute)
1. Fetch stablecoin prices (USDC, USDT, DAI)
2. Fetch BTC and ETH spot prices
3. Check for >5% hourly moves
4. Output: Alert if major dislocation detected

---

## Output Format

```markdown
## DeFi Opportunity Scan Results

**Scan Type**: [Quick / Deep / Emergency]
**Timestamp**: [ISO datetime]
**Networks Covered**: [List]

### Summary
| # | Opportunity | Type | RAR | Net Profit Est. | Confidence |
|---|------------|------|-----|-----------------|------------|
| 1 | [Description] | [Type] | [Score] | [$amount] | [High/Med/Low] |

### Top Opportunity Details
[Full trade plan from template above]

### Watchlist
- Tokens with developing setups (not yet tradeable)
- Upcoming events that may create opportunities

### Avoid List
- Tokens/protocols with red flags
- Known scams or rug pulls detected
```

## Constraints
- Always include gas costs in profitability calculations
- Never recommend trading unaudited contracts
- Flag when data is stale (>5 minutes old)
- Include risk disclaimer in every output
- This skill identifies opportunities — actual execution requires separate tooling
