# CLI Reference — Solana CLI and Anchor CLI Commands

Complete command reference for Solana development. All commands use `NO_DNA=1` prefix.

## Solana CLI

### Configuration

#### `solana config set`

Set CLI configuration options.

```bash
# Set cluster
NO_DNA=1 solana config set --url devnet
NO_DNA=1 solana config set --url mainnet-beta
NO_DNA=1 solana config set --url localhost

# Set keypair
NO_DNA=1 solana config set --keypair ~/.config/solana/id.json

# Set commitment level
NO_DNA=1 solana config set --commitment confirmed

# Set all at once
NO_DNA=1 solana config set --url devnet --keypair ~/.config/solana/id.json --commitment confirmed
```

**Options:**
| Flag | Description |
|------|-------------|
| `--url, -u` | Cluster URL (devnet, testnet, mainnet-beta, localhost, or custom URL) |
| `--keypair, -k` | Path to keypair file |
| `--commitment` | Commitment level: processed, confirmed, finalized |
| `--ws` | WebSocket URL (computed from RPC URL if not specified) |

#### `solana config get`

```bash
NO_DNA=1 solana config get
```

Shows current configuration: RPC URL, WebSocket URL, keypair path, commitment level.

#### `solana config import`

Import configuration from a file.

---

### Wallet Operations

#### `solana address`

```bash
# Get default wallet address
NO_DNA=1 solana address

# Get address from specific keypair
NO_DNA=1 solana address --keypair ~/.config/solana/wallet2.json
```

#### `solana balance`

```bash
# Get default wallet balance
NO_DNA=1 solana balance

# Get specific address balance
NO_DNA=1 solana balance <ADDRESS>

# Get balance with specific commitment
NO_DNA=1 solana balance --commitment finalized
```

#### `solana airdrop`

```bash
# Airdrop 2 SOL to default wallet
NO_DNA=1 solana airdrop 2

# Airdrop to specific address
NO_DNA=1 solana airdrop 2 <RECIPIENT_ADDRESS>
```

**Note:** Devnet airdrops are rate-limited. Use [web faucet](https://faucet.solana.com) if CLI fails.

#### `solana transfer`

```bash
# Transfer SOL
NO_DNA=1 solana transfer <RECIPIENT> 0.5

# Transfer with specific keypair
NO_DNA=1 solana transfer <RECIPIENT> 0.5 --keypair ~/.config/solana/wallet2.json

# Transfer with memo
NO_DNA=1 solana transfer <RECIPIENT> 0.5 --with-memo "Payment for services"
```

---

### Keypair Management

#### `solana-keygen new`

```bash
# Generate new keypair at default location
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json

# Generate with force overwrite
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json --force

# Generate without BIP39 passphrase
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json --no-bip39-passphrase

# Generate from seed phrase
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json --seed
```

#### `solana-keygen recover`

```bash
# Recover from mnemonic
NO_DNA=1 solana-keygen recover -o ~/.config/solana/id.json
```

#### `solana-keygen verify`

```bash
# Verify keypair matches address
NO_DNA=1 solana-keygen verify <PUBKEY> ~/.config/solana/id.json
```

#### `solana-keygen pubkey`

```bash
# Get public key from keypair file
NO_DNA=1 solana-keygen pubkey ~/.config/solana/id.json
```

---

### Program Deployment

#### `solana program deploy`

```bash
# Deploy a program
NO_DNA=1 solana program deploy ./target/deploy/my_program.so

# Deploy with specific program ID
NO_DNA=1 solana program deploy ./target/deploy/my_program.so --program-id ./target/deploy/my_program-keypair.json

# Deploy with upgrade authority
NO_DNA=1 solana program deploy ./target/deploy/my_program.so --upgrade-authority ~/.config/solana/id.json
```

#### `solana program show`

```bash
# Show program info
NO_DNA=1 solana program show <PROGRAM_ID>

# Show all programs
NO_DNA=1 solana program show --all
```

#### `solana program close`

```bash
# Close program (withdraw funds)
NO_DNA=1 solana program close <PROGRAM_ID>
```

---

### Account Operations

#### `solana account`

```bash
# Show account info
NO_DNA=1 solana account <ADDRESS>

# Show with base64 encoding
NO_DNA=1 solana account <ADDRESS> --output base64
```

#### `solana rent`

```bash
# Calculate rent for a data size
NO_DNA=1 solana rent 200

# Calculate rent for multiple sizes
NO_DNA=1 solana rent 0 128 256 512
```

---

### Transaction Operations

#### `solana confirm`

```bash
# Confirm transaction
NO_DNA=1 solana confirm <SIGNATURE>

# Confirm with verbose output
NO_DNA=1 solana confirm -v <SIGNATURE>
```

#### `solana signature-status`

```bash
# Get transaction signature status
NO_DNA=1 solana signature-status <SIGNATURE>
```

---

### Validator Operations

#### `solana-test-validator`

```bash
# Start local validator
NO_DNA=1 solana-test-validator

# Start with specific ledger directory
NO_DNA=1 solana-test-validator --ledger ./test-ledger

# Start with specific RPC port
NO_DNA=1 solana-test-validator --rpc-port 8899

# Start with pre-loaded programs
NO_DNA=1 solana-test-validator --bpf-program <PROGRAM_ID> <PROGRAM.so>

# Start with reset ledger
NO_DNA=1 solana-test-validator --reset
```

---

## Anchor CLI

### Project Management

#### `anchor init`

```bash
# Initialize new Anchor project
NO_DNA=1 anchor init my-project

# Initialize with specific template
NO_DNA=1 anchor init my-project --template counter
```

**Note:** `anchor init` creates a nested `.git` directory. Remove it if the project is inside an existing repo:
```bash
rm -rf my-project/.git
```

#### `anchor build`

```bash
# Build the program
NO_DNA=1 anchor build

# Build with Anchor logging enabled
ANCHOR_LOG=1 anchor build

# Build without IDL generation
NO_DNA=1 anchor build --no-idl

# Build with specific Cargo arguments
NO_DNA=1 anchor build -- --features my-feature
```

**Output:**
- Compiles Rust program to BPF/SBF bytecode
- Generates IDL in `target/idl/`
- Generates TypeScript types in `target/types/`
- Outputs `.so` file in `target/deploy/`

#### `anchor deploy`

```bash
# Deploy to configured cluster
NO_DNA=1 anchor deploy

# Deploy to specific cluster
NO_DNA=1 anchor deploy --provider.cluster devnet

# Deploy with specific keypair
NO_DNA=1 anchor deploy --provider.wallet ~/.config/solana/id.json
```

#### `anchor test`

```bash
# Run tests
NO_DNA=1 anchor test

# Run tests with specific flag
NO_DNA=1 anchor test -- --features test-feature

# Run tests on localnet (default)
NO_DNA=1 anchor test --provider.cluster localnet

# Run tests on devnet
NO_DNA=1 anchor test --provider.cluster devnet

# Skip local validator (if already running)
NO_DNA=1 anchor test --skip-local-validator
```

**Test script:** Defined in `Anchor.toml`:
```toml
[scripts]
test = "yarn run ts-mocha -p ./tsconfig.json -t 1000000 tests/**/*.ts"
```

#### `anchor migrate`

```bash
# Run migrations
NO_DNA=1 anchor migrate
```

---

### IDL Management

#### `anchor idl init`

```bash
# Initialize IDL for a program
NO_DNA=1 anchor idl init --filepath ./target/idl/my_program.json <PROGRAM_ID>
```

#### `anchor idl fetch`

```bash
# Fetch IDL from chain
NO_DNA=1 anchor idl fetch <PROGRAM_ID>
```

#### `anchor idl write`

```bash
# Write IDL to a file
NO_DNA=1 anchor idl write <PROGRAM_ID> --out ./my_program_idl.json
```

---

### AVM (Anchor Version Manager)

#### `avm install`

```bash
# Install Anchor version
avm install 1.1.2
avm install 1.1.2 --from-source
```

#### `avm use`

```bash
# Switch Anchor version
avm use 1.1.2
```

#### `avm list`

```bash
# List installed versions
avm list
```

---

## Cargo Commands

### `cargo build-sbf`

```bash
# Build program for Solana (SBF target)
cargo build-sbf

# Build with specific manifest path
cargo build-sbf --manifest-path ./programs/my_program/Cargo.toml

# Force tools installation
cargo build-sbf --force-tools-install
```

### `cargo build-bpf` (DEPRECATED)

```bash
# Deprecated — use cargo build-sbf instead
cargo build-bpf  # Will show deprecation warning
```

---

## Common Workflows

### Deploy a New Program

```bash
# 1. Build the program
NO_DNA=1 anchor build

# 2. Get program ID from keypair
NO_DNA=1 solana address -k ./target/deploy/my_program-keypair.json

# 3. Update Anchor.toml with program ID
# Edit Anchor.toml: [programs.devnet] my_program = "<PROGRAM_ID>"

# 4. Deploy
NO_DNA=1 anchor deploy

# 5. Verify on Explorer
# https://explorer.solana.com/address/<PROGRAM_ID>?cluster=devnet
```

### Run Tests

```bash
# 1. Start local validator (if testing locally)
NO_DNA=1 solana-test-validator

# 2. In another terminal, run tests
NO_DNA=1 anchor test

# Or test on devnet
NO_DNA=1 anchor test --provider.cluster devnet
```

### Update Program

```bash
# 1. Build new version
NO_DNA=1 anchor build

# 2. Deploy (upgrades existing program)
NO_DNA=1 anchor deploy

# 3. Verify transaction on Explorer
# https://explorer.solana.com/tx/<SIGNATURE>?cluster=devnet
```

---

## Quick Command Reference

| Task | Command |
|------|---------|
| Check config | `NO_DNA=1 solana config get` |
| Set devnet | `NO_DNA=1 solana config set --url devnet` |
| Check balance | `NO_DNA=1 solana balance` |
| Get address | `NO_DNA=1 solana address` |
| Airdrop SOL | `NO_DNA=1 solana airdrop 2` |
| Generate keypair | `NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json` |
| Init Anchor project | `NO_DNA=1 anchor init my-project` |
| Build program | `NO_DNA=1 anchor build` |
| Deploy program | `NO_DNA=1 anchor deploy` |
| Run tests | `NO_DNA=1 anchor test` |
| Start local validator | `NO_DNA=1 solana-test-validator` |
| Check program info | `NO_DNA=1 solana program show <PROGRAM_ID>` |
| Calculate rent | `NO_DNA=1 solana rent 200` |
| Transfer SOL | `NO_DNA=1 solana transfer <ADDR> 0.5` |
| Verify keypair | `NO_DNA=1 solana-keygen verify <PUBKEY> ~/.config/solana/id.json` |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `NO_DNA=1` | Disable "Do Not Assume" mode — always prefix CLI commands |
| `ANCHOR_LOG=1` | Enable Anchor logging for debugging builds |
| `ANCHOR_WALLET` | Path to wallet keypair (overrides config) |
| `RUSTUP_TOOLCHAIN=stable` | Force stable Rust toolchain |
| `SOLANA_RPC_URL` | Override RPC URL |

## See Also

- [Solana CLI Documentation](https://docs.solanalabs.com/cli)
- [Anchor Book](https://www.anchor-lang.com/)
- [Agave Releases](https://github.com/anza-xyz/agave/releases)
- Load `solana-errors-and-compat` skill for error debugging
- Load `solana-anchor-programs` skill for program development