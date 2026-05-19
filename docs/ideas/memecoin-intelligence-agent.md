# Memecoin Intelligence Agent

## Problem Statement

Build an autonomous Agent Zero profile that monitors tracked X accounts for memecoin signals, resolves contract metadata, verifies fundamentals (volume, market cap, dump probability/timing) via token data APIs, and delivers ranked intelligence briefs via email on a recurring schedule — across EVM (Ethereum, Base, Arbitrum, BSC) and non-EVM (Solana, TON, TRON, SUI) chains.

## Recommended Direction

**Direction B — Memecoin Intelligence Agent.** A first-class Agent Zero agent profile that orchestrates:

- Existing `memecoin_monitor.py` for X signal capture (4 tracked accounts: lowkeyfr, haxevm, lookonchain, gemisalpha)
- DexScreener API for contract resolution and market data
- Token fundamentals verification (CoinGecko primary, backed by specialized APIs)
- Email delivery for hot opportunities
- Scheduler tool for recurring runs

This is intelligence-first. Trading execution is out of scope until the intelligence layer is proven.

The agent is a self-contained profile at `usr/agents/memecoin-intelligence.md` that:
1. Monitors X filtered stream for token signals
2. Resolves contracts via DexScreener
3. Verifies fundamentals via CoinGecko (price, volume, market cap, social links, contract age)
4. Scores signals by conviction (accounts posting, volume, market cap, contract age)
5. Generates structured intelligence briefs
6. Sends email digest via configured SMTP relay
7. Logs all signals to SQLite for historical tracking

## Key Assumptions to Validate

| # | Assumption | How to Validate | Risk |
|---|-----------|----------------|------|
| 1 | CoinGecko free API covers memecoins on all 7 chains (Solana, ETH, Base, Arbitrum, BSC, TON, TRON, SUI) with sufficient metadata | Test `coinGecko search + coin details` for 5 known memecoins per chain | MEDIUM — fallback to GeckoTerminal or token.coin if gaps found |
| 2 | Email delivery works from Kali container via SMTP relay | Configure msmtp with Gmail App Password or equivalent; send test email | HIGH — container has no mail by default; must set up delivery |
| 3 | X filtered stream (pay-as-you-go) is sufficient for near-real-time signal capture | Confirm memecoin_monitor.py stream vs polling; ensure <60s latency is acceptable | LOW — stream is already in use |
| 4 | All tracked accounts weighted equally — signal only triggers when token.coin data confirms memecoin criteria | Define thresholds: min liquidity, max market cap (avoid honeypots), contract age > 1h | MEDIUM — thresholds need tuning over first 30 days |
| 5 | TON, TRON, SUI have meaningful DexScreener coverage for memecoin pairs | Spot-check: search "meme" on each chain via DexScreener API | MEDIUM — these chains may have lower DEX coverage; fallback to chain-specific RPC queries |

## MVP Scope

### What's In

1. **Agent profile** (`usr/agents/memecoin-intelligence.md`): System prompt defining role, capabilities, chains, signal processing logic, and output format
2. **Extend memecoin_monitor.py**:
   - Add CoinGecko verification layer for each detected token
   - Add multi-chain expansion (TON, TRON, SUI on top of existing Solana + EVM)
   - Add confidence scoring (signal strength from accounts + fundamentals from API)
3. **Scheduled task** via scheduler tool: runs every 15 min (configurable), calls agent, sends digest
4. **Email digest**: HTML email with ranked token list, links to DexScreener, conviction score, key metrics (price, 24h volume, liquidity, market cap)
5. **SQLite state tracking**: logs all signals with timestamps, scores, outcomes for 30-day backtest
6. **Hot opportunity path**: tokens scoring above threshold trigger immediate email (not waiting for scheduled run)

### Chains (Priority Order)

| Priority | Chain | Justification |
|----------|-------|---------------|
| 1 | Solana | Highest memecoin activity (Pump.fun, Raydium) |
| 2 | Ethereum | Blue-chip memecoins, high liquidity |
| 3 | Base | Growing memecoin activity, low fees |
| 4 | BSC | High volume, many memecoins |
| 5 | Arbitrum | Growing ecosystem |
| 6 | TON | User priority — consistent memecoin activity |
| 7 | TRON | User priority — consistent memecoin activity |
| 8 | Sui | User priority — emerging memecoin activity |

### Data Sources (MVP Priority)

| Source | Purpose | Tier |
|--------|---------|------|
| DexScreener API | Contract resolution, price, liquidity, volume, pool data | PRIMARY — free, no auth, 300 req/min |
| CoinGecko API | Token metadata, market cap, social links, contract age | PRIMARY — free tier, 10-50 req/min |
| GeckoTerminal API | Fallback token data, multi-chain DEX pool data | SECONDARY — free, no auth, 260+ chains |
| Alchemy MCP (existing) | On-chain contract validation, holder analysis | SUPPORT — already configured |
| Nansen API | Smart money tracking, wallet labels, signal enrichment | ENHANCEMENT — for post-MVP |
| Artemis API | Protocol revenue, fees, memecoin fund flow analysis | ENHANCEMENT — for post-MVP |
| Bitquery | Solana DEX trades, Pump.fun data, GMGN tracking | ENHANCEMENT — for post-MVP |

### API Subscription Recommendations (Top-Class Multi-Chain Data)

#### Tier 1 — Critical (subscribe now)

| Provider | What You Get | Why It Matters | Cost |
|---------|-------------|----------------|------|
| **CoinGecko** | Token prices, market cap, volume, contract addresses, social links, metadata — across all chains | Primary verification layer for memecoin fundamentals. Free tier works for MVP. | Free (10-50 req/min) → Pro from $29/mo |
| **DexScreener** | Real-time pair data, liquidity, volume, trending, boosted tokens — 260+ chains | Already integrated. Primary contract resolution and price data. | Free (300 req/min) |
| **GeckoTerminal** | DEX pool data, OHLC, trading pairs across 260+ networks — from CoinGecko team | Best free multi-chain DEX data. Fallback and complement to DexScreener. | Free (no auth) |

#### Tier 2 — High Value (subscribe for production)

| Provider | What You Get | Why It Matters | Cost |
|---------|-------------|----------------|------|
| **QuickNode** | Low-latency RPC endpoints for all target chains (Solana, ETH, Base, Arbitrum, BSC, TON, TRON, Sui), Trading API (order book, swap quotes) | Production-grade node infrastructure. Replaces public RPCs for reliability. Solana trading via GMGN integration. | Starter from $49/mo |
| **Nansen** | 500M+ labelled addresses, Smart Money tracking, wallet profiling, token God Mode, Trade API (DEX swaps on Solana + Base) | The gold standard for on-chain wallet intelligence. Flags smart money accumulating a token before it pumps. Nansen CLI for AI agents already exists. | Enterprise — custom pricing |
| **Bitquery** | GraphQL blockchain API for Solana (Pump.fun, Raydium, Meteora, GMGN, Orca), real-time DEX trades, token flows, WebSocket streams | Best Solana coverage for memecoin activity. Real-time trade data from Pump.fun. Free tier available. | Free tier → Pro from $129/mo |
| **DeFiLlama** | TVL, yields, protocol analytics, cross-chain TVL comparisons | Track which protocols have most liquidity locked — signals where tokens have real utility. | Free API → Pro from $250/mo |

#### Tier 3 — Enhancements (subscribe post-MVP)

| Provider | What You Get | Why It Matters | Cost |
|---------|-------------|----------------|------|
| **Artemis** | Protocol revenue, fees, TVL, stablecoin supply, on-chain metrics for 12,000+ tokens, memecoin fund flow analysis | Track money flowing in/out of memecoins. Detect accumulation patterns. Google Sheets integration for manual workflows. | ~$100/mo |
| **Moralis** | Wallet balances, token transfers, NFT data, Web3 APIs — cross-chain | Wallet-level tracking for tracked influencer accounts. Know when they accumulate/dump. | Free tier → Pro from $15/mo |
| **Covalent** | Universal chain data, transaction history, holder lists, token balances — 100+ chains | Multi-chain unified API. Good for TON, TRON, Sui where other providers lack coverage. | Free tier → Pro from $99/mo |
| **Token Terminal** | Institutional-grade fundamentals: revenue, fees, TVL, standardized metrics — 100+ chains, 3,000+ assets | Verify memecoin has real protocol revenue (not just speculation). Distinguish gems from rugs. | Free tier → Pro from $79/mo |
| **Ankr** | Free tier multi-chain RPC endpoints (Ethereum, Solana, BSC, Polygon, etc.) | Reliable public RPC fallback. Good for testing. Production use needs paid tier. | Free tier → paid from $29/mo |
| **Dune Analytics** | Community-created on-chain analytics dashboards, queryable data | Access pre-built memecoin dashboards (holder distribution, trade volume by wallet size). Community queries for free. | Free tier → Pro from $75/mo |
| **Memescanscan AI** | AI-driven Solana memecoin contract analysis, real-time monitoring | Specialized for Solana memecoin ecosystem. ML-based contract safety scoring. | Custom pricing |

#### QuickNode RPC vs Alchemy

| Feature | QuickNode | Alchemy (existing) |
|---------|-----------|---------------------|
| Multi-chain coverage | All 7 target chains | EVM mainly + Solana |
| Solana RPC quality | Top-tier, low latency | Good but not specialized |
| Trading API | Yes (DEX quotes, order book) | No |
| Free tier | 100k credits/mo | 3 compute units/sec |
| Cost for production | ~$49-200/mo | ~$49/mo |

**Recommendation**: Keep Alchemy for EVM. Add QuickNode for Solana-specific reliability and TON/TRON/Sui coverage.

## Not Doing (and Why)

- **Trading execution** — user confirmed intelligence-first; no exchange integration in MVP
- **Multi-user dashboard** — single Tolu use case; focus on core agent + email
- **Wallet tracing for tracked accounts** — enhancement after fundamentals layer is proven
- **DeFi protocol deep-dive** — beyond memecoin scope; defer to defi-scanner skill
- **Non-DexScreener contract resolution** — DexScreener handles all 7 chains adequately for MVP
- **Social sentiment scoring** (last30days) — integration adds complexity; DexScreener + CoinGecko sufficient for signal scoring
- **On-chain holder analysis via RPC** — requires per-chain RPC setup; use CoinGecko metadata as proxy for contract age/safety

## Architecture Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| Agent framework | Agent Zero profile (`usr/agents/memecoin-intelligence.md`) | Native to Agent Zero, scheduler integration, extensible |
| Signal detection | Extend memecoin_monitor.py (X filtered stream) | Already built, proven, free-tier compatible |
| Contract verification | CoinGecko → DexScreener fallback | CoinGecko has broader metadata; DexScreener has better real-time pair data |
| Chain coverage | Solana + EVM (ETH/Base/BSC/Arbitrum) + TON/TRON/Sui | User priority; Solana primary, others secondary |
| State tracking | SQLite (memecoin_state.json → SQLite migration) | Bounded history, queryable, schedule-friendly |
| Notification | Email (msmtp + Gmail App Password) | User preference for hot opportunities |
| Scheduling | Agent Zero scheduler tool (15-min default) | Native integration, configurable |

## Open Questions

1. **Email delivery**: What SMTP relay to use? Gmail App Password (simple, free) or a dedicated transactional email service (Resend, SendGrid)? Tolu needs to provide credentials.
2. **Hot opportunity threshold**: What conviction score triggers immediate email vs waiting for scheduled digest? Needs calibration on first signals.
3. **Signal deduplication**: If lowkeyfr posts about a token 3 times in one hour, do we send 3 emails or consolidate? Default: consolidate within 2-hour window.
4. **30-day backtest**: Do we want to replay memecoin_monitor.py historical data through the new verification layer to build confidence scores? Yes — build evidence for signal accuracy.
5. **ETHGlobal hackathon deliverable**: Is the deliverable (a) running agent with email digest, (b) demo video, or (c) GitHub repo with agent + config? Clarify before finalizing scope.
