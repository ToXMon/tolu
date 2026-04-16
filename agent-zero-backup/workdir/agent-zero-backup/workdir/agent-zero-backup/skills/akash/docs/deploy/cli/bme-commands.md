# BME (Burn-Mint Equilibrium) CLI Commands

## Overview

Since the Mainnet-17 upgrade, Akash uses the **Burn-Mint Equilibrium (BME)** model for deployment payments. Deployments are priced and paid in **ACT (Akash Compute Token, `uact`)**, a stablecoin pegged at ~$1. The BME module allows converting between AKT (the native staking/governance token) and ACT.

### Key Concepts

- **ACT (`uact`)**: Akash Compute Token, used for deployment pricing and escrow payments since Mainnet-17
- **AKT (`uakt`)**: Native Akash Token, used for staking, governance, and gas fees
- **BME Vault**: Seeded with 300,000 AKT from the community pool, provides the collateral backing ACT
- **Epoch-based minting**: Conversions process in epochs of approximately 1 minute (10 blocks)
- **Circuit breaker**: Safety mechanism that can halt BME operations in emergencies

## Commands

### Mint ACT from AKT

Convert AKT to ACT. The conversion is epoch-based and completes within ~1 minute (10 blocks).

```bash
akash tx bme mint-act 5000000uakt \
  --from wallet \
  --node https://rpc.akashnet.net:443 \
  --chain-id akashnet-2 \
  -y
```

**Parameters:**
- `5000000uakt` — Amount of AKT to burn (in micro-AKT, so 5 AKT)
- `--from` — Key name or address of the signer
- `--node` — RPC node URL
- `--chain-id` — Chain identifier (`akashnet-2` for mainnet)

### Burn ACT to AKT

Convert ACT back to AKT.

```bash
akash tx bme burn-act 5000000uact \
  --from wallet \
  --node https://rpc.akashnet.net:443 \
  --chain-id akashnet-2 \
  -y
```

### Generic Conversion

Convert between any two denominations supported by the BME module.

```bash
akash tx bme burn-mint 1000000uakt uact \
  --from wallet \
  --node https://rpc.akashnet.net:443 \
  --chain-id akashnet-2 \
  -y
```

**Parameters:**
- `1000000uakt` — Amount and source denomination to burn
- `uact` — Target denomination to mint

## Gas Configuration

BME transactions require gas fees paid in `uakt`:

```bash
export AKASH_GAS="auto"
export AKASH_GAS_PRICES="0.025uakt"
export AKASH_GAS_ADJUSTMENT="1.5"
```

Or inline:

```bash
akash tx bme mint-act 5000000uakt \
  --from wallet \
  --gas auto \
  --gas-prices 0.025uakt \
  --gas-adjustment 1.5 \
  -y
```

## Querying BME State

```bash
# Query BME module parameters
akash query bme params --node https://rpc.akashnet.net:443

# Query epoch details
akash query epochs current --node https://rpc.akashnet.net:443

# Check your ACT balance
akash query bank balances <your-address> --node https://rpc.akashnet.net:443
```

## Typical Workflow

1. **Fund wallet with AKT** — Ensure you have AKT for conversion and gas
2. **Mint ACT** — `akash tx bme mint-act <amount>uakt --from wallet -y`
3. **Wait for epoch** — ~1 minute for the conversion to complete
4. **Verify ACT balance** — `akash query bank balances <address>`
5. **Deploy** — Use `uact` in SDL pricing and deployment escrow

```bash
# Full example: Convert AKT to ACT and deploy
export AKASH_NODE=https://rpc.akashnet.net:443
export AKASH_CHAIN_ID=akashnet-2
export AKASH_KEYRING_BACKEND=os
export AKASH_GAS=auto
export AKASH_GAS_PRICES=0.025uakt
export AKASH_GAS_ADJUSTMENT=1.5

# Step 1: Mint ACT
akash tx bme mint-act 10000000uakt --from wallet -y

# Step 2: Wait ~60 seconds for epoch
sleep 60

# Step 3: Verify balance
akash query bank balances $(akash keys show wallet -a)

# Step 4: Create deployment
provider-services tx deployment create deploy.yaml --from wallet -y
```

## Important Notes

- **Gas is always paid in `uakt`** — Keep sufficient AKT for transaction fees
- **Deployment pricing uses `uact`** — SDL `denom` field should be `uact`
- **Conversion is not instant** — Epoch-based processing takes ~1 minute
- **BME vault has limited capacity** — Seeded with 300,000 AKT; extremely large conversions may face limits
- **Circuit breaker** — Governance can halt BME operations in emergencies

## Error Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `insufficient funds` | Not enough AKT for conversion or gas | Fund wallet with AKT |
| `epoch not reached` | Previous mint not yet processed | Wait for current epoch to complete (~1 min) |
| `circuit breaker activated` | BME operations halted by governance | Wait for governance to re-enable |
| `amount too large` | Exceeds BME vault capacity | Convert in smaller batches |

## Sources

- [Akash Documentation — ACT Mint/Burn](https://akash.network/docs/developers/deployment/cli/act-mint-burn/)
- [Mainnet-17 Upgrade Guide](https://akash.network/docs/node-operators/network-upgrades/mainnet-17/)
