---
title: Solana Kit Gotchas (Enhanced)
description: Common type errors and runtime pitfalls with @solana/kit including Kit v7.0.0 gotchas, @solana/react decoupling, @solana/transaction-introspection, and transaction version handling.
---

# Solana Kit Gotchas (Enhanced)

Common type errors and runtime pitfalls with `@solana/kit` and their fixes, including Kit v7.0.0 specific changes.

> **Protocol**: All CLI commands use `NO_DNA=1` prefix. All work targets devnet unless stated otherwise.

## Plugin Client Gotchas

### Plugin Ordering — Type Error

**Cause:** Plugins installed before their dependencies. `solanaRpc` / `solanaLocalRpc` / `solanaDevnetRpc` / `litesvm` all require a `payer` to be installed first.

```ts
// ❌ Type error — solanaRpc requires payer
createClient()
  .use(solanaRpc({ rpcUrl: url }))
  .use(signer(mySigner));

// ✅ Fix: signer first (sets payer + identity), then RPC bundle
createClient()
  .use(signer(mySigner))
  .use(solanaRpc({ rpcUrl: url }));
```

### Forgetting to `await` Async Client

**Cause:** Some plugins (e.g., `signerFromFile`, `generatedSigner`, `generatedSignerWithSol`) are async.

```ts
// ❌ Runtime error — client is a Promise, not a client
const client = createClient()
  .use(signerFromFile('./id.json'))
  .use(solanaLocalRpc());
client.sendTransaction([ix]); // TypeError: not a function

// ✅ Fix: await the client
const client = await createClient()
  .use(signerFromFile('./id.json'))
  .use(solanaLocalRpc());
await client.sendTransaction([ix]);
```

---

## Type Errors

### `IInstruction` does not exist

**Cause:** Using old type name from legacy web3.js.

```ts
// ❌ Type error
import { IInstruction } from '@solana/kit';

// ✅ Fix: Use Instruction
import type { Instruction } from '@solana/kit';
```

### "Transaction message must be signed"

**Cause:** Trying to send unsigned message (manual pipeline only).

```ts
import { assertTransactionMessageIsFullySigned } from '@solana/transaction-messages';
assertTransactionMessageIsFullySigned(message);
```

### "Missing blockhash lifetime"

**Cause:** Message missing lifetime before signing/sending (manual pipeline only).

```ts
import { assertTransactionMessageHasBlockhashLifetime } from '@solana/transaction-messages';
assertTransactionMessageHasBlockhashLifetime(message);
```

### `signAndSendTransactionMessageWithSigners` type error

**Cause:** Fee payer set as address, not signer.

```ts
// ❌ Type error — fee payer is address only
setTransactionMessageFeePayer(address, message);

// ✅ Fix: Use signer version
setTransactionMessageFeePayerSigner(signer, message);
```

### Wrong signer type for wallet

**Cause:** Using `TransactionSigner` for wallet that needs to send.

```ts
// Wallets that submit transactions need TransactionSendingSigner
type TransactionSendingSigner = {
  signAndSendTransactions(txs): Promise<SignatureBytes[]>;
};
```

### Missing Lifetime Type Assertion

**Cause:** `sendAndConfirm` requires typed lifetime assertion (manual pipeline only).

```ts
// ❌ Type error: Property '"__transactionWithBlockhashLifetime"' is missing
const signed = await signTransactionMessageWithSigners(message);
await sendAndConfirm(signed, { commitment: 'confirmed' });

// ✅ Fix: Assert lifetime + size types
assertIsTransactionWithBlockhashLifetime(signed);
assertIsTransactionWithinSizeLimit(signed);
await sendAndConfirm(signed, { commitment: 'confirmed' });
```

### Missing `TransactionWithinSizeLimit`

```ts
import { assertIsTransactionWithinSizeLimit } from '@solana/kit';
assertIsTransactionWithinSizeLimit(signed);
```

### RPC URL String vs Cluster Wrapper

```ts
// ❌ May cause issues
import { devnet } from '@solana/rpc-types';
const rpc = createSolanaRpc(devnet('https://my-custom-endpoint.com'));

// ✅ Simple: use raw URL strings directly
const rpc = createSolanaRpc('https://api.devnet.solana.com');
```

---

## Runtime Errors

### "Account does not exist"

**Cause:** Decoding account that may not exist.

```ts
// ❌ Runtime error if account missing
const account = await fetchEncodedAccount(rpc, address);
const decoded = decodeAccount(account, decoder);

// ✅ Fix: Assert existence first
const account = await fetchEncodedAccount(rpc, address);
assertAccountExists(account);
const decoded = decodeAccount(account, decoder);
```

### Blockhash expired after CU estimation

**Cause:** Simulation takes time, blockhash ages out. Only applies to manual pipeline.

```ts
// ❌ Blockhash may expire
let message = pipe(...blockhash...);
message = await estimateAndUpdateCU(message);
await signAndSendTransactionMessageWithSigners(message);

// ✅ Fix: Refresh blockhash AFTER estimation
let message = pipe(...blockhash...);
message = await estimateAndUpdateCU(message);
const { value: freshBlockhash } = await rpc.getLatestBlockhash().send();
message = setTransactionMessageLifetimeUsingBlockhash(freshBlockhash, message);
await signAndSendTransactionMessageWithSigners(message);
```

### Simulation fails with "account not found"

**Cause:** Account doesn't exist yet (e.g., PDA not initialized).

```ts
const account = await fetchEncodedAccount(rpc, address);
if (!account.exists) {
  // Handle missing account — may need to create it first
}
```

---

## Kit v7.0.0 Specific Gotchas (NEW)

### Node.js 20+ Required

Kit v7.0.0 requires Node.js 20 or higher. Verify before installing:

```bash
NO_DNA=1 node --version  # must be >= 20.x
```

If on Node 18 or lower, upgrade first:
```bash
# Using nvm
nvm install 20
nvm use 20
```

### `@solana/react` Decoupled from Kit

In Kit v7.0.0, React hooks are no longer bundled with `@solana/kit`. They live in a separate `@solana/react` package.

```ts
// ❌ Before (Kit v6.x) — React hooks came with Kit
import { useWallet, useConnection } from '@solana/kit';

// ✅ After (Kit v7.0.0) — install @solana/react separately
// npm install @solana/react
import { useWallet, useConnection } from '@solana/react';
```

**Error if not installed:**
```
Module not found: Can't resolve '@solana/kit' exporting 'useWallet'
```

**Fix:** Install the React package:
```bash
npm install @solana/react
```

### `@solana/transaction-introspection` (NEW Package)

Kit v7.0.0 introduces `@solana/transaction-introspection` for transaction analysis and introspection.

```ts
// Install if needed:
// npm install @solana/transaction-introspection

import { 
  getTransactionDecoder,
  parseTransaction,
  getInstructionFromTransaction
} from '@solana/transaction-introspection';

// Decode and inspect a transaction
const decoder = getTransactionDecoder();
const decodedTx = decoder.decode(serializedTransaction);
const instructions = decodedTx.message.instructions;
```

**Common error if not installed:**
```
Module not found: Can't resolve '@solana/transaction-introspection'
```

**Fix:** Install the package:
```bash
npm install @solana/transaction-introspection
```

### Transaction Versions (Legacy, v0, v1)

Kit v7.0.0 supports three transaction versions. You must handle version-specific logic:

```ts
import {
  assertIsTransactionWithBlockhashLifetime,
  isTransactionWithDurableNonceLifetime
} from '@solana/transactions';

// Legacy transactions (version 0)
const legacyTx = {
  message: { version: 'legacy' as const, ... },
  signatures: [...],
};

// Versioned transactions (v0)
const v0Tx = {
  message: { version: 0 as const, addressTableLookups: [...] },
  signatures: [...],
};

// Versioned transactions (v1) — future use
const v1Tx = {
  message: { version: 1 as const, ... },
  signatures: [...],
};
```

**Gotcha: Mixing transaction versions**
```ts
// ❌ Type error — can't mix Legacy and v0 in same array
const transactions = [legacyTx, v0Tx]; // Type error

// ✅ Fix: Use union type or separate handling
const transactions: BaseTransaction[] = [legacyTx, v0Tx];
// Or handle separately
```

**Gotcha: Address Lookup Tables with Legacy transactions**
```ts
// ❌ Legacy transactions don't support ALTs
const legacyMessage = setTransactionMessageLifetimeUsingBlockhash(blockhash, message);
// Cannot use addressTableLookups on legacy messages

// ✅ v0 transactions support ALTs
import { compileV0Message } from '@solana/kit';
const v0Message = compileV0Message({
  addressTableLookups: [altAccount],
  // ...
});
```

### Package.json Updates for Kit v7.0.0

```json
{
  "dependencies": {
    "@solana/kit": "^7.0.0",
    "@solana/react": "^7.0.0",
    "@solana/transaction-introspection": "^7.0.0"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

### Import Path Changes in v7.0.0

Some imports have moved between packages in v7.0.0:

```ts
// Transaction-related types now split across packages
import { 
  assertIsTransactionWithBlockhashLifetime,
  assertIsTransactionWithinSizeLimit 
} from '@solana/transactions';

import {
  assertTransactionMessageIsFullySigned,
  assertTransactionMessageHasBlockhashLifetime
} from '@solana/transaction-messages';

// Introspection moved to its own package
import {
  getTransactionDecoder,
  parseTransaction
} from '@solana/transaction-introspection';
```

---

## Quick Reference

| Gotcha | Fix |
|--------|-----|
| Plugin ordering type error | Install dependencies before dependents (`signer()` before `solanaRpc`/`litesvm`) |
| Forgot to `await` async client | `const client = await createClient().use(signerFromFile(...)).use(solanaLocalRpc())` |
| `IInstruction` doesn't exist | Use `Instruction` from `@solana/kit` |
| "Transaction message must be signed" | `assertTransactionMessageIsFullySigned(msg)` |
| "Missing blockhash lifetime" | `assertTransactionMessageHasBlockhashLifetime(msg)` |
| Blockhash expired after CU estimation | Refresh blockhash AFTER `estimateAndUpdateCU()` |
| `signAndSendTransactionMessageWithSigners` type error | Use `setTransactionMessageFeePayerSigner` (not address) |
| Account doesn't exist runtime error | `assertAccountExists(account)` before decode |
| Wrong signer type for wallet | Use `TransactionSendingSigner` for wallets |
| Missing lifetime type on send | `assertIsTransactionWithBlockhashLifetime(signed)` |
| Missing size type on send | `assertIsTransactionWithinSizeLimit(signed)` |
| Durable nonce send type error | `assertIsTransactionWithDurableNonceLifetime(signed)` |
| `lifetimeConstraint` lost after deserialize | Re-attach `lifetimeConstraint` metadata manually |
| RPC URL wrapper issues | Use raw URL strings instead of `devnet()`/`mainnet()` |
| **Kit v7: `useWallet` not found** | Install `@solana/react` separately (decoupled from Kit) |
| **Kit v7: `transaction-introspection` not found** | Install `@solana/transaction-introspection` package |
| **Kit v7: Node version too low** | Upgrade to Node 20+ (`nvm install 20`) |
| **Kit v7: Mixing transaction versions** | Use union types or handle Legacy/v0/v1 separately |
| **Kit v7: ALTs on Legacy tx** | Use v0 transactions for Address Lookup Tables |

## Kit v7.0.0 Migration Checklist

- [ ] Node.js upgraded to 20+
- [ ] `@solana/kit` updated to `^7.0.0`
- [ ] `@solana/react` installed if using React hooks
- [ ] `@solana/transaction-introspection` installed if doing tx analysis
- [ ] `package.json` `engines.node` set to `>=20.0.0`
- [ ] Transaction version handling reviewed (Legacy/v0/v1)
- [ ] Import paths updated for moved types
- [ ] All tests pass with Kit v7.0.0
