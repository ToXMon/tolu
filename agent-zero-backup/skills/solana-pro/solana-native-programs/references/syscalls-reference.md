# Solana Syscalls Reference

Solana BPF programs access runtime functionality via syscalls. This reference covers all syscall categories, signatures, usage patterns, and Agave v4.1.0 updates.

## Syscall Categories

| Category | Syscalls | Purpose |
|----------|----------|--------|
| Logging | `sol_log`, `sol_log_64_`, `sol_log_data`, `sol_log_compute_units` | Debug output, event logging |
| CPI | `sol_invoke_signed` | Cross-program invocation |
| Sysvars | `sol_get_clock`, `sol_get_rent`, `sol_get_epoch_schedule`, etc. | Read chain state |
| Crypto | `secp256k1_recover`, `secp256k1_verify`, `ed25519_verify` | Signature verification |
| Memory | `sol_memcpy`, `sol_memset`, `sol_memmove`, `sol_memcmp` | Memory operations |
| Process | `sol_get_return_data`, `sol_set_return_data` | Return data from CPI |
| Heap | `sol_alloc_free` | Heap allocation |
| Alt_bn128 | `alt_bn128_group_op_g1_add`, `g1_mul`, `g1_multiexp`, `g2_add`, `pairing` | ZK proof verification |
| Big_mod_exp | `big_op` | Modular exponentiation |
| Poseidon | `poseidon_hash` | Poseidon hash for ZK |

---

## Logging Syscalls

### sol_log

Log a UTF-8 string.

```rust
// In solana-program:
msg!("Hello, world!");

// Direct syscall (rarely used directly):
unsafe {
    solana_program::syscalls::sol_log("Hello".as_ptr(), 5);
}
```

### sol_log_64_

Log up to 5 u64 values — useful for debugging numeric values.

```rust
use solana_program::log::sol_log_64;

sol_log_64(arg1, arg2, arg3, arg4, arg5);
```

### sol_log_data

Log arbitrary byte data — used for event emission. Indexers parse these logs.

```rust
use solana_program::log::sol_log_data;

sol_log_data(&[&[0x01, 0x02, 0x03]]);
```

### sol_log_compute_units

Log current compute units consumed — useful for optimization.

```rust
use solana_program::log::sol_log_compute_units;

sol_log_compute_units(); // Prints: CU consumed: <number>
```

---

## CPI Syscall: sol_invoke_signed

Cross-program invocation is the fundamental composability mechanism on Solana.

### Signature (Conceptual)

```rust
// Underlying syscall (not called directly — use program::invoke_signed)
unsafe fn sol_invoke_signed(
    instruction: &Instruction,
    account_infos: &[AccountInfo],
    signers_seeds: &[&[&[u8]]],
) -> ProgramResult;
```

### High-Level API (solana-program)

```rust
use solana_program::{program::invoke_signed, instruction::Instruction, account_info::AccountInfo};

pub fn invoke(
    instruction: &Instruction,
    account_infos: &[AccountInfo],
) -> ProgramResult {
    invoke_signed(instruction, account_infos, &[])
}

pub fn invoke_signed(
    instruction: &Instruction,
    account_infos: &[AccountInfo],
    signers_seeds: &[&[&[u8]]],
) -> ProgramResult {
    // Wraps sol_invoke_signed syscall
    invoke_signed(instruction, account_infos, signers_seeds)
}
```

### CPI Pattern: Transfer SOL

```rust
use solana_program::{
    instruction::Instruction,
    program::invoke,
    system_instruction,
    account_info::AccountInfo,
    entrypoint::ProgramResult,
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

### CPI Pattern: Transfer SOL from PDA

```rust
use solana_program::{
    program::invoke_signed,
    system_instruction,
    pubkey::Pubkey,
    account_info::AccountInfo,
    entrypoint::ProgramResult,
};

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

### CPI Pattern: Create Account (PDA)

```rust
use solana_program::{
    program::invoke_signed,
    system_instruction,
    pubkey::Pubkey,
    account_info::AccountInfo,
    entrypoint::ProgramResult,
};

pub fn create_pda_account(
    payer: &AccountInfo,
    pda: &AccountInfo,
    program_id: &Pubkey,
    space: usize,
    seeds: &[&[u8]],
    rent_lamports: u64,
) -> ProgramResult {
    let ix = system_instruction::create_account(
        payer.key,
        pda.key,
        rent_lamports,
        space as u64,
        program_id,
    );
    invoke_signed(&ix, &[payer.clone(), pda.clone()], &[seeds])
}
```

### CPI Pattern: Token Transfer

```rust
use solana_program::{
    instruction::AccountMeta,
    instruction::Instruction,
    program::invoke,
    pubkey::Pubkey,
    account_info::AccountInfo,
    entrypoint::ProgramResult,
};

pub fn token_transfer(
    token_program: &AccountInfo,
    source: &AccountInfo,
    destination: &AccountInfo,
    authority: &AccountInfo,
    amount: u64,
) -> ProgramResult {
    let ix = Instruction {
        program_id: *token_program.key,
        accounts: vec![
            AccountMeta::new(*source.key, false),
            AccountMeta::new(*destination.key, false),
            AccountMeta::new_readonly(*authority.key, true),
        ],
        data: [3, 0, 0, 0, 0, 0, 0, 0, 0] // Transfer instruction discriminator + amount
            .to_vec(),
    };
    invoke(&ix, &[source.clone(), destination.clone(), authority.clone()])
}
```

### CPI with Return Data

```rust
use solana_program::{program::invoke, instruction::Instruction};

// After a CPI call, read return data
let mut return_data = [0u8; 256];
let (len, program_id) = solana_program::program::get_return_data()
    .ok_or(ProgramError::InvalidInstructionData)?;
return_data[..len].copy_from_slice(&/* return data */);
```

---

## Sysvar Syscalls

Sysvars are special accounts that expose chain state. Programs read them via syscalls.

### Common Sysvars

| Sysvar | Address | Purpose |
|--------|---------|--------|
| Clock | `SysvarClock11111111111111111111111111111111` | Slot, epoch, timestamp |
| Rent | `SysvarRent111111111111111111111111111111111` | Rent rates, exemption thresholds |
| EpochSchedule | `SysvarEpochSchedu1e111111111111111111111111` | Slot/epoch mapping |
| RecentBlockhashes | `SysvarRecentB1ockHashes11111111111111111111` | Recent blockhashes |
| StakeHistory | `SysvarStakeHistory1111111111111111111111111` | Stake history |
| LastRestartSlot | `SysvarLastRestartS1ot1111111111111111111111` | Last restart slot (agave) |

### Reading Sysvars

#### Method 1: Via Account (Universal)

```rust
use solana_program::sysvar::clock;

// Pass sysvar account in instruction
let clock_account = accounts.iter().find(|a| a.key == &clock::ID)?;
let clock = Clock::from_account_info(clock_account)?;
let current_slot = clock.slot;
```

#### Method 2: Via Syscall (No account needed)

```rust
use solana_program::sysvar::clock::Clock;

// Some sysvars can be read directly via syscall
let clock = Clock::get()?;
let current_slot = clock.slot;
let unix_timestamp = clock.unix_timestamp;
```

### Clock Sysvar Fields

```rust
pub struct Clock {
    pub slot: u64,                // Current slot
    pub epoch_start_timestamp: i64,  // Epoch start time
    pub epoch: u64,               // Current epoch
    pub leader_schedule_epoch: u64,  // Leader schedule epoch
    pub unix_timestamp: i64,      // Unix timestamp
}
```

### Rent Sysvar

```rust
use solana_program::sysvar::rent::Rent;

let rent = Rent::get()?;
let lamports = rent.minimum_balance(account_size);
```

---

## Crypto Syscalls

### secp256k1_recover

Recover a public key from a signature. Used for Ethereum compatibility.

```rust
// In solana-program, this is wrapped by Secp256k1RecoverInstruction
let recovered_pubkey = solana_program::secp256k1_recover::secp256k1_recover(
    &message_hash,
    recovery_id,
    &signature,
)?;
```

### secp256k1_verify

Verify a secp256k1 signature.

```rust
// Direct verification
let is_valid = solana_program::secp256k1_recover::secp256k1_verify(
    &message_hash,
    &signature,
    &pubkey,
).is_ok();
```

### secp256k1-verify Crate (NEW — Decoupled Verification)

The `secp256k1-verify` crate decouples signature verification from the program, allowing off-chain verification patterns.

```toml
[dependencies]
secp256k1-verify = "0.1"
```

```rust
use secp256k1_verify::verify;

// Verify without embedding verification code in program
let is_valid = verify(&message_hash, &signature, &pubkey)?;
```

**Benefits:**
- Smaller program binary (verification logic not compiled in)
- Lower compute cost (uses native host function)
- Consistent verification across programs

### ed25519_verify

Verify Ed25519 signatures (used by Solana wallets).

```rust
use solana_program::ed25519_program;

// Ed25519 verification is done via a dedicated instruction
// or via the ed25519_program precompile
```

---

## Memory Syscalls

### sol_memcpy

Copy memory regions. Note: BPF memory is limited — use carefully.

```rust
unsafe {
    solana_program::syscalls::sol_memcpy(
        dest.as_mut_ptr(),
        src.as_ptr(),
        len,
    );
}
```

### sol_memset

Fill memory with a byte value.

```rust
unsafe {
    solana_program::syscalls::sol_memset(
        dest.as_mut_ptr(),
        0, // value
        len,
    );
}
```

### sol_memmove

Move memory regions (handles overlapping).

### sol_memcmp

Compare memory regions.

```rust
unsafe {
    let result = solana_program::syscalls::sol_memcmp(
        a.as_ptr(),
        b.as_ptr(),
        len,
    );
}
```

---

## Return Data Syscalls

### sol_set_return_data

Set return data for the caller to read after CPI.

```rust
use solana_program::program::set_return_data;

set_return_data(&my_data)?;
```

### sol_get_return_data

Read return data from a CPI callee.

```rust
use solana_program::program::get_return_data;

let (data, program_id) = get_return_data()
    .ok_or(ProgramError::InvalidInstructionData)?;
```

---

## Heap Allocation

### sol_alloc_free

BPF programs can use heap allocation via the `sol_alloc_free` syscall.

```rust
// In Cargo.toml, the default allocator uses this syscall
// Programs can use `alloc::vec::Vec` etc.

let mut v: Vec<u8> = Vec::new();
v.push(1);
```

**Caution:** Heap allocation consumes compute units. For performance-critical paths, prefer stack allocation or zero-copy patterns.

---

## ZK Cryptography Syscalls

These syscalls support zero-knowledge proof verification on Solana.

### Alt_bn128 Operations

| Syscall | Purpose |
|---------|--------|
| `alt_bn128_group_op_g1_add` | G1 point addition |
| `alt_bn128_group_op_g1_mul` | G1 scalar multiplication |
| `alt_bn128_group_op_g1_multiexp` | G1 multi-scalar multiplication |
| `alt_bn128_group_op_g2_add` | G2 point addition |
| `alt_bn128_group_op_pairing` | Bilinear pairing check |

### Big Modular Exponentiation

```rust
// For RSA verification and other modular exponentiation
sol_big_op(/* params */);
```

### Poseidon Hash

```rust
// Poseidon hash for ZK applications
sol_poseidon_hash(/* params */);
```

---

## Agave v4.1.0 Syscall Updates

Agave v4.1.0 (released 2025) includes several syscall updates:

### Updated Syscall Behavior

| Syscall | Change in v4.1.0 |
|---------|-------------------|
| `sol_log_data` | Improved handling of large log payloads |
| `sol_invoke_signed` | Tighter account validation rules |
| `secp256k1_verify` | Reduced compute cost (approx. 30% faster) |
| Sysvar reads | More sysvars available via direct syscall (no account needed) |

### Compute Cost Changes

| Operation | Pre-v4.1.0 | v4.1.0 |
|-----------|-----------|--------|
| `sol_log` (per byte) | 100 CU | 50 CU |
| `sol_log_data` (per byte) | 100 CU | 50 CU |
| `secp256k1_verify` | 25,000 CU | ~17,500 CU |
| `ed25519_verify` (per sig) | 76,000 CU | ~58,000 CU |
| `sol_memcpy` (per 64 bytes) | 10 CU | 5 CU |

### New Sysvars

v4.1.0 exposes additional sysvars via syscall:
- `LastRestartSlot` — for rollback safety
- `TransactionContext` — limited transaction context access

---

## sbpf CFG Analyses (NEW Tooling)

The sbpf (Solana BPF) framework now includes control-flow graph (CFG) analysis tooling for debugging and optimizing BPF programs.

### What CFG Analysis Provides

- **Dead code detection** — identify unreachable code paths
- **Branch analysis** — visualize jump destinations and sources
- **Compute estimation** — estimate CU cost per basic block
- **Optimization suggestions** — identify redundant operations

### Using CFG Analysis

```bash
# Install sbpf tools
cargo install solana-bpf-tools

# Analyze a compiled program
solana-bpf-analyze target/deploy/my_program.so

# Output includes:
# - CFG visualization (DOT format)
# - Dead code warnings
# - Compute estimates per block
# - Jump optimization suggestions
```

### Common Findings from CFG Analysis

| Finding | Impact | Fix |
|---------|--------|-----|
| Unreachable code blocks | Wasted binary size | Remove dead code |
| Redundant jumps | Extra CU per instruction | Simplify control flow |
| Large basic blocks | High per-instruction CU | Split into smaller blocks |
| Missing fallthrough | Unnecessary jumps | Restructure branches |

---

## Syscall Usage Patterns

### Pattern 1: Log and Continue

```rust
pub fn process_instruction(
    _program_id: &Pubkey,
    _accounts: &[AccountInfo],
    _instruction_data: &[u8],
) -> ProgramResult {
    msg!("Instruction received");
    sol_log_compute_units(); // Log CU consumed so far
    // ... processing ...
    sol_log_compute_units(); // Log CU after processing
    Ok(())
}
```

### Pattern 2: CPI with Return Data

```rust
pub fn query_oracle(
    oracle_program: &AccountInfo,
    oracle_account: &AccountInfo,
) -> Result<[u8; 32], ProgramError> {
    let ix = Instruction {
        program_id: *oracle_program.key,
        accounts: vec![AccountMeta::new_readonly(*oracle_account.key, false)],
        data: vec![0], // Query instruction
    };
    invoke(&ix, &[oracle_account.clone()])?;

    let (return_data, _) = get_return_data()
        .ok_or(ProgramError::InvalidInstructionData)?;

    let mut result = [0u8; 32];
    result.copy_from_slice(&return_data[..32]);
    Ok(result)
}
```

### Pattern 3: Conditional CPI

```rust
pub fn maybe_transfer(
    from: &AccountInfo,
    to: &AccountInfo,
    amount: u64,
    condition: bool,
) -> ProgramResult {
    if condition {
        let ix = system_instruction::transfer(from.key, to.key, amount);
        invoke(&ix, &[from.clone(), to.clone()])
    } else {
        Ok(())
    }
}
```

---

## Compute Unit Costs (Reference)

| Syscall | Base CU | Per-Unit CU |
|---------|---------|------------|
| `sol_log` | 100 | 100/byte |
| `sol_log_64_` | 100 | — |
| `sol_log_data` | 100 | 100/byte (v4.1: 50/byte) |
| `sol_invoke_signed` | 1,000 | 500/account |
| `sol_memcpy` | 10 | 10/64 bytes (v4.1: 5/64 bytes) |
| `secp256k1_verify` | 25,000 | — (v4.1: ~17,500) |
| `ed25519_verify` | 76,000 | — (v4.1: ~58,000) |
| Sysvar read | 100 | — |
| Heap alloc | 10 | 1/byte |

---

## See Also

- [Solana Syscalls Documentation](https://solana.com/docs/programs/syscalls)
- [Agave v4.1.0 Release Notes](https://github.com/anza-xyz/agave/releases)
- [sbpf SDK](https://github.com/anza-xyz/sbpf)
- [secp256k1-verify crate](https://crates.io/crates/secp256k1-verify)
- Load skill `solana-advanced` for advanced syscall patterns
- Load skill `solana-security` for syscall security considerations
