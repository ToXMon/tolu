---
name: solana-testing
description: Test Solana programs with LiteSVM, Mollusk v0.13.4, Surfpool, Anchor tests, fuzzing, and CI gates.
version: 1.0.1
---

# Solana Testing

## When to Use

Use this skill when the task involves:

- writing unit, integration, instruction-level, or local-validator tests
- choosing LiteSVM, Mollusk, Surfpool, bankrun, or Anchor tests
- building regression tests for signers, owners, PDAs, CPIs, Token-2022, and state machines
- adding CI gates for Solana programs and clients
- reproducing transaction failures from logs

Trigger phrases: `solana-testing`, Solana production, devnet, mainnet, Anchor, Solana Kit, Token-2022, RPC, Explorer verification, and the domain phrases above.

## Core Operating Behaviors

- Check current Solana documentation through the Solana MCP server: `https://mcp.solana.com/mcp`.
- Default to devnet unless the user explicitly asks for testnet or mainnet-beta.
- Prefix Solana CLI and Anchor CLI commands with `NO_DNA=1`.
- Verify on-chain evidence with Explorer, RPC, or direct account/program queries.
- Record versions for Anchor, Agave/Solana CLI, Rust, Node, Kit, and relevant SDKs.
- Treat mainnet, custody, admin keys, upgrade authority, and irreversible actions as human-gated.
- Work in small, testable slices: design one account/instruction/client path, test it, then expand.


## Modern Ecosystem Context

- Mollusk v0.13.4 is current for instruction-level testing
- Agave/Firedancer/Mithril conformance fuzzing is expanding around syscalls and transaction costs
- sbpf CFG tooling can support bytecode reachability analysis

## Primary Workflow

1. Choose the lowest test layer that proves the invariant: pure Rust, Mollusk, LiteSVM, Anchor local validator, Surfpool, or devnet smoke test
2. Create fixtures for payer, authority, PDAs, mints, ATAs, sysvars, and mocked oracles
3. Write happy-path and failure-path tests before changing production logic
4. Run focused tests first, then full suite with `NO_DNA=1 anchor test` where applicable
5. Capture logs and exact custom errors for regressions
6. Add CI that pins toolchains and uploads failing logs/artifacts

## Production Design Notes

Test the invariant, not just the function. Every program instruction should have unauthorized signer, wrong owner, wrong PDA, invalid mint/token program, and replay coverage where relevant.

## Common Failure Modes

| Failure | Likely Cause | Fix |
|---|---|---|
| PDA mismatch | Client and program seeds differ | Centralize seed definitions, test derived address, store canonical bump where useful |
| Owner mismatch | Wrong program owns account | Check `owner`, token program ID, and system/SPL/Token-2022 boundaries |
| Missing signer | Authority omitted or PDA signer seeds wrong | Recheck account metas and signer seeds |
| Simulation failed | Bad account order, stale blockhash, compute cap, constraint error | Inspect logs, simulate locally, narrow the failing instruction |
| Devnet differs from local | Toolchain/RPC/cluster mismatch | Pin versions, verify cluster config, reproduce on devnet |
| Mainnet launch risk | Upgrade/admin/oracle/custody path not controlled | Use multisig, runbook, monitoring, and human gate |


## Reference Files

- `references/litesvm-and-mollusk.md` — LiteSVM and Mollusk test strategy
- `references/fuzzing-and-ci.md` — Fuzzing and CI gates
- `references/anchor-test-patterns.md` — Anchor test patterns

## Cross-Skill References

| Related Skill | When to Switch |
|---|---|
| `solana-anchor-programs` | Tests reveal account constraint or instruction design issues |
| `solana-security` | A test covers exploit classes or audit findings |
| `solana-errors-and-compat` | Failures are toolchain or version related |

## Verification Checklist

- [ ] Current docs checked through `https://mcp.solana.com/mcp` or official project docs.
- [ ] Commands use `NO_DNA=1` where applicable.
- [ ] Cluster is explicit: devnet, testnet, or mainnet-beta.
- [ ] Account ownership, signer, writable, PDA seed, bump, rent, and authority assumptions are stated.
- [ ] Tests or verification steps cover the happy path and at least one failure path.
- [ ] On-chain evidence path is provided: Explorer URL, RPC query, signature, program ID, or account address.
- [ ] Security-sensitive assumptions and mainnet risks are named.
- [ ] Related skills are referenced for adjacent work.

