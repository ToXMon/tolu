# Pinocchio Framework Guide

Pinocchio is a minimalist Rust crate for crafting Solana programs **without** the heavyweight `solana-program` crate. It delivers significant performance gains through zero-copy techniques and minimal dependencies.

## When to Use Pinocchio

| Scenario | Use Pinocchio | Use solana-program |
|----------|-------------|-------------------|
| Compute-critical (sub-1000 CU ops) | ✅ | |
| Small binary size needed | ✅ | |
| Zero-copy account access | ✅ | |
| `no_std` environment | ✅ | |
| Quick prototyping | | ✅ |
| Maximum ecosystem compatibility | | ✅ |
| Anchor migration | | ✅ |

### Performance Gains (Typical)

| Metric | solana-program | Pinocchio | Improvement |
|--------|---------------|----------|------------|
| Binary size | 30-80KB | 5-15KB | 60-80% smaller |
| Compute units (simple transfer) | ~1500 CU | ~300 CU | 80% fewer |
| Account deserialization | Copy-based | Zero-copy | No allocation |
| Dependency compile time | 30-60s | 5-15s | 70% faster |

---

## Project Setup

### Cargo.toml

```toml
[package]
name = "my-pinocchio-program"
version = "0.1.0"
edition = "2021"

[dependencies]
pinocchio = "0.8"
pinocchio-system = "0.2"
pinocchio-token = "0.1"

[lib]
crate-type = ["cdylib", "lib"]
```

### Entrypoint

```rust
use pinocchio::{entrypoint, msg, ProgramResult};

entrypoint!(process_instruction);

pub fn process_instruction(instruction: &pinocchio::Instruction) -> ProgramResult {
    msg!("Hello from Pinocchio");
    Ok(())
}
```

The `Instruction` struct provides zero-copy access to:
- `instruction.accounts` — `&[AccountInfo]` (zero-copy views)
- `instruction.data` — `&[u8]` (instruction data)
- `instruction.program_id` — `&Pubkey`

---

## Account Info (Zero-Copy)

Pinocchio's `AccountInfo` is a zero-copy view into the runtime's account memory. No serialization/deserialization overhead.

```rust
use pinocchio::account_info::AccountInfo;

// Access account fields directly
let account = &instruction.accounts[0];
let key = account.key();           // &Pubkey
let owner = account.owner();       // &Pubkey
let lamports = account.lamports(); // u64
let data = account.data();         // &[u8]
let is_signer = account.is_signer();
let is_writable = account.is_writable();
```

### Borrowing Account Data

```rust
// Immutable borrow
let data = account.try_borrow_data()?;

// Mutable borrow
let mut data = account.try_borrow_mut_data()?;
data[0] = 1;
```

---

## Struct Layout and Zero-Copy

### Defining Account Structs

Pinocchio programs define account state with explicit memory layout. Order fields largest-to-smallest for optimal alignment.

```rust
#[repr(C, packed)]
pub struct CounterData {
    pub authority: [u8; 32],  // 32 bytes
    pub count: u64,           // 8 bytes
    pub bump: u8,             // 1 byte
    // Total: 41 bytes
}

impl CounterData {
    pub const LEN: usize = 41;

    /// Zero-copy read — no allocation, no copy
    pub fn from_bytes(data: &[u8]) -> Result<&Self, ProgramError> {
        if data.len() < Self::LEN {
            return Err(ProgramError::InvalidAccountData);
        }
        // Safe because we checked length and struct is #[repr(C, packed)]
        Ok(unsafe { &*(data.as_ptr() as *const Self) })
    }

    /// Zero-copy mutable read
    pub fn from_bytes_mut(data: &mut [u8]) -> Result<&mut Self, ProgramError> {
        if data.len() < Self::LEN {
            return Err(ProgramError::InvalidAccountData);
        }
        Ok(unsafe { &mut *(data.as_mut_ptr() as *mut Self) })
    }
}
```

### assert_no_padding! Macro

Use `assert_no_padding!` to verify struct layout at compile time:

```rust
use pinocchio::assert_no_padding;

#[repr(C)]
pub struct MyStruct {
    pub field1: u64,    // 8 bytes
    pub field2: Pubkey,  // 32 bytes
}

// Compile-time check — fails if compiler added padding
assert_no_padding!(MyStruct);
```

### Field Alignment Best Practices

Order fields from largest to smallest to minimize padding:

```rust
// GOOD — no padding needed
#[repr(C, packed)]
pub struct GoodLayout {
    pub pubkey: [u8; 32],  // 32 bytes
    pub u64_val: u64,      // 8 bytes
    pub u32_val: u32,      // 4 bytes
    pub u16_val: u16,      // 2 bytes
    pub u8_val: u8,        // 1 byte
    // Total: 47 bytes, no padding
}

// BAD — compiler may add padding
#[repr(C)]
pub struct BadLayout {
    pub u8_val: u8,        // 1 byte + 7 padding
    pub u64_val: u64,      // 8 bytes
    pub u16_val: u16,      // 2 bytes + 2 padding
    pub u32_val: u32,      // 4 bytes
}
```

---

## Pinocchio Traits

### Discriminator

Single-byte discriminator (unlike Anchor's 8 bytes):

```rust
use pinocchio::Discriminator;

#[repr(u8)]
enum Instruction {
    Initialize = 0,
    Increment = 1,
    Reset = 2,
}

impl Discriminator for Instruction {
    const DISCRIMINATOR: u8 = Self::INITIALIZE as u8;
}
```

### AccountSize

```rust
use pinocchio::AccountSize;

impl AccountSize for CounterData {
    const SIZE: usize = 41;
}
```

### AccountDeserialize / AccountSerialize

```rust
use pinocchio::{AccountDeserialize, AccountSerialize};

impl AccountDeserialize for CounterData {
    fn try_from_bytes(data: &[u8]) -> Result<Self, ProgramError> {
        // For zero-copy, return reference instead of owned
        Self::from_bytes(data).map(|r| r.clone())
    }
}

impl AccountSerialize for CounterData {
    fn try_to_bytes(&self, dest: &mut [u8]) -> Result<(), ProgramError> {
        if dest.len() < Self::LEN {
            return Err(ProgramError::InvalidAccountData);
        }
        unsafe {
            core::ptr::copy_nonoverlapping(
                self as *const Self as *const u8,
                dest.as_mut_ptr(),
                Self::LEN,
            );
        }
        Ok(())
    }
}
```

### PdaSeeds

```rust
use pinocchio::PdaSeeds;

impl PdaSeeds for CounterData {
    const SEEDS: &[&[u8]] = &[b"counter"];
}
```

---

## Instruction Parsing

### TryFrom Pattern

```rust
use pinocchio::ProgramError;

#[repr(u8)]
enum Instruction {
    Initialize { bump: u8 },
    Increment { amount: u64 },
    Reset,
}

impl TryFrom<&[u8]> for Instruction {
    type Error = ProgramError;

    fn try_from(data: &[u8]) -> Result<Self, Self::Error> {
        let disc = data.first().ok_or(ProgramError::InvalidInstructionData)?;
        match disc {
            0 => {
                let bump = *data.get(1).ok_or(ProgramError::InvalidInstructionData)?;
                Ok(Self::Initialize { bump })
            }
            1 => {
                let amount = data
                    .get(1..9)
                    .and_then(|s| s.try_into().ok())
                    .map(u64::from_le_bytes)
                    .ok_or(ProgramError::InvalidInstructionData)?;
                Ok(Self::Increment { amount })
            }
            2 => Ok(Self::Reset),
            _ => Err(ProgramError::InvalidInstructionData),
        }
    }
}
```

### Account Validation with TryFrom

```rust
use pinocchio::account_info::AccountView;

struct InitializeAccounts<'a> {
    payer: &'a AccountInfo,
    counter: &'a AccountInfo,
    system_program: &'a AccountInfo,
}

impl<'a> TryFrom<&'a [AccountInfo]> for InitializeAccounts<'a> {
    type Error = ProgramError;

    fn try_from(accounts: &'a [AccountInfo]) -> Result<Self, Self::Error> {
        let payer = accounts.first().ok_or(ProgramError::NotEnoughAccountKeys)?;
        let counter = accounts.get(1).ok_or(ProgramError::NotEnoughAccountKeys)?;
        let system_program = accounts.get(2).ok_or(ProgramError::NotEnoughAccountKeys)?;

        // Validate payer
        if !payer.is_signer() || !payer.is_writable() {
            return Err(ProgramError::MissingRequiredSignature);
        }

        // Validate counter PDA
        let (expected_pda, _) = Pubkey::find_program_address(
            &[b"counter"],
            &crate::ID,
        );
        if counter.key() != &expected_pda {
            return Err(ProgramError::InvalidSeeds);
        }

        // Validate system program
        if system_program.key() != &pinocchio_system::ID {
            return Err(ProgramError::IncorrectProgramId);
        }

        Ok(Self { payer, counter, system_program })
    }
}
```

---

## CPI (Cross-Program Invocation)

### Simple Transfer

```rust
use pinocchio_system::instructions::Transfer;

pub fn transfer_sol(
    from: &AccountInfo,
    to: &AccountInfo,
    lamports: u64,
) -> ProgramResult {
    Transfer { from, to, lamports }.invoke()
}
```

### CPI with PDA Signer

```rust
use pinocchio::{seeds, Signer};
use pinocchio_system::instructions::Transfer;

pub fn transfer_from_pda(
    from: &AccountInfo,
    to: &AccountInfo,
    lamports: u64,
    pda_seeds: &[&[u8]],
) -> ProgramResult {
    let signer = Signer::from(seeds![pda_seeds]);
    Transfer { from, to, lamports }.invoke_signed(&[signer])
}
```

### Create Account via System Program

```rust
use pinocchio_system::instructions::CreateAccount;

pub fn create_account(
    from: &AccountInfo,
    to: &AccountInfo,
    lamports: u64,
    space: usize,
    owner: &Pubkey,
    seeds: &[&[u8]],
) -> ProgramResult {
    let signer = Signer::from(seeds![seeds]);
    CreateAccount {
        from,
        to,
        lamports,
        space: space as u64,
        owner,
    }
    .invoke_signed(&[signer])
}
```

### Token Program CPI

```rust
use pinocchio_token::instructions::Transfer;

pub fn transfer_tokens(
    source: &AccountInfo,
    destination: &AccountInfo,
    authority: &AccountInfo,
    amount: u64,
    signer_seeds: Option<&[&[u8]]>,
) -> ProgramResult {
    let transfer = Transfer {
        source,
        destination,
        authority,
        amount,
    };

    match signer_seeds {
        Some(seeds) => {
            let signer = Signer::from(seeds![seeds]);
            transfer.invoke_signed(&[signer])
        }
        None => transfer.invoke(),
    }
}
```

---

## Event Emission

Pinocchio uses CPI-to-self with an `event_authority` PDA for truncation-safe event emission.

### Event Authority PDA

```rust
use pinocchio::Pubkey;

pub fn event_authority(program_id: &Pubkey) -> (Pubkey, u8) {
    Pubkey::find_program_address(&[b"__event_authority"], program_id)
}
```

### Emitting Events

```rust
pub fn emit_event(program_id: &Pubkey, data: &[u8]) -> ProgramResult {
    let (event_authority, bump) = event_authority(program_id);

    // Build event instruction (CPI to self)
    let ix = AccountMeta {
        pubkey: event_authority,
        is_signer: false,
        is_writable: false,
    };

    // Use sol_log_data for simple events
    pinocchio::log::sol_log_data(&[data]);
    Ok(())
}
```

### Using sol_log_data (Simpler Approach)

For most use cases, `sol_log_data` is sufficient and simpler:

```rust
use pinocchio::log::sol_log_data;

#[repr(C, packed)]
struct CounterIncrementedEvent {
    new_count: u64,
    increment_by: u64,
}

pub fn emit_increment(new_count: u64, increment_by: u64) -> ProgramResult {
    let event = CounterIncrementedEvent { new_count, increment_by };
    let bytes = unsafe {
        core::slice::from_raw_parts(
            &event as *const _ as *const u8,
            core::mem::size_of::<CounterIncrementedEvent>(),
        )
    };
    sol_log_data(&[bytes]);
    Ok(())
}
```

---

## Batch Instructions

Pinocchio allows batching multiple operations in a single CPI, saving ~1000 CU per batched operation.

```rust
pub fn process_batch_transfers(
    accounts: &[AccountInfo],
    transfers: &[(usize, usize, u64)], // (from_idx, to_idx, lamports)
) -> ProgramResult {
    for (from_idx, to_idx, lamports) in transfers {
        let from = &accounts[*from_idx];
        let to = &accounts[*to_idx];
        Transfer { from, to, lamports: *lamports }.invoke()?;
    }
    Ok(())
}
```

---

## Performance Optimization Techniques

### 1. Feature Flags

Use feature flags to include/exclude functionality at compile time:

```rust
#[cfg(feature = "debug-logs")]
msg!("Processing instruction: {}", disc);
```

### 2. Bitwise Flags

Pack multiple boolean flags into a single byte:

```rust
const FLAG_IS_INITIALIZED: u8 = 1 << 0;
const FLAG_IS_PAUSED: u8 = 1 << 1;
const FLAG_IS_FROZEN: u8 = 1 << 2;

// Check: if flags & FLAG_IS_PAUSED != 0
// Set: flags |= FLAG_IS_PAUSED
// Clear: flags &= !FLAG_IS_PAUSED
```

### 3. No Allocation

```rust
// Pinocchio provides no_allocator! macro to enforce no heap allocation
pinocchio::no_allocator!();
```

### 4. Skip Redundant Checks

If you know an account is valid from a prior instruction in a batch, skip re-validation:

```rust
pub fn process_increment_then_reset(
    counter: &AccountInfo,
) -> ProgramResult {
    // Validate once
    if counter.owner() != &crate::ID {
        return Err(ProgramError::IllegalOwner);
    }

    // Increment
    let mut data = CounterData::from_bytes_mut(counter.try_borrow_mut_data()?)?;
    data.count = data.count.checked_add(1).ok_or(ProgramError::ArithmeticOverflow)?;

    // Reset — no need to re-validate owner
    data.count = 0;

    Ok(())
}
```

---

## Build and Deploy

### Build

```bash
NO_DNA=1 cargo build-sbf
```

### Check Binary Size

```bash
# Typical Pinocchio binary: 5-15KB
ls -la target/deploy/<program_name>.so

# Verify ELF format
file target/deploy/<program_name>.so
# Expected: ELF 64-bit LSB shared object, x86-64, ...
```

### Common Build Issues

#### Edition 2024 Errors

If you see `edition2024` errors, pin the Rust edition explicitly:

```toml
[package]
edition = "2021"
```

#### Dependency Version Conflicts

Pin compatible versions:

```toml
[dependencies]
pinocchio = "=0.8.0"
pinocchio-system = "=0.2.0"
```

---

## Testing Pinocchio Programs

### Mollusk (Recommended)

```rust
use mollusk_svm::{result::Assert, Mollusk};

#[test]
fn test_initialize() {
    let mollusk = Mollusk::new(&crate::ID, crate::process_instruction);

    let payer = Pubkey::new_unique();
    let (counter_pda, bump) =
        Pubkey::find_program_address(&[b"counter"], &crate::ID);

    let instruction = Instruction {
        program_id: crate::ID,
        accounts: vec![
            AccountMeta::new(payer, true),
            AccountMeta::new(counter_pda, false),
            AccountMeta::new_readonly(solana_system_program::ID, false),
        ],
        data: vec![0, bump], // Initialize instruction
    };

    let result = mollusk.process_instruction(&instruction);
    result.assert_success();
}
```

### LiteSVM

```rust
use litesvm::LiteSVM;

#[test]
fn test_increment() {
    let mut svm = LiteSVM::new();
    // ... setup and test logic
}
```

---

## Security Checklist (Pinocchio)

Since Pinocchio doesn't auto-validate like Anchor, implement these checks manually:

- [ ] **Owner check** — `account.owner() == &crate::ID`
- [ ] **Signer check** — `account.is_signer()` for required signers
- [ ] **Writable check** — `account.is_writable()` for accounts being modified
- [ ] **PDA derivation** — verify `account.key() == &expected_pda`
- [ ] **Data length** — `account.data().len() >= MyStruct::LEN`
- [ ] **Discriminator** — verify instruction discriminator is valid
- [ ] **Rent exemption** — ensure accounts have sufficient lamports
- [ ] **Sysvar identity** — verify sysvar accounts by address
- [ ] **Checked arithmetic** — use `checked_add`, `checked_sub`, etc.
- [ ] **No `unwrap()`/`expect()`** — handle all errors explicitly

---

## See Also

- [Pinocchio Repository](https://github.com/anza-xyz/pinocchio)
- [pinocchio-system crate](https://crates.io/crates/pinocchio-system)
- [pinocchio-token crate](https://crates.io/crates/pinocchio-token)
- [Pinocchio Guide (Community)](https://github.com/vict0rcarvalh0/pinocchio-guide)
- [How to Build with Pinocchio (Helius)](https://www.helius.dev/blog/pinocchio)
- [Solana Optimized Programs](https://github.com/Laugharne/solana_optimized_programs)
- Load skill `solana-security` for comprehensive vulnerability review
- Load skill `solana-testing` for Mollusk/LiteSVM setup details
