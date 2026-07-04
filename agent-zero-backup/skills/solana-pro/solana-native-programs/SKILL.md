---
name: solana-native-programs
description: Native Solana program development without Anchor — raw Rust/BPF entrypoints, Pinocchio high-performance framework, syscalls, compute budget, account serialization, CPI, and manual security validation. Use for native program, process_instruction, BPF, Pinocchio, syscalls, compute budget, priority fee, CPI without Anchor, borsh serialization, secp256k1 verification, sbpf.
version: 1.0.0
---

# Solana Native Programs (Non-Anchor)

## When to Use

- Writing Solana programs in raw Rust/BPF without the Anchor framework
- Using Pinocchio for high-performance, zero-copy programs
- Implementing `process_instruction` entrypoints manually
- Parsing instruction data and routing to handlers without macros
- Serializing/deserializing accounts with borsh or manual byte layouts
- Making CPI calls without Anchor's `invoke`/`invoke_signed` helpers
- Working with syscalls (logging, CPI, sysvars, crypto verification)
- Configuring compute budget instructions (CU limits, priority fees)
- Security validation without Anchor's auto-derived account checks
- Using `secp256k1-verify` crate for decoupled signature verification
- Debugging with sbpf CFG analyses tooling

Trigger phrases: `native program`, `process_instruction`, `BPF program`, `Pinocchio`, `solana syscall`, `compute budget`, `priority fee`, `CPI without Anchor`, `borsh serialization`, `entrypoint`, `instruction parsing`, `secp256k1-verify`, `sbpf CFG`, `raw Rust Solana`

---

## Core Operating Behaviors

- **Devnet default**: All work targets devnet unless explicitly stated. Use `NO_DNA=1 solana config set --url devnet`.
- **NO_DNA=1 protocol**: Prefix all Solana CLI commands with `NO_DNA=1` to prevent DNA (Do Not Assume) errors.
- **MCP first**: Query the Solana MCP server (`https://mcp.solana.com/mcp`) for live documentation before falling back to training data.
- **Explorer verification**: Always verify deployments and transactions on https://explorer.solana.com — never trust terminal output alone.
- **Manual security**: Without Anchor's auto-validation, every account check is your responsibility. Owner, signer, writable, PDA derivation, sysvar identity — all manual.
- **Test before deploy**: Test programs locally (LiteSVM, Mollusk, or `solana-test-validator`) before deploying to devnet.
- **Pin dependency versions**: Explicitly pin all crate versions. No unpinned dependencies.

---

## Architecture Decision: Anchor vs Native vs Pinocchio

| Criteria | Anchor | Native (solana-program) | Pinocchio |
----------|--------|------------------------|----------|
| Development speed | Fastest (macros) | Slow (manual) | Moderate |
| Compute efficiency | Baseline | Better | Best |
| Binary size | Largest | Medium | Smallest |
| Account validation | Auto-derived | Manual | Manual |
| Learning curve | Low (if you know Anchor) | High | High |
| Use case | Most programs | Legacy/migration | High-throughput |

**Choose Native/Pinocchio when:**
- Compute budget is tight (sub-1000 CU operations)
- Binary size matters (deployment cost, load time)
- You need fine-grained memory control (zero-copy)
- Migrating from or integrating with existing native programs
- Building high-throughput infrastructure (oracles, order books)

---

## Program Entrypoint

### Raw solana-program Entry

```rust
use solana_program::{
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    pubkey::Pubkey,
    msg,
};

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    msg!("Hello from native program");
    Ok(())
}
```

### Pinocchio Entry

```rust
use pinocchio::{entrypoint, msg, ProgramResult};

entrypoint!(process_instruction);

pub fn process_instruction(
    instruction: &pinocchio::Instruction,
) -> ProgramResult {
    msg!("Hello from Pinocchio");
    Ok(())
}
```

Pinocchio provides `Instruction` with zero-copy `AccountInfo` views. No `&[u8]` slicing — direct memory access.

---

## Instruction Parsing and Routing

### Pattern: Single-Byte Discriminator

Native programs typically use a 1-byte discriminator (0-255 instructions), unlike Anchor's 8-byte discriminator.

```rust
pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let discriminator = instruction_data
        .first()
        .ok_or(ProgramError::InvalidInstructionData)?;

    match discriminator {
        0 => initialize(accounts, &instruction_data[1..]),
        1 => increment(accounts, &instruction_data[1..]),
        2 => reset(accounts, &instruction_data[1..]),
        _ => Err(ProgramError::InvalidInstructionData),
    }
}
```

### Pinocchio Instruction Parsing

Pinocchio uses `TryFrom<&[u8]>` for instruction data:

```rust
#[repr(u8)]
enum Instruction {
    Initialize { bump: u8 },
    Increment,
    Reset,
}

impl TryFrom<&[u8]> for Instruction {
    type Error = ProgramError;

    fn try_from(data: &[u8]) -> Result<Self, Self::Error> {
        let disc = data.first().ok_or(ProgramError::InvalidInstructionData)?;
        match disc {
            0 => Ok(Self::Initialize { bump: data[1] }),
            1 => Ok(Self::Increment),
            2 => Ok(Self::Reset),
            _ => Err(ProgramError::InvalidInstructionData),
        }
    }
}
```

---

## Account Serialization

### Borsh (Standard)

```rust
use borsh::{BorshDeserialize, BorshSerialize};

#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct CounterAccount {
    pub authority: Pubkey,
    pub count: u64,
}

impl CounterAccount {
    pub fn try_from_bytes(data: &[u8]) -> Result<Self, ProgramError> {
        Self::try_from_slice(data)
            .map_err(|_| ProgramError::InvalidAccountData)
    }

    pub fn save(&self, account: &AccountInfo) -> ProgramResult {
        let mut data = account.try_borrow_mut_data()?;
        borsh::to_writer(&mut data[..], self)
            .map_err(|_| ProgramError::InvalidInstructionData)?;
        Ok(())
    }
}
```

### Manual Byte Layout (Pinocchio / Zero-Copy)

For maximum performance, define structs with explicit memory layout:

```rust
#[repr(C, packed)]
pub struct CounterData {
    pub authority: [u8; 32],
    pub count: u64,
}

impl CounterData {
    pub fn from_bytes(data: &[u8]) -> Result<&Self, ProgramError> {
        if data.len() < 40 {
            return Err(ProgramError::InvalidAccountData);
        }
        Ok(unsafe { &*(data.as_ptr() as *const Self) })
    }
}
```

> **Full Pinocchio guide:** Use `skills_tool` action `read_file` with `skill_name: solana-native-programs` and `file_path: references/pinocchio-guide.md` for complete struct layouts, `assert_no_padding!`, trait implementations, and zero-copy patterns.

---

## Cross-Program Invocation (CPI)

### Native CPI (solana-program)

```rust
use solana_program::{
    program::invoke,
    system_instruction,
};

pub fn transfer_sol(
    from: &AccountInfo,
    to: &AccountInfo,
    lamports: u64,
) -> ProgramResult {
    let ix = system_instruction::transfer(from.key, to.key, lamports);
    invoke(&ix, &[from.clone(), to.clone()])
}
```

### Native CPI with PDA Signer

```rust
use solana_program::{program::invoke_signed, system_instruction};

pub fn transfer_from_pda(
    program_id: &Pubkey,
    pda: &AccountInfo,
    destination: &AccountInfo,
    lamports: u64,
    seeds: &[&[u8]],
) -> ProgramResult {
    let ix = system_instruction::transfer(pda.key, destination.key, lamports);
    let signers = &[seeds];
    invoke_signed(&ix, &[pda.clone(), destination.clone()], signers)
}
```

### Pinocchio CPI

```rust
use pinocchio_system::instructions::Transfer;

pub fn transfer_lamports(
    from: &AccountInfo,
    to: &AccountInfo,
    lamports: u64,
) -> ProgramResult {
    Transfer { from, to, lamports }.invoke()
}

// With PDA signer
use pinocchio::{seeds, Signer};

pub fn transfer_from_pda(
    from: &AccountInfo,
    to: &AccountInfo,
    lamports: u64,
    seeds: &[&[u8]],
) -> ProgramResult {
    let signer = Signer::from(seeds);
    Transfer { from, to, lamports }.invoke_signed(&[signer])
}
```

---

## Security Without Auto-Validation

Anchor auto-derives account checks from `#[account]` and `#[derive(Accounts)]`. Native programs must implement every check manually.

### Mandatory Account Checks

```rust
pub fn validate_authority(
    account: &AccountInfo,
    expected_authority: &Pubkey,
) -> ProgramResult {
    // 1. Owner check — account must be owned by this program
    if account.owner != &crate::ID {
        return Err(ProgramError::IllegalOwner);
    }
    // 2. Signer check — authority must have signed
    if !account.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }
    // 3. Writable check — if modifying account data
    if !account.is_writable {
        return Err(ProgramError::InvalidArgument);
    }
    // 4. Data match — verify stored authority matches
    let data = CounterAccount::try_from_bytes(&account.data.borrow())?;
    if &data.authority != expected_authority {
        return Err(ProgramError::IllegalOwner);
    }
    Ok(())
}
```

### PDA Derivation Verification

```rust
pub fn verify_pda(
    program_id: &Pubkey,
    account: &AccountInfo,
    seeds: &[&[u8]],
) -> ProgramResult {
    let (expected_pda, bump) = Pubkey::find_program_address(seeds, program_id);
    if account.key != &expected_pda {
        return Err(ProgramError::InvalidSeeds);
    }
    Ok(())
}
```

### Security Checklist (Manual)

| Check | Anchor Auto | Native Required |
|-------|-------------|----------------|
| Owner verification | Yes | **Manual** |
| Signer verification | Yes | **Manual** |
| Writable check | Yes | **Manual** |
| PDA derivation | Yes | **Manual** |
| Account discriminator | Yes | **Manual** |
| Rent exemption | Yes | **Manual** |
| Data length | Yes | **Manual** |
| Sysvar identity | N/A | **Manual** |
| Checked arithmetic | Via `#[access]` | **Manual (`checked_*`)** |

> **Full security guide:** Load skill `solana-security` for comprehensive vulnerability review and audit-style checks.

---

## Compute Budget

The Compute Budget program (`ComputeBudget111111111111111111111111111111`) controls transaction prioritization and compute unit allocation.

Key instructions:
- **SetComputeUnitLimit** — cap CU consumption (default: 200,000 per instruction)
- **SetComputeUnitPrice** — priority fee in micro-lamports per CU
- **RequestHeapFrame** — increase heap beyond default 32KB

Total fee = base fee (5,000 lamports/sig) + (CU consumed × price per CU in micro-lamports).

```rust
use solana_program::compute_budget::ComputeBudgetInstruction;

// In client code:
let ix_limit = ComputeBudgetInstruction::set_compute_unit_limit(50_000);
let ix_price = ComputeBudgetInstruction::set_compute_unit_price(5_000); // 5,000 micro-lamports/CU
```

> **Full compute budget guide:** Use `skills_tool` action `read_file` with `skill_name: solana-native-programs` and `file_path: references/compute-budget.md` for CU estimation, fee market dynamics, and optimization strategies.

---

## Syscalls

Solana BPF programs access runtime functionality via syscalls. Key categories:

| Category | Syscalls | Purpose |
|----------|----------|--------|
| Logging | `sol_log`, `sol_log_64_` | Debug output, event logging |
| CPI | `sol_invoke_signed` | Cross-program invocation |
| Sysvars | `sol_get_clock`, `sol_get_rent` | Read chain state |
| Crypto | `secp256k1_recover`, `secp256k1_verify` | ECDSA verification |
| Memory | `sol_memcpy`, `sol_memset`, `sol_memmove` | Memory operations |
| Process | `sol_get_return_data`, `sol_set_return_data` | Return data from CPI |

> **Full syscalls reference:** Use `skills_tool` action `read_file` with `skill_name: solana-native-programs` and `file_path: references/syscalls-reference.md` for complete syscall signatures, usage patterns, and Agave v4.1.0 updates.

---

## Modern Ecosystem Updates

| Update | Version | Impact |
|--------|---------|--------|
| Agave runtime | v4.1.0 | Updated syscall signatures and behavior |
| secp256k1-verify crate | NEW | Decoupled signature verification from program logic — verify off-chain signatures without embedding verification code |
| sbpf CFG analyses | NEW | Control-flow graph debugging tooling for BPF programs — visualize branches, detect dead code, optimize jumps |
| Pinocchio | Latest | Zero-copy, minimal-dep framework — significant CU and binary size savings |

---

## Build and Deploy

### Build

```bash
# Standard BPF build
NO_DNA=1 cargo build-sbf

# Check binary size (typical native: 5-30KB, Pinocchio: 5-15KB)
ls -la target/deploy/<program_name>.so

# Verify ELF format
file target/deploy/<program_name>.so
```

### Deploy

```bash
# Configure devnet
NO_DNA=1 solana config set --url devnet

# Deploy
NO_DNA=1 solana program deploy target/deploy/<program_name>.so

# Verify on Explorer
# https://explorer.solana.com/address/<PROGRAM_ID>?cluster=devnet
```

### Testing

```bash
# Local test validator
NO_DNA=1 solana-test-validator

# Rust-based testing (preferred for native)
cargo test
```

For fast Rust-based testing without a validator, use LiteSVM or Mollusk. Load skill `solana-testing` for detailed setup.

---

## Project Structure (Native)

```
my-native-program/
├── Cargo.toml
├── src/
│   ├── lib.rs          # entrypoint + instruction routing
│   ├── instruction.rs   # instruction parsing/discriminators
│   ├── state.rs         # account structs (borsh or manual)
│   ├── processor.rs     # business logic
│   └── error.rs         # custom error codes
├── tests/
│   └── integration.rs
└── client/              # TypeScript client (optional)
    └── src/
```

### Cargo.toml (Native)

```toml
[package]
name = "my-native-program"
version = "0.1.0"
edition = "2021"

[dependencies]
solana-program = "2.1"
borsh = "1.5"

[lib]
crate-type = ["cdylib", "lib"]
```

### Cargo.toml (Pinocchio)

```toml
[package]
name = "my-pinocchio-program"
version = "0.1.0"
edition = "2021"

[dependencies]
pinocchio = "0.8"

[lib]
crate-type = ["cdylib", "lib"]
```

---

## Cross-Skill References

| Related Skill | When to Switch |
|--------------|----------------|
| `solana-anchor-programs` | When using Anchor framework (macros, `#[account]`, `#[derive(Accounts)]`) |
| `solana-advanced` | Token-2022, confidential transfers, payments, SPL Token operations |
| `solana-security` | Comprehensive security audit and vulnerability review |
| `solana-testing` | LiteSVM, Mollusk, Surfpool test framework setup |
| `solana-errors-and-compat` | Debugging build errors, version mismatches, GLIBC issues |
| `solana-client` | TypeScript client SDK for interacting with native programs |
| `solana-foundations` | Core Solana architecture (accounts, transactions, PDAs) |

---

## Progressive Disclosure

| Reference | Access |
|-----------|--------|
| Pinocchio Guide | `read_file` → `references/pinocchio-guide.md` |
| Syscalls Reference | `read_file` → `references/syscalls-reference.md` |
| Compute Budget | `read_file` → `references/compute-budget.md` |

---

## Resources

- [Pinocchio Repository](https://github.com/anza-xyz/pinocchio)
- [pinocchio-system](https://crates.io/crates/pinocchio-system)
- [pinocchio-token](https://crates.io/crates/pinocchio-token)
- [Pinocchio Guide (Community)](https://github.com/vict0rcarvalh0/pinocchio-guide)
- [How to Build with Pinocchio (Helius)](https://www.helius.dev/blog/pinocchio)
- [Solana Program Documentation](https://solana.com/docs/programs)
- [BPF Documentation](https://solana.com/docs/programs/faq)
- [secp256k1-verify crate](https://crates.io/crates/secp256k1-verify)
- [sbpf SDK](https://github.com/anza-xyz/sbpf)
- [Solana MCP Server](https://mcp.solana.com/mcp)
- [Solana Cookbook](https://solanacookbook.com/)
- [Blueshift Program Security](https://learn.blueshift.gg/en/courses/program-security)
- [Solana Optimized Programs](https://github.com/Laugharne/solana_optimized_programs)

---

## Verification Checklist

- [ ] `NO_DNA=1` prefix used on all CLI commands
- [ ] Solana MCP server queried for live docs before relying on training data
- [ ] Program built with `NO_DNA=1 cargo build-sbf` — no errors
- [ ] Binary size checked (native: <30KB, Pinocchio: <15KB preferred)
- [ ] ELF format verified with `file` command
- [ ] All account checks implemented manually (owner, signer, writable, PDA, data length)
- [ ] Checked arithmetic used (`checked_add`, `checked_sub`, etc.) — no overflow panics
- [ ] Instruction routing handles unknown discriminators with `Err(InvalidInstructionData)`
- [ ] Rent exemption verified for all created accounts
- [ ] Local tests pass (`cargo test` or test-validator)
- [ ] Deployed to devnet: `NO_DNA=1 solana program deploy`
- [ ] Program verified on Solana Explorer (https://explorer.solana.com/?cluster=devnet)
- [ ] Transaction signatures verified on-chain after deployment
- [ ] Dependency versions pinned explicitly in Cargo.toml
- [ ] No `unwrap()` or `expect()` in program code — all errors handled
- [ ] Security review completed (load `solana-security` skill for audit)
