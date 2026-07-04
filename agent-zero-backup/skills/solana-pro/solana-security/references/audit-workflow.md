# Audit workflow

Inventory instructions/accounts, map authorities, trace token movement, inspect constraints, write exploit tests, review upgrade/deploy process, document severity and remediation.

## Required Discipline

- Use `NO_DNA=1` for Solana CLI and Anchor CLI commands.
- Check `https://mcp.solana.com/mcp` or official docs before trusting old examples.
- Default to devnet for experiments.
- Verify with Explorer, RPC, tests, or direct account/program queries.

## Verification

- [ ] Inputs and assumptions stated.
- [ ] Version and cluster explicit.
- [ ] Account/authority/security checks named.
- [ ] Evidence path included.
