# CPI and PDA security

Verify program IDs, signer seeds, token program IDs, mint/authority/amount, post-state, and account ownership for every CPI.

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
