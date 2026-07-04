---
name: solana-environment-setup
description: Set up and configure Solana development environment from scratch. Covers Rust toolchain, Solana CLI, Anchor CLI v1.1.2, Node.js, wallet creation, devnet config, NO_DNA=1 protocol, MCP server, Anchor.toml, version pinning, GLIBC fixes, and cross-platform setup. Use when installing tools, configuring devnet, setting up wallets, fixing environment conflicts, or initializing Anchor projects.
version: 1.0.0
---

# Solana Environment Setup

## When to Use

- "set up Solana development environment"
- "install Rust Solana Anchor CLI"
- "configure devnet"
- "create Solana wallet"
- "import wallet from base58"
- "NO_DNA=1 protocol"
- "MCP server setup"
- "Anchor.toml configuration"
- "version pinning Solana tools"
- "GLIBC error"
- "toolchain conflict"
- "cross-platform Solana setup"
- "initialize Anchor project"
- "verify Solana installation"

## Core Operating Behaviors

- **Verify every installation** — Don't trust install scripts; run `--version` after each tool
- **Pin all versions explicitly** — No unpinned crates, packages, or toolchain versions
- **Devnet default** — All work targets devnet unless explicitly stated otherwise
- **Explorer verification** — Always verify on https://explorer.solana.com/?cluster=devnet
- **Use MCP before training data** — Query `https://mcp.solana.com/mcp` for live docs before falling back to cached knowledge
- **NO_DNA=1 prefix** — All Solana CLI commands use `NO_DNA=1` to prevent assumption-based errors
- **Source build over binary** — When GLIBC issues arise, build Anchor from source rather than using prebuilt binaries

## NO_DNA=1 CLI Protocol

The `NO_DNA=1` environment variable disables Solana CLI's "Do Not Assume" mode, which can silently fill in default values for unspecified parameters. Setting it ensures CLI commands fail explicitly rather than making assumptions.

### Usage

```bash
# Prefix any Solana CLI command
NO_DNA=1 solana config set --url devnet
NO_DNA=1 solana balance
NO_DNA=1 anchor build
NO_DNA=1 anchor deploy
NO_DNA=1 solana airdrop 2
```

### Why It Matters

Without `NO_DNA=1`, the CLI may:
- Auto-select a default keypair when none is specified
- Assume mainnet when cluster is ambiguous
- Use default commitment levels that don't match your intent
- Apply implicit fee payer selection

**Rule:** Every Solana CLI command in this skill suite uses `NO_DNA=1`. Make it a habit.

### Shell Alias (Optional)

```bash
# Add to ~/.bashrc or ~/.zshrc
alias solana='NO_DNA=1 solana'
alias anchor='NO_DNA=1 anchor'
```

## Solana MCP Server

The Solana MCP (Model Context Protocol) server provides live access to Solana documentation, RPC methods, and program references.

### Setup

```bash
# Add MCP server (Claude Desktop / any MCP-compatible client)
claude mcp add --transport http solana-mcp-server https://mcp.solana.com/mcp
```

### Usage Protocol

1. **Before falling back to training data**, query the MCP server for current API specs, CLI references, and program documentation
2. MCP tools return live, version-aware documentation that may differ from cached knowledge
3. Use MCP for: RPC method signatures, program instruction layouts, CLI flag references, account layouts
4. The MCP server is maintained by Solana and reflects the latest Agave/Anchor releases

## Toolchain Overview

### Required Tools

| Tool | Purpose | Current Version | Install Method |
|------|---------|----------------|----------------|
| Rust | On-chain program language | 1.96.0+ | rustup |
| Solana CLI (Agave) | Wallet, deploy, config, airdrop | v4.1.0 | install script |
| Anchor CLI | Project scaffolding, build, test, deploy | v1.1.2 | cargo (from source) or AVM |
| Node.js | Client-side runtime, test runner | v22+ | nvm or system package |
| TypeScript | Client-side type safety | v5.7+ | npm |
| Yarn | Package manager (Anchor default) | 1.22+ | npm |

### Installation Order

1. Rust (foundation — everything depends on it)
2. Solana CLI (needed for wallet, config, deployment)
3. Anchor CLI (depends on Rust + Solana CLI)
4. Node.js + Yarn (for TypeScript client and tests)
5. TypeScript (via npm, project-level)

**Full installation guide with version pins:** See `references/toolchain-checklist.md`

## Wallet Setup

### Quick Start

```bash
# Generate a new keypair
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json

# Set as default wallet
NO_DNA=1 solana config set --keypair ~/.config/solana/id.json

# Check address
NO_DNA=1 solana address

# Fund on devnet
NO_DNA=1 solana airdrop 2
```

### Import from Base58

If you have a base58-encoded private key (e.g., from Phantom), convert it to Solana CLI's JSON format:

```python
import base58, json, os

pk_b58 = 'YOUR_BASE58_PRIVATE_KEY'
keypair_bytes = base58.b58decode(pk_b58)
keypair_list = list(keypair_bytes)
keypair_path = os.path.expanduser('~/.config/solana/id.json')
os.makedirs(os.path.dirname(keypair_path), exist_ok=True)
with open(keypair_path, 'w') as f:
    json.dump(keypair_list, f)
os.chmod(keypair_path, 0o600)
```

**Full wallet setup guide:** See `references/wallet-setup.md`

## Devnet Configuration

```bash
# Set cluster to devnet
NO_DNA=1 solana config set --url devnet

# Verify configuration
NO_DNA=1 solana config get

# Check balance
NO_DNA=1 solana balance

# Airdrop SOL (rate-limited on devnet)
NO_DNA=1 solana airdrop 2

# If airdrop rate-limited, use web faucet: https://faucet.solana.com
```

### Devnet Rate Limits

- Airdrops are rate-limited (typically 2 SOL per request, cooldown between requests)
- If CLI airdrop fails, use the [web faucet](https://faucet.solana.com)
- Program deployment costs ~1.26 SOL rent exemption for a typical 180KB BPF binary
- Monitor balance: `NO_DNA=1 solana balance`

## Anchor.toml Configuration

### Standard Devnet Configuration

```toml
[toolchain]
package_manager = "yarn"

[features]
resolution = true
skip-lint = false

[programs.devnet]
my_program = "PROGRAM_ID_HERE"

[provider]
cluster = "Devnet"
wallet = "~/.config/solana/id.json"

[scripts]
test = "yarn run ts-mocha -p ./tsconfig.json -t 1000000 tests/**/*.ts"
```

### Best Practices

1. **Always specify `cluster = "Devnet"`** — Don't leave cluster ambiguous
2. **Use `[programs.devnet]` section** — Explicit devnet program mapping
3. **Pin wallet path** — `~/.config/solana/id.json` is standard
4. **Use `yarn` as package_manager** — Anchor's default, most compatible
5. **Set `resolution = true`** — Enables dependency resolution
6. **Don't skip lint** — `skip-lint = false` catches issues early
7. **Add `[registry]` if using custom registry** — `url = "https://api.apr.dev"`

### Localnet vs Devnet

For local testing, switch cluster:

```toml
[provider]
cluster = "Localnet"  # or "Devnet" for devnet deployment
```

```bash
# Start local validator
NO_DNA=1 solana-test-validator

# Switch CLI to localnet
NO_DNA=1 solana config set --url localhost
```

## Version Pinning Strategies

### Rust

```bash
# Pin via rustup
rustup install 1.96.0
rustup default 1.96.0

# Per-project override (rust-toolchain.toml)
[toolchain]
channel = "1.96.0"
components = ["rustfmt", "clippy"]
```

### Anchor (via AVM)

```bash
# Install AVM
cargo install anchor-cli --version 0.31.0  # or build from source

# Use AVM for version management
avm install 1.1.2
avm use 1.1.2

# Verify
anchor --version
```

### Cargo.toml Pinning

```toml
[workspace]
members = ["programs/*"]
resolver = "2"

[workspace.dependencies]
anchor-lang = "=1.1.2"
anchor-spl = "=1.1.2"
solana-program = "=4.1.0"
```

### package.json Pinning

```json
{
  "dependencies": {
    "@coral-xyz/anchor": "^1.1.2",
    "@solana/web3.js": "^2.0.0"
  },
  "devDependencies": {
    "typescript": "^5.7.3",
    "@types/bn.js": "^5.1.0"
  }
}
```

**Rule:** Never use `*` or leave versions unpinned. Use `=` for exact, `^` for compatible, `~` for patch-level.

## Common Environment Conflicts

### GLIBC Errors (Most Common)

**Symptom:**
```
anchor: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.39' not found
```

**Cause:** Anchor 0.31+ binaries require GLIBC ≥2.38. Anchor 0.32+ requires ≥2.39.

**Solutions (in priority order):**
1. **Upgrade OS** — Ubuntu 24.04+ has GLIBC 2.39
2. **Build from source:**
   ```bash
   cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli
   ```
3. **Use Docker:**
   ```bash
   docker run -v $(pwd):/workspace -w /workspace solanafoundation/anchor:1.1.2 anchor build
   ```
4. **Use AVM with source build:**
   ```bash
   avm install 1.1.2 --from-source
   ```

### Rust Version Conflicts

**Symptom:** `unknown feature proc_macro_span_shrink`

**Fix:** Pin Rust 1.79.0 for Anchor <0.31, or use Rust 1.96.0+ for Anchor 1.1.2+

### Anchor CLI/Crate Version Mismatch

**Symptom:** `module inner is private` or `error[E0603]`

**Fix:** Ensure `anchor-lang` crate version in Cargo.toml matches `anchor --version`

**Full conflict resolution guide:** See `references/cli-reference.md` and load `solana-errors-and-compat` skill for deep debugging.

## Cross-Platform Setup

### Linux (Ubuntu/Debian)

```bash
# Install build dependencies
sudo apt update
sudo apt install -y build-essential pkg-config libssl-dev libudev-dev git curl

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# Install Solana CLI
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

# Install Anchor CLI (from source for GLIBC compatibility)
cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli

# Install Node.js via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 22
nvm use 22

# Install Yarn
npm install -g yarn
```

### macOS

```bash
# Install Homebrew (if not present)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install pkg-config openssl rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# Solana CLI
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"

# Anchor CLI
cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli

# Node.js
brew install node@22
```

### Windows (WSL2)

```bash
# Inside WSL2 Ubuntu
sudo apt update
sudo apt install -y build-essential pkg-config libssl-dev libudev-dev git curl

# Follow Linux instructions above
# WSL2 provides full Linux compatibility — no special Windows setup needed
```

**Full cross-platform guide:** See `references/toolchain-checklist.md`

## Verification Commands

After setup, verify all tools:

```bash
NO_DNA=1 rustc --version          # Expected: 1.96.0+
NO_DNA=1 cargo --version          # Expected: cargo 1.96.0
NO_DNA=1 solana --version         # Expected: solana-cli 4.1.0
NO_DNA=1 anchor --version         # Expected: anchor-cli 1.1.2
NO_DNA=1 node --version           # Expected: v22+
NO_DNA=1 yarn --version           # Expected: 1.22+
NO_DNA=1 solana config get        # Expected: RPC URL = devnet
NO_DNA=1 solana address           # Expected: your wallet address
NO_DNA=1 solana balance           # Expected: > 0 SOL on devnet
```

## CLI Reference

**Full CLI command reference:** See `references/cli-reference.md`

Covers: `solana config`, `solana-keygen`, `solana airdrop`, `solana balance`, `solana address`, `anchor init`, `anchor build`, `anchor deploy`, `anchor test`, `cargo build-sbf`.

## Cross-Skill References

| Related Skill | When to Switch |
|--------------|----------------|
| `solana-foundations` | Need conceptual understanding of Account Model, PDAs, transactions before setup |
| `solana-errors-and-compat` | Environment conflicts beyond basic GLIBC — deep debugging, version matrices, migration guides |
| `solana-anchor-programs` | Environment is set up; ready to write/build/deploy Anchor programs |
| `solana-testing` | Environment ready; need to set up test suites with LiteSVM/Mollusk |
| `solana-client` | Environment ready; building TypeScript client with @solana/kit |
| `solana-deployment-devops` | Environment ready; need deployment automation, CI/CD, multi-environment configs |

## Verification Checklist

- [ ] Rust installed and verified (`rustc --version` returns 1.96.0+)
- [ ] Solana CLI installed and verified (`solana --version` returns 4.1.0+)
- [ ] Anchor CLI installed and verified (`anchor --version` returns 1.1.2+)
- [ ] Node.js installed and verified (`node --version` returns v22+)
- [ ] Yarn installed and verified (`yarn --version` returns 1.22+)
- [ ] TypeScript installed (`tsc --version` returns 5.7+)
- [ ] Solana CLI configured to devnet (`solana config get` shows devnet URL)
- [ ] Wallet keypair generated or imported at `~/.config/solana/id.json`
- [ ] Wallet address verified (`solana address` returns correct address)
- [ ] Devnet SOL funded (`solana balance` returns > 0 SOL)
- [ ] `NO_DNA=1` protocol understood and applied
- [ ] MCP server configured (`claude mcp add --transport http solana-mcp-server https://mcp.solana.com/mcp`)
- [ ] Anchor.toml created with devnet configuration
- [ ] All versions pinned in Cargo.toml and package.json
- [ ] GLIBC compatibility verified (no `GLIBC_2.39 not found` errors)
- [ ] `anchor init` creates a valid project structure
- [ ] `anchor build` completes without errors
