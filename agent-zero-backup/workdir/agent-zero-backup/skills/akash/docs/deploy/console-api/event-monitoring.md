# Event Monitoring for Akash Deployments

Comprehensive guide to monitoring deployment lifecycle events, lease state transitions, and provider bids through the Akash Console API. Covers polling strategies, event-driven patterns, and production-ready TypeScript implementations.

---

## Table of Contents

1. [Overview](#overview)
2. [Polling Deployment Status via Console API](#polling-deployment-status)
3. [WebSocket Events (Future Direction)](#websocket-events)
4. [Lease Status Change Detection](#lease-status-change-detection)
5. [Provider Bid Monitoring](#provider-bid-monitoring)
6. [Building an Event-Driven Architecture](#building-an-event-driven-architecture)
7. [Example Monitoring Service Code](#example-monitoring-service-code)

---

## Overview

The Akash Console API uses a **request-response** model — there are no native server-push or WebSocket endpoints for real-time event streaming. All event monitoring is built on **polling** with intelligent backoff strategies and client-side event derivation.

### Key Endpoints for Monitoring

| Endpoint | Purpose | Poll Priority |
|----------|---------|---------------|
| `GET /v1/deployment/{dseq}` | Deployment status | High |
| `GET /v1/bids/{dseq}` | Bid collection | High (post-deploy) |
| `GET /v1/lease/{dseq}/{gseq}/{oseq}` | Individual lease status | Medium |
| `GET /v1/providers/{address}/status` | Provider health | Low |
| `GET /v1/deployments?state=active` | Bulk status check | Low |

### Base URLs

| Environment | URL |
|-------------|-----|
| **Production** | `https://console-api.akash.network/v1` |
| **Sandbox** | `https://console-api.sandbox-01.aksh.pw/v1` |

### Rate Limits

| Tier | Requests / Minute |
|------|------------------|
| Free | 60 |
| Pro | 300 |

> **Important**: Design your polling intervals to stay well within your tier's rate limit. A single monitoring loop polling 10 deployments at 5-second intervals consumes 120 requests/minute — exceeding the free tier.

---

## Polling Deployment Status

### How to Poll Deployment Status

Polling deployment status is the foundation of event monitoring. The Console API returns the full deployment state on each request, and your client must derive state changes by comparing successive responses.

```typescript
interface DeploymentResponse {
  success: boolean;
  data: {
    deployment: {
      deployment_id: {
        owner: string;
        dseq: string;
      };
      state: DeploymentState;
      version: string;
      created_at: string;
    };
    groups: DeploymentGroup[];
    escrow_account: EscrowAccount;
  };
  error?: string;
}

type DeploymentState = 'active' | 'closed' | 'inactive';

interface EscrowAccount {
  id: {
    scope: string;
    xid: string;
  owner: string;
  settled_at: string;
  balance: { denom: string; amount: string };
  transferred: { denom: string; amount: string };
  };
}
```

#### Basic Polling Request

```typescript
async function fetchDeploymentStatus(
  dseq: string,
  apiKey: string,
  baseUrl: string = 'https://console-api.akash.network/v1'
): Promise<DeploymentResponse> {
  const response = await fetch(`${baseUrl}/deployment/${dseq}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(
      `Failed to fetch deployment ${dseq}: ${response.status} ${response.statusText} - ${errorBody}`
    );
  }

  const data: DeploymentResponse = await response.json();

  if (!data.success) {
    throw new Error(`API error for deployment ${dseq}: ${data.error ?? 'Unknown error'}`);
  }

  return data;
}
```

### Recommended Polling Intervals

Use an **exponential backoff with jitter** strategy that adapts to the deployment's current state:

```typescript
interface PollingConfig {
  /** Interval when waiting for bids (deployment just created) */
  bidWaitIntervalMs: number;      // default: 3000 (3s)
  /** Interval when deployment is active and stable */
  activeIntervalMs: number;       // default: 30000 (30s)
  /** Interval when deployment is closing/closed */
  closedIntervalMs: number;       // default: 60000 (60s)
  /** Maximum backoff multiplier */
  maxBackoffMs: number;           // default: 300000 (5min)
  /** Backoff multiplier on repeated same-state responses */
  backoffMultiplier: number;      // default: 1.5
}

const DEFAULT_POLLING_CONFIG: PollingConfig = {
  bidWaitIntervalMs: 3_000,
  activeIntervalMs: 30_000,
  closedIntervalMs: 60_000,
  maxBackoffMs: 300_000,
  backoffMultiplier: 1.5,
};

function getBaseIntervalForState(state: DeploymentState, config: PollingConfig): number {
  switch (state) {
    case 'active':
      return config.activeIntervalMs;
    case 'closed':
    case 'inactive':
      return config.closedIntervalMs;
    default:
      return config.bidWaitIntervalMs;
  }
}

/**
 * Calculate next poll interval with exponential backoff and jitter.
 * Backoff increases when consecutive polls return the same state.
 */
function calculatePollInterval(
  state: DeploymentState,
  consecutiveSameState: number,
  config: PollingConfig,
): number {
  const base = getBaseIntervalForState(state, config);
  const backoff = Math.pow(config.backoffMultiplier, Math.min(consecutiveSameState, 10));
  const interval = Math.min(base * backoff, config.maxBackoffMs);

  // Add jitter: random value between -25% and +25% of the interval
  const jitter = interval * 0.25 * (Math.random() * 2 - 1);
  return Math.max(1_000, Math.floor(interval + jitter));
}
```

#### Why Backoff with Jitter?

- **Without backoff**: You waste rate limit on unchanged deployments.
- **Without jitter**: All your monitoring clients sync up, causing request spikes.
- **With both**: Gradually reduce polling frequency for stable deployments, while spreading requests evenly over time.

### Rate Limit Considerations

Calculate your maximum concurrent monitored deployments:

```
Max deployments = (Rate limit / min) / (60_000 / activeIntervalMs)

Example (Free tier, 30s active interval):
  60 req/min / (60_000 / 30_000) = 60 / 2 = 30 deployments

Example (Pro tier, 10s active interval):
  300 req/min / (60_000 / 10_000) = 300 / 6 = 50 deployments
```

If you exceed your tier's capacity:

1. Increase `activeIntervalMs` for stable deployments.
2. Use bulk status checks (`GET /v1/deployments?state=active`) to batch-monitor.
3. Upgrade to Pro tier for higher limits.
4. Implement priority-based polling (new deployments get shorter intervals).

### Deployment Status Values

| State | Meaning | Typical Transition |
|-------|---------|-------------------|
| `active` | Deployment is live and accepting bids or running leases. | → `closed` (manual close or escrow depletion) |
| `closed` | Deployment has been explicitly closed. No more leases or bids. | Terminal state |
| `inactive` | Deployment exists on-chain but has no active leases. Often pre-bid or post-lease-expiration. | → `active` (new bid accepted) or → `closed` |

#### State Transition Diagram

```
            CREATE
              │
              ▼
         ┌──────────┐
    ┌───►│  active   │◄───┐
    │    └────┬─────┘    │
    │         │          │
    │         ▼          │
    │    ┌──────────┐    │
    │    │  closed   │    │ (re-deployment)
    │    └──────────┘    │
    │                    │
    │    ┌──────────┐    │
    └────│ inactive  │────┘
         └──────────┘
```

---

## WebSocket Events

### Current Status: Not Supported

The Akash Console API **does not** currently support WebSocket connections, Server-Sent Events (SSE), or any server-push mechanism. All monitoring must be polling-based.

### Future Direction

The Akash team has indicated interest in real-time event streaming. When available, a WebSocket API would likely expose:

```typescript
// Future conceptual API — NOT currently available
interface AkashWebSocketEvent {
  type: 'deployment.state_changed'
       | 'lease.created'
       | 'lease.closed'
       | 'bid.received'
       | 'provider.status_changed'
       | 'escrow.balance_changed';
  data: Record<string, unknown>;
  timestamp: string;
  block_height: number;
}

// Future usage — NOT currently available
// const ws = new WebSocket('wss://console-api.akash.network/v1/events');
// ws.onmessage = (event) => {
//   const akashEvent: AkashWebSocketEvent = JSON.parse(event.data);
//   handleEvent(akashEvent);
// };
```

### Monitoring the Blockchain Directly

For lower-latency event detection, you can subscribe to blockchain events via Tendermint RPC's WebSocket:

```typescript
import { EventEmitter } from 'events';

/**
 * Subscribe to Akash blockchain events via Tendermint RPC WebSocket.
 * This bypasses the Console API and listens to on-chain events directly.
 *
 * RPC endpoint: wss://rpc.akash.network:443/websocket
 */
class ChainEventSubscriber extends EventEmitter {
  private ws: WebSocket | null = null;
  private readonly rpcUrl = 'wss://rpc.akash.network:443/websocket';

  async connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.rpcUrl);

      this.ws.on('open', () => {
        // Subscribe to Akash event queries
        this.ws!.send(
          JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'subscribe',
            params: {
              query: "tm.event='Tx' AND message.module='deployment'",
            },
          })
        );
        resolve();
      });

      this.ws.on('message', (data: Buffer) => {
        try {
          const parsed = JSON.parse(data.toString());
          if (parsed.result?.data) {
            this.emit('chainEvent', parsed.result.data);
          }
        } catch {
          // Ignore non-JSON messages (heartbeats, etc.)
        }
      });

      this.ws.on('error', (err) => {
        this.emit('error', err);
        reject(err);
      });

      this.ws.on('close', () => {
        this.emit('disconnected');
      });
    });
  }

  async disconnect(): Promise<void> {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

> **Warning**: The Tendermint RPC WebSocket approach requires understanding of ABCI event keys and may change between chain upgrades. The Console API polling approach is more stable across versions.

---

## Lease Status Change Detection

### Monitoring Lease State Transitions

Leases represent the binding between a deployment group and a provider. Tracking lease transitions is critical for:

- **SLA monitoring**: Detect when a workload loses its provider.
- **Cost tracking**: Monitor escrow depletion.
- **Failover triggering**: Initiate redeployment when leases close unexpectedly.

```typescript
interface LeaseResponse {
  success: boolean;
  data: {
    lease: {
      lease_id: {
        owner: string;
        dseq: string;
        gseq: number;
        oseq: number;
        provider: string;
      };
      state: LeaseState;
      price: { denom: string; amount: string };
      created_at: string;
      closed_on: string;
    };
    escrow_payment: EscrowPayment;
    group: {
      group_spec: {
        name: string;
        resources: ResourceUnit[];
      };
    };
  };
}

type LeaseState = 'active' | 'insufficient_funds' | 'closed';

interface EscrowPayment {
  balance: { denom: string; amount: string };
  rate: { denom: string; amount: string }; // uakt per block
  paid: { denom: string; amount: string };
}
```

#### Lease State Machine

```
  BID ACCEPTED
       │
       ▼
  ┌─────────┐    insufficient escrow    ┌─────────────────────┐
  │  active  │──────────────────────────►│  insufficient_funds  │
  └────┬─────┘                           └──────────┬──────────┘
       │                                            │
       │  explicit close / escrow empty             │  deposit added
       │                                            │
       ▼                                            ▼
  ┌─────────┐                              ┌─────────┐
  │  closed  │◄─────────────────────────────│  active  │
  └─────────┘                              └─────────┘
```

### Detecting Provider Offline

A provider may go offline while the lease remains `active` on-chain. Detect this by polling the provider's status endpoint:

```typescript
interface ProviderStatus {
  cluster: {
    leases: number;
    inventory: {
      active: number;
      pending: number;
    };
  };
}

async function checkProviderHealth(
  providerAddress: string,
  apiKey: string,
  baseUrl: string = 'https://console-api.akash.network/v1'
): Promise<{ isHealthy: boolean; responseTimeMs: number; status?: ProviderStatus }> {
  const startTime = Date.now();

  try {
    const response = await fetch(
      `${baseUrl}/providers/${providerAddress}/status`,
      {
        headers: { 'Authorization': `Bearer ${apiKey}` },
        signal: AbortSignal.timeout(10_000), // 10s timeout for health checks
      }
    );

    const responseTimeMs = Date.now() - startTime;

    if (!response.ok) {
      return { isHealthy: false, responseTimeMs };
    }

    const data = await response.json();
    return {
      isHealthy: true,
      responseTimeMs,
      status: data.data as ProviderStatus,
    };
  } catch (error) {
    const responseTimeMs = Date.now() - startTime;
    return { isHealthy: false, responseTimeMs };
  }
}
```

#### Provider Health Check Strategy

```typescript
interface ProviderHealthConfig {
  /** Interval between health checks (default: 60s) */
  checkIntervalMs: number;
  /** Number of consecutive failures before declaring offline (default: 3) */
  failureThreshold: number;
  /** Number of consecutive successes to restore healthy status (default: 2) */
  successThreshold: number;
}

interface ProviderHealthState {
  address: string;
  isHealthy: boolean;
  consecutiveFailures: number;
  consecutiveSuccesses: number;
  lastCheckAt: Date;
  lastHealthyAt: Date | null;
  lastFailureAt: Date | null;
}

function evaluateProviderHealth(
  checkResult: { isHealthy: boolean },
  currentState: ProviderHealthState,
  config: ProviderHealthConfig,
): ProviderHealthState {
  const now = new Date();

  if (checkResult.isHealthy) {
    const newSuccesses = currentState.consecutiveSuccesses + 1;
    return {
      ...currentState,
      consecutiveFailures: 0,
      consecutiveSuccesses: newSuccesses,
      isHealthy: newSuccesses >= config.successThreshold,
      lastCheckAt: now,
      lastHealthyAt: now,
    };
  }

  const newFailures = currentState.consecutiveFailures + 1;
  return {
    ...currentState,
    consecutiveFailures: newFailures,
    consecutiveSuccesses: 0,
    isHealthy: newFailures < config.failureThreshold,
    lastCheckAt: now,
    lastFailureAt: now,
  };
}
```

### Lease Expiration Tracking

Leases on Akash don't have a fixed expiration timestamp — they persist as long as the escrow account has sufficient funds. Track escrow depletion to predict lease expiry:

```typescript
interface LeaseExpirationEstimate {
  dseq: string;
  gseq: number;
  oseq: number;
  provider: string;
  currentBalance: number;    // uakt
  paymentRate: number;       // uakt per block
  estimatedBlocksRemaining: number;
  estimatedExpirationTime: Date;
  isLowBalance: boolean;     // less than 20% of initial deposit
}

// Average block time on Akash is ~6 seconds
const AKASH_BLOCK_TIME_SECONDS = 6;

function estimateLeaseExpiration(
  dseq: string,
  gseq: number,
  oseq: number,
  provider: string,
  escrowBalance: number, // uakt
  paymentRate: number,   // uakt per block
  initialDeposit?: number,
): LeaseExpirationEstimate {
  if (paymentRate <= 0) {
    throw new Error(`Invalid payment rate: ${paymentRate}`);
  }

  const blocksRemaining = Math.floor(escrowBalance / paymentRate);
  const secondsRemaining = blocksRemaining * AKASH_BLOCK_TIME_SECONDS;
  const estimatedExpirationTime = new Date(Date.now() + secondsRemaining * 1_000);

  const isLowBalance = initialDeposit
    ? escrowBalance < initialDeposit * 0.2
    : blocksRemaining < 500; // ~50 minutes at 6s/block

  return {
    dseq,
    gseq,
    oseq,
    provider,
    currentBalance: escrowBalance,
    paymentRate,
    estimatedBlocksRemaining: blocksRemaining,
    estimatedExpirationTime,
    isLowBalance,
  };
}
```

---

## Provider Bid Monitoring

### Polling for New Bids After Deployment Creation

After creating a deployment, providers submit bids. The window for receiving bids varies — typically 30–120 seconds, but can extend to several minutes for specialized workloads (GPU, specific regions).

```typescript
interface BidsResponse {
  success: boolean;
  data: {
    bids: Bid[];
  };
}

interface Bid {
  bid_id: {
    owner: string;
    dseq: string;
    gseq: number;
    oseq: number;
    provider: string;
  };
  state: 'open' | 'active' | 'lost' | 'closed';
  price: { denom: string; amount: string };
  created_at: string;
  resources_offer: {
    group_spec: {
      name: string;
      resources: ResourceUnit[];
    };
  };
}

interface ResourceUnit {
  resource: {
    cpu: { units: { val: string } };
    memory: { quantity: { val: string } };
    gpu: { units: { val: string } };
    storage: { quantity: { val: string } };
  };
  count: number;
}
```

#### Bid Polling Strategy

```typescript
interface BidPollingConfig {
  /** Fast polling while waiting for first bid (default: 2s) */
  initialIntervalMs: number;
  /** Slow polling once bids are flowing in (default: 5s) */
  settledIntervalMs: number;
  /** Maximum time to wait for bids before warning (default: 120s) */
  maxWaitMs: number;
  /** Maximum time to wait before giving up (default: 600s = 10min) */
  abortWaitMs: number;
}

const DEFAULT_BID_POLLING_CONFIG: BidPollingConfig = {
  initialIntervalMs: 2_000,
  settledIntervalMs: 5_000,
  maxWaitMs: 120_000,
  abortWaitMs: 600_000,
};

async function pollForBids(
  dseq: string,
  apiKey: string,
  onBidReceived: (bid: Bid, allBids: Bid[]) => void,
  onBidsSettled: (bids: Bid[]) => Promise<void>,
  config: BidPollingConfig = DEFAULT_BID_POLLING_CONFIG,
  baseUrl: string = 'https://console-api.akash.network/v1',
): Promise<Bid[]> {
  const startTime = Date.now();
  const seenBidProviders = new Set<string>();
  let lastBidCount = 0;
  let stableCount = 0;

  while (Date.now() - startTime < config.abortWaitMs) {
    const elapsed = Date.now() - startTime;

    const response = await fetch(`${baseUrl}/bids/${dseq}`, {
      headers: { 'Authorization': `Bearer ${apiKey}` },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch bids for ${dseq}: ${response.status}`);
    }

    const data: BidsResponse = await response.json();
    const bids = data.data.bids.filter((b) => b.state === 'open');

    // Detect new bids
    for (const bid of bids) {
      const key = `${bid.bid_id.provider}-${bid.bid_id.gseq}-${bid.bid_id.oseq}`;
      if (!seenBidProviders.has(key)) {
        seenBidProviders.add(key);
        onBidReceived(bid, bids);
      }
    }

    // Detect when bids have settled (no new bids for 3 consecutive checks)
    if (bids.length === lastBidCount) {
      stableCount++;
    } else {
      stableCount = 0;
    }
    lastBidCount = bids.length;

    if (stableCount >= 3 && bids.length > 0) {
      await onBidsSettled(bids);
      return bids;
    }

    // Warn if no bids after maxWaitMs
    if (elapsed >= config.maxWaitMs && bids.length === 0) {
      console.warn(
        `[BidMonitor] No bids received for dseq=${dseq} after ${elapsed / 1000}s. ` +
        `Check SDL requirements and provider availability.`
      );
    }

    // Select interval based on whether bids have started arriving
    const interval = bids.length > 0 ? config.settledIntervalMs : config.initialIntervalMs;
    await sleep(interval);
  }

  throw new Error(
    `Bid polling timed out for dseq=${dseq} after ${config.abortWaitMs / 1000}s. ` +
    `Received ${seenBidProviders.size} bids.`
  );
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

### Bid Comparison and Selection Triggers

```typescript
interface BidEvaluation {
  bid: Bid;
  score: number;
  pricePerBlock: number; // uakt
  providerAddress: string;
  rank: number;
}

function evaluateBids(bids: Bid[]): BidEvaluation[] {
  const openBids = bids.filter((b) => b.state === 'open');

  if (openBids.length === 0) {
    return [];
  }

  // Parse prices
  const evaluations = openBids.map((bid) => ({
    bid,
    pricePerBlock: parseInt(bid.price.amount, 10),
    providerAddress: bid.bid_id.provider,
    score: 0,
    rank: 0,
  }));

  // Sort by price (lowest first)
  evaluations.sort((a, b) => a.pricePerBlock - b.pricePerBlock);

  // Assign ranks and scores (lower price = better score)
  const minPrice = evaluations[0].pricePerBlock;
  const maxPrice = evaluations[evaluations.length - 1].pricePerBlock;
  const priceRange = maxPrice - minPrice || 1;

  evaluations.forEach((evaluation, index) => {
    evaluation.rank = index + 1;
    // Score: 100 for cheapest, scaling down linearly
    evaluation.score = Math.round(
      100 * (1 - (evaluation.pricePerBlock - minPrice) / priceRange)
    );
  });

  return evaluations;
}
```

---

## Building an Event-Driven Architecture

### Event Emitter Pattern

Build a monitoring layer that emits typed events, decoupling polling logic from business logic:

```typescript
import { EventEmitter } from 'events';

/**
 * All event types emitted by the monitoring system.
 */
enum AkashEventType {
  // Deployment events
  DEPLOYMENT_CREATED = 'deployment.created',
  DEPLOYMENT_STATE_CHANGED = 'deployment.state_changed',
  DEPLOYMENT_CLOSED = 'deployment.closed',
  DEPLOYMENT_ESCROW_LOW = 'deployment.escrow_low',

  // Bid events
  BID_RECEIVED = 'bid.received',
  BIDS_SETTLED = 'bids.settled',
  BID_SELECTED = 'bid.selected',

  // Lease events
  LEASE_CREATED = 'lease.created',
  LEASE_STATE_CHANGED = 'lease.state_changed',
  LEASE_CLOSED = 'lease.closed',
  LEASE_EXPIRING = 'lease.expiring',

  // Provider events
  PROVIDER_OFFLINE = 'provider.offline',
  PROVIDER_ONLINE = 'provider.online',
  PROVIDER_DEGRADED = 'provider.degraded',

  // System events
  MONITOR_STARTED = 'monitor.started',
  MONITOR_STOPPED = 'monitor.stopped',
  MONITOR_ERROR = 'monitor.error',
}

/**
 * Typed event payloads.
 */
interface AkashEventMap {
  [AkashEventType.DEPLOYMENT_CREATED]: {
    dseq: string;
    owner: string;
    createdAt: Date;
  };
  [AkashEventType.DEPLOYMENT_STATE_CHANGED]: {
    dseq: string;
    previousState: DeploymentState;
    newState: DeploymentState;
    changedAt: Date;
  };
  [AkashEventType.DEPLOYMENT_CLOSED]: {
    dseq: string;
    closedAt: Date;
    reason: 'manual' | 'escrow_depleted' | 'unknown';
  };
  [AkashEventType.DEPLOYMENT_ESCROW_LOW]: {
    dseq: string;
    currentBalance: number;
    estimatedExpiration: Date;
    percentRemaining: number;
  };
  [AkashEventType.BID_RECEIVED]: {
    dseq: string;
    provider: string;
    pricePerBlock: number;
    totalBids: number;
  };
  [AkashEventType.BIDS_SETTLED]: {
    dseq: string;
    bids: BidEvaluation[];
    bestBid: BidEvaluation;
  };
  [AkashEventType.LEASE_STATE_CHANGED]: {
    dseq: string;
    gseq: number;
    oseq: number;
    provider: string;
    previousState: LeaseState;
    newState: LeaseState;
  };
  [AkashEventType.LEASE_EXPIRING]: {
    dseq: string;
    gseq: number;
    oseq: number;
    provider: string;
    estimatedExpiration: Date;
    blocksRemaining: number;
  };
  [AkashEventType.PROVIDER_OFFLINE]: {
    provider: string;
    lastHealthyAt: Date | null;
    consecutiveFailures: number;
    affectedLeases: string[]; // dseq values
  };
  [AkashEventType.PROVIDER_ONLINE]: {
    provider: string;
    wasOffline: boolean;
    responseTimeMs: number;
  };
  [AkashEventType.MONITOR_ERROR]: {
    error: Error;
    context: string;
    dseq?: string;
  };
}

type AkashEventHandler<T extends AkashEventType> = (
  payload: AkashEventMap[T]
) => void | Promise<void>;
```

### Subscription-Based Monitoring

```typescript
type Unsubscribe = () => void;

class AkashEventBus {
  private emitter = new EventEmitter();

  constructor() {
    // Increase max listeners for monitoring many deployments
    this.emitter.setMaxListeners(100);
  }

  /**
   * Subscribe to a specific event type.
   * Returns an unsubscribe function.
   */
  on<T extends AkashEventType>(
    eventType: T,
    handler: AkashEventHandler<T>,
  ): Unsubscribe {
    this.emitter.on(eventType, handler);
    return () => this.emitter.off(eventType, handler);
  }

  /**
   * Subscribe to all events matching a pattern.
   */
  onPattern(
    pattern: string, // e.g., 'deployment.*' or 'lease.*'
    handler: (eventType: string, payload: unknown) => void,
  ): Unsubscribe {
    const allTypes = Object.values(AkashEventType);
    const matchingTypes = allTypes.filter((t) =>
      pattern.endsWith('.*')
        ? t.startsWith(pattern.slice(0, -1))
        : t === pattern
    );

    const wrappedHandler = (payload: unknown) => handler(pattern, payload);
    for (const type of matchingTypes) {
      this.emitter.on(type, wrappedHandler);
    }

    return () => {
      for (const type of matchingTypes) {
        this.emitter.off(type, wrappedHandler);
      }
    };
  }

  /**
   * Emit an event. Internal use by monitoring services.
   */
  emit<T extends AkashEventType>(eventType: T, payload: AkashEventMap[T]): void {
    this.emitter.emit(eventType, payload);
  }

  /**
   * Remove all listeners.
   */
  removeAllListeners(): void {
    this.emitter.removeAllListeners();
  }
}
```

---

## Example Monitoring Service Code

### Full TypeScript Monitoring Service

A production-ready monitoring service that orchestrates deployment polling, lease tracking, provider health checks, and bid detection:

```typescript
import { EventEmitter } from 'events';

// ─────────────────────────────────────────────────
// Configuration
// ─────────────────────────────────────────────────

interface MonitorConfig {
  apiKey: string;
  baseUrl: string;
  polling: PollingConfig;
  providerHealth: ProviderHealthConfig;
  bidPolling: BidPollingConfig;
  /** Warn when escrow drops below this percentage (default: 0.2 = 20%) */
  escrowWarningThreshold: number;
}

const DEFAULT_MONITOR_CONFIG: Omit<MonitorConfig, 'apiKey'> = {
  baseUrl: 'https://console-api.akash.network/v1',
  polling: DEFAULT_POLLING_CONFIG,
  providerHealth: {
    checkIntervalMs: 60_000,
    failureThreshold: 3,
    successThreshold: 2,
  },
  bidPolling: DEFAULT_BID_POLLING_CONFIG,
  escrowWarningThreshold: 0.2,
};

// ─────────────────────────────────────────────────
// Tracked Deployment State
// ─────────────────────────────────────────────────

interface TrackedDeployment {
  dseq: string;
  owner: string;
  currentState: DeploymentState;
  previousState: DeploymentState | null;
  consecutiveSameState: number;
  lastPolledAt: Date;
  initialDeposit: number | null;
  leases: Map<string, TrackedLease>; // key: "gseq-oseq"
  abortController: AbortController;
}

interface TrackedLease {
  dseq: string;
  gseq: number;
  oseq: number;
  provider: string;
  state: LeaseState;
  escrowBalance: number;
  paymentRate: number;
  lastCheckedAt: Date;
}

// ─────────────────────────────────────────────────
// DeploymentStatusMonitor
// ─────────────────────────────────────────────────

export class DeploymentStatusMonitor extends EventEmitter {
  private config: MonitorConfig;
  private trackedDeployments = new Map<string, TrackedDeployment>();
  private providerHealthStates = new Map<string, ProviderHealthState>();
  private isRunning = false;
  private pollTimers = new Map<string, NodeJS.Timeout>();
  private healthCheckTimer: NodeJS.Timeout | null = null;

  constructor(config: Partial<MonitorConfig> & { apiKey: string }) {
    super();
    this.setMaxListeners(200);
    this.config = { ...DEFAULT_MONITOR_CONFIG, ...config } as MonitorConfig;
  }

  // ── Lifecycle ──────────────────────────────────

  /**
   * Start monitoring a deployment.
   * Emits DEPLOYMENT_CREATED and begins polling.
   */
  async trackDeployment(dseq: string, owner: string): Promise<void> {
    if (this.trackedDeployments.has(dseq)) {
      return; // Already tracking
    }

    const abortController = new AbortController();
    const tracked: TrackedDeployment = {
      dseq,
      owner,
      currentState: 'active',
      previousState: null,
      consecutiveSameState: 0,
      lastPolledAt: new Date(),
      initialDeposit: null,
      leases: new Map(),
      abortController,
    };

    this.trackedDeployments.set(dseq, tracked);

    this.emit(AkashEventType.DEPLOYMENT_CREATED, {
      dseq,
      owner,
      createdAt: new Date(),
    });

    // Start polling loop for this deployment
    this.startDeploymentPolling(tracked);
  }

  /**
   * Stop monitoring a specific deployment.
   */
  untrackDeployment(dseq: string): void {
    const tracked = this.trackedDeployments.get(dseq);
    if (!tracked) return;

    tracked.abortController.abort();
    const timer = this.pollTimers.get(dseq);
    if (timer) {
      clearTimeout(timer);
      this.pollTimers.delete(dseq);
    }

    this.trackedDeployments.delete(dseq);
  }

  /**
   * Start the global monitoring loop.
   */
  start(): void {
    if (this.isRunning) return;
    this.isRunning = true;
    this.emit(AkashEventType.MONITOR_STARTED, { timestamp: new Date() });
    this.startProviderHealthChecks();
  }

  /**
   * Stop all monitoring.
   */
  stop(): void {
    this.isRunning = false;

    // Abort all deployment polling
    for (const [dseq, tracked] of this.trackedDeployments) {
      tracked.abortController.abort();
      const timer = this.pollTimers.get(dseq);
      if (timer) clearTimeout(timer);
    }
    this.pollTimers.clear();
    this.trackedDeployments.clear();

    // Stop health checks
    if (this.healthCheckTimer) {
      clearInterval(this.healthCheckTimer);
      this.healthCheckTimer = null;
    }

    this.emit(AkashEventType.MONITOR_STOPPED, { timestamp: new Date() });
  }

  // ── Deployment Polling ─────────────────────────

  private startDeploymentPolling(tracked: TrackedDeployment): void {
    const poll = async () => {
      if (tracked.abortController.signal.aborted) return;

      try {
        const response = await this.fetchDeploymentStatus(tracked.dseq);
        tracked.lastPolledAt = new Date();

        const newState = response.data.deployment.state;

        // Track escrow
        const escrowBalance = parseInt(
          response.data.escrow_account?.id?.balance?.amount ?? '0',
          10
        );
        if (tracked.initialDeposit === null && escrowBalance > 0) {
          tracked.initialDeposit = escrowBalance;
        }

        // Detect state change
        if (newState !== tracked.currentState) {
          const previousState = tracked.currentState;
          tracked.previousState = previousState;
          tracked.currentState = newState;
          tracked.consecutiveSameState = 0;

          this.emit(AkashEventType.DEPLOYMENT_STATE_CHANGED, {
            dseq: tracked.dseq,
            previousState,
            newState,
            changedAt: new Date(),
          });

          if (newState === 'closed') {
            this.emit(AkashEventType.DEPLOYMENT_CLOSED, {
              dseq: tracked.dseq,
              closedAt: new Date(),
              reason: 'unknown',
            });
            this.untrackDeployment(tracked.dseq);
            return;
          }
        } else {
          tracked.consecutiveSameState++;
        }

        // Check escrow levels
        if (tracked.initialDeposit && tracked.initialDeposit > 0) {
          const percentRemaining = escrowBalance / tracked.initialDeposit;
          if (percentRemaining < this.config.escrowWarningThreshold) {
            const estimate = estimateLeaseExpiration(
              tracked.dseq,
              0, 0, '',
              escrowBalance,
              100, // approximate rate
              tracked.initialDeposit,
            );
            this.emit(AkashEventType.DEPLOYMENT_ESCROW_LOW, {
              dseq: tracked.dseq,
              currentBalance: escrowBalance,
              estimatedExpiration: estimate.estimatedExpirationTime,
              percentRemaining,
            });
          }
        }

        // Fetch lease details for active deployments
        if (newState === 'active') {
          await this.pollLeases(tracked);
        }

      } catch (error) {
        this.emit(AkashEventType.MONITOR_ERROR, {
          error: error instanceof Error ? error : new Error(String(error)),
          context: 'deployment_polling',
          dseq: tracked.dseq,
        });
      }

      // Schedule next poll with adaptive interval
      if (!tracked.abortController.signal.aborted) {
        const interval = calculatePollInterval(
          tracked.currentState,
          tracked.consecutiveSameState,
          this.config.polling,
        );
        const timer = setTimeout(poll, interval);
        this.pollTimers.set(tracked.dseq, timer);
      }
    };

    // Start immediately
    poll();
  }

  // ── Lease Polling ──────────────────────────────

  private async pollLeases(tracked: TrackedDeployment): Promise<void> {
    // Poll each known lease for state changes
    for (const [key, lease] of tracked.leases) {
      try {
        const leaseData = await this.fetchLeaseStatus(
          tracked.dseq,
          lease.gseq,
          lease.oseq,
        );

        const newState = leaseData.data.lease.state;
        lease.lastCheckedAt = new Date();

        if (newState !== lease.state) {
          const previousState = lease.state;
          lease.state = newState;

          this.emit(AkashEventType.LEASE_STATE_CHANGED, {
            dseq: tracked.dseq,
            gseq: lease.gseq,
            oseq: lease.oseq,
            provider: lease.provider,
            previousState,
            newState,
          });

          if (newState === 'closed') {
            this.emit(AkashEventType.LEASE_CLOSED, {
              dseq: tracked.dseq,
              gseq: lease.gseq,
              oseq: lease.oseq,
              provider: lease.provider,
              previousState,
              newState,
            });
          }
        }

        // Update escrow tracking
        const escrowBalance = parseInt(
          leaseData.data.escrow_payment?.balance?.amount ?? '0',
          10
        );
        const paymentRate = parseInt(
          leaseData.data.escrow_payment?.rate?.amount ?? '0',
          10
        );
        lease.escrowBalance = escrowBalance;
        lease.paymentRate = paymentRate;

        // Check for expiring lease
        if (paymentRate > 0 && escrowBalance > 0) {
          const estimate = estimateLeaseExpiration(
            lease.dseq,
            lease.gseq,
            lease.oseq,
            lease.provider,
            escrowBalance,
            paymentRate,
          );

          if (estimate.isLowBalance) {
            this.emit(AkashEventType.LEASE_EXPIRING, {
              dseq: lease.dseq,
              gseq: lease.gseq,
              oseq: lease.oseq,
              provider: lease.provider,
              estimatedExpiration: estimate.estimatedExpirationTime,
              blocksRemaining: estimate.estimatedBlocksRemaining,
            });
          }
        }

      } catch (error) {
        this.emit(AkashEventType.MONITOR_ERROR, {
          error: error instanceof Error ? error : new Error(String(error)),
          context: 'lease_polling',
          dseq: tracked.dseq,
        });
      }
    }
  }

  // ── Provider Health Checks ─────────────────────

  private startProviderHealthChecks(): void {
    const checkAll = async () => {
      // Collect unique providers from tracked leases
      const providers = new Set<string>();
      for (const tracked of this.trackedDeployments.values()) {
        for (const lease of tracked.leases.values()) {
          providers.add(lease.provider);
        }
      }

      for (const providerAddress of providers) {
        try {
          const result = await checkProviderHealth(
            providerAddress,
            this.config.apiKey,
            this.config.baseUrl,
          );

          // Get or initialize health state
          let healthState = this.providerHealthStates.get(providerAddress);
          if (!healthState) {
            healthState = {
              address: providerAddress,
              isHealthy: true,
              consecutiveFailures: 0,
              consecutiveSuccesses: 0,
              lastCheckAt: new Date(),
              lastHealthyAt: new Date(),
              lastFailureAt: null,
            };
          }

          const wasHealthy = healthState.isHealthy;
          healthState = evaluateProviderHealth(result, healthState, this.config.providerHealth);
          this.providerHealthStates.set(providerAddress, healthState);

          // Emit state change events
          if (wasHealthy && !healthState.isHealthy) {
            const affectedLeases = this.getLeasesForProvider(providerAddress);
            this.emit(AkashEventType.PROVIDER_OFFLINE, {
              provider: providerAddress,
              lastHealthyAt: healthState.lastHealthyAt,
              consecutiveFailures: healthState.consecutiveFailures,
              affectedLeases,
            });
          } else if (!wasHealthy && healthState.isHealthy) {
            this.emit(AkashEventType.PROVIDER_ONLINE, {
              provider: providerAddress,
              wasOffline: true,
              responseTimeMs: result.responseTimeMs,
            });
          }

        } catch (error) {
          this.emit(AkashEventType.MONITOR_ERROR, {
            error: error instanceof Error ? error : new Error(String(error)),
            context: 'provider_health_check',
          });
        }
      }
    };

    // Run immediately, then on interval
    checkAll();
    this.healthCheckTimer = setInterval(
      checkAll,
      this.config.providerHealth.checkIntervalMs,
    );
  }

  private getLeasesForProvider(providerAddress: string): string[] {
    const dseqs: string[] = [];
    for (const tracked of this.trackedDeployments.values()) {
      for (const lease of tracked.leases.values()) {
        if (lease.provider === providerAddress) {
          dseqs.push(tracked.dseq);
          break;
        }
      }
    }
    return dseqs;
  }

  // ── API Helpers ────────────────────────────────

  private async fetchDeploymentStatus(dseq: string): Promise<DeploymentResponse> {
    const response = await fetch(
      `${this.config.baseUrl}/deployment/${dseq}`,
      {
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(15_000),
      }
    );

    if (!response.ok) {
      throw new Error(`Deployment fetch failed (${dseq}): ${response.status} ${response.statusText}`);
    }

    const data: DeploymentResponse = await response.json();
    if (!data.success) {
      throw new Error(`API error (${dseq}): ${data.error ?? 'Unknown'}`);
    }

    return data;
  }

  private async fetchLeaseStatus(
    dseq: string,
    gseq: number,
    oseq: number,
  ): Promise<LeaseResponse> {
    const response = await fetch(
      `${this.config.baseUrl}/lease/${dseq}/${gseq}/${oseq}`,
      {
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(15_000),
      }
    );

    if (!response.ok) {
      throw new Error(
        `Lease fetch failed (${dseq}/${gseq}/${oseq}): ${response.status}`
      );
    }

    const data: LeaseResponse = await response.json();
    if (!data.success) {
      throw new Error(`API error (lease ${dseq}/${gseq}/${oseq}): ${data.error ?? 'Unknown'}`);
    }

    return data;
  }

  // ── Utility ────────────────────────────────────

  /**
   * Get the current status of all tracked deployments.
   */
  getStatus(): { dseq: string; state: DeploymentState; leases: number; lastPolledAt: Date }[] {
    return Array.from(this.trackedDeployments.values()).map((tracked) => ({
      dseq: tracked.dseq,
      state: tracked.currentState,
      leases: tracked.leases.size,
      lastPolledAt: tracked.lastPolledAt,
    }));
  }

  /**
   * Register a known lease for a tracked deployment.
   * Call this after creating or discovering a lease.
   */
  registerLease(dseq: string, gseq: number, oseq: number, provider: string): void {
    const tracked = this.trackedDeployments.get(dseq);
    if (!tracked) {
      throw new Error(`Deployment ${dseq} is not being tracked`);
    }

    const key = `${gseq}-${oseq}`;
    if (!tracked.leases.has(key)) {
      tracked.leases.set(key, {
        dseq,
        gseq,
        oseq,
        provider,
        state: 'active',
        escrowBalance: 0,
        paymentRate: 0,
        lastCheckedAt: new Date(),
      });
    }
  }
}
```

### Lease Health Checker

A standalone health checker that can operate independently or alongside the monitor:

```typescript
/**
 * Dedicated lease health checker with configurable alerting thresholds.
 */
export class LeaseHealthChecker {
  private readonly checkIntervalMs: number;
  private readonly lowBalanceThreshold: number;
  private readonly criticalBalanceThreshold: number;
  private timer: NodeJS.Timeout | null = null;
  private leaseStates = new Map<string, LeaseHealthState>();

  constructor(
    private readonly config: {
      apiKey: string;
      baseUrl?: string;
      checkIntervalMs?: number;
      lowBalanceThreshold?: number;   // default: 0.25 (25%)
      criticalBalanceThreshold?: number; // default: 0.10 (10%)
    }
  ) {
    this.checkIntervalMs = config.checkIntervalMs ?? 45_000;
    this.lowBalanceThreshold = config.lowBalanceThreshold ?? 0.25;
    this.criticalBalanceThreshold = config.criticalBalanceThreshold ?? 0.10;
  }

  interface LeaseHealthState {
    dseq: string;
    gseq: number;
    oseq: number;
    provider: string;
    state: 'healthy' | 'low_balance' | 'critical' | 'closed' | 'error';
    escrowBalance: number;
    paymentRate: number;
    initialDeposit: number;
    lastCheckedAt: Date;
    lastStateChangeAt: Date;
    errorCount: number;
  }

  start(
    leases: Array<{ dseq: string; gseq: number; oseq: number; provider: string; initialDeposit: number }>
  ): void {
    // Initialize lease states
    for (const lease of leases) {
      const key = `${lease.dseq}-${lease.gseq}-${lease.oseq}`;
      this.leaseStates.set(key, {
        ...lease,
        state: 'healthy',
        escrowBalance: lease.initialDeposit,
        paymentRate: 0,
        lastCheckedAt: new Date(),
        lastStateChangeAt: new Date(),
        errorCount: 0,
      });
    }

    this.runCheck();
    this.timer = setInterval(() => this.runCheck(), this.checkIntervalMs);
  }

  stop(): void {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    this.leaseStates.clear();
  }

  private async runCheck(): Promise<void> {
    for (const [key, state] of this.leaseStates) {
      if (state.state === 'closed') continue;

      try {
        const baseUrl = this.config.baseUrl ?? 'https://console-api.akash.network/v1';
        const response = await fetch(
          `${baseUrl}/lease/${state.dseq}/${state.gseq}/${state.oseq}`,
          {
            headers: { 'Authorization': `Bearer ${this.config.apiKey}` },
            signal: AbortSignal.timeout(15_000),
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        state.escrowBalance = parseInt(
          data.data?.escrow_payment?.balance?.amount ?? '0', 10
        );
        state.paymentRate = parseInt(
          data.data?.escrow_payment?.rate?.amount ?? '0', 10
        );
        state.lastCheckedAt = new Date();
        state.errorCount = 0;

        const leaseState = data.data?.lease?.state;
        if (leaseState === 'closed') {
          this.updateState(state, 'closed');
          continue;
        }

        // Evaluate balance health
        const percentRemaining = state.initialDeposit > 0
          ? state.escrowBalance / state.initialDeposit
          : 0;

        if (percentRemaining < this.criticalBalanceThreshold) {
          this.updateState(state, 'critical');
        } else if (percentRemaining < this.lowBalanceThreshold) {
          this.updateState(state, 'low_balance');
        } else {
          this.updateState(state, 'healthy');
        }

      } catch (error) {
        state.errorCount++;
        if (state.errorCount >= 3) {
          this.updateState(state, 'error');
        }
      }
    }
  }

  private updateState(
    state: LeaseHealthState,
    newState: LeaseHealthState['state'],
  ): void {
    if (state.state !== newState) {
      const previousState = state.state;
      state.state = newState;
      state.lastStateChangeAt = new Date();

      // Log state transition
      console.log(
        `[LeaseHealth] ${state.dseq}/${state.gseq}/${state.oseq} ` +
        `${previousState} → ${newState} ` +
        `(balance: ${state.escrowBalance} uakt)`
      );
    }
  }

  /**
   * Get current health status for all monitored leases.
   */
  getHealthReport(): LeaseHealthState[] {
    return Array.from(this.leaseStates.values());
  }
}
```

### Alert System

A basic alert system that reacts to monitoring events:

```typescript
/**
 * Alert severity levels.
 */
type AlertSeverity = 'info' | 'warning' | 'critical';

/**
 * Alert notification channel.
 */
interface AlertChannel {
  name: string;
  send(alert: Alert): Promise<void>;
}

interface Alert {
  id: string;
  severity: AlertSeverity;
  eventType: AkashEventType;
  title: string;
  message: string;
  dseq?: string;
  provider?: string;
  timestamp: Date;
  metadata: Record<string, unknown>;
}

/**
 * Basic alert system that subscribes to the DeploymentStatusMonitor
 * and dispatches alerts through configured channels.
 */
export class AlertSystem {
  private channels: AlertChannel[] = [];
  private alertHistory: Alert[] = [];
  private readonly maxHistorySize: number;
  private unsubscribers: Unsubscribe[] = [];

  constructor(maxHistorySize: number = 1_000) {
    this.maxHistorySize = maxHistorySize;
  }

  /**
   * Add a notification channel (e.g., webhook, email, Slack).
   */
  addChannel(channel: AlertChannel): void {
    this.channels.push(channel);
  }

  /**
   * Connect the alert system to a DeploymentStatusMonitor.
   */
  connect(monitor: DeploymentStatusMonitor): void {
    // Deployment escrow low → warning
    this.unsubscribers.push(
      monitor.on(AkashEventType.DEPLOYMENT_ESCROW_LOW, (payload) => {
        this.dispatchAlert({
          severity: 'warning',
          eventType: AkashEventType.DEPLOYMENT_ESCROW_LOW,
          title: `Low Escrow Balance: ${payload.dseq}`,
          message: `Deployment ${payload.dseq} escrow at ${(payload.percentRemaining * 100).toFixed(1)}%. ` +
                   `Estimated expiration: ${payload.estimatedExpiration.toISOString()}`,
          dseq: payload.dseq,
          metadata: payload as unknown as Record<string, unknown>,
        });
      })
    );

    // Deployment closed → info
    this.unsubscribers.push(
      monitor.on(AkashEventType.DEPLOYMENT_CLOSED, (payload) => {
        this.dispatchAlert({
          severity: 'info',
          eventType: AkashEventType.DEPLOYMENT_CLOSED,
          title: `Deployment Closed: ${payload.dseq}`,
          message: `Deployment ${payload.dseq} was closed at ${payload.closedAt.toISOString()}. ` +
                   `Reason: ${payload.reason}`,
          dseq: payload.dseq,
          metadata: payload as unknown as Record<string, unknown>,
        });
      })
    );

    // Provider offline → critical
    this.unsubscribers.push(
      monitor.on(AkashEventType.PROVIDER_OFFLINE, (payload) => {
        this.dispatchAlert({
          severity: 'critical',
          eventType: AkashEventType.PROVIDER_OFFLINE,
          title: `Provider Offline: ${payload.provider}`,
          message: `Provider ${payload.provider} appears offline after ${payload.consecutiveFailures} failed checks. ` +
                   `Affected deployments: ${payload.affectedLeases.join(', ')}`,
          provider: payload.provider,
          metadata: payload as unknown as Record<string, unknown>,
        });
      })
    );

    // Provider online (recovered) → info
    this.unsubscribers.push(
      monitor.on(AkashEventType.PROVIDER_ONLINE, (payload) => {
        if (payload.wasOffline) {
          this.dispatchAlert({
            severity: 'info',
            eventType: AkashEventType.PROVIDER_ONLINE,
            title: `Provider Recovered: ${payload.provider}`,
            message: `Provider ${payload.provider} is back online. Response time: ${payload.responseTimeMs}ms`,
            provider: payload.provider,
            metadata: payload as unknown as Record<string, unknown>,
          });
        }
      })
    );

    // Lease expiring → warning
    this.unsubscribers.push(
      monitor.on(AkashEventType.LEASE_EXPIRING, (payload) => {
        this.dispatchAlert({
          severity: 'warning',
          eventType: AkashEventType.LEASE_EXPIRING,
          title: `Lease Expiring: ${payload.dseq}/${payload.gseq}/${payload.oseq}`,
          message: `Lease on provider ${payload.provider} has ~${payload.blocksRemaining} blocks remaining. ` +
                   `Estimated expiration: ${payload.estimatedExpiration.toISOString()}`,
          dseq: payload.dseq,
          metadata: payload as unknown as Record<string, unknown>,
        });
      })
    );

    // Monitor errors → warning
    this.unsubscribers.push(
      monitor.on(AkashEventType.MONITOR_ERROR, (payload) => {
        this.dispatchAlert({
          severity: 'warning',
          eventType: AkashEventType.MONITOR_ERROR,
          title: `Monitor Error: ${payload.context}`,
          message: `Error in ${payload.context}: ${payload.error.message}`,
          dseq: payload.dseq,
          metadata: { error: payload.error.message, stack: payload.error.stack },
        });
      })
    );
  }

  private async dispatchAlert(alert: Omit<Alert, 'id' | 'timestamp'>): Promise<void> {
    const fullAlert: Alert = {
      ...alert,
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
      timestamp: new Date(),
    };

    // Store in history
    this.alertHistory.push(fullAlert);
    if (this.alertHistory.length > this.maxHistorySize) {
      this.alertHistory.shift();
    }

    // Send to all channels concurrently
    const results = await Promise.allSettled(
      this.channels.map((channel) =>
        channel.send(fullAlert).catch((err) => {
          console.error(`[AlertSystem] Failed to send via ${channel.name}:`, err);
          throw err;
        })
      )
    );

    const failures = results.filter(
      (r): r is PromiseRejectedResult => r.status === 'rejected'
    );
    if (failures.length > 0) {
      console.error(
        `[AlertSystem] ${failures.length}/${this.channels.length} channels failed`
      );
    }
  }

  /**
   * Get recent alerts, optionally filtered by severity.
   */
  getAlertHistory(severity?: AlertSeverity): Alert[] {
    return severity
      ? this.alertHistory.filter((a) => a.severity === severity)
      : [...this.alertHistory];
  }

  /**
   * Disconnect from the monitor and clear subscriptions.
   */
  disconnect(): void {
    for (const unsubscribe of this.unsubscribers) {
      unsubscribe();
    }
    this.unsubscribers = [];
  }
}

// ─────────────────────────────────────────────────
// Built-in Alert Channels
// ─────────────────────────────────────────────────

/**
 * Console (stdout) alert channel for development.
 */
export class ConsoleAlertChannel implements AlertChannel {
  name = 'console';

  async send(alert: Alert): Promise<void> {
    const emoji = {
      info: 'ℹ️',
      warning: '⚠️',
      critical: '🔴',
    }[alert.severity];

    console.log(
      `${emoji} [${alert.severity.toUpperCase()}] ${alert.title}\n` +
      `   ${alert.message}\n` +
      `   Time: ${alert.timestamp.toISOString()}`
    );
  }
}

/**
 * Webhook alert channel for external integrations (Slack, Discord, PagerDuty, etc.).
 */
export class WebhookAlertChannel implements AlertChannel {
  name = 'webhook';

  constructor(
    private readonly webhookUrl: string,
    private readonly formatPayload: (alert: Alert) => Record<string, unknown>,
    private readonly headers: Record<string, string> = {},
  ) {}

  async send(alert: Alert): Promise<void> {
    const payload = this.formatPayload(alert);

    const response = await fetch(this.webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.headers,
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(10_000),
    });

    if (!response.ok) {
      throw new Error(
        `Webhook delivery failed: ${response.status} ${response.statusText}`
      );
    }
  }
}

/**
 * Slack-specific webhook channel.
 */
export class SlackAlertChannel extends WebhookAlertChannel {
  name = 'slack';

  constructor(slackWebhookUrl: string) {
    super(
      slackWebhookUrl,
      (alert) => ({
        text: `${alert.severity === 'critical' ? '<!channel> ' : ''}*${alert.title}*`,
        blocks: [
          {
            type: 'header',
            text: { type: 'plain_text', text: `${alert.severity.toUpperCase()}: ${alert.title}` },
          },
          {
            type: 'section',
            text: { type: 'mrkdwn', text: alert.message },
          },
          {
            type: 'context',
            elements: [
              { type: 'mrkdwn', text: `*Time:* ${alert.timestamp.toISOString()}` },
              ...(alert.dseq ? [{ type: 'mrkdwn', text: `*DSEQ:* ${alert.dseq}` }] : []),
              ...(alert.provider ? [{ type: 'mrkdwn', text: `*Provider:* ${alert.provider}` }] : []),
            ],
          },
        ],
      })
    );
  }
}
```

### Complete Usage Example

```typescript
/**
 * Full usage example: set up monitoring, alerting, and bid tracking
 * for an Akash deployment.
 */
async function main(): Promise<void> {
  const API_KEY = process.env['AKASH_API_KEY']!;
  const DSEQ = process.env['AKASH_DSEQ']!;
  const SLACK_WEBHOOK = process.env['SLACK_WEBHOOK_URL'];

  // 1. Create the monitor
  const monitor = new DeploymentStatusMonitor({
    apiKey: API_KEY,
    baseUrl: 'https://console-api.akash.network/v1',
  });

  // 2. Create and configure the alert system
  const alertSystem = new AlertSystem();
  alertSystem.addChannel(new ConsoleAlertChannel());

  if (SLACK_WEBHOOK) {
    alertSystem.addChannel(new SlackAlertChannel(SLACK_WEBHOOK));
  }

  alertSystem.connect(monitor);

  // 3. Subscribe to specific events for custom logic
  monitor.on(AkashEventType.BID_RECEIVED, (payload) => {
    console.log(
      `New bid from ${payload.provider}: ${payload.pricePerBlock} uakt/block ` +
      `(${payload.totalBids} total bids for dseq=${payload.dseq})`
    );
  });

  monitor.on(AkashEventType.PROVIDER_OFFLINE, (payload) => {
    console.error(
      `CRITICAL: Provider ${payload.provider} is offline! ` +
      `Affected deployments: ${payload.affectedLeases.join(', ')}`
    );
    // Trigger failover logic here
  });

  monitor.on(AkashEventType.LEASE_EXPIRING, (payload) => {
    console.warn(
      `Lease ${payload.dseq}/${payload.gseq}/${payload.oseq} expiring soon. ` +
      `${payload.blocksRemaining} blocks remaining (~${Math.round(payload.blocksRemaining * 6 / 60)} minutes).`
    );
    // Auto-deposit logic could go here
  });

  // 4. Start the monitor
  monitor.start();

  // 5. Track a deployment
  await monitor.trackDeployment(DSEQ, 'your-wallet-address');

  // 6. Register known leases (or discover them via deployment polling)
  monitor.registerLease(DSEQ, 1, 1, 'akash1provider...');

  console.log(`Monitoring deployment ${DSEQ}. Press Ctrl+C to stop.`);

  // Graceful shutdown
  const shutdown = (): void => {
    console.log('\nShutting down monitor...');
    alertSystem.disconnect();
    monitor.stop();
    process.exit(0);
  };

  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
```

---

## Best Practices Summary

| Practice | Recommendation |
|----------|---------------|
| **Polling interval** | Start at 3s for bids, 30s for active deployments. Backoff exponentially. |
| **Rate limit budget** | Allocate 60% to deployment checks, 30% to lease checks, 10% to provider health. |
| **Error handling** | Retry with exponential backoff. Fail open for non-critical checks. |
| **Alert fatigue** | Deduplicate alerts within a 5-minute window. Group related events. |
| **State persistence** | Snapshot monitoring state periodically to survive restarts. |
| **Provider health** | Use 3-strike failure threshold before declaring offline. |
| **Escrow monitoring** | Check every 30s. Alert at 25% remaining, critical at 10%. |
| **Bid detection** | Poll every 2s initially, settle to 5s once bids arrive. Abort after 10 minutes. |

---

## Deprecation Notice

> **Note**: The `@akashnetwork/akash-api` npm package is deprecated. All examples in this guide use the **Akash Console API** (`https://console-api.akash.network/v1`) directly via standard `fetch` calls. If you are migrating from `@akashnetwork/akash-api`, replace all gRPC/protobuf client calls with the REST endpoints documented here.

---

## See Also

- [Console API Overview](./overview.md)
- [Authentication](./authentication.md)
- [Deployment Endpoints](./deployment-endpoints.md)
- [Managed Wallet](./managed-wallet.md)
