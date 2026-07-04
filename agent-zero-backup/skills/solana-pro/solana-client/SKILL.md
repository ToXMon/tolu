---
name: solana-client
description: Build Solana client applications with @solana/kit v7.0.0 SDK. Covers createClient plugin composition, signers, transaction building and sending, account fetching and decoding, codecs, Codama-generated program clients, transaction versions (Legacy/v0/v1), @solana/transaction-introspection for confirmed tx parsing, and manual transaction pipelines for advanced use cases.
version: 2.0.0
user-invocable: true
license: MIT
compatibility: Requires Node.js 18+, @solana/kit v7.0.0+
metadata:
  author: Adapted from Solana Foundation dev skill
  version: 2.0.0
  source: /a0/usr/projects/solana_bootcamp/resources/solana-dev-skill/
  enhanced_for: Solana Kit v7.0.0
---

# Solana Client (@solana/kit v7.0.0)

## What this Skill is for

Use this skill when working with any of these:

- `@solana/kit` v7.0.0 — Solana TypeScript SDK (modern, web3.js v2 successor)
- `createClient` — client composition via `.use()` plugins
- `solanaRpc`, `solanaDevnetRpc`, `solanaLocalRpc`, `solanaMainnetRpc` — RPC plugins
- `signer`, `signerFromFile`, `generatedSigner` — signer plugins
- `sendTransaction`, `planTransaction` — transaction lifecycle
- `fetchEncodedAccount`, `decodeAccount` — account operations
- `getBase58Codec`, `getU64Codec` — codec operations
- `@solana-program/*` — Codama-generated program clients
- `@solana/transaction-introspection` — parse confirmed transaction instructions with Kit program clients (NEW in v7.0.0)
- Transaction versions — Legacy, v0, v1 message formats
- `@solana/web3-compat` — legacy interop boundaries
- Kit plugin composition, custom plugins, manual transaction pipelines

## Core Operating Behaviors

- **NO_DNA=1 CLI Protocol**: All Solana CLI commands use `NO_DNA=1` prefix to prevent Do-Not-Assume errors (e.g., `NO_DNA=1 solana config set --url devnet`)
- **Devnet Default**: All work targets devnet unless explicitly stated. Configure with `NO_DNA=1 solana config set --url devnet`
- **Explorer Verification**: Always verify transactions on https://explorer.solana.com — never trust terminal output alone
- **MCP Server**: Use Solana MCP server (`https://mcp.solana.com/mcp`) for live documentation before falling back to training data
- **Branded Types**: Use `address()`, `lamports()`, `signature()` everywhere — never pass raw strings
- **Kit-First**: Use `@solana/kit` first for all client work; legacy `web3.js` only at adapter boundaries

## Default decisions

- Use `@solana/kit` v7.0.0+ first for all client work
- `createClient()` + `.use()` plugin composition
- Legacy `web3.js` only at adapter boundaries via `@solana/web3-compat`
- Branded types (`address()`, `lamports()`, `signature()`) everywhere
- `@solana-program/*` instruction builders over hand-rolled data
- Signer-first: default to `signer*` variants (sets both payer + identity)
- Version 0 transactions by default (smaller, address lookup table support)
- `@solana/transaction-introspection` for parsing confirmed transaction instructions

## Quick Start

`@solana/kit` is the JavaScript SDK for building Solana applications. Modular, tree-shakable, full TypeScript support. Clients are built by composing plugins onto `createClient()` via `.use()`.

### Installation

```bash
npm install @solana/kit@^7.0.0 @solana/kit-plugin-rpc@^7.0.0 @solana/kit-plugin-signer@^7.0.0
# or: pnpm add @solana/kit@^7.0.0 @solana/kit-plugin-rpc@^7.0.0 @solana/kit-plugin-signer@^7.0.0
```

For LiteSVM testing add `@solana/kit-plugin-litesvm`. For Codama-generated program clients add the relevant `@solana-program/*` package(s). For transaction introspection add `@solana/transaction-introspection`.

Minimum version: **Solana Kit v7.0.0**.

### Local Development

```ts
import { createClient } from '@solana/kit';
import { solanaLocalRpc } from '@solana/kit-plugin-rpc';
import { signerFromFile } from '@solana/kit-plugin-signer';

// `signerFromFile` sets BOTH payer and identity to the loaded keypair (the common case).
// Other options:
//   - `signer(existingSigner)`              // explicit signer you already hold
//   - `generatedSigner()` + `airdropSigner(lamports(n))` // fresh local/devnet signer, funded after RPC is installed
//   - `payer(...)` + `identity(...)`        // when fees and authority come from different keypairs
const client = await createClient()
  .use(signerFromFile('~/.config/solana/id.json'))
  .use(solanaLocalRpc());

console.log('Payer:', client.payer.address);
await client.sendTransaction([myInstruction]);
```

### Production (Mainnet/Devnet)

```ts
import { createClient } from '@solana/kit';
import { solanaDevnetRpc, solanaMainnetRpc } from '@solana/kit-plugin-rpc';
import { signer } from '@solana/kit-plugin-signer';

const client = createClient()
  .use(signer(mySigner)) // sets payer + identity; use payer(...) + identity(...) if they differ
  .use(solanaDevnetRpc()); // or solanaMainnetRpc({ rpcUrl: 'https://...' })

await client.sendTransaction([myInstruction]);
```

`solanaDevnetRpc()` defaults to `https://api.devnet.solana.com` and bundles airdrop. `solanaMainnetRpc({ rpcUrl })` is type-narrowed to a mainnet URL — no devnet-only methods like `airdrop`.

### Testing with LiteSVM

```ts
import { createClient, lamports } from '@solana/kit';
import { litesvm } from '@solana/kit-plugin-litesvm';
import { airdropSigner, generatedSigner } from '@solana/kit-plugin-signer';

const client = await createClient()
  .use(generatedSigner())
  .use(litesvm())
  .use(airdropSigner(lamports(1_000_000_000n)));

client.svm.addProgramFromFile(myProgramAddress, 'program.so');
await client.sendTransaction([myInstruction]);
```

Full documentation: [LiteSVM](https://www.litesvm.com/docs/typescript/getting-started).

## Kit v7.0.0 — What's New

### Transaction Versions

Kit v7.0.0 provides full support for Solana's three transaction message versions:

| Version | `createTransactionMessage({ version })` | Description |
|---------|------------------------------------------|-------------|
| **Legacy** | `{ version: 'legacy' }` | Original format, no ALT support. Max 35 accounts. |
| **v0** | `{ version: 0 }` | Address Lookup Table (ALT) support, compact account encoding. Up to 256 accounts. **Default recommendation.** |
| **v1** | `{ version: 1 }` | Future-proofed for upcoming features. |

```ts
import { createTransactionMessage } from '@solana/kit';

// Legacy (compatibility with older validators)
const legacyMsg = createTransactionMessage({ version: 'legacy' });

// Version 0 (recommended — ALT support, smaller tx size)
const v0Msg = createTransactionMessage({ version: 0 });

// Version 1 (forward-compatible)
const v1Msg = createTransactionMessage({ version: 1 });
```

**Default to version 0** for new applications. Use legacy only when interacting with services that don't support versioned transactions.

### @solana/transaction-introspection (NEW)

Parse confirmed transaction instructions using Kit program clients. This package lets you decode individual instructions within a confirmed transaction, even if they were emitted by programs you didn't build.

```bash
npm install @solana/transaction-introspection
```

```ts
import { parseTransactionInstructions } from '@solana/transaction-introspection';
import { getTransferSolInstructionParser } from '@solana-program/system';
import { getTokenInstructionParser } from '@solana-program/token';

// Fetch a confirmed transaction from RPC
const confirmedTx = await rpc.getTransaction(signature, {
  maxSupportedTransactionVersion: 0, // Required for v0 transactions
  encoding: 'jsonParsed',
}).send();

// Parse instructions using Kit program clients
const instructions = parseTransactionInstructions(confirmedTx, [
  getTransferSolInstructionParser(),
  getTokenInstructionParser(),
]);

for (const ix of instructions) {
  if (ix.programAddress === SYSTEM_PROGRAM_ADDRESS) {
    console.log('System transfer:', ix.data);
  }
}
```

**Key use cases:**
- Transaction monitoring and indexing
- Audit trails — reconstruct what a transaction did
- Debugging — inspect failed transaction instructions
- Analytics — aggregate instruction-level data across transactions

**Important:** Always pass `maxSupportedTransactionVersion` when fetching transactions that may be v0. Without it, the RPC will reject versioned transactions.

### Other v7.0.0 Improvements

- Improved codec tree-shaking for smaller bundles
- Enhanced error messages with actionable context
- Better TypeScript inference for plugin composition
- Updated `@solana/react` decoupled from Kit core (see solana-frontend skill)

## Client API

After applying `solanaRpc` / `solanaLocalRpc` / `solanaDevnetRpc` / `solanaMainnetRpc` (or `litesvm`), the client exposes:

| Property/Method | Description |
|-----------------|-------------|
| `client.rpc` | RPC methods (`getBalance`, `getAccountInfo`, etc.) |
| `client.rpcSubscriptions` | WebSocket subscriptions (RPC plugins only) |
| `client.payer` | Transaction fee payer signer (set by `signer()` or `payer()`) |
| `client.identity` | Authority signer (set by `signer()` or `identity()`) |
| `client.sendTransaction(instructions)` | Plan + sign + send in one call |
| `client.sendTransactions(plan)` | Execute a planned multi-tx plan |
| `client.planTransaction(s)` | Plan without executing |
| `client.getMinimumBalance(dataSize)` | Rent-exempt minimum lamports |
| `client.airdrop(address, lamports)` | Faucet (devnet/local/litesvm only) |
| `client.svm` | LiteSVM instance (litesvm plugin only) |

`solanaRpc({ ... })` accepts `rpcUrl` (required) plus `rpcSubscriptionsUrl`, `transactionConfig` (priority fees), `maxConcurrency`, `skipPreflight`, and the underlying `rpcConfig` / `rpcSubscriptionsConfig`. See [plugins.md](references/kit/plugins.md) for the full options table, plugin catalog, and custom composition.

## Core Concepts

### Branded Types

```ts
import { address, lamports, signature } from '@solana/kit';

const myAddress = address('So11111111111111111111111111111111111111112');
const myLamports = lamports(1_000_000_000n);
const mySig = signature('5eykt...');
```

### Signers

```ts
import { generateKeyPairSigner } from '@solana/kit';
const signer = await generateKeyPairSigner();
// signer.address — the public key
// signer is a TransactionSigner
```

Kit clients hold two signer roles:
- **`payer`** — pays fees and rent
- **`identity`** — wallet/authority for application accounts

In most apps both roles are the same keypair, so **default to the `signer*` variants** — they install one keypair into both slots in one call. Use the role-specific `payer*` / `identity*` variants only when fees and authority come from different keypairs (e.g., gasless flows, treasury accounts, multisig).

| Variant | Sets |
|---|---|
| `signer*` (recommended default) | both `payer` and `identity` (same keypair) |
| `payer*` | only `payer` |
| `identity*` | only `identity` |

| Plugin | Behavior |
|---|---|
| `signer(s)` / `payer(s)` / `identity(s)` | Install an existing `TransactionSigner` |
| `generatedSigner()` / `generatedPayer()` / `generatedIdentity()` | Async; generate a new keypair |
| `generatedSignerWithSol(amount)` / `generatedPayerWithSol(amount)` / `generatedIdentityWithSol(amount)` | Async; generate + airdrop. Requires an airdrop function already on the client |
| `signerFromFile(path)` / `payerFromFile(path)` / `identityFromFile(path)` | Async; load keypair from a JSON file |
| `airdropSigner(amount)` / `airdropPayer(amount)` / `airdropIdentity(amount)` | Airdrop SOL to an already-installed signer |

### Codec Direction

- **`encode()`**: values → `Uint8Array`
- **`decode()`**: `Uint8Array` → values

Always use native codecs (e.g., `getBase58Codec()`). Never import bs58.

## Common Patterns

### Send SOL Transfer

```ts
import { createClient, address, lamports } from '@solana/kit';
import { solanaLocalRpc } from '@solana/kit-plugin-rpc';
import { signerFromFile } from '@solana/kit-plugin-signer';
import { getTransferSolInstruction } from '@solana-program/system';

const client = await createClient()
  .use(signerFromFile('~/.config/solana/id.json'))
  .use(solanaLocalRpc());

const ix = getTransferSolInstruction({
  source: client.payer,
  destination: address('recipient...'),
  amount: lamports(1_000_000_000n),
});

const sig = await client.sendTransaction([ix]);
// Verify on Explorer: https://explorer.solana.com/tx/{sig}?cluster=devnet
```

### Fetch Account

```ts
import { fetchEncodedAccount, assertAccountExists, decodeAccount } from '@solana/kit';

const account = await fetchEncodedAccount(client.rpc, myAddress);
assertAccountExists(account);
const decoded = decodeAccount(account, myDecoder);
```

### Token Operations

Use the `tokenProgram()` plugin from `@solana-program/token` for a fluent token API. It auto-derives ATAs, auto-creates them if needed, and defaults the payer from the client.

```ts
import { createClient, generateKeyPairSigner } from '@solana/kit';
import { solanaLocalRpc } from '@solana/kit-plugin-rpc';
import { signerFromFile } from '@solana/kit-plugin-signer';
import { tokenProgram } from '@solana-program/token';

const client = await createClient()
  .use(signerFromFile('~/.config/solana/id.json'))
  .use(solanaLocalRpc())
  .use(tokenProgram());

const mintAuthority = await generateKeyPairSigner();
const mint = await generateKeyPairSigner();

// Create a new mint
await client.token.instructions
  .createMint({ newMint: mint, decimals: 2, mintAuthority: mintAuthority.address })
  .sendTransaction();

// Mint tokens to an owner's ATA (created automatically if needed)
await client.token.instructions
  .mintToATA({
    mint: mint.address,
    owner: recipientAddress,
    mintAuthority,
    amount: 1_000_000n,
    decimals: 2,
  })
  .sendTransaction();
```

### Transaction Introspection (Parse Confirmed Transaction)

```ts
import { parseTransactionInstructions } from '@solana/transaction-introspection';
import { getTransferSolInstructionParser } from '@solana-program/system';

// Fetch confirmed transaction — MUST set maxSupportedTransactionVersion for v0
const confirmedTx = await client.rpc
  .getTransaction(signature, {
    maxSupportedTransactionVersion: 0,
    encoding: 'jsonParsed',
  })
  .send();

// Parse all instructions using registered program parsers
const parsed = parseTransactionInstructions(confirmedTx, [
  getTransferSolInstructionParser(),
]);

for (const ix of parsed) {
  console.log(`${ix.programAddress}:`, ix.data);
}
```

### RPC Queries

```ts
// Balance
const { value: balance } = await client.rpc.getBalance(myAddress).send();

// Token accounts
const { value: tokenAccs } = await client.rpc.getTokenAccountsByOwner(
  owner,
  { mint: mintAddr },
  { encoding: 'jsonParsed' },
).send();

// Latest blockhash
const { value: blockhash } = await client.rpc.getLatestBlockhash().send();
```

## Codama Generated Clients

`@solana-program/*` packages are Codama-generated, Kit-compatible clients for Solana programs.

### Available Packages

| Package | Purpose |
|---------|------------|
| `@solana-program/system` | Account creation, transfers, nonces |
| `@solana-program/token` | SPL Token operations |
| `@solana-program/token-2022` | Token Extensions (transfer fees, metadata, etc.) |
| `@solana-program/compute-budget` | CU limits & priority fees |
| `@solana-program/memo` | Memo program |
| `@solana-program/stake` | Staking operations |

**Note:** These packages export both low-level `get{Name}Instruction()` helpers and higher-level program plugins (e.g., `tokenProgram()`) that attach fluent APIs to the client. ATA functions are in `@solana-program/token` and `@solana-program/token-2022`, not a separate package.

### Naming Conventions

| Category | Pattern | Example |
|----------|---------|---------|
| Program address | `{PROGRAM}_PROGRAM_ADDRESS` | `SYSTEM_PROGRAM_ADDRESS` |
| Instructions | `get{Name}Instruction()` | `getTransferSolInstruction()` |
| Instruction parse | `parse{Name}Instruction()` | `parseTransferSolInstruction()` |
| Account fetch | `fetch{Account}()` | `fetchMint()` |
| Account fetch maybe | `fetchMaybe{Account}()` | `fetchMaybeMint()` |
| Account fetch all | `fetchAll{Account}()` | `fetchAllMint()` |
| Account decode | `decode{Account}()` | `decodeMint()` |
| Account size | `get{Account}Size()` | `getMintSize()` |
| Codec | `get{Type}[Encoder\|Decoder\|Codec]()` | `getMintDecoder()` |
| PDA derivation | `find{Name}Pda()` | `findAssociatedTokenPda()` |
| Errors | `{PROGRAM}_ERROR__{NAME}` | `SYSTEM_ERROR__INSUFFICIENT_FUNDS` |
| Error check | `is{Program}Error()` | `isSystemError()` |

## Legacy Interop (Kit ↔ web3.js)

### The Rule

- **New code:** Kit types and Kit-first APIs.
- **Legacy dependencies:** isolate web3.js-shaped types behind an adapter boundary.

### Preferred Bridge: @solana/web3-compat

Use `@solana/web3-compat` when:
- A dependency expects `PublicKey`, `Keypair`, `Transaction`, `VersionedTransaction`, `Connection`, etc.
- You are migrating an existing web3.js codebase incrementally.

### Conversion Helpers

Use web3-compat helpers such as:
- `toAddress(...)`
- `toPublicKey(...)`
- `toWeb3Instruction(...)`
- `toKitSigner(...)`

### Decision Checklist

If you're about to add web3.js:
1. Is there a Kit-native equivalent? Prefer Kit.
2. Is the only reason a dependency? Use web3-compat at the boundary.
3. Can you generate a Kit-native client (Codama) instead? Prefer codegen.

## Package Overview (v7.0.0)

| Package | Purpose |
|---------|---------|
| `@solana/kit` | Main SDK, re-exports all sub-packages, exports `createClient` |
| `@solana/kit-plugin-rpc` | All-in-one RPC plugins: `solanaRpc`, `solanaMainnetRpc`, `solanaDevnetRpc`, `solanaLocalRpc` |
| `@solana/kit-plugin-signer` | Signer plugins. Default `signer*` variants set both `payer` and `identity` |
| `@solana/kit-plugin-litesvm` | All-in-one `litesvm` plugin (Node.js only) for in-memory testing |
| `@solana/kit-plugin-airdrop` | Standalone airdrop plugin |
| `@solana/kit-plugin-instruction-plan` | `planAndSendTransactions` and instruction batching |
| `@solana/transaction-introspection` | **NEW** — Parse confirmed transaction instructions with Kit program clients |
| `@solana/addresses` | Address validation |
| `@solana/accounts` | Account fetching/decoding |
| `@solana/codecs` | Data encoding/decoding |
| `@solana/rpc` | JSON RPC client primitives |
| `@solana/rpc-subscriptions` | WebSocket subscription primitives |
| `@solana/transactions` | Compile/sign/serialize (Legacy, v0, v1) |
| `@solana/transaction-messages` | Build tx messages (versioned) |
| `@solana/signers` | Signing abstraction |
| `@solana/keychain` | Common Signing Interface for external signers |
| `@solana/instruction-plans` | Multi-instruction batching |
| `@solana/errors` | Error identification/decoding |
| `@solana/functional` | Pipe and compose utilities |
| `@solana/react` | React wallet hooks (decoupled from Kit core in v7.0.0 — see solana-frontend skill) |
| `@solana/web3-compat` | Legacy web3.js interop |

## Best Practices

1. **Compose with `.use()`** — `createClient().use(signer(...)).use(solanaRpc(...))`; the signer plugin must come before the RPC/litesvm plugin.
2. **Use branded types** — `address()`, `lamports()`, `signature()`.
3. **Use `@solana-program/*`** instruction builders over hand-rolled instruction data.
4. **Handle account existence** — `assertAccountExists()` before decode.
5. **Set compute budget** — pass `transactionConfig` to `solanaRpc({ ... })` or use manual CU estimation for production.
6. **Default to version 0 transactions** — smaller size, ALT support. Use legacy only for compatibility.
7. **Set `maxSupportedTransactionVersion`** when fetching transactions that may be v0.
8. **Use `@solana/transaction-introspection`** for parsing confirmed transaction instructions.

## CLI Usage (NO_DNA)

This skill is a reference skill for code generation. It does not define CLI commands directly. However, when using Solana CLI alongside Kit clients:

- All CLI commands use `NO_DNA=1` prefix: `NO_DNA=1 solana config set --url devnet`
- Verify all transactions on Explorer: `https://explorer.solana.com/tx/{sig}?cluster=devnet`
- Use MCP server for live docs: `https://mcp.solana.com/mcp`

## Cross-Skill References

| Related Skill | When to Switch |
|--------------|----------------|
| `solana-frontend` | Building dApp UI with React/wallet integration. `@solana/react` decoupled from Kit in v7.0.0. |
| `solana-rpc-data` | Deep RPC method reference, RPC 2.0 methods, gRPC streaming, commitment levels, subscription patterns. |
| `solana-anchor-programs` | Writing/building Anchor programs that Kit clients interact with via Codama-generated clients. |
| `solana-errors-and-compat` | Kit-specific gotchas, version conflicts, GLIBC issues, error decoding. |
| `solana-testing` | LiteSVM/Mollusk/Surfpool testing with Kit clients. |
| `solana-tokens-spl` | SPL Token and Token-2022 program interactions. |
| `solana-deployment-devops` | Deploying programs that Kit clients call. |

## Verification Checklist

Before shipping Kit client code:

- [ ] Using `@solana/kit` v7.0.0+ (check `package.json`)
- [ ] Branded types used everywhere (`address()`, `lamports()`, `signature()`)
- [ ] `createClient()` + `.use()` plugin composition (not direct RPC calls)
- [ ] Signer plugin installed before RPC plugin (TypeScript enforces ordering)
- [ ] Transaction version explicitly set (`version: 0` recommended)
- [ ] `maxSupportedTransactionVersion` set when fetching confirmed transactions
- [ ] `assertAccountExists()` called before `decodeAccount()`
- [ ] `@solana-program/*` instruction builders used (not hand-rolled data)
- [ ] Compute budget set for production transactions (priority fees)
- [ ] NO_DNA=1 prefix on all Solana CLI commands
- [ ] Devnet configured: `NO_DNA=1 solana config set --url devnet`
- [ ] Transactions verified on https://explorer.solana.com
- [ ] `@solana/transaction-introspection` used for confirmed tx parsing (when needed)
- [ ] MCP server consulted for live docs before falling back to training data
- [ ] No raw `bs58` imports — using `getBase58Codec()` instead

## Progressive Disclosure — Deeper References

Load these files with `skills_tool` action `read_file` when you need deeper patterns:

### Plugins & Client Composition

```
skill_name: solana-client
file_path: references/kit/plugins.md
```

Covers: all-in-one RPC variants and full options table, signer plugin catalog, LiteSVM test client, custom low-level composition, async plugins, third-party plugins, and domain-specific clients.

### Advanced Patterns (Manual Transactions, Direct RPC, Custom Plugins)

```
skill_name: solana-client
file_path: references/kit/advanced.md
```

Covers: manual transaction pipeline with pipe composition, fee payer + lifetime + instructions + sign + send, direct RPC client creation, RPC method reference, building custom plugins, assembling domain-specific clients.

### Account Operations

```
skill_name: solana-client
file_path: references/kit/accounts.md
```

Covers: batch fetching, PDAs, subscriptions, token queries, account existence checks, decoding patterns.

### Codecs

```
skill_name: solana-client
file_path: references/kit/codecs.md
```

Covers: complete codec patterns, built-in codecs, custom codecs, struct/tuple codecs, nullable options, data size hints.

## See Also

- **solana-anchor-programs** — for programs being called via Anchor IDL
- **solana-frontend** — UI layer using Kit (`@solana/react` decoupled in v7.0.0)
- **solana-rpc-data** — deep RPC method reference, RPC 2.0 methods, gRPC streaming
- **solana-errors-and-compat** — Kit-specific gotchas and common error fixes
