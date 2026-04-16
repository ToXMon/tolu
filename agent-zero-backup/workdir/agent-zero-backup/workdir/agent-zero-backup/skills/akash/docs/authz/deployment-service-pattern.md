# Deployment Service Pattern — AuthZ + FeeGrant + Managed Wallet

> ⚠️ **Note:** Some examples use `@akashnetwork/akash-api` which has been deprecated. Use `@akashnetwork/chain-sdk` instead.

## Overview

This document describes the end-to-end pattern for building a managed deployment service on Akash that combines three delegation mechanisms:

- **AuthZ** — Users authorize a service account to create and manage deployments on their behalf.
- **FeeGrant** — Users (or a sponsor) pay gas fees for on-chain transactions, so end users never hold AKT for gas.
- **Managed Wallet** — Console API wallets let users deploy without managing private keys directly.

The result is a three-party flow where the **User** interacts only with your **Service**, and the **Service** handles all on-chain operations against the **Akash Network**.

### Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Deployment Service                        │
│                                                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐  │
│  │ AuthZ Engine │   │ FeeGrant     │   │ Console API Client   │  │
│  │ MsgExec      │   │ Sponsor      │   │ Managed Wallets      │  │
│  │ Grant Mgmt   │   │ MsgGrant     │   │ Deposit Tracking     │  │
│  └──────┬───────┘   └──────┬───────┘   └──────────┬───────────┘  │
│         │                  │                      │              │
│         └──────────────────┼──────────────────────┘              │
│                            │                                     │
│                   ┌────────▼────────┐                            │
│                   │ Service Account │                            │
│                   │ (Grantee/Signer)│                            │
│                   └────────┬────────┘                            │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Akash Network   │
                    │  (akashnet-2)    │
                    └─────────────────┘

┌──────────┐                        ┌──────────────────┐
│   User   │───── REST/API ────────▶│ Deployment Svc   │
│          │                        │                  │
│  Wallet  │─── Grant AuthZ ────▶  │ Service Account  │─── MsgExec ──▶ Akash
│          │                        │                  │
│  Funds   │─── Grant FeeAllow ──▶ │ Service Account  │─── Tx fees ──▶ Akash
│          │                        │                  │
│  (or)    │                        │ Console API      │─── Deploy ───▶ Provider
│  Managed │─── Deposit to WAL ──▶ │ Managed Wallet   │─── Manifest ─▶ Provider
│  Wallet  │                        │                  │
└──────────┘                        └──────────────────┘
```

### Data Flow Summary

```
 1. User                    → Service : "Create deployment" (SDL + config)
 2. Service (on behalf)     → Akash   : MsgCreateDeployment (via MsgExec)
 3. Akash                   → Service : Bids received
 4. Service (on behalf)     → Akash   : MsgCreateLease (via MsgExec)
 5. Service                 → Provider: Send manifest
 6. Service                 → Akash   : Monitor lease status
 7. Service (on behalf)     → Akash   : MsgCloseDeployment (via MsgExec)
```

## Prerequisites

```bash
npm install @akashnetwork/chain-sdk @cosmjs/proto-signing @cosmjs/stargate cosmjs-types
```

### Constants

```typescript
// ── Network Configuration ──────────────────────────────────────────
const CHAIN_ID = "akashnet-2";
const RPC_ENDPOINT = "https://rpc.akashnet.net:443";
const CONSOLE_API_BASE = "https://console-api.akash.network";
const DEPLOYMENT_DEPOSIT_DENOM = "uakt";
const GAS_DENOM = "uakt";
const GAS_PRICE = "0.025uakt";

// ── AuthZ Type URLs ───────────────────────────────────────────────
const MSG_CREATE_DEPLOYMENT_URL = "/akash.deployment.v1beta3.MsgCreateDeployment";
const MSG_CLOSE_DEPLOYMENT_URL = "/akash.deployment.v1beta3.MsgCloseDeployment";
const MSG_DEPOSIT_DEPLOYMENT_URL = "/akash.deployment.v1beta3.MsgDepositDeployment";
const MSG_CREATE_LEASE_URL = "/akash.market.v1beta4.MsgCreateLease";
const MSG_GRANT_ALLOWANCE_URL = "/cosmos.feegrant.v1beta1.MsgGrantAllowance";

// ── Default Grant Duration ────────────────────────────────────────
const DEFAULT_GRANT_DURATION_DAYS = 90;
const DEFAULT_DEPLOYMENT_DEPOSIT = "5000000"; // 5 AKT
```

### Types

```typescript
import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";
import { SigningStargateClient, GasPrice, DeliverTxResponse } from "@cosmjs/stargate";
import { MsgExec, MsgGrant } from "cosmjs-types/cosmos/authz/v1beta1/tx";
import { GenericAuthorization } from "cosmjs-types/cosmos/authz/v1beta1/authz";
import { MsgGrantAllowance } from "cosmjs-types/cosmos/feegrant/v1beta1/tx";
import { BasicAllowance } from "cosmjs-types/cosmos/feegrant/v1beta1/feegrant";
import { Timestamp } from "cosmjs-types/google/protobuf/timestamp";

interface DeploymentServiceConfig {
  serviceMnemonic: string;
  rpcEndpoint?: string;
  consoleApiKey?: string;
  gasPrice?: string;
}

interface CreateUserResult {
  address: string;
  mnemonic?: string; // only returned for self-custodial wallets
  walletId?: string; // Console API managed wallet ID
  depositAddress?: string;
}

interface GrantResult {
  txHash: string;
  height: number;
  grantType: "authz" | "feegrant";
  msgTypeUrl?: string;
  expiration: Date;
}

interface CreateDeploymentResult {
  dseq: string;
  owner: string;
  txHash: string;
  height: number;
}

interface LeaseInfo {
  dseq: string;
  gseq: number;
  oseq: number;
  provider: string;
  state: string;
  price: { denom: string; amount: string };
}

interface CloseDeploymentResult {
  dseq: string;
  txHash: string;
  height: number;
}

interface ServiceContext {
  userAddress: string;
  grants: {
    hasDeploymentGrant: boolean;
    hasCloseGrant: boolean;
    hasLeaseGrant: boolean;
    hasFeeGrant: boolean;
    feeGrantExpiration?: Date;
    authzExpiration?: Date;
  };
  deploymentCount: number;
  activeLeases: number;
}
```

### Service Initialization

```typescript
class AkashDeploymentService {
  private client: SigningStargateClient;
  private serviceAddress: string;
  private config: Required<DeploymentServiceConfig>;

  constructor() {
    this.client = null!;
    this.serviceAddress = "";
    this.config = null!;
  }

  async initialize(config: DeploymentServiceConfig): Promise<void> {
    this.config = {
      serviceMnemonic: config.serviceMnemonic,
      rpcEndpoint: config.rpcEndpoint ?? RPC_ENDPOINT,
      consoleApiKey: config.consoleApiKey ?? "",
      gasPrice: config.gasPrice ?? GAS_PRICE,
    };

    const wallet = await DirectSecp256k1HdWallet.fromMnemonic(
      this.config.serviceMnemonic,
      { prefix: "akash" }
    );

    const [account] = await wallet.getAccounts();
    this.serviceAddress = account.address;

    // Import the Akash type registry to handle custom message types
    // With @akashnetwork/chain-sdk, use the exported registry helper:
    //   import { getAkashTypeRegistry } from "@akashnetwork/chain-sdk";
    // Migration note: Previously this came from @akashnetwork/akashjs/build/stargate
    const { getAkashTypeRegistry } = await import("@akashnetwork/chain-sdk");
    const registry = getAkashTypeRegistry();

    this.client = await SigningStargateClient.connectWithSigner(
      this.config.rpcEndpoint,
      wallet,
      {
        registry,
        gasPrice: GasPrice.fromString(this.config.gasPrice),
      }
    );
  }

  getServiceAddress(): string {
    return this.serviceAddress;
  }
}
```

---

## Step 1 — User Creates Wallet

The user needs an Akash address. Offer two paths: **self-custodial** (user holds mnemonic) or **managed** (Console API holds keys).

### Self-Custodial Wallet

```typescript
async function createSelfCustodialWallet(): Promise<CreateUserResult> {
  const wallet = await DirectSecp256k1HdWallet.generate(24, { prefix: "akash" });
  const [account] = await wallet.getAccounts();
  const mnemonic = wallet.mnemonic;

  // IMPORTANT: Return the mnemonic to the user exactly once.
  // Never store it server-side in production.
  return {
    address: account.address,
    mnemonic,
  };
}
```

### Managed Wallet via Console API

```typescript
async function createManagedWallet(
  apiKey: string,
  name: string = "deployment-service"
): Promise<CreateUserResult> {
  const response = await fetch(`${CONSOLE_API_BASE}/v1/wallet/create`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name }),
  });

  if (!response.ok) {
    throw new Error(
      `Failed to create managed wallet: ${response.status} ${await response.text()}`
    );
  }

  const result = await response.json();
  if (!result.success) {
    throw new Error(`Console API error: ${JSON.stringify(result)}`);
  }

  // Retrieve deposit address for user funding
  const depositResponse = await fetch(`${CONSOLE_API_BASE}/v1/wallet/deposit`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ denom: DEPLOYMENT_DEPOSIT_DENOM }),
  });

  const depositResult = await depositResponse.json();

  return {
    address: result.data.address,
    walletId: result.data.id,
    depositAddress: depositResult.success
      ? depositResult.data.address
      : result.data.address,
  };
}
```

### Error Handling — Step 1

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Console API unreachable | `fetch` throws / status 5xx | Retry with exponential backoff; fall back to self-custodial |
| Invalid API key | Status 401 | Alert operator; do not retry automatically |
| Rate limited | Status 429 | Respect `Retry-After` header |
| Wallet already exists for user | Status 409 | Return existing wallet instead |

---

## Step 2 — User Grants AuthZ Permissions to Service

The user authorizes the service account (grantee) to execute deployment messages on their behalf.

### Granting Permissions (Called by User)

The user signs a `MsgGrant` transaction from their own wallet, authorizing the service address.

```typescript
import { GenericAuthorization } from "cosmjs-types/cosmos/authz/v1beta1/authz";
import { MsgGrant } from "cosmjs-types/cosmos/authz/v1beta1/tx";

interface AuthzGrantParams {
  userClient: SigningStargateClient;
  userAddress: string;
  serviceAddress: string;
  expirationDays?: number;
}

/**
 * Grant deployment lifecycle permissions to the service account.
 * This transaction is signed and paid for by the USER.
 */
async function grantDeploymentAuthz(params: AuthzGrantParams): Promise<GrantResult[]> {
  const {
    userClient,
    userAddress,
    serviceAddress,
    expirationDays = DEFAULT_GRANT_DURATION_DAYS,
  } = params;

  const expiration = new Date();
  expiration.setDate(expiration.getDate() + expirationDays);

  const expirationTimestamp: Timestamp = {
    seconds: BigInt(Math.floor(expiration.getTime() / 1000)),
    nanos: 0,
  };

  // Grant messages the service needs
  const requiredGrants = [
    MSG_CREATE_DEPLOYMENT_URL,
    MSG_CLOSE_DEPLOYMENT_URL,
    MSG_DEPOSIT_DEPLOYMENT_URL,
    MSG_CREATE_LEASE_URL,
  ];

  const messages = requiredGrants.map((msgTypeUrl) => {
    const authorization = GenericAuthorization.fromPartial({
      msg: msgTypeUrl,
    });

    return {
      typeUrl: "/cosmos.authz.v1beta1.MsgGrant",
      value: MsgGrant.fromPartial({
        granter: userAddress,
        grantee: serviceAddress,
        grant: {
          authorization: {
            typeUrl: "/cosmos.authz.v1beta1.GenericAuthorization",
            value: GenericAuthorization.encode(authorization).finish(),
          },
          expiration: expirationTimestamp,
        },
      }),
    };
  });

  const result: DeliverTxResponse = await userClient.signAndBroadcast(
    userAddress,
    messages,
    "auto"
  );

  if (result.code !== 0) {
    throw new Error(`AuthZ grant failed: code ${result.code} — ${result.rawLog}`);
  }

  return requiredGrants.map((msgTypeUrl) => ({
    txHash: result.transactionHash,
    height: result.height,
    grantType: "authz" as const,
    msgTypeUrl,
    expiration,
  }));
}
```

### Verifying Grants Exist (Called by Service)

```typescript
import { QueryClientImpl as AuthzQueryClient } from "cosmjs-types/cosmos/authz/v1beta1/query";

async function verifyAuthzGrants(
  client: SigningStargateClient,
  userAddress: string,
  serviceAddress: string
): Promise<{ hasCreateDeployment: boolean; hasCloseDeployment: boolean; hasCreateLease: boolean }> {
  // Use the stargate query client to check grants
  // Note: Cosmos SDK AuthZ query is /cosmos.authz.v1beta1.Query/Grants
  const queryClient = client.getQueryClient();
  if (!queryClient) {
    throw new Error("Query client not available");
  }

  // Check each grant type individually
  const [createDep, closeDep, createLease] = await Promise.all([
    queryClient.authz.grants(userAddress, serviceAddress, MSG_CREATE_DEPLOYMENT_URL)
      .then((r: any) => r.grants?.length > 0)
      .catch(() => false),
    queryClient.authz.grants(userAddress, serviceAddress, MSG_CLOSE_DEPLOYMENT_URL)
      .then((r: any) => r.grants?.length > 0)
      .catch(() => false),
    queryClient.authz.grants(userAddress, serviceAddress, MSG_CREATE_LEASE_URL)
      .then((r: any) => r.grants?.length > 0)
      .catch(() => false),
  ]);

  return {
    hasCreateDeployment: createDep,
    hasCloseDeployment: closeDep,
    hasCreateLease: createLease,
  };
}
```

### Error Handling — Step 2

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Grant already exists | Tx fails with `codespace: authz, code: 9` | Query existing grants; skip if valid and not expired |
| Insufficient gas funds | Tx fails with `insufficient fees` | Prompt user to fund wallet; suggest minimum balance |
| Grant expired | Query returns empty grants | Re-request grant from user |
| Wrong grantee address | Grant exists but for different address | Alert user; provide correct service address |

---

## Step 3 — User Grants Fee Allowance to Service (Optional)

This step lets the **user** sponsor gas fees for the service's on-chain transactions executed on their behalf. Without this, the **service** pays gas from its own account.

```typescript
import { MsgGrantAllowance } from "cosmjs-types/cosmos/feegrant/v1beta1/tx";
import { BasicAllowance } from "cosmjs-types/cosmos/feegrant/v1beta1/feegrant";
import { Coin } from "cosmjs-types/cosmos/base/v1beta1/coin";

interface FeeGrantParams {
  userClient: SigningStargateClient;
  userAddress: string;
  serviceAddress: string;
  spendLimit?: string; // e.g. "10000000" for 10 AKT cap; omit for unlimited
  expirationDays?: number;
}

/**
 * User grants a fee allowance to the service account.
 * After this, the service can specify --fee-granter=<userAddress>
 * and the user's AKT pays for gas.
 */
async function grantFeeAllowance(params: FeeGrantParams): Promise<GrantResult> {
  const {
    userClient,
    userAddress,
    serviceAddress,
    spendLimit,
    expirationDays = DEFAULT_GRANT_DURATION_DAYS,
  } = params;

  const expiration = new Date();
  expiration.setDate(expiration.getDate() + expirationDays);

  const expirationTimestamp: Timestamp = {
    seconds: BigInt(Math.floor(expiration.getTime() / 1000)),
    nanos: 0,
  };

  // Build the BasicAllowance
  const allowance = BasicAllowance.fromPartial({
    spendLimit: spendLimit
      ? [{ denom: GAS_DENOM, amount: spendLimit } as unknown as Coin]
      : undefined, // undefined = unlimited
    expiration: expirationTimestamp,
  });

  const msg = {
    typeUrl: "/cosmos.feegrant.v1beta1.MsgGrantAllowance",
    value: MsgGrantAllowance.fromPartial({
      granter: userAddress,
      grantee: serviceAddress,
      allowance: {
        typeUrl: "/cosmos.feegrant.v1beta1.BasicAllowance",
        value: BasicAllowance.encode(allowance).finish(),
      },
    }),
  };

  const result: DeliverTxResponse = await userClient.signAndBroadcast(
    userAddress,
    [msg],
    "auto"
  );

  if (result.code !== 0) {
    throw new Error(`FeeGrant failed: code ${result.code} — ${result.rawLog}`);
  }

  return {
    txHash: result.transactionHash,
    height: result.height,
    grantType: "feegrant",
    expiration,
  };
}
```

### Using Fee Grants When Executing

When the service broadcasts a `MsgExec`, it includes the `feeGranter` option:

```typescript
// The fee payer is the user, not the service
const result = await this.client.signAndBroadcast(
  this.serviceAddress,   // signer = grantee
  [execMsg],
  {
    amount: [{ denom: GAS_DENOM, amount: "5000" }],
    gas: "500000",
    granter: userAddress,  // user pays gas via their fee grant
  }
);
```

### Error Handling — Step 3

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Fee grant already exists | Tx fails with `codespace: feegrant, code: 10` | Query existing allowance; skip if valid |
| Spend limit exceeded | Tx fails with `fee grant exhausted` | Notify user to renew or increase allowance |
| Allowance expired | Tx fails with `fee allowance expired` | Request new fee grant from user |
| User has insufficient balance | Tx fails at grant time | Inform user of minimum funding requirement |

---

## Step 4 — Service Creates Deployment on User's Behalf

This is the core of the pattern. The service wraps `MsgCreateDeployment` inside `MsgExec`, signing as the grantee.

```typescript
import { MsgExec } from "cosmjs-types/cosmos/authz/v1beta1/tx";

interface CreateDeploymentParams {
  userAddress: string;
  sdl: ParsedSDL;
  dseq?: string;
  deposit?: string;
  useFeeGrant?: boolean;
}

interface ParsedSDL {
  groups: any[];       // SDL group specifications
  version: Uint8Array; // manifest version hash
}

/**
 * Parse and validate an SDL, then create a deployment on-chain
 * on behalf of the user via AuthZ MsgExec.
 *
 * With @akashnetwork/chain-sdk, SDL parsing uses:
 *   import { SDL } from "@akashnetwork/chain-sdk/sdl";
 * Migration note: Previously SDL came from @akashnetwork/akashjs/build/sdl
 */
async function createDeploymentOnBehalf(
  service: AkashDeploymentService,
  params: CreateDeploymentParams
): Promise<CreateDeploymentResult> {
  const {
    userAddress,
    sdl,
    dseq,
    deposit = DEFAULT_DEPLOYMENT_DEPOSIT,
    useFeeGrant = false,
  } = params;

  // DSEQ must be unique per deployment; use current block height or timestamp
  const effectiveDseq = dseq ?? BigInt(Date.now()).toString();

  // Build the inner MsgCreateDeployment — from the USER's perspective
  const innerMsg = {
    id: {
      owner: userAddress,             // user owns the deployment
      dseq: BigInt(effectiveDseq),
    },
    groups: sdl.groups,
    version: sdl.version,
    deposit: {
      denom: DEPLOYMENT_DEPOSIT_DENOM,
    },
    depositor: userAddress,           // deposit comes from user's balance
  };

  // Encode the inner message as an Any type for MsgExec
  // With @akashnetwork/chain-sdk:
  //   import { MsgCreateDeployment } from "@akashnetwork/chain-sdk/deployment";
  // Migration note: Previously from @akashnetwork/akash-api/akash/deployment/v1beta3
  const { MsgCreateDeployment } = await import("@akashnetwork/chain-sdk/deployment");
  const encodedInner = MsgCreateDeployment.encode(
    MsgCreateDeployment.fromPartial(innerMsg)
  ).finish();

  // Wrap in MsgExec
  const execMsg = {
    typeUrl: "/cosmos.authz.v1beta1.MsgExec",
    value: MsgExec.fromPartial({
      grantee: service.getServiceAddress(),
      msgs: [
        {
          typeUrl: MSG_CREATE_DEPLOYMENT_URL,
          value: encodedInner,
        },
      ],
    }),
  };

  // Build fee options
  const feeOptions = useFeeGrant
    ? {
        amount: [{ denom: GAS_DENOM, amount: "5000" }],
        gas: "500000",
        granter: userAddress,
      }
    : "auto";

  const result: DeliverTxResponse = await service["client"].signAndBroadcast(
    service.getServiceAddress(),
    [execMsg],
    feeOptions
  );

  if (result.code !== 0) {
    throw new Error(
      `Deployment creation failed: code ${result.code} — ${result.rawLog}`
    );
  }

  return {
    dseq: effectiveDseq,
    owner: userAddress,
    txHash: result.transactionHash,
    height: result.height,
  };
}
```

### SDL Parsing Helper

```typescript
/**
 * Parse SDL content into the format expected by MsgCreateDeployment.
 *
 * With @akashnetwork/chain-sdk:
 *   import { SDL } from "@akashnetwork/chain-sdk/sdl";
 */
async function parseSDL(sdlContent: string): Promise<ParsedSDL> {
  // Dynamic import supports the migration path
  const { SDL } = await import("@akashnetwork/chain-sdk/sdl");

  const sdl = SDL.fromString(sdlContent);

  return {
    groups: sdl.groups(),
    version: await sdl.manifestVersion(),
  };
}
```

### Error Handling — Step 4

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| No AuthZ grant | Tx fails `no authorization found` | Verify grants with `verifyAuthzGrants`; prompt user to re-grant |
| Grant expired | Tx fails `authorization expired` | Notify user; request fresh grant |
| Insufficient user balance | Tx fails `insufficient funds` | Check user balance first; suggest minimum funding |
| DSEQ collision | Tx fails `deployment exists` | Generate new DSEQ from current timestamp or block height |
| Invalid SDL | `parseSDL` throws | Validate SDL before submission; return validation errors to user |
| Fee grant exhausted | Tx fails `fee grant not found` or `spent` | Fall back to service-paid gas; notify user |

---

## Step 5 — Service Sends Manifest to Provider

After the deployment is created on-chain and a lease is formed, the service must deliver the deployment manifest to the winning provider.

```typescript
import axios from "axios";

interface SendManifestParams {
  providerUri: string;
  dseq: string;
  manifest: Uint8Array;
  certificate: {
    cert: Uint8Array;
    key: Uint8Array;
  };
}

/**
 * Send the deployment manifest to the provider using mTLS.
 *
 * The provider validates the manifest against the version hash
 * submitted on-chain in Step 4.
 */
async function sendManifestToProvider(
  params: SendManifestParams
): Promise<void> {
  const { providerUri, dseq, manifest, certificate } = params;

  const url = `${providerUri}/deployment/${dseq}/manifest";

  try {
    const response = await axios.post(url, manifest, {
      headers: {
        "Content-Type": "application/json",
      },
      httpsAgent: new (await import("https")).Agent({
        cert: Buffer.from(certificate.cert),
        key: Buffer.from(certificate.key),
        rejectUnauthorized: false,
      }),
      timeout: 30_000,
    });

    if (response.status !== 200 && response.status !== 201) {
      throw new Error(`Provider rejected manifest: ${response.status} ${response.data}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        throw new Error(
          `Provider returned ${error.response.status}: ${JSON.stringify(error.response.data)}`
        );
      }
      throw new Error(`Provider unreachable: ${error.message}`);
    }
    throw error;
  }
}
```

### Certificate Management

```typescript
/**
 * Create or load a client certificate for provider communication.
 *
 * With @akashnetwork/chain-sdk:
 *   import { CertificateManager } from "@akashnetwork/chain-sdk/certificate";
 * Migration note: Previously from @akashnetwork/akashjs/build/certificates
 */
async function getOrCreateCertificate(
  userAddress: string,
  userClient: SigningStargateClient
): Promise<{ cert: Uint8Array; key: Uint8Array; certPem: string }> {
  const { CertificateManager } = await import("@akashnetwork/chain-sdk/certificate");

  // Generate a new certificate pair
  const certManager = new CertificateManager();
  const { cert, key } = certManager.generatePEM(userAddress);

  // Publish the certificate on-chain so providers can verify it
  const { MsgCreateCertificate } = await import("@akashnetwork/chain-sdk/certificate");
  const msg = {
    typeUrl: "/akash.cert.v1beta3.MsgCreateCertificate",
    value: MsgCreateCertificate.fromPartial({
      owner: userAddress,
      cert: cert,
    }),
  };

  await userClient.signAndBroadcast(userAddress, [msg], "auto");

  return {
    cert: new TextEncoder().encode(cert),
    key: new TextEncoder().encode(key),
    certPem: cert,
  };
}
```

### Error Handling — Step 5

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Provider offline | Connection timeout / ECONNREFUSED | Retry with exponential backoff (3 attempts); try alternate providers |
| Certificate rejected | 403 Forbidden | Re-publish certificate on-chain; retry |
| Manifest hash mismatch | 400 Bad Request | Verify SDL matches what was submitted on-chain |
| Provider rate limit | 429 Too Many Requests | Respect `Retry-After`; queue retry |
| TLS handshake failure | UNABLE_TO_VERIFY_LEAF_SIGNATURE | Use provider's self-signed cert; set `rejectUnauthorized: false` |

---

## Step 6 — Service Monitors Lease Status

The service continuously monitors active leases to detect provider health, price changes, and expiration.

```typescript
interface LeaseMonitorConfig {
  pollIntervalMs: number;
  onLeaseActive: (lease: LeaseInfo) => Promise<void>;
  onLeaseClosed: (lease: LeaseInfo) => Promise<void>;
  onLeaseInsufficientFunds: (lease: LeaseInfo) => Promise<void>;
}

/**
 * Monitor leases for a user's deployment.
 *
 * With @akashnetwork/chain-sdk:
 *   import { QueryClient } from "@akashnetwork/chain-sdk/query";
 * Migration note: Previously query clients came from @akashnetwork/akash-api
 */
async function monitorLeases(
  client: SigningStargateClient,
  userAddress: string,
  config: LeaseMonitorConfig
): Promise<() => void> {
  let running = true;
  let timeoutId: ReturnType<typeof setTimeout>;

  const poll = async () => {
    if (!running) return;

    try {
      const leases = await queryActiveLeases(client, userAddress);

      for (const lease of leases) {
        switch (lease.state) {
          case "active":
            await config.onLeaseActive(lease);

            // Check escrow balance — warn if running low
            const escrowBalance = await queryEscrowBalance(client, userAddress, lease.dseq);
            const estimatedBlockRate = parseFloat(lease.price.amount);
            const blocksRemaining = Math.floor(escrowBalance / estimatedBlockRate);

            if (blocksRemaining < 1000) {
              // ~1000 blocks ≈ ~1.5 hours on Akash
              await config.onLeaseInsufficientFunds(lease);
            }
            break;

          case "closed":
            await config.onLeaseClosed(lease);
            break;
        }
      }
    } catch (error) {
      console.error(`Lease monitor error for ${userAddress}:`, error);
    } finally {
      if (running) {
        timeoutId = setTimeout(poll, config.pollIntervalMs);
      }
    }
  };

  // Start polling
  poll();

  // Return a stop function
  return () => {
    running = false;
    clearTimeout(timeoutId);
  };
}

/**
 * Query all active leases for a user.
 */
async function queryActiveLeases(
  client: SigningStargateClient,
  owner: string
): Promise<LeaseInfo[]> {
  // With @akashnetwork/chain-sdk, use the market query module:
  //   import { MarketQueryClient } from "@akashnetwork/chain-sdk/query/market";
  // Migration note: Previously from @akashnetwork/akash-api/akash/market/v1beta4
  const { MarketQueryClient } = await import("@akashnetwork/chain-sdk/query/market");

  const queryClient = new MarketQueryClient(client.getQueryClient()!);

  const response = await queryClient.Leases({
    filters: {
      owner,
      state: "active",
    },
  });

  return response.leases.map((l: any) => ({
    dseq: l.lease.id.dseq.toString(),
    gseq: l.lease.id.gseq,
    oseq: l.lease.id.oseq,
    provider: l.lease.id.provider,
    state: l.lease.state,
    price: {
      denom: l.lease.price.denom,
      amount: l.lease.price.amount,
    },
  }));
}

/**
 * Query the deployment escrow balance.
 */
async function queryEscrowBalance(
  client: SigningStargateClient,
  owner: string,
  dseq: string
): Promise<number> {
  const { DeploymentQueryClient } = await import("@akashnetwork/chain-sdk/query/deployment");

  const queryClient = new DeploymentQueryClient(client.getQueryClient()!);

  const response = await queryClient.Deployment({
    id: { owner, dseq: BigInt(dseq) },
  });

  // Escrow balance from the deployment response
  const escrow = response.deployment?.escrowAccount;
  if (!escrow) return 0;

  // Sum all balances in the escrow
  return escrow.balance?.reduce((sum: number, coin: any) => {
    return sum + parseInt(coin.amount, 10);
  }, 0) ?? 0;
}
```

### Error Handling — Step 6

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| RPC node down | Query timeout / connection error | Failover to backup RPC; retry with backoff |
| Lease closed unexpectedly | State changes to `closed` | Alert user; auto-redeploy with new SDL if configured |
| Escrow depleted | `blocksRemaining < threshold` | Notify user to deposit; optionally auto-deposit via AuthZ |
| Stale data | Same height repeated | Force refresh from different RPC node |

---

## Step 7 — Service Closes Deployment on User's Behalf

The service terminates a deployment by wrapping `MsgCloseDeployment` in `MsgExec`.

```typescript
interface CloseDeploymentParams {
  userAddress: string;
  dseq: string;
  useFeeGrant?: boolean;
}

/**
 * Close a deployment on behalf of the user via AuthZ MsgExec.
 */
async function closeDeploymentOnBehalf(
  service: AkashDeploymentService,
  params: CloseDeploymentParams
): Promise<CloseDeploymentResult> {
  const { userAddress, dseq, useFeeGrant = false } = params;

  // Build the inner MsgCloseDeployment — from the USER's perspective
  // With @akashnetwork/chain-sdk:
  //   import { MsgCloseDeployment } from "@akashnetwork/chain-sdk/deployment";
  const { MsgCloseDeployment } = await import("@akashnetwork/chain-sdk/deployment");

  const innerMsg = MsgCloseDeployment.fromPartial({
    id: {
      owner: userAddress,
      dseq: BigInt(dseq),
    },
  });

  // Encode and wrap in MsgExec
  const encodedInner = MsgCloseDeployment.encode(innerMsg).finish();

  const execMsg = {
    typeUrl: "/cosmos.authz.v1beta1.MsgExec",
    value: MsgExec.fromPartial({
      grantee: service.getServiceAddress(),
      msgs: [
        {
          typeUrl: MSG_CLOSE_DEPLOYMENT_URL,
          value: encodedInner,
        },
      ],
    }),
  };

  // Build fee options
  const feeOptions = useFeeGrant
    ? {
        amount: [{ denom: GAS_DENOM, amount: "5000" }],
        gas: "200000",
        granter: userAddress,
      }
    : "auto";

  const result: DeliverTxResponse = await service["client"].signAndBroadcast(
    service.getServiceAddress(),
    [execMsg],
    feeOptions
  );

  if (result.code !== 0) {
    throw new Error(
      `Deployment close failed: code ${result.code} — ${result.rawLog}`
    );
  }

  return {
    dseq,
    txHash: result.transactionHash,
    height: result.height,
  };
}
```

### Error Handling — Step 7

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| No AuthZ grant for close | Tx fails `no authorization found` | Verify `MSG_CLOSE_DEPLOYMENT_URL` grant exists |
| Deployment already closed | Tx fails `deployment not found` or `deployment closed` | Query deployment state first; return success if already closed |
| Active leases preventing close | Unexpected state | Close all leases first (if grant exists) or wait for provider to close |
| Wrong DSEQ | Tx fails `deployment not found` | Verify DSEQ with on-chain query before closing |

---

## Complete Service Integration Example

The following shows all steps working together in a deployment service class:

```typescript
class ManagedDeploymentService {
  private service: AkashDeploymentService;
  private monitors: Map<string, () => void> = new Map();

  constructor(service: AkashDeploymentService) {
    this.service = service;
  }

  /**
   * Full lifecycle: onboard user, create deployment, monitor, and teardown.
   */
  async deploy(
    userAddress: string,
    sdlContent: string,
    options?: {
      useFeeGrant?: boolean;
      monitorIntervalMs?: number;
    }
  ): Promise<CreateDeploymentResult & { stopMonitor: () => void }> {
    const opts = {
      useFeeGrant: options?.useFeeGrant ?? false,
      monitorIntervalMs: options?.monitorIntervalMs ?? 60_000,
    };

    // 1. Verify AuthZ grants exist
    const grants = await verifyAuthzGrants(
      this.service["client"],
      userAddress,
      this.service.getServiceAddress()
    );

    if (!grants.hasCreateDeployment) {
      throw new Error(
        `User ${userAddress} has not granted deployment creation permissions to ${this.service.getServiceAddress()}`
      );
    }

    // 2. Parse SDL
    const sdl = await parseSDL(sdlContent);

    // 3. Create deployment on behalf
    const deployment = await createDeploymentOnBehalf(this.service, {
      userAddress,
      sdl,
      useFeeGrant: opts.useFeeGrant,
    });

    // 4. Start monitoring
    const stopMonitor = await monitorLeases(
      this.service["client"],
      userAddress,
      {
        pollIntervalMs: opts.monitorIntervalMs,
        onLeaseActive: async (lease) => {
          console.log(`Lease active: ${lease.dseq} on provider ${lease.provider}`);
          // Send manifest when lease becomes active
          // await sendManifestToProvider({ ... });
        },
        onLeaseClosed: async (lease) => {
          console.log(`Lease closed: ${lease.dseq}`);
        },
        onLeaseInsufficientFunds: async (lease) => {
          console.warn(`Low escrow: ${lease.dseq} — user should deposit more funds`);
        },
      }
    );

    return { ...deployment, stopMonitor };
  }

  /**
   * Gracefully shut down a deployment.
   */
  async teardown(
    userAddress: string,
    dseq: string,
    options?: { useFeeGrant?: boolean }
  ): Promise<CloseDeploymentResult> {
    // Stop the monitor
    const stopKey = `${userAddress}:${dseq}`;
    const stopFn = this.monitors.get(stopKey);
    if (stopFn) {
      stopFn();
      this.monitors.delete(stopKey);
    }

    return closeDeploymentOnBehalf(this.service, {
      userAddress,
      dseq,
      useFeeGrant: options?.useFeeGrant ?? false,
    });
  }
}
```

---

## Security Best Practices

### 1. Principle of Least Privilege

Only grant the minimum message types required:

```typescript
// ✅ GOOD — Only grant what the service needs
const MINIMAL_GRANTS = [
  MSG_CREATE_DEPLOYMENT_URL,
  MSG_CLOSE_DEPLOYMENT_URL,
];

// ❌ BAD — Do NOT grant broad permissions like Send
const OVERLY_BROAD = [
  "/cosmos.bank.v1beta1.MsgSend", // Never grant this to a deployment service
];
```

### 2. Grant Expiration

Always set short-lived grants. Users can re-grant when needed:

```typescript
// ✅ GOOD — 30-day expiry, renewable
const SHORT_LIVED = 30;

// ❌ BAD — 10-year grant (effectively permanent)
const TOO_LONG = 365 * 10;
```

### 3. Fee Grant Spend Limits

Cap fee grants to prevent abuse:

```typescript
// ✅ GOOD — Capped at 50 AKT for gas
await grantFeeAllowance({
  spendLimit: "50000000", // 50 AKT in uakt
});

// ❌ BAD — Unlimited fee grant
await grantFeeAllowance({
  spendLimit: undefined, // no cap
});
```

### 4. Service Account Isolation

- Use a **dedicated service account** — never reuse an existing wallet.
- The service mnemonic should be stored in a secrets manager (Vault, AWS Secrets Manager, etc.), not in environment variables or code.
- Rotate the service account periodically.

```typescript
// ✅ GOOD — Load from secrets manager
import { SecretsManager } from "@aws-sdk/client-secrets-manager";

async function loadServiceMnemonic(): Promise<string> {
  const client = new SecretsManager({});
  const secret = await client.getSecretValue({
    SecretId: "akash/deployment-service/mnemonic",
  });
  return JSON.parse(secret.SecretString!).mnemonic;
}
```

### 5. Input Validation

Always validate SDL before on-chain submission:

```typescript
async function validateSDL(sdlContent: string): Promise<string[]> {
  const errors: string[] = [];

  try {
    const { SDL } = await import("@akashnetwork/chain-sdk/sdl");
    const sdl = SDL.fromString(sdlContent);
    // SDL.fromString will throw on invalid YAML or schema violations
  } catch (error) {
    errors.push(`SDL validation failed: ${(error as Error).message}`);
  }

  // Additional checks
  if (sdlContent.length > 1_000_000) {
    errors.push("SDL exceeds maximum size (1MB)");
  }

  return errors;
}
```

### 6. Audit Logging

Log every AuthZ MsgExec with full context:

```typescript
interface AuditLogEntry {
  timestamp: string;
  action: "create_deployment" | "close_deployment" | "create_lease";
  userAddress: string;
  dseq: string;
  serviceAddress: string;
  txHash: string;
  blockHeight: number;
  feeGranter?: string;
}

function auditLog(entry: AuditLogEntry): void {
  // Write to immutable audit store
  console.info(JSON.stringify({
    ...entry,
    timestamp: new Date().toISOString(),
  }));
}
```

### 7. Rate Limiting per User

```typescript
import rateLimit from "express-rate-limit";

const deploymentLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // limit each user to 10 deployment requests per window
  keyGenerator: (req) => req.body.userAddress ?? req.ip,
  message: "Too many deployment requests. Please try again later.",
});
```

---

## Error Handling — Comprehensive Reference

### Common Failure Modes Across All Steps

| Error Pattern | Typical Message | Root Cause | Recovery |
|---------------|-----------------|------------|----------|
| AuthZ not found | `no authorization found` | Grant never created or revoked | User must re-grant |
| AuthZ expired | `authorization expired` | Grant `expiration` timestamp passed | User must create new grant |
| Insufficient funds | `insufficient funds` | User wallet empty or escrow depleted | Fund wallet or deposit to deployment |
| Fee grant exhausted | `fee grant not found` / `spend limit exceeded` | Fee allowance cap reached | User re-grants fee allowance |
| Deployment exists | `deployment already exists` | DSEQ collision | Use unique DSEQ (block height / timestamp) |
| Deployment not found | `deployment not found` | Wrong DSEQ or already closed | Verify with on-chain query |
| RPC timeout | `timed out waiting for tx to be included` | Congested network | Retry with higher gas price |
| Node unavailable | `ECONNREFUSED` / `ETIMEDOUT` | RPC node down | Failover to backup RPC endpoint |
| Provider rejected | `400` / `403` from provider | Invalid manifest or cert | Re-validate SDL; re-publish certificate |

### Retry Strategy

```typescript
interface RetryConfig {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  retryableErrors: string[];
}

const DEFAULT_RETRY: RetryConfig = {
  maxAttempts: 3,
  baseDelayMs: 2000,
  maxDelayMs: 30_000,
  retryableErrors: [
    "ECONNREFUSED",
    "ETIMEDOUT",
    "timed out waiting",
    "timeout",
    "ECONNRESET",
    "5xx",
  ],
};

async function withRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      const errorMessage = lastError.message.toLowerCase();

      const isRetryable = config.retryableErrors.some((e) =>
        errorMessage.includes(e.toLowerCase())
      );

      if (!isRetryable || attempt === config.maxAttempts) {
        throw lastError;
      }

      const jitter = Math.random() * 1000;
      const delay = Math.min(
        config.baseDelayMs * Math.pow(2, attempt - 1) + jitter,
        config.maxDelayMs
      );

      console.warn(
        `Attempt ${attempt}/${config.maxAttempts} failed: ${lastError.message}. Retrying in ${delay}ms...`
      );

      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}
```

---

## Console API Integration

The Console API provides managed wallets that simplify the user onboarding flow. In this pattern, the Console API handles key management while AuthZ + FeeGrant handle delegation.

### When to Use Managed Wallets vs Self-Custodial

| Factor | Self-Custodial | Managed Wallet |
|--------|---------------|----------------|
| User manages keys | ✅ Yes | ❌ No |
| AuthZ grant flow | User signs from own wallet | Service signs on behalf via Console API |
| Fee grant source | User's on-chain wallet | User's managed wallet balance |
| Complexity | Higher (key management) | Lower (API-driven) |
| Security model | User controls keys | Console API is trusted custodian |
| Use case | Power users, teams | End-user apps, SaaS platforms |

### Console API Wallet + AuthZ Flow

For managed wallet users, the service can create the wallet and set up grants in a single onboarding flow:

```typescript
interface ConsoleApiConfig {
  apiKey: string;
  baseUrl?: string;
}

class ConsoleApiAuthzIntegration {
  private config: ConsoleApiConfig;

  constructor(config: ConsoleApiConfig) {
    this.config = {
      baseUrl: CONSOLE_API_BASE,
      ...config,
    };
  }

  /**
   * Full onboarding: create wallet → fund → grant AuthZ → grant fee allowance.
   */
  async onboardUser(params: {
    serviceAddress: string;
    initialFundingDenom?: string;
    grantDurationDays?: number;
  }): Promise<{
    wallet: CreateUserResult;
    authzGrants: GrantResult[];
    feeGrant?: GrantResult;
  }> {
    const { serviceAddress, initialFundingDenom, grantDurationDays } = params;

    // 1. Create managed wallet
    const wallet = await createManagedWallet(
      this.config.apiKey,
      `user-${Date.now()}`
    );

    // 2. Wait for initial funding (user must deposit to the deposit address)
    if (initialFundingDenom) {
      const funded = await this.waitForFunding(
        wallet.address,
        initialFundingDenom,
        300_000 // 5-minute timeout
      );

      if (!funded) {
        throw new Error(
          `Wallet ${wallet.address} was not funded within the timeout period. `
          + `Deposit address: ${wallet.depositAddress}`
        );
      }
    }

    // 3. Create AuthZ grants (requires user wallet client)
    // For managed wallets, the Console API handles signing
    const authzResult = await this.grantAuthzViaConsole(
      wallet.address,
      serviceAddress,
      grantDurationDays ?? DEFAULT_GRANT_DURATION_DAYS
    );

    // 4. Optionally grant fee allowance
    const feeGrant = await this.grantFeeViaConsole(
      wallet.address,
      serviceAddress,
      grantDurationDays ?? DEFAULT_GRANT_DURATION_DAYS
    );

    return {
      wallet,
      authzGrants: authzResult,
      feeGrant,
    };
  }

  /**
   * Grant AuthZ permissions via Console API for a managed wallet.
   * The Console API signs on behalf of the managed wallet.
   */
  private async grantAuthzViaConsole(
    walletAddress: string,
    serviceAddress: string,
    expirationDays: number
  ): Promise<GrantResult[]> {
    const expiration = new Date();
    expiration.setDate(expiration.getDate() + expirationDays);

    const grants = [
      MSG_CREATE_DEPLOYMENT_URL,
      MSG_CLOSE_DEPLOYMENT_URL,
      MSG_CREATE_LEASE_URL,
    ];

    // Console API can broadcast transactions from managed wallets
    // This is an example of how the integration might work;
    // check the Console API docs for the exact endpoint.
    const response = await fetch(
      `${this.config.baseUrl}/v1/authz/grant`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${this.config.apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          walletAddress,
          grantee: serviceAddress,
          messageTypes: grants,
          expiration: expiration.toISOString(),
        }),
      }
    );

    if (!response.ok) {
      // Fallback: if Console API doesn't support AuthZ grants directly,
      // the service must handle this via a separate transaction flow
      throw new Error(
        `Console API AuthZ grant failed: ${response.status}. `
        + `Grant AuthZ manually or use the self-custodial flow.`
      );
    }

    const result = await response.json();

    return grants.map((msgTypeUrl) => ({
      txHash: result.data?.txHash ?? "console-api",
      height: result.data?.height ?? 0,
      grantType: "authz" as const,
      msgTypeUrl,
      expiration,
    }));
  }

  /**
   * Grant fee allowance via Console API for a managed wallet.
   */
  private async grantFeeViaConsole(
    walletAddress: string,
    serviceAddress: string,
    expirationDays: number
  ): Promise<GrantResult> {
    const expiration = new Date();
    expiration.setDate(expiration.getDate() + expirationDays);

    const response = await fetch(
      `${this.config.baseUrl}/v1/feegrant/grant`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${this.config.apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          walletAddress,
          grantee: serviceAddress,
          spendLimit: "50000000", // 50 AKT cap
          denom: GAS_DENOM,
          expiration: expiration.toISOString(),
        }),
      }
    );

    if (!response.ok) {
      // Fee grant is optional — log warning but don't fail onboarding
      console.warn(
        `Fee grant failed (${response.status}). Service will pay gas from its own account.`
      );
      return {
        txHash: "",
        height: 0,
        grantType: "feegrant",
        expiration,
      };
    }

    const result = await response.json();

    return {
      txHash: result.data?.txHash ?? "console-api",
      height: result.data?.height ?? 0,
      grantType: "feegrant",
      expiration,
    };
  }

  /**
   * Poll wallet balance until funded.
   */
  private async waitForFunding(
    address: string,
    denom: string,
    timeoutMs: number
  ): Promise<boolean> {
    const startTime = Date.now();
    const pollInterval = 5_000; // 5 seconds

    while (Date.now() - startTime < timeoutMs) {
      try {
        const response = await fetch(
          `${this.config.baseUrl}/v1/wallet/balance`,
          {
            headers: {
              Authorization: `Bearer ${this.config.apiKey}`,
            },
          }
        );

        if (response.ok) {
          const result = await response.json();
          const balance = result.data?.balances?.find(
            (b: any) => b.denom === denom
          );

          if (balance && parseInt(balance.amount, 10) > 0) {
            return true;
          }
        }
      } catch {
        // Continue polling
      }

      await new Promise((resolve) => setTimeout(resolve, pollInterval));
    }

    return false;
  }
}
```

### Console API Deployment Shortcuts

For simpler use cases, the Console API provides direct deployment endpoints that bypass the AuthZ flow entirely:

```typescript
/**
 * Deploy directly via Console API (no AuthZ required).
 * The Console API manages the wallet and signs transactions.
 *
 * This is simpler but gives less control than the AuthZ pattern.
 */
async function consoleApiDeploy(
  apiKey: string,
  sdlContent: string,
  options?: { preferredProvider?: string }
): Promise<{ dseq: string; provider: string; leaseUrl: string }> {
  // 1. Validate SDL
  const validateResponse = await fetch(
    `${CONSOLE_API_BASE}/v1/sdl/validate`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sdl: sdlContent }),
    }
  );

  if (!validateResponse.ok) {
    const error = await validateResponse.json();
    throw new Error(`SDL validation failed: ${JSON.stringify(error)}`);
  }

  // 2. Estimate price
  const priceResponse = await fetch(
    `${CONSOLE_API_BASE}/v1/sdl/price`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        sdl: sdlContent,
        preferredProvider: options?.preferredProvider,
      }),
    }
  );

  const priceResult = await priceResponse.json();

  // 3. Create deployment via Console API
  const deployResponse = await fetch(
    `${CONSOLE_API_BASE}/v1/deployment`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        sdl: sdlContent,
        deposit: {
          denom: DEPLOYMENT_DEPOSIT_DENOM,
          amount: DEFAULT_DEPLOYMENT_DEPOSIT,
        },
        preferredProvider: options?.preferredProvider,
      }),
    }
  );

  if (!deployResponse.ok) {
    throw new Error(
      `Deployment failed: ${deployResponse.status} ${await deployResponse.text()}`
    );
  }

  const result = await deployResponse.json();

  return {
    dseq: result.data.dseq,
    provider: result.data.provider,
    leaseUrl: result.data.leaseUrl,
  };
}
```

### Choosing Between AuthZ Pattern and Console API Direct

```
                    Need full control over
                    on-chain transactions?
                           │
                    ┌──────┴──────┐
                    │ Yes         │ No
                    ▼             ▼
              Use AuthZ      Use Console API
              Pattern        Deploy Endpoint
              (Steps 1-7)    (consoleApiDeploy)
                    │             │
                    │             │
              Need user to     Service manages
              hold their       everything via
              own keys?        API keys
                    │
             ┌──────┴──────┐
             │ Yes         │ No
             ▼             ▼
       Self-custodial   Managed Wallet
       + AuthZ grant    + Console API
                        signs grants
```

---

## Summary

| Component | Purpose | Key Message Type |
|-----------|---------|------------------|
| AuthZ | Delegate deployment actions | `MsgExec` wrapping deployment messages |
| FeeGrant | Sponsor gas fees | `MsgGrantAllowance` with `BasicAllowance` |
| Managed Wallet | Simplify key management | Console API `/v1/wallet/*` endpoints |

The pattern enables building production deployment services where:

1. **Users** never expose private keys to the service.
2. **Services** operate autonomously within bounded permissions.
3. **Gas costs** can be sponsored by users or the service.
4. **Key management** can be delegated to the Console API for simpler UX.

Every on-chain action flows through `MsgExec`, ensuring the service acts only within the permissions explicitly granted by the user, with automatic expiration and revocability.
