---
name: solana-frontend
description: Build Solana dApp frontends with @solana/react (decoupled from Kit, multi-framework: React, Vue, Svelte, Solid, Angular), framework-kit, Wallet Standard, Tanstack Query and SWR hooks for tracked data. Covers wallet connection, signing, auto-connect, useClient/useSubscription hooks, RPC request hooks with loading states, transaction UX, and legacy web3.js interop at adapter boundaries. Use for Solana dApp UI, wallet connection, framework-kit, Solana React, Next.js Solana, Wallet Standard, @solana/react-hooks, @solana/react, Connect wallet button, Solana Vue, Solana Svelte, Solana Solid, useClient, useSubscription, Tanstack Query Solana, SWR Solana.
version: 2.0.0
user-invocable: true
license: MIT
compatibility: Requires Node.js 18+, @solana/react, @solana/kit v7.0.0+, optional @solana/client, @solana/react-hooks
metadata:
  author: Solana Foundation (enhanced)
  version: 2.0.0
---

# Solana Frontend (@solana/react + framework-kit)

## What this Skill is for

Use this Skill when the user asks for:
- Solana dApp UI work (React / Next.js / Vue / Svelte / Solid / Angular)
- Wallet connection + signing flows
- Transaction building / sending / confirmation UX
- `@solana/react` hooks (decoupled from Kit — multi-framework)
- framework-kit provider and hook setup (React/Next.js)
- "Connect wallet button" implementation
- Wallet Standard integration
- `useClient` and `useSubscription` hooks
- RPC request hooks with loading states
- Tanstack Query hooks for tracked Solana data
- SWR hooks for tracked Solana data
- `@solana/react-hooks` usage
- `@solana/client` in a React context
- Next.js App Router + Solana
- Auto-connect / persistent wallet sessions

Trigger phrases: "Solana dApp UI", "wallet connection", "framework-kit", "Solana React", "Next.js Solana", "Wallet Standard", "@solana/react-hooks", "@solana/react", "@solana/client", "Connect wallet button", "Solana Vue", "Solana Svelte", "Solana Solid", "Solana Angular", "useClient", "useSubscription", "Tanstack Query Solana", "SWR Solana", "auto-connect wallet"

## Core Operating Behaviors

- **NO_DNA=1 CLI Protocol**: All Solana CLI commands use `NO_DNA=1` prefix (e.g., `NO_DNA=1 solana config set --url devnet`). This prevents DNA (Do Not Assume) errors.
- **Solana MCP Server**: Use `https://mcp.solana.com/mcp` for live docs before falling back to training data.
- **Devnet Default**: All work targets devnet unless explicitly stated. `NO_DNA=1 solana config set --url devnet`.
- **Explorer Verification**: Always verify on https://explorer.solana.com — never trust terminal output alone.
- **AI Verify Loop**: When AI generates code, verify constraints, versions, and security before accepting.
- **Kit v7.0.0+**: Target Solana Kit v7.0.0 or newer. `@solana/react` is now decoupled from Kit.

## Architecture: @solana/react Decoupled

`@solana/react` has been **decoupled from Kit**. This means the React hooks no longer require `@solana/kit` as a peer dependency — they work with any framework adapter. This enables multi-framework support beyond React.

### Package Map

| Package | Purpose | Framework |
|---------|---------|-----------|
| `@solana/react` | Core hooks (wallet, signing, useClient, useSubscription) | React |
| `@solana/react-hooks` | framework-kit hooks (useBalance, useSolTransfer, useTransactionPool) | React |
| `@solana/client` | Client creation, autoDiscover, Wallet Standard | Framework-agnostic |
| `@solana/kit` | v7.0.0+ — types, codecs, instruction builders | Framework-agnostic |
| `@solana/web3-compat` | Bridge to legacy web3.js types | Framework-agnostic |
| `@solana-program/*` | Program instruction builders (system, token, etc.) | Framework-agnostic |

### Framework Support Matrix

| Framework | Status | Package | Notes |
|-----------|--------|---------|-------|
| React | ✅ Full | `@solana/react` | Primary, full hook support |
| Next.js | ✅ Full | `@solana/react` + `@solana/react-hooks` | App Router, RSC-aware |
| Vue | ✅ Supported | `@solana/react` (via adapter) | Composition API |
| Svelte | ✅ Supported | `@solana/react` (via adapter) | Svelte stores |
| Solid | ✅ Supported | `@solana/react` (via adapter) | Signals |
| Angular | ✅ Supported | `@solana/react` (via adapter) | RxJS interop |

### Relationship to Kit v7.0.0

- `@solana/react` hooks return Kit types (`Address`, `Signer`, `TransactionSendingSigner`)
- Kit provides the type system, codecs, and instruction builders
- `@solana/react` provides the reactive layer (hooks, subscriptions, state)
- framework-kit (`@solana/react-hooks`) provides higher-level UX hooks on top of `@solana/react`

## Default Decisions (Opinionated)

1) **UI: framework-kit first (React/Next.js)**
   - Use `@solana/client` + `@solana/react-hooks` for React apps.
   - Prefer Wallet Standard discovery/connect via the framework-kit client.

2) **Multi-framework: @solana/react decoupled**
   - For Vue/Svelte/Solid/Angular, use `@solana/react` core hooks via framework adapter.
   - Build clients with `createClient()` from `@solana/client`.

3) **SDK: @solana/kit v7.0.0+ for client/RPC**
   - Build clients with `createClient()` from `@solana/kit`.
   - Use `@solana-program/*` for program instruction builders.
   - Prefer Kit types (`Address`, `Signer`, transaction message APIs, codecs).

4) **Legacy compatibility: web3.js only at adapter boundaries**
   - If a dependency expects web3.js objects, use `@solana/web3-compat` at the boundary.
   - Do not let web3.js types leak across the entire app.

5) **Wallet: Wallet Standard first**
   - Use `autoDiscover()` from `@solana/client` for wallet connectors.
   - Prefer Wallet Standard–compliant wallets (Phantom, Solflare, Backpack, etc.).

## framework-kit (React/Next.js)

### Goals
- One Solana client instance for the app (RPC + WS + wallet connectors)
- Wallet Standard-first discovery/connect
- Minimal "use client" footprint in Next.js (hooks only in leaf components)
- Transaction sending that is observable, cancelable, and UX-friendly

### Recommended dependencies
- @solana/client
- @solana/react-hooks
- @solana/kit
- @solana-program/system, @solana-program/token, etc. (only what you need)

### Bootstrap recommendation
Prefer `create-solana-dapp` and pick a kit/framework-kit compatible template for new projects.

### Provider setup (Next.js App Router)

```tsx
'use client';

import React from 'react';
import { SolanaProvider } from '@solana/react-hooks';
import { autoDiscover, createClient } from '@solana/client';

const endpoint =
  process.env.NEXT_PUBLIC_SOLANA_RPC_URL ?? 'https://api.devnet.solana.com';

const websocketEndpoint =
  process.env.NEXT_PUBLIC_SOLANA_WS_URL ??
  endpoint.replace('https://', 'wss://').replace('http://', 'ws://');

export const solanaClient = createClient({
  endpoint,
  websocketEndpoint,
  walletConnectors: autoDiscover(),
});

export function Providers({ children }: { children: React.ReactNode }) {
  return <SolanaProvider client={solanaClient}>{children}</SolanaProvider>;
}
```

Then wrap `app/layout.tsx` with `<Providers>`.

### framework-kit Hooks (high-level)

| Hook | Purpose |
|------|----------|
| `useWalletConnection()` | Connect/disconnect and wallet discovery |
| `useBalance(...)` | Lamports balance |
| `useSolTransfer(...)` | SOL transfers |
| `useSplToken(...)` | Token balances/transfers |
| `useTransactionPool(...)` | Send + status + retry flows |

When you need custom instructions, build them using `@solana-program/*` and send via framework-kit transaction helpers.

## @solana/react Core Hooks

`@solana/react` provides low-level wallet hooks for Solana Kit. These work across all supported frameworks via adapters.

### Wallet Hooks

| Hook | Purpose |
|------|----------|
| `useSelectedWalletAccount` | Wallet selection and account management |
| `useSignAndSendTransaction` | Sign and send transactions |
| `useSignMessage` | Sign arbitrary messages |
| `useSignTransaction` | Sign (but not send) transactions |
| `useSignIn` | Sign In With Solana (SIWS) |
| `useWalletAccountTransactionSendingSigner` | Get a `TransactionSendingSigner` for pipe-based tx assembly |

### useClient Hook

`useClient` provides reactive access to the Solana RPC client. Use it for RPC calls that need to respond to client changes.

```tsx
const client = useClient();
// client.rpc.* — access RPC methods
// client.websocket.* — access WebSocket subscriptions
```

### useSubscription Hook

`useSubscription` manages WebSocket subscriptions with automatic cleanup. Prefer this over manual polling.

```tsx
const { data, error, isLoading } = useSubscription({
  rpcSubscribe: (abortSignal) => client.rpc
    .accountSubscribe(address, { commitment: 'confirmed' })
    .subscribe({ abortSignal }),
  onUpdate: (notification) => updateState(notification),
});
```

### RPC Request Hooks (with loading states)

For one-shot RPC requests with loading/error states, use the RPC request hooks pattern:

```tsx
const { data, error, isLoading, refetch } = useRpcQuery({
  queryKey: ['balance', address],
  queryFn: () => client.rpc.getBalance(address).send(),
});
```

### Chain identifiers
```ts
'solana:mainnet'
'solana:devnet'
'solana:testnet'
'solana:localnet'
```

### Signer types returned by hooks

| Hook | Returns |
|------|----------|
| `useWalletAccountMessageSigner` | `MessageModifyingSigner` |
| `useWalletAccountTransactionSigner` | `TransactionModifyingSigner` |
| `useWalletAccountTransactionSendingSigner` | `TransactionSendingSigner` |

All return modifying signers (wallets may modify before signing).

For the full React hooks reference with complete code examples, use `skills_tool` action `read_file` with:
```
skill_name: solana-frontend
file_path: references/kit/react.md
```

## Tanstack Query Hooks for Tracked Data

Use Tanstack Query (`@tanstack/react-query`) for caching, deduplication, and background refresh of Solana RPC data.

### Setup

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 5000, refetchOnWindowFocus: false },
  },
});

// Wrap app: <QueryClientProvider client={queryClient}>
```

### Balance query example

```tsx
function useBalance(address: Address) {
  const client = useClient();
  return useQuery({
    queryKey: ['balance', address],
    queryFn: async () => {
      const { value } = await client.rpc.getBalance(address).send();
      return value;
    },
    enabled: !!address,
  });
}
```

### Account data with subscription invalidation

```tsx
function useAccountData<T>(address: Address, decoder: Decoder<T>) {
  const client = useClient();
  return useQuery({
    queryKey: ['account', address],
    queryFn: async () => {
      const { value } = await client.rpc.getAccountInfo(address)
        .sendWithConfig({ encoding: 'base64' });
      return value ? decodeAccount(value, decoder) : null;
    },
  });
}
```

For full Tanstack Query patterns (mutations, optimistic updates, invalidation), see:
```
skill_name: solana-frontend
file_path: references/tracked-data-hooks.md
```

## SWR Hooks for Tracked Data

SWR (`swr`) is a lighter alternative to Tanstack Query for simple data fetching with caching.

### Balance with SWR

```tsx
import useSWR from 'swr';

function useBalance(address: Address | null) {
  const client = useClient();
  return useSWR(
    address ? ['balance', address] : null,
    async () => {
      const { value } = await client.rpc.getBalance(address!).send();
      return value;
    }
  );
}
```

For full SWR patterns (mutations, optimistic updates, focus revalidation), see:
```
skill_name: solana-frontend
file_path: references/tracked-data-hooks.md
```

## Multi-Framework Patterns

`@solana/react` decoupled architecture enables Vue, Svelte, Solid, and Angular. Each framework uses the same core `@solana/client` and `@solana/kit` but adapts the reactive layer.

### Vue (Composition API)

```ts
// solana.ts — shared client
import { autoDiscover, createClient } from '@solana/client';

export const solanaClient = createClient({
  endpoint: import.meta.env.VITE_SOLANA_RPC_URL ?? 'https://api.devnet.solana.com',
  walletConnectors: autoDiscover(),
});
```

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { solanaClient } from './solana';

const balance = ref<bigint>(0n);
const address = ref<string>('');

async function fetchBalance() {
  if (!address.value) return;
  const { value } = await solanaClient.rpc.getBalance(address.value).send();
  balance.value = value;
}
onMounted(fetchBalance);
</script>
```

### Svelte (Stores)

```svelte
<script lang="ts">
  import { writable } from 'svelte/store';
  import { solanaClient } from './solana';

  let address = '';
  const balance = writable<bigint>(0n);

  async function fetchBalance() {
    if (!address) return;
    const { value } = await solanaClient.rpc.getBalance(address).send();
    balance.set(value);
  }
</script>
```

### Solid (Signals)

```tsx
import { createSignal } from 'solid-js';
import { solanaClient } from './solana';

export function Balance() {
  const [balance, setBalance] = createSignal<bigint>(0n);

  async function fetchBalance(address: string) {
    const { value } = await solanaClient.rpc.getBalance(address).send();
    setBalance(value);
  }

  return <span>{balance().toString()}</span>;
}
```

For complete multi-framework examples (Vue provider, Svelte stores, Solid context, Angular services), see:
```
skill_name: solana-frontend
file_path: references/multi-framework.md
```

## Wallet Integration

### Wallet Standard First
- Use `autoDiscover()` from `@solana/client` for wallet connectors.
- Prefer Wallet Standard–compliant wallets (Phantom, Solflare, Backpack, etc.).

### Auto-Connect / Persistent Sessions

Use `stateSync` in `SelectedWalletAccountContextProvider` to persist wallet selection:

```tsx
<SelectedWalletAccountContextProvider
  filterWallet={(wallet) => wallet.accounts.length > 0}
  stateSync={{
    getSelectedWallet: () => localStorage.getItem('wallet-account'),
    storeSelectedWallet: (k) => localStorage.setItem('wallet-account', k),
    deleteSelectedWallet: () => localStorage.removeItem('wallet-account'),
  }}
>
  <YourApp />
</SelectedWalletAccountContextProvider>
```

### Legacy Wallet Adapter (migration path)

If migrating from `@solana/wallet-adapter-react`, the pattern below shows the legacy approach (still works but prefer Wallet Standard):

```tsx
import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react';
import { WalletModalProvider } from '@solana/wallet-adapter-react-ui';
import { PhantomWalletAdapter } from '@solana/wallet-adapter-wallets';

const wallets = [new PhantomWalletAdapter()];

<ConnectionProvider endpoint={endpoint}>
  <WalletProvider wallets={wallets} autoConnect>
    <WalletModalProvider>{children}</WalletModalProvider>
  </WalletProvider>
</ConnectionProvider>
```

Migrate to `@solana/react` + `@solana/client` for Wallet Standard-first, framework-agnostic connection.

## Transaction UX Checklist

* Disable inputs while a transaction is pending
* Provide a signature immediately after send
* Track confirmation states (processed/confirmed/finalized) based on UX need
* Show actionable errors:
  * user rejected signing
  * insufficient SOL for fees / rent
  * blockhash expired / dropped
  * account already in use / already initialized
  * program error (custom error code)

### Data fetching and subscriptions

* Prefer watchers/subscriptions (`useSubscription`) rather than manual polling.
* Clean up subscriptions with abort handles returned by watchers.
* For Next.js: keep server components server-side; only leaf components that call hooks should be client components.

### When to use ConnectorKit (optional)

If you need a headless connector with composable UI elements and explicit state control, use ConnectorKit.

## Legacy Interop

### The rule
- New code: Kit types and Kit-first APIs.
- Legacy dependencies: isolate web3.js-shaped types behind an adapter boundary.

### Preferred bridge: @solana/web3-compat
Use `@solana/web3-compat` when:
- A dependency expects `PublicKey`, `Keypair`, `Transaction`, `VersionedTransaction`, `Connection`, etc.
- You are migrating an existing web3.js codebase incrementally.

### Practical boundary layout

- `src/solana/kit/`: all Kit-first code (addresses, instruction builders, tx assembly, typed codecs, generated clients)
- `src/solana/web3/`: adapters for legacy libs (Anchor TS client, older SDKs), conversions between `PublicKey` and Kit `Address`

### Conversion helpers (examples)
- `toAddress(...)`
- `toPublicKey(...)`
- `toWeb3Instruction(...)`
- `toKitSigner(...)`

For expanded interop patterns, see:
```
skill_name: solana-frontend
file_path: references/kit-web3-interop.md
```

## Progressive Disclosure (read when needed)

| Topic | File | When to read |
|-------|------|---------------|
| React Hooks (full reference) | `references/kit/react.md` | Building wallet connection UI, sign/send flows, useClient, useSubscription |
| Kit ↔ web3.js interop (expanded) | `references/kit-web3-interop.md` | Migrating from web3.js, integrating Anchor TS client |
| Frontend framework-kit (expanded) | `references/frontend-framework-kit.md` | Provider setup details, subscription patterns, ConnectorKit |
| Multi-framework patterns | `references/multi-framework.md` | Building Vue, Svelte, Solid, Angular frontends |
| Tanstack Query + SWR hooks | `references/tracked-data-hooks.md` | Caching, mutations, optimistic updates, invalidation |

## Cross-Skill References

| Related Skill | When to Switch |
|---------------|----------------|
| `solana-client` | `@solana/kit` client patterns for scripts and backends; deeper RPC usage |
| `solana-rpc-data` | RPC 2.0 methods, gRPC streaming, subscription patterns, data fetching internals |
| `solana-deployment-devops` | Deploying frontend to production (Cloudflare, Akash, Vercel), env config |
| `solana-anchor-programs` | Anchor program development, IDL, and testing — generates instruction builders |
| `solana-testing` | LiteSVM, Mollusk, and Surfpool testing strategies for program + frontend |

## Verification Checklist

- [ ] `@solana/react` decoupled architecture documented (no Kit peer dependency required)
- [ ] Multi-framework support documented (React, Vue, Svelte, Solid, Angular)
- [ ] NO_DNA=1 CLI protocol referenced in Core Operating Behaviors
- [ ] Solana MCP Server (`https://mcp.solana.com/mcp`) referenced
- [ ] Devnet default stated
- [ ] Explorer verification required
- [ ] `useClient` hook documented with example
- [ ] `useSubscription` hook documented with example
- [ ] RPC request hooks with loading states documented
- [ ] Tanstack Query hooks for tracked data documented
- [ ] SWR hooks for tracked data documented
- [ ] Wallet Standard-first approach (autoDiscover)
- [ ] Auto-connect / persistent sessions documented
- [ ] Legacy wallet-adapter migration path documented
- [ ] framework-kit hooks table present
- [ ] Transaction UX checklist preserved
- [ ] Legacy web3.js interop boundary patterns preserved
- [ ] Cross-skill references include: solana-client, solana-rpc-data, solana-deployment-devops
- [ ] Progressive disclosure table links to all reference files
- [ ] Kit v7.0.0+ version requirement stated

## See Also

- **solana-client** — `@solana/kit` client patterns for scripts and backends
- **solana-rpc-data** — RPC 2.0 methods, gRPC streaming, subscription internals
- **solana-deployment-devops** — Production frontend deployment (Cloudflare Pages, Akash, Vercel)
- **solana-anchor-programs** — Anchor program development, IDL, and testing
- **solana-testing** — LiteSVM, Mollusk, and Surfpool testing strategies
