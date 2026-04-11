# Go SDK Client Setup

Complete client configuration for Akash Go SDK.

## Full Client Setup

```go
package akash

import (
    "context"
    "fmt"
    "os"

    "github.com/cosmos/cosmos-sdk/client"
    "github.com/cosmos/cosmos-sdk/client/flags"
    "github.com/cosmos/cosmos-sdk/client/tx"
    "github.com/cosmos/cosmos-sdk/codec"
    codectypes "github.com/cosmos/cosmos-sdk/codec/types"
    "github.com/cosmos/cosmos-sdk/crypto/hd"
    "github.com/cosmos/cosmos-sdk/crypto/keyring"
    sdk "github.com/cosmos/cosmos-sdk/types"
    "github.com/cosmos/cosmos-sdk/types/tx/signing"
    authtypes "github.com/cosmos/cosmos-sdk/x/auth/types"
    authtx "github.com/cosmos/cosmos-sdk/x/auth/tx"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"

    akashcodec "github.com/akash-network/akash-api/go/node/codec"
)

type AkashClient struct {
    clientCtx client.Context
    txFactory tx.Factory
    keyring   keyring.Keyring
    address   sdk.AccAddress
}

func NewAkashClient(
    nodeURI string,
    chainID string,
    keyringBackend string,
    keyringDir string,
    keyName string,
) (*AkashClient, error) {
    // Configure SDK
    config := sdk.GetConfig()
    config.SetBech32PrefixForAccount("akash", "akashpub")
    config.Seal()

    // Create codec
    interfaceRegistry := codectypes.NewInterfaceRegistry()
    akashcodec.RegisterInterfaces(interfaceRegistry)
    cdc := codec.NewProtoCodec(interfaceRegistry)

    // Setup keyring
    kr, err := keyring.New(
        "akash",
        keyringBackend,
        keyringDir,
        os.Stdin,
        cdc,
    )
    if err != nil {
        return nil, fmt.Errorf("failed to create keyring: %w", err)
    }

    // Get key
    keyInfo, err := kr.Key(keyName)
    if err != nil {
        return nil, fmt.Errorf("failed to get key: %w", err)
    }

    address, err := keyInfo.GetAddress()
    if err != nil {
        return nil, fmt.Errorf("failed to get address: %w", err)
    }

    // Create gRPC connection
    grpcConn, err := grpc.Dial(
        nodeURI,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to node: %w", err)
    }

    // Create client context
    clientCtx := client.Context{}.
        WithChainID(chainID).
        WithCodec(cdc).
        WithInterfaceRegistry(interfaceRegistry).
        WithTxConfig(authtx.NewTxConfig(cdc, authtx.DefaultSignModes)).
        WithAccountRetriever(authtypes.AccountRetriever{}).
        WithBroadcastMode(flags.BroadcastSync).
        WithKeyring(kr).
        WithFromName(keyName).
        WithFromAddress(address).
        WithGRPCClient(grpcConn)

    // Create tx factory
    txFactory := tx.Factory{}.
        WithChainID(chainID).
        WithKeybase(kr).
        WithGas(200000).
        WithGasAdjustment(1.5).
        WithGasPrices("0.025uakt").
        WithSignMode(signing.SignMode_SIGN_MODE_DIRECT)

    return &AkashClient{
        clientCtx: clientCtx,
        txFactory: txFactory,
        keyring:   kr,
        address:   address,
    }, nil
}

func (c *AkashClient) Address() string {
    return c.address.String()
}

func (c *AkashClient) Close() error {
    if c.clientCtx.GRPCClient != nil {
        return c.clientCtx.GRPCClient.Close()
    }
    return nil
}
```

## Deployment Operations

```go
import (
    deploymentv1beta3 "github.com/akash-network/akash-api/go/node/deployment/v1beta3"
)

func (c *AkashClient) CreateDeployment(
    ctx context.Context,
    dseq uint64,
    groups []deploymentv1beta3.GroupSpec,
    version []byte,
    deposit sdk.Coin,
) (*sdk.TxResponse, error) {
    msg := &deploymentv1beta3.MsgCreateDeployment{
        ID: deploymentv1beta3.DeploymentID{
            Owner: c.address.String(),
            DSeq:  dseq,
        },
        Groups:    groups,
        Version:   version,
        Deposit:   deposit,
        Depositor: c.address.String(),
    }

    return c.broadcastTx(ctx, msg)
}

func (c *AkashClient) CloseDeployment(
    ctx context.Context,
    dseq uint64,
) (*sdk.TxResponse, error) {
    msg := &deploymentv1beta3.MsgCloseDeployment{
        ID: deploymentv1beta3.DeploymentID{
            Owner: c.address.String(),
            DSeq:  dseq,
        },
    }

    return c.broadcastTx(ctx, msg)
}

func (c *AkashClient) DepositDeployment(
    ctx context.Context,
    dseq uint64,
    amount sdk.Coin,
) (*sdk.TxResponse, error) {
    msg := &deploymentv1beta3.MsgDepositDeployment{
        ID: deploymentv1beta3.DeploymentID{
            Owner: c.address.String(),
            DSeq:  dseq,
        },
        Amount:    amount,
        Depositor: c.address.String(),
    }

    return c.broadcastTx(ctx, msg)
}

func (c *AkashClient) QueryDeployment(
    ctx context.Context,
    dseq uint64,
) (*deploymentv1beta3.QueryDeploymentResponse, error) {
    queryClient := deploymentv1beta3.NewQueryClient(c.clientCtx.GRPCClient)

    return queryClient.Deployment(ctx, &deploymentv1beta3.QueryDeploymentRequest{
        ID: deploymentv1beta3.DeploymentID{
            Owner: c.address.String(),
            DSeq:  dseq,
        },
    })
}
```

## Market Operations

```go
import (
    marketv1beta4 "github.com/akash-network/akash-api/go/node/market/v1beta4"
)

func (c *AkashClient) CreateLease(
    ctx context.Context,
    dseq uint64,
    gseq uint32,
    oseq uint32,
    provider string,
) (*sdk.TxResponse, error) {
    msg := &marketv1beta4.MsgCreateLease{
        BidID: marketv1beta4.BidID{
            Owner:    c.address.String(),
            DSeq:     dseq,
            GSeq:     gseq,
            OSeq:     oseq,
            Provider: provider,
        },
    }

    return c.broadcastTx(ctx, msg)
}

func (c *AkashClient) QueryBids(
    ctx context.Context,
    dseq uint64,
) (*marketv1beta4.QueryBidsResponse, error) {
    queryClient := marketv1beta4.NewQueryClient(c.clientCtx.GRPCClient)

    return queryClient.Bids(ctx, &marketv1beta4.QueryBidsRequest{
        Filters: marketv1beta4.BidFilters{
            Owner: c.address.String(),
            DSeq:  dseq,
        },
    })
}

func (c *AkashClient) QueryLeases(
    ctx context.Context,
) (*marketv1beta4.QueryLeasesResponse, error) {
    queryClient := marketv1beta4.NewQueryClient(c.clientCtx.GRPCClient)

    return queryClient.Leases(ctx, &marketv1beta4.QueryLeasesRequest{
        Filters: marketv1beta4.LeaseFilters{
            Owner: c.address.String(),
        },
    })
}
```

## Transaction Broadcasting

```go
func (c *AkashClient) broadcastTx(
    ctx context.Context,
    msgs ...sdk.Msg,
) (*sdk.TxResponse, error) {
    // Build unsigned tx
    txBuilder, err := tx.BuildUnsignedTx(c.txFactory, msgs...)
    if err != nil {
        return nil, fmt.Errorf("failed to build tx: %w", err)
    }

    // Sign tx
    err = tx.Sign(c.txFactory, c.clientCtx.FromName, txBuilder, true)
    if err != nil {
        return nil, fmt.Errorf("failed to sign tx: %w", err)
    }

    // Encode tx
    txBytes, err := c.clientCtx.TxConfig.TxEncoder()(txBuilder.GetTx())
    if err != nil {
        return nil, fmt.Errorf("failed to encode tx: %w", err)
    }

    // Broadcast
    res, err := c.clientCtx.BroadcastTx(txBytes)
    if err != nil {
        return nil, fmt.Errorf("failed to broadcast tx: %w", err)
    }

    if res.Code != 0 {
        return res, fmt.Errorf("tx failed: %s", res.RawLog)
    }

    return res, nil
}
```

## Usage Example

```go
func main() {
    client, err := NewAkashClient(
        "grpc.akashnet.net:443",
        "akashnet-2",
        "file",
        os.ExpandEnv("$HOME/.akash"),
        "wallet",
    )
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    ctx := context.Background()

    // Create deployment
    dseq := uint64(time.Now().Unix())
    deposit := sdk.NewCoin("uact", sdk.NewInt(5000000))

    txRes, err := client.CreateDeployment(ctx, dseq, groups, version, deposit)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Deployment created: %s\n", txRes.TxHash)
}
```

## AuthZ Operations

Akash supports Cosmos SDK AuthZ for delegating specific on-chain actions to another address
without transferring tokens or ownership. Combined with FeeGrants, this enables fully
delegated deployment platforms where a service can authorize and fund user deployments.

### AuthZ Message Types

```go
import (
    "time"

    "github.com/cosmos/cosmos-sdk/x/authz"
    authztypes "github.com/cosmos/cosmos-sdk/x/authz/types"
    feegranttypes "github.com/cosmos/cosmos-sdk/x/feegrant"

    deploymentv1beta3 "github.com/akash-network/akash-api/go/node/deployment/v1beta3"
    marketv1beta4 "github.com/akash-network/akash-api/go/node/market/v1beta4"
)

// Supported Akash AuthZ message type URLs:
//   "/akash.deployment.v1beta3.MsgCreateDeployment"
//   "/akash.deployment.v1beta3.MsgCloseDeployment"
//   "/akash.deployment.v1beta3.MsgDepositDeployment"
//   "/akash.market.v1beta4.MsgCreateLease"
```

### Granting Deployment Permissions

Grant a **GenericAuthorization** to a grantee for specific Akash deployment and market
message types. The grant includes an expiration timestamp.

```go
// GrantDeploymentPermissions creates AuthZ grants for Akash deployment operations.
// The granter authorizes the grantee to create/close deployments and create leases
// on their behalf until the specified expiration.
func (c *AkashClient) GrantDeploymentPermissions(
    ctx context.Context,
    granteeAddr sdk.AccAddress,
    expiration time.Time,
) (*sdk.TxResponse, error) {

    granter := c.address.String()
    grantee := granteeAddr.String()

    // Define the message types the grantee is authorized to execute
    grantedMsgTypes := []string{
        "/akash.deployment.v1beta3.MsgCreateDeployment",
        "/akash.deployment.v1beta3.MsgCloseDeployment",
        "/akash.market.v1beta4.MsgCreateLease",
    }

    // Create one MsgGrant per message type
    // Each grant uses GenericAuthorization which allows the grantee to execute
    // the specific message type on behalf of the granter
    var msgs []sdk.Msg
    for _, msgType := range grantedMsgTypes {
        grant := &authztypes.Grant{
            Authorization: &codectypes.Any{
                TypeUrl: "/cosmos.authz.v1beta1.GenericAuthorization",
                Value: mustMarshalGenericAuthorization(
                    authztypes.NewGenericAuthorization(msgType),
                ),
            },
            Expiration: &expiration,
        }

        msgs = append(msgs, &authztypes.MsgGrant{
            Granter: granter,
            Grantee: grantee,
            Grant:   *grant,
        })
    }

    return c.broadcastTx(ctx, msgs...)
}

// mustMarshalGenericAuthorization serializes a GenericAuthorization for inclusion
// in a Grant.
func mustMarshalGenericAuthorization(
    auth *authztypes.GenericAuthorization,
) []byte {
    cdc := codec.NewProtoCodec(nil) // use the client's codec in production
    bz, err := cdc.MarshalJSON(auth)
    if err != nil {
        panic(err)
    }
    return bz
}
```

#### Grant with Codec Registration

AuthZ types must be registered in the interface registry for proper serialization:

```go
import (
    codectypes "github.com/cosmos/cosmos-sdk/codec/types"
    cryptocodec "github.com/cosmos/cosmos-sdk/crypto/codec"
    sdkcodec "github.com/cosmos/cosmos-sdk/codec"
    authzcodec "github.com/cosmos/cosmos-sdk/x/authz/codec"
)

// Register AuthZ codec interfaces when setting up the client
func registerAuthZCodec(ir codectypes.InterfaceRegistry) {
    // Standard SDK codec registrations
    cryptocodec.RegisterInterfaces(ir)
    sdkcodec.RegisterInterfaces(ir)

    // AuthZ module codec
    authzcodec.RegisterInterfaces(ir)
}
```

### Executing Deployment via Grant

A grantee executes a deployment on behalf of the granter by wrapping the inner message
in a **MsgExec**. The inner message is constructed from the granter's perspective (the
granter's address is used as the owner).

```go
// ExecuteCreateDeploymentViaGrant wraps a MsgCreateDeployment inside an AuthZ MsgExec
// so the grantee can create a deployment on behalf of the granter.
func (c *AkashClient) ExecuteCreateDeploymentViaGrant(
    ctx context.Context,
    granterAddr sdk.AccAddress,
    dseq uint64,
    groups []deploymentv1beta3.GroupSpec,
    version []byte,
    deposit sdk.Coin,
) (*sdk.TxResponse, error) {

    // Build the inner message from the GRANTER's perspective
    // The granter is the owner of the deployment
    innerMsg := &deploymentv1beta3.MsgCreateDeployment{
        ID: deploymentv1beta3.DeploymentID{
            Owner: granterAddr.String(),
            DSeq:  dseq,
        },
        Groups:    groups,
        Version:   version,
        Deposit:   deposit,
        Depositor: granterAddr.String(),
    }

    // Wrap the inner message in an Any for MsgExec
    msgAny, err := codectypes.NewAnyWithValue(innerMsg)
    if err != nil {
        return nil, fmt.Errorf("failed to pack inner msg: %w", err)
    }

    // MsgExec is signed by the GRANTEE (c.address)
    // The grantee executes the granter's authorized message
    execMsg := &authztypes.MsgExec{
        Grantee: c.address.String(),
        Msgs:    []*codectypes.Any{msgAny},
    }

    return c.broadcastTx(ctx, execMsg)
}

// ExecuteCloseDeploymentViaGrant wraps a MsgCloseDeployment inside MsgExec.
func (c *AkashClient) ExecuteCloseDeploymentViaGrant(
    ctx context.Context,
    granterAddr sdk.AccAddress,
    dseq uint64,
) (*sdk.TxResponse, error) {

    innerMsg := &deploymentv1beta3.MsgCloseDeployment{
        ID: deploymentv1beta3.DeploymentID{
            Owner: granterAddr.String(),
            DSeq:  dseq,
        },
    }

    msgAny, err := codectypes.NewAnyWithValue(innerMsg)
    if err != nil {
        return nil, fmt.Errorf("failed to pack inner msg: %w", err)
    }

    execMsg := &authztypes.MsgExec{
        Grantee: c.address.String(),
        Msgs:    []*codectypes.Any{msgAny},
    }

    return c.broadcastTx(ctx, execMsg)
}

// ExecuteCreateLeaseViaGrant wraps a MsgCreateLease inside MsgExec.
func (c *AkashClient) ExecuteCreateLeaseViaGrant(
    ctx context.Context,
    granterAddr sdk.AccAddress,
    dseq uint64,
    gseq uint32,
    oseq uint32,
    provider string,
) (*sdk.TxResponse, error) {

    innerMsg := &marketv1beta4.MsgCreateLease{
        BidID: marketv1beta4.BidID{
            Owner:    granterAddr.String(),
            DSeq:     dseq,
            GSeq:     gseq,
            OSeq:     oseq,
            Provider: provider,
        },
    }

    msgAny, err := codectypes.NewAnyWithValue(innerMsg)
    if err != nil {
        return nil, fmt.Errorf("failed to pack inner msg: %w", err)
    }

    execMsg := &authztypes.MsgExec{
        Grantee: c.address.String(),
        Msgs:    []*codectypes.Any{msgAny},
    }

    return c.broadcastTx(ctx, execMsg)
}
```

### Fee Grant Operations

FeeGrants allow a granter to pay transaction fees on behalf of a grantee. Combined
with AuthZ, this enables a service to fully subsidize user deployments.

```go
import (
    feegrant "github.com/cosmos/cosmos-sdk/x/feegrant"
    feegranttypes "github.com/cosmos/cosmos-sdk/x/feegrant"
)

// GrantFeeAllowance creates a BasicAllowance fee grant allowing the grantee
// to spend up to the specified spend limit from the granter's account for gas fees,
// until the expiration time.
func (c *AkashClient) GrantFeeAllowance(
    ctx context.Context,
    granteeAddr sdk.AccAddress,
    spendLimit sdk.Coins,
    expiration *time.Time,
) (*sdk.TxResponse, error) {

    // BasicAllowance: simple spend limit with optional expiration
    allowance := &feegranttypes.BasicAllowance{
        SpendLimit: spendLimit, // e.g. sdk.NewCoins(sdk.NewCoin("uakt", sdk.NewInt(10000000)))
        Expiration: expiration, // nil means no expiration
    }

    // Wrap the allowance in an Any for the MsgGrantAllowance
    allowanceAny, err := codectypes.NewAnyWithValue(allowance)
    if err != nil {
        return nil, fmt.Errorf("failed to pack allowance: %w", err)
    }

    msg := &feegranttypes.MsgGrantAllowance{
        Granter:   c.address.String(),
        Grantee:   granteeAddr.String(),
        Allowance: allowanceAny,
    }

    return c.broadcastTx(ctx, msg)
}

// Example: Grant 10 AKT fee allowance with 30-day expiration
func (c *AkashClient) GrantFeeAllowanceExample(
    ctx context.Context,
    granteeAddr sdk.AccAddress,
) (*sdk.TxResponse, error) {

    spendLimit := sdk.NewCoins(sdk.NewCoin("uakt", sdk.NewInt(10000000)))
    expiration := time.Now().Add(30 * 24 * time.Hour)

    return c.GrantFeeAllowance(ctx, granteeAddr, spendLimit, &expiration)
}

// RevokeFeeAllowance removes a previously granted fee allowance.
func (c *AkashClient) RevokeFeeAllowance(
    ctx context.Context,
    granteeAddr sdk.AccAddress,
) (*sdk.TxResponse, error) {

    msg := &feegranttypes.MsgRevokeAllowance{
        Granter: c.address.String(),
        Grantee: granteeAddr.String(),
    }

    return c.broadcastTx(ctx, msg)
}
```

### Querying Grants

Query existing AuthZ grants to verify permissions are in place before executing
delegated operations.

```go
import (
    authzquery "github.com/cosmos/cosmos-sdk/x/authz/types"
)

// QueryAuthZGrants retrieves all grants from a granter to a grantee.
// Returns the list of active grants with their message types and expirations.
func (c *AkashClient) QueryAuthZGrants(
    ctx context.Context,
    granterAddr sdk.AccAddress,
    granteeAddr sdk.AccAddress,
) (*authzquery.QueryGrantsResponse, error) {

    queryClient := authzquery.NewQueryClient(c.clientCtx.GRPCClient)

    return queryClient.Grants(ctx, &authzquery.QueryGrantsRequest{
        Granter:    granterAddr.String(),
        Grantee:    granteeAddr.String(),
        MsgTypeUrl: "", // empty string returns all grants
    })
}

// CheckGrantValid verifies that a specific AuthZ grant exists and is not expired.
// Returns the grant if valid, or an error if missing/expired.
func (c *AkashClient) CheckGrantValid(
    ctx context.Context,
    granterAddr sdk.AccAddress,
    granteeAddr sdk.AccAddress,
    msgTypeURL string,
) error {

    queryClient := authzquery.NewQueryClient(c.clientCtx.GRPCClient)

    res, err := queryClient.Grants(ctx, &authzquery.QueryGrantsRequest{
        Granter:    granterAddr.String(),
        Grantee:    granteeAddr.String(),
        MsgTypeUrl: msgTypeURL,
    })
    if err != nil {
        return fmt.Errorf("failed to query grants: %w", err)
    }

    if len(res.Grants) == 0 {
        return fmt.Errorf("no grant found for %s", msgTypeURL)
    }

    // Check expiration
    grant := res.Grants[0]
    if grant.Expiration != nil && grant.Expiration.Before(time.Now()) {
        return fmt.Errorf("grant for %s expired at %s", msgTypeURL, grant.Expiration)
    }

    return nil
}

// QueryFeeGrantAllowance retrieves the current fee allowance granted to a grantee.
func (c *AkashClient) QueryFeeGrantAllowance(
    ctx context.Context,
    granterAddr sdk.AccAddress,
    granteeAddr sdk.AccAddress,
) (*feegranttypes.QueryAllowanceResponse, error) {

    queryClient := feegranttypes.NewQueryClient(c.clientCtx.GRPCClient)

    return queryClient.Allowance(ctx, &feegranttypes.QueryAllowanceRequest{
        Granter: granterAddr.String(),
        Grantee: granteeAddr.String(),
    })
}

// IsGrantValidForDeployment checks all required AuthZ grants for deployment operations.
func (c *AkashClient) IsGrantValidForDeployment(
    ctx context.Context,
    granterAddr sdk.AccAddress,
    granteeAddr sdk.AccAddress,
) error {

    requiredMsgTypes := []string{
        "/akash.deployment.v1beta3.MsgCreateDeployment",
        "/akash.deployment.v1beta3.MsgCloseDeployment",
        "/akash.market.v1beta4.MsgCreateLease",
    }

    for _, msgType := range requiredMsgTypes {
        if err := c.CheckGrantValid(ctx, granterAddr, granteeAddr, msgType); err != nil {
            return fmt.Errorf("missing grant for %s: %w", msgType, err)
        }
    }

    return nil
}
```

#### Combined AuthZ + FeeGrant Usage

```go
// Full delegated setup: grant permissions AND fund the grantee's gas fees
func (c *AkashClient) SetupDelegatedAccess(
    ctx context.Context,
    granteeAddr sdk.AccAddress,
    authzExpiration time.Time,
    feeSpendLimit sdk.Coins,
    feeExpiration *time.Time,
) error {

    // 1. Grant AuthZ permissions for deployment operations
    _, err := c.GrantDeploymentPermissions(ctx, granteeAddr, authzExpiration)
    if err != nil {
        return fmt.Errorf("failed to grant authz permissions: %w", err)
    }

    // 2. Grant fee allowance so grantee can submit txs paid by granter
    _, err = c.GrantFeeAllowance(ctx, granteeAddr, feeSpendLimit, feeExpiration)
    if err != nil {
        return fmt.Errorf("failed to grant fee allowance: %w", err)
    }

    return nil
}
```
