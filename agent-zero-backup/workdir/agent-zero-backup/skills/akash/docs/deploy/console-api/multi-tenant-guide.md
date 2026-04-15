# Multi-Tenant Deployment Service Guide

Build a multi-tenant deployment platform on Akash that serves multiple users with per-tenant isolation, flexible wallet strategies, and centralized management.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [User Onboarding Flow](#user-onboarding-flow)
3. [AuthZ Delegation Setup](#authz-delegation-setup)
4. [Fee Delegation](#fee-delegation)
5. [Deployment Lifecycle for Multiple Users](#deployment-lifecycle-for-multiple-users)
6. [Lease Management Across Tenants](#lease-management-across-tenants)
7. [Security Considerations](#security-considerations)
8. [Rate Limiting and Scaling](#rate-limiting-and-scaling)
9. [Example Architecture Diagram](#example-architecture-diagram)
10. [Full TypeScript Service Scaffold](#full-typescript-service-scaffold)

---

## Architecture Overview

A multi-tenant deployment service sits between your users and the Akash Network, providing a unified API while managing wallets, deployments, and billing on a per-tenant basis.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Multi-Tenant Deployment Service                     │
│                                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       ┌──────────────────┐   │
│  │ Tenant A │  │ Tenant B │  │ Tenant C │  ...  │   Tenant N       │   │
│  │ (User)   │  │ (User)   │  │ (Org)    │       │   (Enterprise)   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       └───────┬──────────┘   │
│       │              │              │                     │              │
│       ▼              ▼              ▼                     ▼              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Service API Gateway                        │   │
│  │            (Auth, Rate Limiting, Tenant Resolution)             │   │
│  └────────────────────────────┬────────────────────────────────────┘   │
│                               │                                         │
│       ┌───────────────────────┼───────────────────────┐                 │
│       ▼                       ▼                       ▼                 │
│  ┌──────────┐          ┌──────────────┐        ┌──────────────┐        │
│  │ Managed  │          │    AuthZ     │        │  Tenant DB   │        │
│  │ Wallet   │          │  Delegation  │        │  (Metadata,  │        │
│  │ Manager  │          │   Engine     │        │   Billing)   │        │
│  └────┬─────┘          └──────┬───────┘        └──────────────┘        │
│       │                       │                                         │
│       ▼                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Deployment Orchestrator                       │   │
│  │         (Lifecycle, Lease Tracking, Event Pipeline)             │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │                                             │
└───────────────────────────┼─────────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
   ┌──────────────────┐        ┌──────────────────┐
   │   Console API    │        │  Akash Network   │
   │ (Managed Wallets)│        │  (Direct Chain)  │
   └──────────────────┘        └──────────────────┘
```

### Key Components

| Component | Role | Strategy |
|-----------|------|----------|
| **Service API Gateway** | Authentication, rate limiting, tenant routing | Per-tenant API keys or JWT |
| **Managed Wallet Manager** | Console API wallets for users without their own keys | POST /wallet/create per tenant |
| **AuthZ Delegation Engine** | Execute deployments on behalf of users with their own wallets | MsgGrant + MsgExec |
| **Deployment Orchestrator** | Lifecycle management across all tenants | Create → Bid → Lease → Monitor → Close |
| **Tenant DB** | Metadata, billing, deployment tracking | PostgreSQL / any persistent store |

### Wallet Strategy Per Tenant

```
Tenant Onboarding
       │
       ▼
┌──────────────────┐     ┌─────────────────────┐
│  Managed Wallet  │ OR  │  Connect Existing    │
│  (Console API)   │     │  Wallet (AuthZ)      │
│                  │     │                       │
│  • No key mgmt   │     │  • User keeps keys    │
│  • API-funded    │     │  • AuthZ delegation   │
│  • Simplest UX   │     │  • User-funded        │
└──────────────────┘     └─────────────────────┘
```

---

## User Onboarding Flow

When a new tenant signs up, you must establish a wallet strategy before they can deploy.

### Option A: Create Managed Wallet (Recommended for SaaS)

The service creates a wallet via the Console API on behalf of the tenant. The service controls all keys and funding.

```bash
# Step 1: Create tenant record in your database
# Step 2: Create managed wallet via Console API

curl -X POST https://console-api.akash.network/v1/wallet/create \
  -H "Authorization: Bearer <service-api-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tenant-abc-123"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "wallet-abc123",
    "name": "tenant-abc-123",
    "address": "akash1qwk2...",
    "createdAt": "2025-06-15T10:00:00Z"
  }
}
```

```bash
# Step 3: Fund the managed wallet
curl -X POST https://console-api.akash.network/v1/wallet/deposit \
  -H "Authorization: Bearer <service-api-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "denom": "uakt"
  }'

# Step 4: Verify balance
curl https://console-api.akash.network/v1/wallet/balance?walletId=wallet-abc123 \
  -H "Authorization: Bearer <service-api-key>"
```

**Managed wallet onboarding sequence:**

1. Register tenant in your database
2. Call `POST /wallet/create` with tenant identifier as name
3. Store `walletId` and `address` in tenant record
4. Provide deposit address to tenant (or fund from service treasury)
5. Verify balance before allowing first deployment

### Option B: Connect Existing Wallet (For crypto-native users)

The user keeps their own keys and grants your service permission to deploy on their behalf via AuthZ.

**Step 1: User provides their Akash address**

```
User provides: akash1user...
```

**Step 2: User grants AuthZ permissions to your service wallet**

The user must execute grant transactions from their wallet:

```bash
# User grants deployment creation to your service
akash tx authz grant <SERVICE_WALLET_ADDRESS> generic \
  --msg-type /akash.deployment.v1beta3.MsgCreateDeployment \
  --from user-wallet

# User grants deployment closure
akash tx authz grant <SERVICE_WALLET_ADDRESS> generic \
  --msg-type /akash.deployment.v1beta3.MsgCloseDeployment \
  --from user-wallet

# User grants deposit capability
akash tx authz grant <SERVICE_WALLET_ADDRESS> generic \
  --msg-type /akash.deployment.v1beta3.MsgDepositDeployment \
  --from user-wallet

# User grants lease creation
akash tx authz grant <SERVICE_WALLET_ADDRESS> generic \
  --msg-type /akash.market.v1beta4.MsgCreateLease \
  --from user-wallet
```

**Step 3: Optionally grant fee allowance**

```bash
# User pays their own fees via fee grant
akash tx feegrant grant <USER_ADDRESS> <SERVICE_WALLET_ADDRESS> \
  --spend-limit 50000000uakt \
  --expiration "2026-12-31T23:59:59Z" \
  --from user-wallet
```

**Step 4: Verify grants on-chain**

```bash
# Check active grants
akash query authz grants <USER_ADDRESS> <SERVICE_WALLET_ADDRESS>
```

**Step 5: Store tenant record**

```
{
  tenantId: "tenant-xyz-789",
  walletType: "authz",
  granterAddress: "akash1user...",
  granteeAddress: "akash1service...",
  grantsVerified: true,
  feeGrantActive: true
}
```

### Onboarding Decision Matrix

| Factor | Managed Wallet | AuthZ Delegation |
|--------|---------------|------------------|
| User expertise | No crypto knowledge required | Crypto-native users |
| Key management | Service handles everything | User keeps their keys |
| Funding | Service-funded or user deposits | User-funded directly |
| Complexity | Low — single API integration | Medium — requires user to sign transactions |
| UX friction | Minimal (signup only) | User must sign 4-5 grant transactions |
| Best for | SaaS platforms, enterprise | Power users, DAOs, teams |

---

## AuthZ Delegation Setup

AuthZ allows your service to execute deployment transactions on behalf of users who connect their own wallets.

### Required Grants

Your service needs the following authorizations from each user:

| Message Type | Purpose | Required |
|-------------|---------|----------|
| `/akash.deployment.v1beta3.MsgCreateDeployment` | Create new deployments | **Yes** |
| `/akash.deployment.v1beta3.MsgCloseDeployment` | Close/shutdown deployments | **Yes** |
| `/akash.deployment.v1beta3.MsgDepositDeployment` | Add funds to deployments | **Yes** |
| `/akash.market.v1beta4.MsgCreateLease` | Accept bids and create leases | **Yes** |

### Programmatic Grant Creation

For users who prefer a guided flow, provide a web-based grant creation tool:

```typescript
import { MsgGrant } from "cosmjs-types/cosmos/authz/v1beta1/tx";
import { GenericAuthorization } from "cosmjs-types/cosmos/authz/v1beta1/authz";
import type { SigningStargateClient } from "@cosmjs/stargate";

// DEPRECATION NOTICE: @akashnetwork/akash-api is deprecated.
// For new projects, use @akashnetwork/chain-sdk instead.
// The grant creation pattern below uses cosmjs-types which remain current.

const REQUIRED_GRANT_MSG_TYPES = [
  "/akash.deployment.v1beta3.MsgCreateDeployment",
  "/akash.deployment.v1beta3.MsgCloseDeployment",
  "/akash.deployment.v1beta3.MsgDepositDeployment",
  "/akash.market.v1beta4.MsgCreateLease",
];

const GRANT_EXPIRATION_YEARS = 2;

async function createAllGrants(
  client: SigningStargateClient,
  userAddress: string,
  serviceAddress: string
): Promise<string[]> {
  const expirationDate = new Date();
  expirationDate.setFullYear(expirationDate.getFullYear() + GRANT_EXPIRATION_YEARS);

  const expiration = {
    seconds: BigInt(Math.floor(expirationDate.getTime() / 1000)),
    nanos: 0,
  };

  const txHashes: string[] = [];

  for (const msgType of REQUIRED_GRANT_MSG_TYPES) {
    const authorization = GenericAuthorization.fromPartial({
      msg: msgType,
    });

    const grantMsg = {
      typeUrl: "/cosmos.authz.v1beta1.MsgGrant",
      value: MsgGrant.fromPartial({
        granter: userAddress,
        grantee: serviceAddress,
        grant: {
          authorization: {
            typeUrl: "/cosmos.authz.v1beta1.GenericAuthorization",
            value: GenericAuthorization.encode(authorization).finish(),
          },
          expiration,
        },
      }),
    };

    const result = await client.signAndBroadcast(
      userAddress,
      [grantMsg],
      "auto"
    );

    txHashes.push(result.transactionHash);
  }

  return txHashes;
}
```

### Executing as Grantee (Deploying on User's Behalf)

When your service needs to deploy for an AuthZ-connected tenant:

```typescript
import { MsgExec } from "cosmjs-types/cosmos/authz/v1beta1/tx";
import { MsgCreateDeployment } from "@akashnetwork/akash-api/akash/deployment/v1beta3";
// DEPRECATION NOTICE: @akashnetwork/akash-api is deprecated.
// For new projects, migrate to @akashnetwork/chain-sdk.
// See migration notes at the end of this guide.

async function createDeploymentAsGrantee(
  client: SigningStargateClient,
  serviceAddress: string,
  userAddress: string,
  sdl: { groups: any; manifestVersion: () => Promise<Uint8Array> },
  depositAmount: string
): Promise<{ dseq: string; txHash: string }> {
  const dseq = BigInt(Date.now());

  // Build inner message — owner is the USER (granter), not the service
  const innerMsg = MsgCreateDeployment.fromPartial({
    id: {
      owner: userAddress,
      dseq,
    },
    groups: sdl.groups(),
    version: await sdl.manifestVersion(),
    deposit: { denom: "uakt", amount: depositAmount },
    depositor: userAddress,
  });

  // Wrap in MsgExec
  const execMsg = {
    typeUrl: "/cosmos.authz.v1beta1.MsgExec",
    value: MsgExec.fromPartial({
      grantee: serviceAddress,
      msgs: [
        {
          typeUrl: "/akash.deployment.v1beta3.MsgCreateDeployment",
          value: MsgCreateDeployment.encode(innerMsg).finish(),
        },
      ],
    }),
  };

  // Sign and broadcast as the SERVICE (grantee)
  const result = await client.signAndBroadcast(
    serviceAddress,
    [execMsg],
    "auto"
  );

  return {
    dseq: dseq.toString(),
    txHash: result.transactionHash,
  };
}
```

### Grant Verification

Always verify grants are active before executing on a tenant's behalf:

```typescript
import { AkashClient } from "@akashnetwork/akashjs";
// Or use the Stargate query client

interface GrantStatus {
  canCreateDeployment: boolean;
  canCloseDeployment: boolean;
  canDeposit: boolean;
  canCreateLease: boolean;
  grantExpiration: Date | null;
}

async function verifyTenantGrants(
  rpcEndpoint: string,
  granterAddress: string,
  granteeAddress: string
): Promise<GrantStatus> {
  const response = await fetch(
    `${rpcEndpoint}/cosmos/authz/v1beta1/grants?granter=${granterAddress}&grantee=${granteeAddress}`
  );

  const { grants } = await response.json();

  const activeGrants = new Set(
    grants
      .filter((g: any) => {
        if (!g.expiration) return true;
        return new Date(g.expiration) > new Date();
      })
      .map((g: any) => g.authorization.value.msg)
  );

  return {
    canCreateDeployment: activeGrants.has(
      "/akash.deployment.v1beta3.MsgCreateDeployment"
    ),
    canCloseDeployment: activeGrants.has(
      "/akash.deployment.v1beta3.MsgCloseDeployment"
    ),
    canDeposit: activeGrants.has(
      "/akash.deployment.v1beta3.MsgDepositDeployment"
    ),
    canCreateLease: activeGrants.has(
      "/akash.market.v1beta4.MsgCreateLease"
    ),
    grantExpiration: grants[0]?.expiration
      ? new Date(grants[0].expiration)
      : null,
  };
}
```

---

## Fee Delegation

A multi-tenant service must decide who pays for gas fees and deployment escrow. There are two primary models.

### Model 1: Service-Funded (Recommended for SaaS)

The service pays all gas and deployment costs, billing tenants through a subscription or usage model.

```
┌──────────┐    subscribes     ┌──────────────────┐    pays gas/escrow    ┌────────────┐
│  Tenant   │ ────────────────► │  Service Treasury │ ────────────────────► │   Akash    │
│           │    $$/month       │  (Service Wallet) │                      │  Network   │
└──────────┘                   └──────────────────┘                       └────────────┘
```

**Implementation:** Use Console API managed wallets funded from a central treasury.

```typescript
async function fundTenantWallet(
  consoleApiUrl: string,
  serviceApiKey: string,
  tenantWalletId: string,
  amount: string,
  denom: string = "uakt"
): Promise<void> {
  // For managed wallets, transfer from service treasury to tenant wallet
  // This is done via standard bank send or through Console API funding

  const response = await fetch(`${consoleApiUrl}/v1/wallet/deposit`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${serviceApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ denom }),
  });

  const { data } = await response.json();
  console.log(
    `Fund tenant wallet ${tenantWalletId} via deposit address: ${data.address}`
  );
}
```

### Model 2: User-Funded via FeeGrant

The user grants the service a fee allowance, allowing the service to pay gas from the user's wallet.

```bash
# User grants fee allowance to service
akash tx feegrant grant <USER_ADDRESS> <SERVICE_ADDRESS> \
  --spend-limit 100000000uakt \
  --expiration "2026-12-31T23:59:59Z" \
  --from user-wallet
```

**Programmatic fee grant check:**

```typescript
interface FeeGrantStatus {
  hasFeeGrant: boolean;
  spendLimit: string | null;
  expiration: Date | null;
}

async function checkFeeGrant(
  rpcEndpoint: string,
  granterAddress: string,
  granteeAddress: string
): Promise<FeeGrantStatus> {
  try {
    const response = await fetch(
      `${rpcEndpoint}/cosmos/feegrant/v1beta1/allowance/${granterAddress}/${granteeAddress}`
    );

    if (!response.ok) {
      return { hasFeeGrant: false, spendLimit: null, expiration: null };
    }

    const { allowance } = await response.json();

    return {
      hasFeeGrant: true,
      spendLimit: allowance?.allowance?.spend_limit?.[0]?.amount ?? null,
      expiration: allowance?.expiration
        ? new Date(allowance.expiration)
        : null,
    };
  } catch {
    return { hasFeeGrant: false, spendLimit: null, expiration: null };
  }
}
```

### Model Comparison

| Aspect | Service-Funded | User-Funded (FeeGrant) |
|--------|---------------|----------------------|
| Billing | Subscription / credits | User wallet balance |
| Gas cost owner | Service treasury | User wallet |
| Escrow funding | Service or tenant deposits | User wallet directly |
| Complexity | Lower — centralized | Higher — per-user fee grants |
| UX | Seamless for user | User must manage AKT balance |
| Best for | SaaS, enterprise, free tiers | Power users, crypto-native |

---

## Deployment Lifecycle for Multiple Users

Manage the full deployment lifecycle across all tenants from creation through teardown.

### Lifecycle States

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
    ┌───────┐    ┌──┴──────┐    ┌───────┐    ┌────────┐    ┌──┴─────┐
    │ Create │───►│ Bidding │───►│ Lease │───►│ Active │───►│ Closed │
    └───────┘    └────────┘    └───────┘    └────────┘    └────────┘
         │           │             │            │              │
         │      Select bid    Accept bid   Monitor/       Release
         │                                    Renew         escrow
         │                                                      │
         └────────────── Failed ◄─────────── Error ───────────┘
```

### Per-Tenant Deployment Tracking

Your service must track every deployment across all tenants:

```typescript
interface TenantDeployment {
  tenantId: string;
  dseq: string;
  gseq: number;
  oseq: number;
  state:
    | "creating"
    | "bidding"
    | "selecting"
    | "leasing"
    | "active"
    | "closing"
    | "closed"
    | "error";
  sdl: string;
  providerAddress: string | null;
  leasePrice: string | null;
  leaseDenom: string;
  createdAt: Date;
  updatedAt: Date;
  expiresAt: Date | null;
  error: string | null;
}
```

### Create Deployment (Managed Wallet Tenant)

```typescript
async function createDeploymentForTenant(
  consoleApiUrl: string,
  serviceApiKey: string,
  tenant: TenantRecord,
  sdl: string,
  deposit: string = "5000000uakt"
): Promise<TenantDeployment> {
  // Validate SDL first
  const validation = await fetch(`${consoleApiUrl}/v1/sdl/validate`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${serviceApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sdl }),
  });

  if (!validation.ok) {
    const err = await validation.json();
    throw new Error(`SDL validation failed: ${err.error?.message ?? "unknown"}`);
  }

  // Create deployment via managed wallet
  const response = await fetch(`${consoleApiUrl}/v1/deployment`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${serviceApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sdl,
      deposit,
      walletId: tenant.walletId,
    }),
  });

  const { data, success, error } = await response.json();

  if (!success) {
    throw new Error(`Deployment creation failed: ${error?.message}`);
  }

  return {
    tenantId: tenant.id,
    dseq: data.dseq,
    gseq: 1,
    oseq: 1,
    state: "bidding",
    sdl,
    providerAddress: null,
    leasePrice: null,
    leaseDenom: "uakt",
    createdAt: new Date(),
    updatedAt: new Date(),
    expiresAt: null,
    error: null,
  };
}
```

### Monitor Bids and Accept Best

```typescript
interface Bid {
  providerAddress: string;
  price: { denom: string; amount: string };
  dseq: string;
  gseq: number;
  oseq: number;
}

async function selectBestBid(
  consoleApiUrl: string,
  serviceApiKey: string,
  dseq: string,
  strategy: "cheapest" | "fastest" | "reputable" = "cheapest"
): Promise<{ provider: string; price: string }> {
  // Fetch all bids for the deployment
  const response = await fetch(`${consoleApiUrl}/v1/bids/${dseq}`, {
    headers: { Authorization: `Bearer ${serviceApiKey}` },
  });

  const { data } = await response.json();
  const bids: Bid[] = data.bids;

  if (!bids || bids.length === 0) {
    throw new Error(`No bids received for deployment ${dseq}`);
  }

  // Sort by strategy
  let selectedBid: Bid;

  switch (strategy) {
    case "cheapest":
      selectedBid = bids.sort((a, b) =>
        BigInt(a.price.amount) < BigInt(b.price.amount) ? -1 : 1
      )[0];
      break;
    case "fastest":
      // Select first available bid (first responder)
      selectedBid = bids[0];
      break;
    default:
      selectedBid = bids.sort((a, b) =>
        BigInt(a.price.amount) < BigInt(b.price.amount) ? -1 : 1
      )[0];
  }

  // Accept the bid to create a lease
  const leaseResponse = await fetch(`${consoleApiUrl}/v1/lease`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${serviceApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      dseq,
      gseq: selectedBid.gseq,
      oseq: selectedBid.oseq,
      provider: selectedBid.providerAddress,
    }),
  });

  const leaseResult = await leaseResponse.json();

  if (!leaseResult.success) {
    throw new Error(
      `Failed to create lease: ${leaseResult.error?.message}`
    );
  }

  return {
    provider: selectedBid.providerAddress,
    price: selectedBid.price.amount,
  };
}
```

### Close Deployment

```typescript
async function closeDeploymentForTenant(
  consoleApiUrl: string,
  serviceApiKey: string,
  dseq: string,
  walletId?: string
): Promise<void> {
  const response = await fetch(`${consoleApiUrl}/v1/deployment/${dseq}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${serviceApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ walletId }),
  });

  const result = await response.json();

  if (!result.success) {
    throw new Error(`Failed to close deployment ${dseq}: ${result.error?.message}`);
  }
}
```

---

## Lease Management Across Tenants

### Tracking Active Leases

Maintain a real-time view of all leases across your tenant base:

```typescript
interface LeaseRecord {
  tenantId: string;
  dseq: string;
  gseq: number;
  oseq: number;
  providerAddress: string;
  pricePerBlock: { denom: string; amount: string };
  state: "active" | "insufficient_funds" | "closed" | "migration_needed";
  createdAt: Date;
  estimatedExpiry: Date | null;
  totalCostSpent: string;
}

// Poll all deployments and update lease state
async function pollAllLeases(
  consoleApiUrl: string,
  serviceApiKey: string,
  tenants: TenantRecord[]
): Promise<LeaseRecord[]> {
  const allLeases: LeaseRecord[] = [];

  for (const tenant of tenants) {
    try {
      const response = await fetch(
        `${consoleApiUrl}/v1/deployments?owner=${tenant.walletAddress}`,
        {
          headers: { Authorization: `Bearer ${serviceApiKey}` },
        }
      );

      const { data } = await response.json();

      for (const deployment of data.deployments ?? []) {
        for (const lease of deployment.leases ?? []) {
          allLeases.push({
            tenantId: tenant.id,
            dseq: lease.dseq,
            gseq: lease.gseq,
            oseq: lease.oseq,
            providerAddress: lease.provider,
            pricePerBlock: lease.price,
            state: mapLeaseState(lease.state),
            createdAt: new Date(lease.createdAt),
            estimatedExpiry: lease.escrow
              ? calculateEscrowExpiry(lease.escrow, lease.price)
              : null,
            totalCostSpent: lease.totalSpent ?? "0",
          });
        }
      }
    } catch (error) {
      console.error(
        `Failed to poll leases for tenant ${tenant.id}:`,
        error
      );
    }
  }

  return allLeases;
}

function mapLeaseState(
  chainState: string
): LeaseRecord["state"] {
  switch (chainState) {
    case "active":
      return "active";
    case "insufficient_funds":
      return "insufficient_funds";
    case "closed":
      return "closed";
    default:
      return "active";
  }
}

function calculateEscrowExpiry(
  escrow: { balance: string; settled: string },
  pricePerBlock: { amount: string }
): Date {
  const remaining = BigInt(escrow.balance) - BigInt(escrow.settled);
  const rate = BigInt(pricePerBlock.amount);
  const blocksRemaining = remaining / rate;
  // Approximate: ~6 seconds per block on Akash
  const secondsRemaining = Number(blocksRemaining) * 6;
  return new Date(Date.now() + secondsRemaining * 1000);
}
```

### Automatic Renewal / Refill

Refill deployments that are running low on escrow:

```typescript
async function refillLowBalanceDeployments(
  consoleApiUrl: string,
  serviceApiKey: string,
  leases: LeaseRecord[],
  thresholdBlocks: number = 1000
): Promise<string[]> {
  const refilled: string[] = [];

  for (const lease of leases) {
    if (lease.state !== "active" || !lease.estimatedExpiry) continue;

    const blocksRemaining = Math.floor(
      (lease.estimatedExpiry.getTime() - Date.now()) / 6000
    );

    if (blocksRemaining < thresholdBlocks) {
      try {
        await fetch(
          `${consoleApiUrl}/v1/deployment/${lease.dseq}/deposit`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${serviceApiKey}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              deposit: "5000000uakt",
            }),
          }
        );

        refilled.push(lease.dseq);
        console.log(
          `Refilled deployment ${lease.dseq} for tenant ${lease.tenantId}`
        );
      } catch (error) {
        console.error(
          `Failed to refill ${lease.dseq} for tenant ${lease.tenantId}:`,
          error
        );
      }
    }
  }

  return refilled;
}
```

### Lease Cleanup

Periodically clean up stale closed deployments:

```typescript
async function cleanupClosedLeases(
  deploymentStore: Map<string, TenantDeployment>,
  retentionDays: number = 7
): Promise<number> {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - retentionDays);

  let cleaned = 0;

  for (const [dseq, deployment] of deploymentStore.entries()) {
    if (
      deployment.state === "closed" &&
      deployment.updatedAt < cutoff
    ) {
      deploymentStore.delete(dseq);
      cleaned++;
    }
  }

  return cleaned;
}
```

---

## Security Considerations

### Key Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    Key Hierarchy                                │
│                                                                 │
│  ┌─────────────────┐     ┌──────────────────────────────────┐  │
│  │ Service Treasury │     │     Per-Tenant Managed Wallets    │  │
│  │ (Master Key)     │     │     (Console API Controlled)     │  │
│  │                  │     │                                   │  │
│  │  • HSM / Vault   │     │  wallet-abc → tenant A           │  │
│  │  • High security │     │  wallet-def → tenant B           │  │
│  │  • Limited access│     │  wallet-ghi → tenant C           │  │
│  └─────────────────┘     └──────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              AuthZ Grantee Key (for user-owned wallets)  │   │
│  │              • Single key to execute for all users        │   │
│  │              • Store in HSM or encrypted keystore         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Best practices:**

1. **Service treasury key** — Store in an HSM (AWS KMS, HashiCorp Vault) with strict access policies. Never expose in environment variables or code.
2. **AuthZ grantee key** — The single key that can execute on behalf of all AuthZ tenants. Protect with the same rigor as the treasury key. If compromised, an attacker can deploy on behalf of every connected user.
3. **Console API key** — Rotate regularly. Use separate keys per environment (development, staging, production).
4. **Managed wallet isolation** — Each tenant's managed wallet is a separate address. The Console API handles signing internally; your service never sees private keys.

### Access Control

```typescript
interface TenantPermissions {
  tenantId: string;
  tier: "free" | "pro" | "enterprise";
  maxDeployments: number;
  maxCpuUnits: number;
  maxMemoryMB: number;
  maxStorageGB: number;
  allowedRegions: string[];  // empty = all
  canUseGpu: boolean;
  canUseCustomSdl: boolean;
}

const TIER_LIMITS: Record<string, TenantPermissions> = {
  free: {
    tenantId: "",
    tier: "free",
    maxDeployments: 2,
    maxCpuUnits: 2,
    maxMemoryMB: 4096,
    maxStorageGB: 20,
    allowedRegions: [],
    canUseGpu: false,
    canUseCustomSdl: false,
  },
  pro: {
    tenantId: "",
    tier: "pro",
    maxDeployments: 20,
    maxCpuUnits: 20,
    maxMemoryMB: 65536,
    maxStorageGB: 500,
    allowedRegions: [],
    canUseGpu: true,
    canUseCustomSdl: true,
  },
  enterprise: {
    tenantId: "",
    tier: "enterprise",
    maxDeployments: -1, // unlimited
    maxCpuUnits: -1,
    maxMemoryMB: -1,
    maxStorageGB: -1,
    allowedRegions: [],
    canUseGpu: true,
    canUseCustomSdl: true,
  },
};

function validateDeploymentRequest(
  tenant: TenantPermissions,
  currentDeployments: number,
  requestedResources: { cpu: number; memoryMB: number; storageGB: number; gpu: number }
): { allowed: boolean; reason?: string } {
  if (
    tenant.maxDeployments !== -1 &&
    currentDeployments >= tenant.maxDeployments
  ) {
    return { allowed: false, reason: "Deployment limit reached" };
  }

  if (
    tenant.maxCpuUnits !== -1 &&
    requestedResources.cpu > tenant.maxCpuUnits
  ) {
    return { allowed: false, reason: "CPU limit exceeded" };
  }

  if (requestedResources.gpu > 0 && !tenant.canUseGpu) {
    return { allowed: false, reason: "GPU not available on current tier" };
  }

  return { allowed: true };
}
```

### Tenant Isolation

1. **Wallet isolation** — Each tenant gets a separate managed wallet address. No shared wallets.
2. **Deployment ownership** — Managed wallet deployments are owned by the wallet address, not the service. Track ownership in your database.
3. **AuthZ scope** — AuthZ grants are per-user → service. The service can only execute message types explicitly granted.
4. **API key per tenant** — Issue separate API keys for each tenant to access your service. Never share Console API keys with tenants.
5. **SDL validation** — Always validate and sanitize SDL before submission. Reject SDL with host-level access or privileged capabilities.
6. **Audit logging** — Log every deployment action with tenant ID, timestamp, dseq, and action type.

---

## Rate Limiting and Scaling

### Rate Limiting Strategy

```
┌──────────────────────────────────────────────────────────┐
│                   Rate Limiting Layers                    │
│                                                           │
│  Layer 1: Tenant Rate Limit (per-tenant API key)         │
│  └─ Free: 10 req/min, Pro: 60 req/min, Ent: unlimited   │
│                                                           │
│  Layer 2: Service Rate Limit (aggregate to Console API)  │
│  └─ Based on Console API tier (60-300 req/min)           │
│                                                           │
│  Layer 3: Chain Rate Limit (RPC node limits)             │
│  └─ Mempool / block space constraints                     │
└──────────────────────────────────────────────────────────┘
```

### Tenant Rate Limiter

```typescript
import { RateLimiterMemory } from "rate-limiter-flexible";

const tenantLimiters = new Map<
  string,
  RateLimiterMemory
>();

function getTenantLimiter(tenantId: string, tier: string): RateLimiterMemory {
  if (!tenantLimiters.has(tenantId)) {
    const limits = {
      free: { points: 10, duration: 60 },
      pro: { points: 60, duration: 60 },
      enterprise: { points: 600, duration: 60 },
    };

    const config = limits[tier] ?? limits.free;
    tenantLimiters.set(
      tenantId,
      new RateLimiterMemory({
        points: config.points,
        duration: config.duration,
        keyPrefix: tenantId,
      })
    );
  }

  return tenantLimiters.get(tenantId)!;
}

async function checkRateLimit(
  tenantId: string,
  tier: string
): Promise<{ allowed: boolean; retryAfterMs: number }> {
  const limiter = getTenantLimiter(tenantId, tier);

  try {
    await limiter.consume(tenantId, 1);
    return { allowed: true, retryAfterMs: 0 };
  } catch {
    const info = await limiter.get(tenantId);
    const retryAfterMs = info
      ? Math.ceil((info.msBeforeNext / 1000) * 1000)
      : 60000;
    return { allowed: false, retryAfterMs };
  }
}
```

### Scaling Considerations

| Concern | Recommendation |
|---------|---------------|
| **Deployment throughput** | Batch deployment creation; stagger bid-wait periods |
| **Lease polling** | Use websocket/event subscriptions instead of polling where available |
| **Console API rate limits** | Request enterprise tier or deploy your own Console API instance |
| **Database** | Use connection pooling; shard by tenant ID for high scale |
| **Horizontal scaling** | Deploy service instances behind a load balancer; use shared state (Redis) for rate limits and deployment locks |
| **Deployment locks** | Use distributed locks (Redis) to prevent concurrent deployments for the same tenant |

### Deployment Queue

For high-traffic multi-tenant services, queue deployments instead of processing synchronously:

```typescript
import { EventEmitter } from "events";

interface DeploymentJob {
  tenantId: string;
  sdl: string;
  deposit: string;
  strategy: "cheapest" | "fastest" | "reputable";
  resolve: (result: TenantDeployment) => void;
  reject: (error: Error) => void;
}

class DeploymentQueue extends EventEmitter {
  private queue: DeploymentJob[] = [];
  private processing = false;
  private maxConcurrency: number;
  private activeCount = 0;

  constructor(maxConcurrency: number = 5) {
    super();
    this.maxConcurrency = maxConcurrency;
  }

  enqueue(
    tenantId: string,
    sdl: string,
    deposit: string,
    strategy: "cheapest" | "fastest" | "reputable" = "cheapest"
  ): Promise<TenantDeployment> {
    return new Promise((resolve, reject) => {
      this.queue.push({ tenantId, sdl, deposit, strategy, resolve, reject });
      this.processNext();
    });
  }

  private async processNext(): Promise<void> {
    if (this.processing) return;
    if (this.activeCount >= this.maxConcurrency) return;
    if (this.queue.length === 0) return;

    this.processing = true;

    while (
      this.queue.length > 0 &&
      this.activeCount < this.maxConcurrency
    ) {
      const job = this.queue.shift()!;
      this.activeCount++;

      // Process asynchronously — do not await
      this.executeJob(job)
        .then((result) => {
          job.resolve(result);
          this.emit("deployment:completed", result);
        })
        .catch((error) => {
          job.reject(error);
          this.emit("deployment:failed", {
            tenantId: job.tenantId,
            error: error.message,
          });
        })
        .finally(() => {
          this.activeCount--;
          this.processNext();
        });
    }

    this.processing = false;
  }

  private async executeJob(job: DeploymentJob): Promise<TenantDeployment> {
    // Full deployment lifecycle: create → wait for bids → select → lease
    // Implementation uses createDeploymentForTenant and selectBestBid
    // from the Deployment Lifecycle section above.
    throw new Error("Implementation injects dependencies at service init");
  }
}
```

---

## Example Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MULTI-TENANT DEPLOYMENT SERVICE                     │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         SERVICE API (REST/GraphQL)                    │   │
│  │                                                                      │   │
│  │  POST /tenants                     GET /tenants/:id/deployments     │   │
│  │  POST /tenants/:id/wallet          POST /tenants/:id/deployments    │   │
│  │  POST /tenants/:id/authz/connect   DELETE /deployments/:dseq        │   │
│  │  GET  /tenants/:id/balance         GET  /deployments/:dseq/status   │   │
│  │  POST /deployments/:dseq/refill    GET  /leases                     │   │
│  └─────────────────────────────┬────────────────────────────────────────┘   │
│                                │                                            │
│  ┌─────────────────────────────┴────────────────────────────────────────┐   │
│  │                        MIDDLEWARE LAYER                               │   │
│  │                                                                      │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  ┌─────────────┐ │   │
│  │  │ Auth (JWT /  │  │ Rate Limiter │  │  Tenant    │  │  Audit      │ │   │
│  │  │ API Key)     │  │ (per-tenant) │  │ Resolver   │  │  Logger     │ │   │
│  │  └─────────────┘  └──────────────┘  └───────────┘  └─────────────┘ │   │
│  └─────────────────────────────┬────────────────────────────────────────┘   │
│                                │                                            │
│  ┌─────────────────────────────┴────────────────────────────────────────┐   │
│  │                      CORE SERVICE ENGINE                              │   │
│  │                                                                      │   │
│  │  ┌──────────────────┐  ┌─────────────────┐  ┌─────────────────────┐ │   │
│  │  │  Multi-Tenant     │  │  Deployment      │  │  Lease Manager      │ │   │
│  │  │  Manager          │  │  Orchestrator    │  │                     │ │   │
│  │  │                   │  │                  │  │  • Track all leases │ │   │
│  │  │  • Onboard users  │  │  • Create/close  │  │  • Monitor escrow   │ │   │
│  │  │  • Wallet mgmt    │  │  • Bid selection │  │  • Auto-refill      │ │   │
│  │  │  • AuthZ grants   │  │  • Event pipeline│  │  • Expiry alerts    │ │   │
│  │  └────────┬─────────┘  └────────┬────────┘  └──────────┬──────────┘ │   │
│  │           │                      │                      │           │   │
│  └───────────┼──────────────────────┼──────────────────────┼───────────┘   │
│              │                      │                      │               │
│  ┌───────────┴──────────┐  ┌────────┴──────────────┐      │               │
│  │   Console API Client │  │   AuthZ / Chain Client│      │               │
│  │                      │  │                       │      │               │
│  │  Managed Wallet Ops  │  │  MsgExec wrappers     │      │               │
│  │  SDL Validation      │  │  Grant verification   │      │               │
│  │  Deployment CRUD     │  │  FeeGrant checks      │      │               │
│  └───────────┬──────────┘  └────────┬──────────────┘      │               │
│              │                      │                      │               │
│  ┌───────────┴──────────────────────┴──────────────────────┴───────────┐   │
│  │                        EVENT BUS / JOB QUEUE                        │   │
│  │      (Redis / BullMQ / Kafka for async processing)                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     PERSISTENCE LAYER                               │   │
│  │                                                                     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │  PostgreSQL   │  │    Redis      │  │  Encrypted Key Store     │  │   │
│  │  │  • Tenants    │  │  • Sessions   │  │  (Vault / KMS)           │  │   │
│  │  │  • Deploys    │  │  • Rate limits│  │  • Service keys          │  │   │
│  │  │  • Leases     │  │  • Locks      │  │  • Grantee wallet        │  │   │
│  │  │  • Audit logs │  │  • Cache      │  │                          │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                              │
                    ▼                              ▼
      ┌──────────────────────┐      ┌──────────────────────┐
      │   Console API         │      │   Akash Network      │
      │   (Managed Wallets)   │      │   (RPC / gRPC)       │
      │                       │      │                       │
      │  console-api.         │      │  rpc.akash.network   │
      │  akash.network        │      │  :26657              │
      └──────────────────────┘      └──────────────────────┘
```

---

## Full TypeScript Service Scaffold

A complete, production-grade multi-tenant deployment service with Console API integration, AuthZ support, and per-tenant tracking.

### Installation

```bash
npm install @akashnetwork/chain-sdk @cosmjs/stargate @cosmjs/encoding
npm install cosmjs-types
npm install express jsonwebtoken dotenv
npm install ioredis rate-limiter-flexible
npm install pg  # or your preferred ORM
```

> **Deprecation Notice:** `@akashnetwork/akash-api` is deprecated. New projects should use `@akashnetwork/chain-sdk`. The scaffold below uses `@akashnetwork/chain-sdk` for new patterns and notes where `@akashnetwork/akash-api` types are still needed for AuthZ message encoding.

### Types

```typescript
// types.ts

export interface TenantRecord {
  id: string;
  name: string;
  email: string;
  tier: "free" | "pro" | "enterprise";
  walletType: "managed" | "authz";

  // Managed wallet fields
  walletId: string | null;
  walletAddress: string | null;

  // AuthZ fields
  granterAddress: string | null; // user's wallet
  granteeAddress: string | null; // service wallet
  grantsVerified: boolean;
  feeGrantActive: boolean;

  createdAt: Date;
  updatedAt: Date;
}

export interface TenantDeployment {
  tenantId: string;
  dseq: string;
  gseq: number;
  oseq: number;
  state:
    | "creating"
    | "bidding"
    | "selecting"
    | "leasing"
    | "active"
    | "closing"
    | "closed"
    | "error";
  sdl: string;
  providerAddress: string | null;
  leasePrice: string | null;
  leaseDenom: string;
  createdAt: Date;
  updatedAt: Date;
  expiresAt: Date | null;
  error: string | null;
}

export interface LeaseRecord {
  tenantId: string;
  dseq: string;
  gseq: number;
  oseq: number;
  providerAddress: string;
  pricePerBlock: { denom: string; amount: string };
  state: "active" | "insufficient_funds" | "closed" | "migration_needed";
  createdAt: Date;
  estimatedExpiry: Date | null;
  totalCostSpent: string;
}

export interface TenantPermissions {
  tenantId: string;
  tier: "free" | "pro" | "enterprise";
  maxDeployments: number;
  maxCpuUnits: number;
  maxMemoryMB: number;
  maxStorageGB: number;
  allowedRegions: string[];
  canUseGpu: boolean;
  canUseCustomSdl: boolean;
}

export interface DeploymentResult {
  dseq: string;
  provider: string;
  price: string;
  state: TenantDeployment["state"];
}

export type BidStrategy = "cheapest" | "fastest" | "reputable";

export type DeployEvent =
  | { type: "deployment:created"; tenantId: string; dseq: string }
  | { type: "deployment:bidding"; tenantId: string; dseq: string }
  | { type: "deployment:leased"; tenantId: string; dseq: string; provider: string }
  | { type: "deployment:active"; tenantId: string; dseq: string }
  | { type: "deployment:closed"; tenantId: string; dseq: string }
  | { type: "deployment:error"; tenantId: string; dseq: string; error: string }
  | { type: "lease:refilled"; tenantId: string; dseq: string }
  | { type: "lease:expiring"; tenantId: string; dseq: string; blocksRemaining: number };
```

### Console API Client

```typescript
// console-api-client.ts

export class ConsoleApiClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(baseUrl: string, apiKey: string) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.apiKey = apiKey;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<{ success: boolean; data?: T; error?: { code: string; message: string } }> {
    const url = `${this.baseUrl}/v1${path}`;

    const options: RequestInit = {
      method,
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    return response.json();
  }

  // ── Wallet Operations ──────────────────────────────────────

  async createWallet(name: string): Promise<{
    id: string;
    name: string;
    address: string;
    createdAt: string;
  }> {
    const result = await this.request<{
      id: string;
      name: string;
      address: string;
      createdAt: string;
    }>("POST", "/wallet/create", { name });

    if (!result.success || !result.data) {
      throw new Error(`Failed to create wallet: ${result.error?.message}`);
    }

    return result.data;
  }

  async getBalance(walletId?: string): Promise<
    Array<{ denom: string; amount: string }>
  > {
    const path = walletId
      ? `/wallet/balance?walletId=${walletId}`
      : "/wallet/balance";

    const result = await this.request<{
      address: string;
      balances: Array<{ denom: string; amount: string }>;
    }>("GET", path);

    if (!result.success || !result.data) {
      throw new Error(`Failed to get balance: ${result.error?.message}`);
    }

    return result.data.balances;
  }

  async getDepositAddress(denom: string = "uakt"): Promise<{
    address: string;
    memo: string;
    minimumDeposit: string;
  }> {
    const result = await this.request<{
      address: string;
      memo: string;
      minimumDeposit: string;
    }>("POST", "/wallet/deposit", { denom });

    if (!result.success || !result.data) {
      throw new Error(
        `Failed to get deposit address: ${result.error?.message}`
      );
    }

    return result.data;
  }

  // ── SDL Operations ─────────────────────────────────────────

  async validateSdl(sdl: string): Promise<boolean> {
    const result = await this.request("POST", "/sdl/validate", { sdl });
    return result.success === true;
  }

  async estimatePrice(sdl: string): Promise<string> {
    const result = await this.request<{ price: string }>(
      "POST",
      "/sdl/price",
      { sdl }
    );

    if (!result.success || !result.data) {
      throw new Error(`Failed to estimate price: ${result.error?.message}`);
    }

    return result.data.price;
  }

  // ── Deployment Operations ──────────────────────────────────

  async createDeployment(
    sdl: string,
    deposit: string = "5000000uakt",
    walletId?: string
  ): Promise<{ dseq: string; owner: string; state: string }> {
    const body: Record<string, string> = { sdl, deposit };
    if (walletId) body.walletId = walletId;

    const result = await this.request<{
      dseq: string;
      owner: string;
      state: string;
    }>("POST", "/deployment", body);

    if (!result.success || !result.data) {
      throw new Error(`Failed to create deployment: ${result.error?.message}`);
    }

    return result.data;
  }

  async getDeployment(dseq: string): Promise<{
    dseq: string;
    owner: string;
    state: string;
    escrow?: { balance: string; transferred: string; settled: string };
  }> {
    const result = await this.request("GET", `/deployment/${dseq}`);

    if (!result.success || !result.data) {
      throw new Error(`Failed to get deployment: ${result.error?.message}`);
    }

    return result.data as ReturnType<typeof this.getDeployment> extends Promise<infer T> ? T : never;
  }

  async listDeployments(params?: {
    owner?: string;
    state?: string;
    limit?: number;
    offset?: number;
  }): Promise<Array<{ dseq: string; state: string; owner: string }>> {
    const query = new URLSearchParams();
    if (params?.owner) query.set("owner", params.owner);
    if (params?.state) query.set("state", params.state);
    if (params?.limit) query.set("limit", params.limit.toString());
    if (params?.offset) query.set("offset", params.offset.toString());

    const path = `/deployments${query.toString() ? `?${query}` : ""}`;
    const result = await this.request<{ deployments: Array<{ dseq: string; state: string; owner: string }> }>("GET", path);

    if (!result.success) {
      throw new Error(`Failed to list deployments: ${result.error?.message}`);
    }

    return result.data?.deployments ?? [];
  }

  async closeDeployment(
    dseq: string,
    walletId?: string
  ): Promise<void> {
    const body = walletId ? { walletId } : {};
    const result = await this.request("DELETE", `/deployment/${dseq}`, body);

    if (!result.success) {
      throw new Error(
        `Failed to close deployment ${dseq}: ${result.error?.message}`
      );
    }
  }

  async depositToDeployment(
    dseq: string,
    deposit: string,
    walletId?: string
  ): Promise<void> {
    const body: Record<string, string> = { deposit };
    if (walletId) body.walletId = walletId;

    const result = await this.request(
      "POST",
      `/deployment/${dseq}/deposit`,
      body
    );

    if (!result.success) {
      throw new Error(
        `Failed to deposit to deployment ${dseq}: ${result.error?.message}`
      );
    }
  }

  // ── Bid & Lease Operations ─────────────────────────────────

  async listBids(dseq: string): Promise<
    Array<{
      provider: string;
      price: { denom: string; amount: string };
      dseq: string;
      gseq: number;
      oseq: number;
      state: string;
    }>
  > {
    const result = await this.request<{ bids: any[] }>("GET", `/bids/${dseq}`);

    if (!result.success) {
      throw new Error(`Failed to list bids: ${result.error?.message}`);
    }

    return result.data?.bids ?? [];
  }

  async createLease(
    dseq: string,
    gseq: number,
    oseq: number,
    provider: string,
    walletId?: string
  ): Promise<{ dseq: string; gseq: number; oseq: number; provider: string }> {
    const body: Record<string, unknown> = { dseq, gseq, oseq, provider };
    if (walletId) body.walletId = walletId;

    const result = await this.request("POST", "/lease", body);

    if (!result.success) {
      throw new Error(`Failed to create lease: ${result.error?.message}`);
    }

    return result.data as { dseq: string; gseq: number; oseq: number; provider: string };
  }
}
```

### AuthZ Client

```typescript
// authz-client.ts

import { MsgExec, MsgGrant } from "cosmjs-types/cosmos/authz/v1beta1/tx";
import { GenericAuthorization } from "cosmjs-types/cosmos/authz/v1beta1/authz";
import type { SigningStargateClient } from "@cosmjs/stargate";

// DEPRECATION NOTICE: @akashnetwork/akash-api is deprecated.
// For new projects, use @akashnetwork/chain-sdk for chain interactions.
// AuthZ protobuf types from cosmjs-types remain valid and are not deprecated.

const DEPLOYMENT_MSG_TYPES = {
  CREATE_DEPLOYMENT: "/akash.deployment.v1beta3.MsgCreateDeployment",
  CLOSE_DEPLOYMENT: "/akash.deployment.v1beta3.MsgCloseDeployment",
  DEPOSIT_DEPLOYMENT: "/akash.deployment.v1beta3.MsgDepositDeployment",
  CREATE_LEASE: "/akash.market.v1beta4.MsgCreateLease",
} as const;

export interface GrantVerification {
  allGrantsActive: boolean;
  grants: Record<string, boolean>;
  expiration: Date | null;
}

export class AuthZClient {
  private client: SigningStargateClient;
  private serviceAddress: string;

  constructor(client: SigningStargateClient, serviceAddress: string) {
    this.client = client;
    this.serviceAddress = serviceAddress;
  }

  getServiceAddress(): string {
    return this.serviceAddress;
  }

  // ── Grant Verification ────────────────────────────────────

  async verifyGrants(userAddress: string): Promise<GrantVerification> {
    const grants: Record<string, boolean> = {};
    let earliestExpiration: Date | null = null;

    for (const [, msgType] of Object.entries(DEPLOYMENT_MSG_TYPES)) {
      try {
        const response = await fetch(
          `${this.getRpcEndpoint()}/cosmos/authz/v1beta1/grants?granter=${userAddress}&grantee=${this.serviceAddress}&msg_type_url=${msgType}`
        );

        if (response.ok) {
          const data = await response.json();
          const grant = data.grants?.[0];

          if (grant) {
            const isExpired = grant.expiration
              ? new Date(grant.expiration) < new Date()
              : false;

            grants[msgType] = !isExpired;

            if (grant.expiration) {
              const exp = new Date(grant.expiration);
              if (!earliestExpiration || exp < earliestExpiration) {
                earliestExpiration = exp;
              }
            }
          } else {
            grants[msgType] = false;
          }
        } else {
          grants[msgType] = false;
        }
      } catch {
        grants[msgType] = false;
      }
    }

    const allGrantsActive = Object.values(grants).every(Boolean);

    return {
      allGrantsActive,
      grants,
      expiration: earliestExpiration,
    };
  }

  // ── Fee Grant Check ───────────────────────────────────────

  async checkFeeGrant(userAddress: string): Promise<{
    active: boolean;
    spendLimit: string | null;
    expiration: Date | null;
  }> {
    try {
      const response = await fetch(
        `${this.getRpcEndpoint()}/cosmos/feegrant/v1beta1/allowance/${userAddress}/${this.serviceAddress}`
      );

      if (!response.ok) {
        return { active: false, spendLimit: null, expiration: null };
      }

      const { allowance } = await response.json();

      return {
        active: true,
        spendLimit: allowance?.allowance?.spend_limit?.[0]?.amount ?? null,
        expiration: allowance?.expiration
          ? new Date(allowance.expiration)
          : null,
      };
    } catch {
      return { active: false, spendLimit: null, expiration: null };
    }
  }

  // ── Execute on Behalf of User ─────────────────────────────

  async executeOnBehalf(
    userAddress: string,
    msgs: Array<{ typeUrl: string; value: Uint8Array }>
  ): Promise<string> {
    const execMsg = {
      typeUrl: "/cosmos.authz.v1beta1.MsgExec",
      value: MsgExec.fromPartial({
        grantee: this.serviceAddress,
        msgs: msgs.map((m) => ({
          typeUrl: m.typeUrl,
          value: m.value,
        })),
      }),
    };

    const result = await this.client.signAndBroadcast(
      this.serviceAddress,
      [execMsg],
      "auto"
    );

    if (result.code !== 0) {
      throw new Error(
        `AuthZ execution failed (code ${result.code}): ${result.rawLog}`
      );
    }

    return result.transactionHash;
  }

  private getRpcEndpoint(): string {
    // Use the RPC endpoint from the client or a configured default
    return process.env.AKASH_RPC_ENDPOINT ?? "https://rpc.akash.network";
  }
}
```

### Multi-Tenant Manager

```typescript
// multi-tenant-manager.ts

import { ConsoleApiClient } from "./console-api-client";
import { AuthZClient } from "./authz-client";
import { EventEmitter } from "events";
import type {
  TenantRecord,
  TenantDeployment,
  LeaseRecord,
  DeploymentResult,
  BidStrategy,
  DeployEvent,
  TenantPermissions,
} from "./types";

// ── Tier Permissions ─────────────────────────────────────────

const TIER_LIMITS: Record<string, Omit<TenantPermissions, "tenantId">> = {
  free: {
    tier: "free",
    maxDeployments: 2,
    maxCpuUnits: 2,
    maxMemoryMB: 4096,
    maxStorageGB: 20,
    allowedRegions: [],
    canUseGpu: false,
    canUseCustomSdl: false,
  },
  pro: {
    tier: "pro",
    maxDeployments: 20,
    maxCpuUnits: 20,
    maxMemoryMB: 65536,
    maxStorageGB: 500,
    allowedRegions: [],
    canUseGpu: true,
    canUseCustomSdl: true,
  },
  enterprise: {
    tier: "enterprise",
    maxDeployments: -1,
    maxCpuUnits: -1,
    maxMemoryMB: -1,
    maxStorageGB: -1,
    allowedRegions: [],
    canUseGpu: true,
    canUseCustomSdl: true,
  },
};

// ── Deployment Poller ─────────────────────────────────────────

const BID_WAIT_INTERVAL_MS = 5_000;
const BID_WAIT_TIMEOUT_MS = 120_000;
const LEASE_POLL_INTERVAL_MS = 10_000;
const ESCROW_REFILL_THRESHOLD_BLOCKS = 1000;
const BLOCK_TIME_SECONDS = 6;

export class MultiTenantManager extends EventEmitter {
  private consoleApi: ConsoleApiClient;
  private authzClient: AuthZClient | null;
  private tenants: Map<string, TenantRecord> = new Map();
  private deployments: Map<string, TenantDeployment> = new Map(); // key = dseq
  private leases: Map<string, LeaseRecord> = new Map(); // key = dseq-gseq-oseq
  private pollTimers: Map<string, NodeJS.Timeout> = new Map();
  private maxConcurrentDeploys: number;
  private activeDeploys = 0;

  constructor(
    consoleApiUrl: string,
    consoleApiKey: string,
    authzClient: AuthZClient | null = null,
    maxConcurrentDeploys: number = 10
  ) {
    super();
    this.consoleApi = new ConsoleApiClient(consoleApiUrl, consoleApiKey);
    this.authzClient = authzClient;
    this.maxConcurrentDeploys = maxConcurrentDeploys;
  }

  // ═══════════════════════════════════════════════════════════
  //  TENANT ONBOARDING
  // ═══════════════════════════════════════════════════════════

  /**
   * Onboard a new tenant with a managed wallet.
   * The service creates and controls the wallet via Console API.
   */
  async onboardManagedWalletTenant(
    tenantId: string,
    name: string,
    email: string,
    tier: "free" | "pro" | "enterprise" = "free"
  ): Promise<TenantRecord> {
    // Create managed wallet
    const wallet = await this.consoleApi.createWallet(`tenant-${tenantId}`);

    const tenant: TenantRecord = {
      id: tenantId,
      name,
      email,
      tier,
      walletType: "managed",
      walletId: wallet.id,
      walletAddress: wallet.address,
      granterAddress: null,
      granteeAddress: null,
      grantsVerified: false,
      feeGrantActive: false,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.tenants.set(tenantId, tenant);
    this.emit("tenant:onboarded", { tenantId, walletType: "managed" });

    return tenant;
  }

  /**
   * Onboard a tenant who connects their existing wallet via AuthZ.
   * The user must have already granted AuthZ permissions to the service.
   */
  async onboardAuthZTenant(
    tenantId: string,
    name: string,
    email: string,
    userWalletAddress: string,
    tier: "free" | "pro" | "enterprise" = "free"
  ): Promise<TenantRecord> {
    if (!this.authzClient) {
      throw new Error(
        "AuthZ client not configured. Provide AuthZClient to constructor."
      );
    }

    // Verify grants are active
    const verification = await this.authzClient.verifyGrants(
      userWalletAddress
    );

    if (!verification.allGrantsActive) {
      const missing = Object.entries(verification.grants)
        .filter(([, active]) => !active)
        .map(([msgType]) => msgType);
      throw new Error(
        `Missing or expired AuthZ grants: ${missing.join(", ")}`
      );
    }

    // Check fee grant
    const feeGrant = await this.authzClient.checkFeeGrant(
      userWalletAddress
    );

    const tenant: TenantRecord = {
      id: tenantId,
      name,
      email,
      tier,
      walletType: "authz",
      walletId: null,
      walletAddress: userWalletAddress,
      granterAddress: userWalletAddress,
      granteeAddress: this.authzClient.getServiceAddress(),
      grantsVerified: true,
      feeGrantActive: feeGrant.active,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.tenants.set(tenantId, tenant);
    this.emit("tenant:onboarded", { tenantId, walletType: "authz" });

    return tenant;
  }

  /**
   * Get tenant record by ID.
   */
  getTenant(tenantId: string): TenantRecord | undefined {
    return this.tenants.get(tenantId);
  }

  // ═══════════════════════════════════════════════════════════
  //  DEPLOYMENT OPERATIONS
  // ═══════════════════════════════════════════════════════════

  /**
   * Create a new deployment for a tenant.
   * Handles the full lifecycle: create → bid → select → lease.
   */
  async createDeployment(
    tenantId: string,
    sdl: string,
    deposit: string = "5000000uakt",
    bidStrategy: BidStrategy = "cheapest"
  ): Promise<DeploymentResult> {
    const tenant = this.requireTenant(tenantId);
    this.validateQuota(tenantId);

    // Validate SDL
    const isValid = await this.consoleApi.validateSdl(sdl);
    if (!isValid) {
      throw new Error("Invalid SDL: failed validation");
    }

    // Estimate price
    const estimatedPrice = await this.consoleApi.estimatePrice(sdl);
    this.emit("deployment:estimated", {
      tenantId,
      estimatedPrice,
    });

    // Wait for concurrency slot
    await this.waitForSlot();
    this.activeDeploys++;

    try {
      // Create deployment
      const deployment = await this.consoleApi.createDeployment(
        sdl,
        deposit,
        tenant.walletType === "managed" ? tenant.walletId ?? undefined : undefined
      );

      const dseq = deployment.dseq;

      const record: TenantDeployment = {
        tenantId,
        dseq,
        gseq: 1,
        oseq: 1,
        state: "bidding",
        sdl,
        providerAddress: null,
        leasePrice: null,
        leaseDenom: "uakt",
        createdAt: new Date(),
        updatedAt: new Date(),
        expiresAt: null,
        error: null,
      };

      this.deployments.set(dseq, record);
      this.emitDeployEvent("deployment:created", tenantId, dseq);

      // Wait for bids
      this.emitDeployEvent("deployment:bidding", tenantId, dseq);
      const bids = await this.waitForBids(dseq);

      // Select best bid
      record.state = "selecting";
      const selectedBid = this.selectBid(bids, bidStrategy);

      // Create lease
      record.state = "leasing";
      await this.consoleApi.createLease(
        dseq,
        selectedBid.gseq,
        selectedBid.oseq,
        selectedBid.provider,
        tenant.walletType === "managed"
          ? tenant.walletId ?? undefined
          : undefined
      );

      // Update record
      record.state = "active";
      record.providerAddress = selectedBid.provider;
      record.leasePrice = selectedBid.price.amount;
      record.updatedAt = new Date();

      this.emitDeployEvent("deployment:leased", tenantId, dseq);
      this.emitDeployEvent("deployment:active", tenantId, dseq);

      return {
        dseq,
        provider: selectedBid.provider,
        price: selectedBid.price.amount,
        state: "active",
      };
    } catch (error) {
      const dseq = "unknown";
      this.emit("deployment:error", {
        type: "deployment:error",
        tenantId,
        dseq,
        error: error instanceof Error ? error.message : String(error),
      });
      throw error;
    } finally {
      this.activeDeploys--;
    }
  }

  /**
   * Get deployment status for a tenant.
   */
  async getDeploymentStatus(
    tenantId: string,
    dseq: string
  ): Promise<TenantDeployment> {
    const record = this.deployments.get(dseq);

    if (!record || record.tenantId !== tenantId) {
      throw new Error(
        `Deployment ${dseq} not found for tenant ${tenantId}`
      );
    }

    // Refresh state from Console API
    try {
      const chainState = await this.consoleApi.getDeployment(dseq);
      record.state = this.mapChainState(chainState.state);
      record.updatedAt = new Date();
    } catch {
      // Return cached state if API call fails
    }

    return { ...record };
  }

  /**
   * List all deployments for a tenant.
   */
  listTenantDeployments(tenantId: string): TenantDeployment[] {
    return Array.from(this.deployments.values()).filter(
      (d) => d.tenantId === tenantId
    );
  }

  /**
   * Close a deployment.
   */
  async closeDeployment(
    tenantId: string,
    dseq: string
  ): Promise<void> {
    const record = this.deployments.get(dseq);

    if (!record || record.tenantId !== tenantId) {
      throw new Error(
        `Deployment ${dseq} not found for tenant ${tenantId}`
      );
    }

    const tenant = this.requireTenant(tenantId);

    await this.consoleApi.closeDeployment(
      dseq,
      tenant.walletType === "managed"
        ? tenant.walletId ?? undefined
        : undefined
    );

    record.state = "closed";
    record.updatedAt = new Date();

    // Cleanup poll timer if active
    const timer = this.pollTimers.get(dseq);
    if (timer) {
      clearInterval(timer);
      this.pollTimers.delete(dseq);
    }

    this.emitDeployEvent("deployment:closed", tenantId, dseq);
  }

  // ═══════════════════════════════════════════════════════════
  //  LEASE MANAGEMENT
  // ═══════════════════════════════════════════════════════════

  /**
   * Start monitoring all active leases.
   * Emits events for low-balance and expired leases.
   */
  startLeaseMonitoring(
    intervalMs: number = 60_000
  ): void {
    const timer = setInterval(async () => {
      try {
        await this.refreshAllLeases();
        await this.checkEscrowLevels();
      } catch (error) {
        this.emit("monitor:error", {
          error: error instanceof Error ? error.message : String(error),
        });
      }
    }, intervalMs);

    this.pollTimers.set("__lease_monitor__", timer);
  }

  /**
   * Stop all monitoring.
   */
  stopMonitoring(): void {
    for (const timer of this.pollTimers.values()) {
      clearInterval(timer);
    }
    this.pollTimers.clear();
  }

  /**
   * Get all leases across all tenants.
   */
  getAllLeases(): LeaseRecord[] {
    return Array.from(this.leases.values());
  }

  /**
   * Get leases for a specific tenant.
   */
  getTenantLeases(tenantId: string): LeaseRecord[] {
    return Array.from(this.leases.values()).filter(
      (l) => l.tenantId === tenantId
    );
  }

  /**
   * Refill escrow for a deployment.
   */
  async refillDeployment(
    tenantId: string,
    dseq: string,
    amount: string = "5000000uakt"
  ): Promise<void> {
    const record = this.deployments.get(dseq);

    if (!record || record.tenantId !== tenantId) {
      throw new Error(
        `Deployment ${dseq} not found for tenant ${tenantId}`
      );
    }

    const tenant = this.requireTenant(tenantId);

    await this.consoleApi.depositToDeployment(
      dseq,
      amount,
      tenant.walletType === "managed"
        ? tenant.walletId ?? undefined
        : undefined
    );

    this.emit("lease:refilled", {
      type: "lease:refilled",
      tenantId,
      dseq,
    });
  }

  /**
   * Cleanup closed deployments older than retention period.
   */
  cleanupClosedDeployments(retentionDays: number = 7): number {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - retentionDays);

    let cleaned = 0;

    for (const [dseq, deployment] of this.deployments.entries()) {
      if (deployment.state === "closed" && deployment.updatedAt < cutoff) {
        this.deployments.delete(dseq);
        this.leases.delete(dseq);
        cleaned++;
      }
    }

    return cleaned;
  }

  // ═══════════════════════════════════════════════════════════
  //  WALLET OPERATIONS
  // ═══════════════════════════════════════════════════════════

  /**
   * Get tenant wallet balance.
   */
  async getTenantBalance(
    tenantId: string
  ): Promise<Array<{ denom: string; amount: string }>> {
    const tenant = this.requireTenant(tenantId);

    if (tenant.walletType === "managed") {
      return this.consoleApi.getBalance(
        tenant.walletId ?? undefined
      );
    }

    // For AuthZ tenants, query chain directly
    const rpc = process.env.AKASH_RPC_ENDPOINT ?? "https://rpc.akash.network";
    const response = await fetch(
      `${rpc}/cosmos/bank/v1beta1/balances/${tenant.walletAddress}`
    );
    const { balances } = await response.json();
    return balances ?? [];
  }

  /**
   * Get deposit address for a managed wallet tenant.
   */
  async getDepositAddress(
    tenantId: string,
    denom: string = "uakt"
  ): Promise<{ address: string; memo: string }> {
    const tenant = this.requireTenant(tenantId);

    if (tenant.walletType !== "managed") {
      throw new Error(
        "Deposit addresses only available for managed wallet tenants"
      );
    }

    const depositInfo = await this.consoleApi.getDepositAddress(denom);
    return {
      address: depositInfo.address,
      memo: depositInfo.memo,
    };
  }

  // ═══════════════════════════════════════════════════════════
  //  PRIVATE HELPERS
  // ═══════════════════════════════════════════════════════════

  private requireTenant(tenantId: string): TenantRecord {
    const tenant = this.tenants.get(tenantId);
    if (!tenant) {
      throw new Error(`Tenant not found: ${tenantId}`);
    }
    return tenant;
  }

  private validateQuota(tenantId: string): void {
    const tenant = this.requireTenant(tenantId);
    const limits = TIER_LIMITS[tenant.tier];
    const currentCount = this.listTenantDeployments(tenantId).filter(
      (d) => d.state !== "closed" && d.state !== "error"
    ).length;

    if (limits.maxDeployments !== -1 && currentCount >= limits.maxDeployments) {
      throw new Error(
        `Deployment limit reached (${limits.maxDeployments}) for tenant ${tenantId} on ${tenant.tier} tier`
      );
    }
  }

  private async waitForSlot(): Promise<void> {
    while (this.activeDeploys >= this.maxConcurrentDeploys) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }

  private async waitForBids(
    dseq: string
  ): Promise<
    Array<{
      provider: string;
      price: { denom: string; amount: string };
      dseq: string;
      gseq: number;
      oseq: number;
    }>
  > {
    const start = Date.now();

    while (Date.now() - start < BID_WAIT_TIMEOUT_MS) {
      const bids = await this.consoleApi.listBids(dseq);

      if (bids.length > 0) {
        return bids;
      }

      await new Promise((resolve) =>
        setTimeout(resolve, BID_WAIT_INTERVAL_MS)
      );
    }

    throw new Error(
      `Timeout waiting for bids on deployment ${dseq} (${BID_WAIT_TIMEOUT_MS / 1000}s)`
    );
  }

  private selectBid(
    bids: Array<{
      provider: string;
      price: { denom: string; amount: string };
      dseq: string;
      gseq: number;
      oseq: number;
    }>,
    strategy: BidStrategy
  ): (typeof bids)[0] {
    switch (strategy) {
      case "cheapest":
        return bids.sort((a, b) =>
          BigInt(a.price.amount) < BigInt(b.price.amount) ? -1 : 1
        )[0];
      case "fastest":
        return bids[0];
      case "reputable":
        // In production, factor in provider reputation/uptime
        return bids.sort((a, b) =>
          BigInt(a.price.amount) < BigInt(b.price.amount) ? -1 : 1
        )[0];
      default:
        return bids[0];
    }
  }

  private async refreshAllLeases(): Promise<void> {
    for (const [dseq, deployment] of this.deployments.entries()) {
      if (deployment.state !== "active") continue;

      try {
        const chainState = await this.consoleApi.getDeployment(dseq);
        deployment.state = this.mapChainState(chainState.state);
        deployment.updatedAt = new Date();

        if (chainState.escrow) {
          const escrow = chainState.escrow;
          const remaining =
            BigInt(escrow.balance) - BigInt(escrow.settled);

          const leaseRecord = this.leases.get(dseq);
          if (leaseRecord && leaseRecord.pricePerBlock) {
            const rate = BigInt(leaseRecord.pricePerBlock.amount);
            if (rate > 0n) {
              const blocksRemaining = remaining / rate;
              leaseRecord.estimatedExpiry = new Date(
                Date.now() + Number(blocksRemaining) * BLOCK_TIME_SECONDS * 1000
              );
              leaseRecord.totalCostSpent = escrow.settled;
            }
          }
        }
      } catch {
        // Continue processing other leases on error
      }
    }
  }

  private async checkEscrowLevels(): Promise<void> {
    for (const [dseq, lease] of this.leases.entries()) {
      if (lease.state !== "active" || !lease.estimatedExpiry) continue;

      const blocksRemaining = Math.floor(
        (lease.estimatedExpiry.getTime() - Date.now()) /
          (BLOCK_TIME_SECONDS * 1000)
      );

      if (blocksRemaining < ESCROW_REFILL_THRESHOLD_BLOCKS) {
        this.emit("lease:expiring", {
          type: "lease:expiring",
          tenantId: lease.tenantId,
          dseq,
          blocksRemaining,
        });

        // Auto-refill if tenant has sufficient balance
        try {
          await this.refillDeployment(lease.tenantId, dseq);
        } catch {
          this.emit("lease:refill_failed", {
            tenantId: lease.tenantId,
            dseq,
            blocksRemaining,
          });
        }
      }
    }
  }

  private mapChainState(
    chainState: string
  ): TenantDeployment["state"] {
    switch (chainState) {
      case "active":
        return "active";
      case "closed":
        return "closed";
      case "inactive":
        return "error";
      default:
        return "active";
    }
  }

  private emitDeployEvent(
    type: DeployEvent["type"],
    tenantId: string,
    dseq: string
  ): void {
    this.emit(type, { type, tenantId, dseq });
  }
}
```

### Service Bootstrap

```typescript
// index.ts — Service entry point

import { MultiTenantManager } from "./multi-tenant-manager";
import { AuthZClient } from "./authz-client";
import type { DeployEvent } from "./types";

// ── Configuration ──────────────────────────────────────────────

const CONSOLE_API_URL =
  process.env.CONSOLE_API_URL ??
  "https://console-api.akash.network";

const CONSOLE_API_KEY =
  process.env.CONSOLE_API_KEY ?? "";

const SANDBOX_MODE = process.env.SANDBOX === "true";

const SANDBOX_API_URL = "https://console-api.sandbox-01.aksh.pw";

// ── Initialize Service ─────────────────────────────────────────

async function bootstrap(): Promise<void> {
  const apiUrl = SANDBOX_MODE ? SANDBOX_API_URL : CONSOLE_API_URL;

  // AuthZ client is optional — only needed if accepting user-owned wallets
  // Initialize with your service's signing client if AuthZ is enabled
  let authzClient: AuthZClient | null = null;
  // if (process.env.AUTHZ_ENABLED === "true") {
  //   const client = await SigningStargateClient.connectWithSigner(
  //     process.env.AKASH_RPC_ENDPOINT!,
  //     signer
  //   );
  //   authzClient = new AuthZClient(client, serviceAddress);
  // }

  const manager = new MultiTenantManager(
    apiUrl,
    CONSOLE_API_KEY,
    authzClient
  );

  // ── Event Listeners ─────────────────────────────────────────

  manager.on("tenant:onboarded", ({ tenantId, walletType }) => {
    console.log(`[TENANT] Onboarded ${tenantId} via ${walletType}`);
  });

  manager.on("deployment:active", ({ tenantId, dseq }) => {
    console.log(`[DEPLOY] Active: ${dseq} (tenant: ${tenantId})`);
  });

  manager.on("deployment:error", ({ tenantId, dseq, error }) => {
    console.error(
      `[ERROR] Deployment ${dseq} failed for tenant ${tenantId}: ${error}`
    );
  });

  manager.on("lease:expiring", ({ tenantId, dseq, blocksRemaining }) => {
    console.warn(
      `[LEASE] Expiring: ${dseq} (tenant: ${tenantId}, blocks remaining: ${blocksRemaining})`
    );
  });

  manager.on("lease:refilled", ({ tenantId, dseq }) => {
    console.log(`[LEASE] Refilled: ${dseq} (tenant: ${tenantId})`);
  });

  manager.on("monitor:error", ({ error }) => {
    console.error(`[MONITOR] Error: ${error}`);
  });

  // ── Start Lease Monitoring ──────────────────────────────────

  manager.startLeaseMonitoring(60_000); // Poll every 60s

  // ── Example: Onboard a Managed Wallet Tenant ────────────────

  const tenant = await manager.onboardManagedWalletTenant(
    "demo-tenant-001",
    "Demo Corp",
    "admin@democorp.example",
    "pro"
  );

  console.log("Tenant onboarded:", {
    id: tenant.id,
    address: tenant.walletAddress,
    walletType: tenant.walletType,
  });

  // ── Example: Get Balance ────────────────────────────────────

  const balance = await manager.getTenantBalance(tenant.id);
  console.log(
    "Tenant balance:",
    balance.map((b) => `${b.amount} ${b.denom}`)
  );

  // ── Example: Deploy ─────────────────────────────────────────

  const sdl = `
version: "2.0"
services:
  web:
    image: nginx:1.25.3
    expose:
      - port: 80
        to:
          - global: true
profiles:
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 512Mi
        storage:
          size: 1Gi
  placement:
    dcloud:
      pricing:
        web:
          denom: uact
          amount: 1000
deployment:
  web:
    dcloud:
      profile: web
      count: 1
`.trim();

  try {
    const result = await manager.createDeployment(
      tenant.id,
      sdl,
      "5000000uakt",
      "cheapest"
    );

    console.log("Deployment created:", result);
  } catch (error) {
    console.error(
      "Deployment failed:",
      error instanceof Error ? error.message : error
    );
  }

  // ── Graceful Shutdown ───────────────────────────────────────

  process.on("SIGINT", () => {
    console.log("\nShutting down...");
    manager.stopMonitoring();
    process.exit(0);
  });

  process.on("SIGTERM", () => {
    manager.stopMonitoring();
    process.exit(0);
  });
}

bootstrap().catch((error) => {
  console.error("Service bootstrap failed:", error);
  process.exit(1);
});
```

### Environment Configuration

```bash
# .env

# Console API
CONSOLE_API_URL=https://console-api.akash.network
CONSOLE_API_KEY=your-api-key-here

# Sandbox mode (use sandbox Console API)
SANDBOX=false

# AuthZ (optional, for user-owned wallets)
AUTHZ_ENABLED=false
AKASH_RPC_ENDPOINT=https://rpc.akash.network:443
SERVICE_MNEMONIC=your service wallet mnemonic here

# Monitoring
LEASE_POLL_INTERVAL_MS=60000
ESCROW_REFILL_THRESHOLD=1000

# Service
MAX_CONCURRENT_DEPLOYS=10
PORT=3000
```

---

## Migration: @akashnetwork/akash-api → @akashnetwork/chain-sdk

The older `@akashnetwork/akash-api` package is **deprecated**. For new projects, use `@akashnetwork/chain-sdk`.

| Old (@akashnetwork/akash-api) | New (@akashnetwork/chain-sdk) |
|------|------|
| `import { MsgCreateDeployment } from "@akashnetwork/akash-api/akash/deployment/v1beta3"` | `import { MsgCreateDeployment } from "@akashnetwork/chain-sdk"` |
| `SDL.fromString(sdl)` | Use SDL parsing from chain-sdk or construct messages directly |
| `SigningStargateClient` from `@cosmjs/stargate` | `SigningStargateClient` from `@cosmjs/stargate` (unchanged) |
| `akashjs` for queries | chain-sdk includes query clients |

**Key differences:**

- `@akashnetwork/chain-sdk` provides a unified import path and improved TypeScript types
- AuthZ protobuf types (`cosmjs-types/cosmos/authz/v1beta1/*`) are **not** deprecated and work with both packages
- The Console API client pattern (REST calls) remains unchanged regardless of SDK choice

---

## Summary

Building a multi-tenant deployment service on Akash involves:

1. **Choose wallet strategy** — Managed wallets for simplicity, AuthZ for user-controlled keys
2. **Implement tenant onboarding** — Create managed wallets or verify AuthZ grants
3. **Build deployment orchestrator** — Handle the full lifecycle per tenant with concurrency control
4. **Monitor leases** — Track escrow levels, auto-refill, and alert on expiry
5. **Secure the service** — Per-tenant isolation, API key rotation, encrypted key storage
6. **Scale with queues** — Use deployment queues and rate limiting for high-traffic scenarios

The Console API simplifies managed wallet operations, while AuthZ enables trustless delegation for crypto-native users. A production service should support both strategies to serve the widest range of users.
