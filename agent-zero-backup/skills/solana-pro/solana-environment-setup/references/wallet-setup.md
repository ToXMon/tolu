# Wallet Setup — Keypair Generation, Import, and Configuration

Complete guide to Solana wallet setup for development. Covers CLI keypair generation, importing from base58 (Phantom), hardware wallet config, and multi-wallet management.

## Solana Wallet Fundamentals

A Solana wallet is an Ed25519 keypair:
- **Public key** (32 bytes) — Your address, shareable
- **Secret key** (32 bytes) — Used for signing, NEVER share
- **Keypair file** — JSON array of 64 integers (secret + public key concatenated)

The standard wallet location is `~/.config/solana/id.json`.

## Method 1: Generate New Keypair (CLI)

### Basic Generation

```bash
# Generate keypair at default location
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json

# Output will show:
# Generating new keypair: /home/user/.config/solana/id.json
# Wrote new keypair to /home/user/.config/solana/id.json
# ===========================================================================
# pubkey: 7xKXt...Dy3M
# ===========================================================================
# Save this seed phrase to recover your new keypair:
# <12-24 word mnemonic>
# ===========================================================================
```

### With Custom BIP39 Passphrase

```bash
# Generate with additional passphrase
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json --no-bip39-passphrase

# Or with passphrase (will prompt)
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json
```

### With Custom Seed (Reproducible)

```bash
# Generate from a specific seed phrase
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json --seed
# Paste your 12-24 word mnemonic when prompted
```

### Force Overwrite

```bash
# Overwrite existing keypair (DANGEROUS)
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json --force
```

### Set as Default Wallet

```bash
# Set as default keypair for CLI
NO_DNA=1 solana config set --keypair ~/.config/solana/id.json

# Verify
NO_DNA=1 solana config get
```

## Method 2: Import from Base58 (Phantom/Backpack)

If you have a base58-encoded private key from Phantom or another wallet:

### Step 1: Install base58 Library

```bash
pip install base58
```

### Step 2: Convert and Save

```python
import base58
import json
import os

# Your base58-encoded private key from Phantom
# In Phantom: Settings → Export Private Key
pk_b58 = 'YOUR_BASE58_PRIVATE_KEY_HERE'

# Decode to bytes
data = base58.b58decode(pk_b58)

# Check if it's 64 bytes (keypair format) or 32 bytes (seed format)
if len(data) == 64:
    keypair_bytes = data
elif len(data) == 32:
    from nacl.signing import SigningKey
    sk = SigningKey(data)
    keypair_bytes = bytes(sk) + bytes(sk.verify_key)
else:
    raise ValueError(f"Unexpected key length: {len(data)}")

# Convert to JSON array format
keypair_list = list(keypair_bytes)

# Save to file
keypair_path = os.path.expanduser('~/.config/solana/id.json')
os.makedirs(os.path.dirname(keypair_path), exist_ok=True)
with open(keypair_path, 'w') as f:
    json.dump(keypair_list, f)

# Set permissions
os.chmod(keypair_path, 0o600)

print(f"Wallet saved to {keypair_path}")
print(f"Public key: {base58.b58encode(keypair_bytes[32:]).decode()}")
```

### Step 3: Verify

```bash
# Set as default
NO_DNA=1 solana config set --keypair ~/.config/solana/id.json

# Check address matches expected
NO_DNA=1 solana address

# Check balance
NO_DNA=1 solana balance
```

## Method 3: Restore from Mnemonic

```bash
# Restore from seed phrase
NO_DNA=1 solana-keygen recover -o ~/.config/solana/id.json
# Enter your 12-24 word mnemonic when prompted
```

## Method 4: Multiple Wallets

### Create Additional Wallets

```bash
# Create a second wallet (e.g., for testing recipient)
NO_DNA=1 solana-keygen new -o ~/.config/solana/wallet2.json

# Create a third wallet
NO_DNA=1 solana-keygen new -o ~/.config/solana/wallet3.json
```

### Switch Between Wallets

```bash
# Switch to wallet2
NO_DNA=1 solana config set --keypair ~/.config/solana/wallet2.json

# Check current address
NO_DNA=1 solana address

# Switch back to default
NO_DNA=1 solana config set --keypair ~/.config/solana/id.json
```

### Use Wallet Without Setting Default

```bash
# Use specific keypair for a single command
NO_DNA=1 solana balance --keypair ~/.config/solana/wallet2.json
NO_DNA=1 solana address --keypair ~/.config/solana/wallet2.json
```

## Phantom Wallet Configuration

### Connect Phantom to Devnet

1. Open Phantom browser extension
2. Click **Settings** (gear icon)
3. Click **Change Network**
4. Select **Devnet**

### Import CLI Wallet to Phantom

1. Get your keypair array:
   ```bash
   cat ~/.config/solana/id.json
   ```
2. Open Phantom → Settings → **Import Private Key**
3. Select **Solana**
4. Paste the JSON array or base58 private key
5. Name the account (e.g., "Devnet CLI")

### Export Phantom Private Key for CLI

1. Open Phantom → Settings → **Show Private Key**
2. Enter password
3. Copy the base58 private key
4. Follow Method 2 above to convert to CLI format

## File Permissions

```bash
# Set secure permissions
chmod 600 ~/.config/solana/id.json

# Verify permissions
ls -la ~/.config/solana/id.json
# Expected: -rw------- 1 user user  ... id.json
```

**Rule:** Keypair files should be `600` (owner read/write only). Never `644` or world-readable.

## Funding Wallets

### Devnet

```bash
# Airdrop 2 SOL (CLI)
NO_DNA=1 solana airdrop 2

# Airdrop to specific address
NO_DNA=1 solana airdrop 2 <RECIPIENT_ADDRESS>

# Use web faucet if rate-limited
# https://faucet.solana.com
```

### Testnet

```bash
# Switch to testnet
NO_DNA=1 solana config set --url testnet

# Airdrop
NO_DNA=1 solana airdrop 2

# Web faucet: https://faucet.solana.com (select testnet)
```

### Mainnet (REAL FUNDS)

```bash
# DANGER: This uses real SOL
NO_DNA=1 solana config set --url mainnet-beta

# Cannot airdrop on mainnet — must transfer from exchange or another wallet
# Use `solana transfer <address> <amount>` from a funded wallet
```

## Anchor.toml Wallet Configuration

In your `Anchor.toml`:

```toml
[provider]
cluster = "Devnet"
wallet = "~/.config/solana/id.json"
```

For alternative wallet paths:

```toml
[provider]
cluster = "Devnet"
wallet = "~/.config/solana/wallet2.json"
```

## Keypair in TypeScript Tests

```typescript
import * as anchor from "@coral-xyz/anchor";
import { Keypair } from "@solana/web3.js";

// Load default wallet
const wallet = anchor.Wallet.local();

// Load custom wallet
import fs from "fs";
const keypairData = JSON.parse(
  fs.readFileSync(process.env.HOME + "/.config/solana/wallet2.json", "utf-8")
);
const customWallet = new Keypair(keypairData);
```

## Using @solana/kit (Modern Client)

```typescript
import {
  createKeyPairSignerFromBytes,
  getBase58Encoder,
} from "@solana/kit";

// From base58
const keypairBytes = getBase58Encoder().encode(base58PrivateKey);
const signer = await createKeyPairSignerFromBytes(keypairBytes);

// From file
import fs from "fs";
const keypairData = JSON.parse(
  fs.readFileSync("~/.config/solana/id.json", "utf-8")
);
const signer = await createKeyPairSignerFromBytes(new Uint8Array(keypairData));
```

## Security Best Practices

1. **Never commit keypair files** — Add to `.gitignore`:
   ```
   # .gitignore
   *.json
   !package.json
   !tsconfig.json
   !Anchor.toml
   id.json
   wallet*.json
   ```

2. **Set file permissions** — `chmod 600 ~/.config/solana/*.json`

3. **Use separate wallets** — Don't reuse mainnet wallet for devnet testing

4. **Fund devnet wallets via faucet** — Never transfer real SOL to devnet

5. **Backup seed phrases** — Store mnemonics offline, never in code or env files

6. **Don't export private keys in code** — Use environment variables or file paths

## Verification

```bash
# Verify wallet is configured correctly
NO_DNA=1 solana config get
# Should show:
# Keypair Path: /home/user/.config/solana/id.json

NO_DNA=1 solana address
# Should show your address

NO_DNA=1 solana balance
# Should show > 0 SOL on devnet

# Verify file permissions
ls -la ~/.config/solana/id.json
# Should show: -rw------- (600)
```

## Troubleshooting

### "Keypair not found" error

```bash
# Check file exists
ls -la ~/.config/solana/id.json

# If missing, regenerate
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json
```

### Wrong network balance

```bash
# Check current cluster
NO_DNA=1 solana config get

# Switch to devnet if needed
NO_DNA=1 solana config set --url devnet
```

### "Invalid private key" when importing

- Ensure you're using the base58-encoded **secret key**, not the public key
- The secret key is typically 88-90 characters in base58
- Verify the key decodes to 64 bytes (keypair format) or 32 bytes (seed)

### Phantom shows different balance than CLI

- Ensure Phantom is set to **Devnet** (not Mainnet)
- Ensure CLI is set to devnet: `solana config set --url devnet`
- Wait 10-30 seconds for RPC sync
