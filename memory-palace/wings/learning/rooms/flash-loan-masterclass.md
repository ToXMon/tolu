# Flash Loan Masterclass — Dapp University

- **Source**: Dapp University YouTube Masterclass (Gregory + Anthony)
- **Date Captured**: 2026-04-24
- **Topics**: Flash loans, leverage trading, DeFi, Solidity smart contracts
- **Chain**: Ethereum (EVM-compatible, multi-chain deployable)

---

## What is a Flash Loan?

- Borrow millions of dollars in crypto **for free** (zero fees on Balancer)
- Must repay in the **same transaction** — if you can't, the whole tx reverts
- **No collateral required** — no money down
- Happens instantly on-chain
- Provider: **Balancer** (liquidity pool with vault contract)

## Key Protocols Used

| Protocol | Role |
|----------|------|
| **Balancer** | Flash loan provider (vault contract, `IFlashLoanRecipient`) |
| **Aave** | Lending/borrowing platform (supply collateral, borrow against it) |
| **Uniswap V3** | DEX for token swaps (WETH/USDC pair, 0.05% fee tier) |

## ERC20 Token Standard

- All tokens in the strategy are ERC20-compliant
- ETH itself is NOT ERC20 — must wrap to **WETH** via `deposit()` function
- USDC has 6 decimal places; ETH/WETH has 18
- Code works on any EVM-compatible chain (swap addresses for target chain)

---

## Leverage Trading Strategies

### Going Long (Bullish)

**Without flash loan:**
1. Supply 2,000 USDC to Aave
2. Borrow 1,000 USDC against it
3. Swap on Uniswap for more WETH
4. Hold 1.5 WETH instead of 1 WETH
5. If ETH 2x: $6,000 position → $3,000 profit (vs $2,000 without leverage)

**With flash loan (3x leverage):**
1. Start with 1,000 USDC
2. Flash loan 2,000 USDC from Balancer
3. Swap 3,000 USDC for WETH on Uniswap
4. Supply WETH to Aave as collateral
5. Borrow 2,000 USDC from Aave
6. Use borrowed 2,000 USDC to repay flash loan
7. **Result**: Leveraged position created instantly in one tx

### Going Short (Bearish)

**With flash loan:**
1. Start with 1 WETH
2. Flash loan 2 WETH from Balancer
3. Swap 3 WETH for USDC on Uniswap
4. Supply USDC to Aave as collateral
5. Borrow 1 WETH from Aave
6. Repay flash loan with borrowed WETH
7. **Result**: 4,000 USDC collateral, 1 WETH debt — profit if ETH price drops

---

## Smart Contract Architecture

### Flash Loan Pattern (from Balancer docs)

```
Two functions required:
1. getFlashLoan() — calls vault.flashLoan()
2. receiveFlashLoan() — callback from Balancer after sending funds
```

- Must inherit `IFlashLoanRecipient`
- `receiveFlashLoan` is called BY Balancer, not by you
- Security check: `msg.sender == address(vault)` — rejects anyone except Balancer
- Repay at end: `ERC20(token).transfer(address(vault), amount + feeAmount)`
- Balancer fees are zero, so `feeAmount` is 0

### Position.sol — Main Contract

**Structs:**
- `OpenParams`: assetToSupply, assetToBorrow, assetToBorrowAmount, initialCapital, expectedSwapAmount
- `CloseParams`: assetToWithdraw, assetToRepay

**Flow — Open Position:**
1. Owner calls `openPosition(OpenParams)`
2. Sets `isOpenPosition = true`, ABI-encodes params
3. Calls `vault.flashLoan()` with token + amount
4. Balancer calls `receiveFlashLoan()` callback
5. Inside callback → routes to `_open()`:
   - Swap borrowed + initial capital on Uniswap
   - Supply result to Aave
   - Borrow from Aave to repay flash loan
   - Check health factor > 1 (liquidation protection)

**Flow — Close Position:**
1. Owner calls `closePosition(CloseParams)`
2. Gets current debt from Aave (includes accrued interest)
3. Flash loans exact debt amount
4. Inside callback → routes to `_close()`:
   - Repay debt to Aave
   - Withdraw collateral from Aave
   - Swap collateral back to repay flash loan
   - Keep remaining profit

**Key Functions:**
- `swap()` — Uniswap V3 exact input single swap with slippage protection
- `supply()` — Deposit to Aave, receive aTokens
- `borrow()` — Borrow from Aave (variable rate mode = 2)
- `repay()` — Repay Aave debt (approve max uint256 to avoid math)
- `withdraw()` — Withdraw from Aave
- `supplyToAave()` — Add more collateral to existing position
- `getHealthFactor()` — Check liquidation risk (>1 safe, <1 danger)
- `getDebt()` — Get current outstanding loan including interest

**Security:**
- `onlyOwner` modifier on open/close/withdraw functions
- `receiveFlashLoan` checks `msg.sender == vault`
- Health factor check immediately after opening position
- Slippage protection via `expectedSwapAmount` (minimum output)

---

## Testing Setup

### Tools
- **Hardhat** — fork mainnet at specific block, deploy locally
- **Foundry** — Solidity-based unit tests with cheat codes
- **Alchemy** — RPC provider for forking mainnet

### Forked Mainnet Testing
- Freeze blockchain at specific block number
- Use impersonator accounts (whale wallets) to fund tests
- Manipulate market prices locally (massive buy/sell orders via impersonator)
- Zero cost, zero risk sandbox

### Test Structure
- `position-fixture.ts` — Base: deploy contract, fund with 8,000 USDC from whale
- `long-fixture.ts` — Opens 3x long, manipulates price UP, closes, checks profit
- `short-fixture.ts` — Opens 3x short, manipulates price DOWN, closes, checks profit
- Foundry tests: verify onlyOwner, only vault can call receiveFlashLoan, withdraw works

### Running Tests
```bash
npx hardhat test --network hardhat
```

---

## Key Risks

| Risk | Description |
|------|-------------|
| **Liquidation** | If health factor drops below 1, position gets liquidated |
| **Price movement** | Leverage amplifies losses as well as gains |
| **Interest accrual** | Aave debt grows over time (variable rate) |
| **Slippage** | Large swaps can get unfavorable prices |
| **Smart contract risk** | Code is NOT audited — not production-ready |
| **Max leverage** | ~4x realistic max (Aave ETH liquidation threshold: 82-83%) |

## Practical Advice

1. **Always test on forked mainnet first** — never skip sandbox testing
2. **Start with tiny amounts** ($5 trades for weeks before scaling)
3. **Monitor health factor** — add collateral if it drops toward 1
4. **Lower leverage = safer** — 1.5-2x can survive ~50% price drops
5. **Multi-chain works** — swap contract addresses for target EVM chain
6. **Not cross-chain** — each position stays on one chain

---

## Cross-References
- Related: `wings/technical/rooms/solidity-patterns.md` (if exists)
- Related: `wings/domain/rooms/defi-protocols.md` (if exists)
- Related: `wings/projects/rooms/tolutrade.md` — Tolu's trading project
