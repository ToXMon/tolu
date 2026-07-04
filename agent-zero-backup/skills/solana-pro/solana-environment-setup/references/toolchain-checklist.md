# Toolchain Checklist — Full Installation Guide

Complete Solana development environment setup with version pins. Follow in order.

## Version Matrix (Tested Compatible)

| Tool | Version | Notes |
|------|---------|-------|
| Rust | 1.96.0+ | Via rustup; required by Anchor and Solana programs |
| Solana CLI (Agave) | v4.1.0 | Install script from anza.xyz |
| Anchor CLI | v1.1.2 | Build from source or AVM |
| Anchor Lang (crate) | =1.1.2 | In Cargo.toml |
| Solana Program (crate) | =4.1.0 | In Cargo.toml |
| Node.js | v22+ | Via nvm for version management |
| TypeScript | 5.7+ | Project-level dev dependency |
| Yarn | 1.22+ | Anchor's default package manager |
| @coral-xyz/anchor | ^1.1.2 | npm package for TypeScript client |
| @solana/web3.js | ^2.0.0 | Or @solana/kit v7.0.0 for modern client |

## Step 1: System Dependencies

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  pkg-config \
  libssl-dev \
  libudev-dev \
  git \
  curl \
  ca-certificates
```

### macOS

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install pkg-config openssl
```

### Windows (WSL2)

```bash
# Install WSL2 if not present (in PowerShell as admin)
# wsl --install -d Ubuntu-24.04

# Inside WSL2, follow Linux instructions above
sudo apt update
sudo apt install -y build-essential pkg-config libssl-dev libudev-dev git curl
```

## Step 2: Install Rust

```bash
# Install via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Load cargo environment
source "$HOME/.cargo/env"

# Verify
rustc --version    # Expected: rustc 1.96.0 (or newer)
cargo --version     # Expected: cargo 1.96.0
```

### Pin Rust Version (Optional but Recommended)

```bash
# Install specific version
rustup install 1.96.0
rustup default 1.96.0

# Or use rust-toolchain.toml for per-project pinning
# Create rust-toolchain.toml in project root:
```

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.96.0"
components = ["rustfmt", "clippy"]
```

## Step 3: Install Solana CLI (Agave)

```bash
# Install latest stable
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

# Verify
solana --version    # Expected: solana-cli 4.1.0 (or newer)
```

### Install Specific Version

```bash
# Install specific version
sh -c "$(curl -sSfL https://release.anza.xyz/v4.1.0/install)"
```

### Verify Solana CLI Components

```bash
# Check all tools are available
solana --version
solana-test-validator --version
cargo-build-sbf --version
solana-keygen --version
```

## Step 4: Install Anchor CLI

### Option A: Build from Source (Recommended for GLIBC Compatibility)

```bash
# Install Anchor CLI v1.1.2 from source
cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli

# This takes 5-15 minutes depending on machine
# The --locked flag may cause issues with yanked packages; omit if needed

# Verify
anchor --version    # Expected: anchor-cli 1.1.2
```

### Option B: Install via AVM (Anchor Version Manager)

```bash
# Install AVM
cargo install anchor-cli --version 0.31.0  # Bootstrap install

# Use AVM for version management
avm install 1.1.2
avm use 1.1.2

# Verify
anchor --version    # Expected: anchor-cli 1.1.2
```

### Option C: Build from Source with AVM

```bash
# If GLIBC issues prevent binary install
avm install 1.1.2 --from-source
avm use 1.1.2
```

### Important Notes

- The npm package `@coral-xyz/anchor-cli` is **only a JS wrapper**, not the actual binary
- The Anchor CLI crate is **NOT published on crates.io** — `cargo install anchor-cli --version X.Y.Z` fails
- Always install from the GitHub repository with `--git` flag
- Building from source takes 5-15 minutes depending on machine

## Step 5: Install Node.js

### Via NVM (Recommended)

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# Reload shell
source ~/.bashrc  # or ~/.zshrc

# Install Node.js v22
nvm install 22
nvm use 22
nvm alias default 22

# Verify
node --version    # Expected: v22.x.x
npm --version     # Expected: 10.x+
```

### macOS via Homebrew

```bash
brew install node@22
brew link --force --overwrite node@22
```

## Step 6: Install Yarn

```bash
# Install Yarn globally
npm install -g yarn

# Verify
yarn --version     # Expected: 1.22.x
```

## Step 7: Install TypeScript

```bash
# Install TypeScript globally (also install per-project)
npm install -g typescript

# Verify
tsc --version      # Expected: 5.7+
```

TypeScript should also be installed as a dev dependency in each project:

```bash
# In project directory
yarn add -D typescript@^5.7.3
```

## Step 8: Configure Solana CLI for Devnet

```bash
# Set cluster to devnet
NO_DNA=1 solana config set --url devnet

# Verify configuration
NO_DNA=1 solana config get

# Expected output:
# Config File: /home/user/.config/solana/cli/config.yml
# RPC URL: https://api.devnet.solana.com
# WebSocket URL: wss://api.devnet.solana.com/ (computed)
# Keypair Path: /home/user/.config/solana/id.json
# Commitment: confirmed
```

## Step 9: Set Up Wallet

See `wallet-setup.md` for full guide.

```bash
# Generate new keypair
NO_DNA=1 solana-keygen new -o ~/.config/solana/id.json

# Set as default
NO_DNA=1 solana config set --keypair ~/.config/solana/id.json

# Get devnet SOL
NO_DNA=1 solana airdrop 2
```

## Step 10: Verify Complete Installation

```bash
# Run all verification commands
echo "=== Toolchain Verification ==="
NO_DNA=1 rustc --version
NO_DNA=1 cargo --version
NO_DNA=1 solana --version
NO_DNA=1 anchor --version
NO_DNA=1 node --version
NO_DNA=1 yarn --version
NO_DNA=1 tsc --version
NO_DNA=1 solana config get
NO_DNA=1 solana address
NO_DNA=1 solana balance
```

### Expected Output Summary

| Command | Expected Output |
|---------|----------------|
| `rustc --version` | `rustc 1.96.0` (or newer) |
| `cargo --version` | `cargo 1.96.0` |
| `solana --version` | `solana-cli 4.1.0` (or newer) |
| `anchor --version` | `anchor-cli 1.1.2` |
| `node --version` | `v22.x.x` |
| `yarn --version` | `1.22.x` |
| `tsc --version` | `Version 5.7.x` |
| `solana config get` | RPC URL: `https://api.devnet.solana.com` |
| `solana address` | Your wallet address |
| `solana balance` | `> 0 SOL` |

## GLIBC Troubleshooting

### Check GLIBC Version

```bash
ldd --version    # Shows GLIBC version
```

### GLIBC Requirements

| Anchor Version | GLIBC Required |
|---------------|----------------|
| 0.30.x | 2.35+ (Ubuntu 22.04) |
| 0.31.x | 2.38+ (Ubuntu 23.10+) |
| 0.32.x+ | 2.39+ (Ubuntu 24.04+) |
| 1.1.2 | 2.39+ (Ubuntu 24.04+) |

### If GLIBC Too Old

1. **Best: Upgrade OS** — Ubuntu 24.04+ has GLIBC 2.39
2. **Build from source:**
   ```bash
   cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli
   ```
3. **Use Docker:**
   ```bash
   docker run -v $(pwd):/workspace -w /workspace solanafoundation/anchor:1.1.2 anchor build
   ```

## Docker Alternative

If local setup is problematic, use Docker:

```bash
# Pull Anchor image
docker pull solanafoundation/anchor:1.1.2

# Run Anchor commands
docker run -v $(pwd):/workspace -w /workspace solanafoundation/anchor:1.1.2 anchor build
docker run -v $(pwd):/workspace -w /workspace solanafoundation/anchor:1.1.2 anchor test
```

For a full development container:

```dockerfile
# Dockerfile.dev
FROM ubuntu:24.04

RUN apt update && apt install -y \
    build-essential pkg-config libssl-dev libudev-dev \
    git curl ca-certificates

# Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Solana CLI
RUN sh -c "$(curl -sSfL https://release.anza.xyz/v4.1.0/install)"
ENV PATH="/root/.local/share/solana/install/active_release/bin:${PATH}"

# Anchor CLI
RUN cargo install --git https://github.com/solana-foundation/anchor --tag v1.1.2 anchor-cli

# Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt install -y nodejs
RUN npm install -g yarn

WORKDIR /workspace
```

## Common Issues

### `cargo build-sbf` not found

Solana CLI not in PATH. Fix:
```bash
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"
```

### Anchor install fails with `time` crate error

Anchor <0.31 incompatible with Rust ≥1.80. Fix: Use Anchor 1.1.2+ with Rust 1.96.0+.

### Platform tools download failure

```bash
rm -rf ~/.cache/solana/
cargo build-sbf
```

### `No space left on device`

Solana platform tools are ~3GB. Clean up:
```bash
# Remove old Solana versions
rm -rf ~/.local/share/solana/install/releases/1.*

# Remove cargo cache
cargo cache -a  # if cargo-cache installed
# Or manually:
rm -rf ~/.cargo/registry/cache/
```

## Next Steps

After toolchain is set up:
1. Initialize an Anchor project: `NO_DNA=1 anchor init my-project`
2. Configure Anchor.toml (see SKILL.md)
3. See `cli-reference.md` for command reference
4. Load `solana-anchor-programs` skill for program development