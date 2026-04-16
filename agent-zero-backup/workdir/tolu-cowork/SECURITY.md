# Tolu Cowork — Security Architecture

**Version**: 0.1.0  
**Status**: Implementation Complete  
**Last Updated**: 2025-04-15

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Sandboxing Layer](#2-sandboxing-layer)
3. [Security Middleware](#3-security-middleware)
4. [Network Security](#4-network-security)
5. [Remote Access Security](#5-remote-access-security)
6. [Tool Security](#6-tool-security)
7. [Data Protection](#7-data-protection)
8. [Threat Model](#8-threat-model)
9. [Configuration Guide](#9-configuration-guide)
10. [Deployment Security](#10-deployment-security)

---

## 1. Architecture Overview

Tolu Cowork employs a defense-in-depth security model with five distinct layers:

```
┌─────────────────────────────────────────────────────────┐
│                    Remote Access Layer                    │
│         QR Pairing · Session Tokens · Device Trust        │
├─────────────────────────────────────────────────────────┤
│                    Network Security Layer                  │
│      E2E Encryption · TLS · mTLS · Cert Pinning          │
├─────────────────────────────────────────────────────────┤
│                   Security Middleware                      │
│   API Key Mgmt · Rate Limiting · Audit · Permissions     │
├─────────────────────────────────────────────────────────┤
│                     Sandboxing Layer                       │
│       Docker Isolation · Path Restrictions · Host         │
├─────────────────────────────────────────────────────────┤
│                      Tool Security                         │
│    Command Filtering · Path Validation · Resource Limits   │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

- **Least Privilege**: Tools and agents operate with minimum required permissions
- **Defense in Depth**: Multiple independent security layers; compromise of one does not compromise all
- **Secure by Default**: Default configuration prioritizes safety over convenience
- **Audit Everything**: All tool executions, API calls, and access decisions are logged
- **Fail Closed**: On error or ambiguity, deny access rather than permit

---

## 2. Sandboxing Layer

**Location**: `tolu-cowork-core/src/sandbox/`

### Three Isolation Levels

| Level | Isolation | Use Case | Overhead |
|-------|-----------|----------|----------|
| `none` | None (host execution) | Trusted environments only | None |
| `path-only` | Filesystem path restrictions | Default for development | Minimal |
| `docker` | Full container isolation | Production, untrusted code | Medium |

### Docker Sandbox

Adapted from pi-mono's `pi-mom` Docker executor pattern:

- **Container Lifecycle**: Dedicated container per sandbox instance, created on demand
- **Resource Limits**: CPU shares (`--cpus`), memory (`--memory`), process count (`--pids-limit`)
- **Timeout Enforcement**: Process tree kill on timeout, followed by `docker stop`
- **Buffer Limits**: 10MB per stdout/stderr stream, truncation not error
- **Workspace Mount**: Project directory mounted read-write at `/workspace`
- **Execution**: Commands run via `docker exec` through `child_process.spawn` (no dockerode dependency)

### Path Sandbox

Adapted from lunel's CLI filesystem patterns:

- **Allowed Roots**: Whitelist of directories the agent can access
- **Path Traversal Prevention**: `path.resolve()` + `startsWith()` check on normalized paths
- **Default Blacklist**: `/etc/passwd`, `/etc/shadow`, `/root/.ssh`, `~/.gnupg`, `/proc`, `/sys`
- **Host Execution**: Commands run directly on host but file operations validated first

### SandboxManager API

```typescript
const manager = new SandboxManager();
const sandbox = await manager.createSandbox({
  level: 'docker',
  docker: { image: 'ubuntu:22.04', containerName: 'my-sandbox', workspaceMount: '/project' },
  resourceLimits: { cpuShares: 512, memoryMB: 512, timeoutSeconds: 60 },
});
const result = await sandbox.execute('npm test');
await manager.destroySandbox(sandbox.getInfo().id);
```

---

## 3. Security Middleware

**Location**: `tolu-cowork-core/src/security/`

### API Key Management

- **Encryption at Rest**: AES-256-GCM with scrypt-derived key from master encryption key
- **Master Key Source**: `TOLU_ENCRYPTION_KEY` env var or auto-generated `~/.tolu/master.key`
- **Key Rotation**: In-place rotation with old key marked as rotated
- **Key Hashing**: SHA-256 hash stored for integrity verification (never stores raw key)
- **Environment Injection**: `injectToEnv()` returns provider-specific env var mapping without exposing raw key

### Rate Limiting

- **Algorithm**: Sliding window with burst allowance
- **Default Policies**:
  - LLM providers: 60 requests/minute
  - Tool execution: 120 requests/minute
  - Internal operations: 10,000 requests/minute
- **Per-Provider**: Each provider gets independent rate limit tracking
- **Response Headers**: Returns `allowed`, `remaining`, and `resetAt` metadata

### Request/Response Sanitization

Automatic pattern removal from all logged/forwarded data:

| Pattern | Example | Replacement |
|---------|---------|-------------|
| OpenAI keys | `sk-proj-abc123...` | `[REDACTED_API_KEY]` |
| Generic API keys | `key-abc123...` | `[REDACTED_API_KEY]` |
| Bearer tokens | `Bearer eyJ...` | `[REDACTED_TOKEN]` |
| Private IPs | `192.168.x.x`, `10.x.x.x` | `[REDACTED_IP]` |
| Home paths | `/home/user/`, `/Users/name/` | `[REDACTED_PATH]` |

### Audit Logging

- **Format**: JSONL (one JSON object per line)
- **Location**: `~/.tolu/audit.log`
- **Fields**: id (UUID), timestamp (ISO 8601), actor, action, resource, result, details, sandboxLevel, sourceIp
- **Retention**: `prune(maxAgeMs)` for age-based cleanup
- **Export**: JSON or CSV format for compliance reporting
- **Sanitization**: All logged data passes through the sanitizer before writing

### Permission System

Least-privilege defaults for tool execution:

| Tool Category | Allowed Sandbox Levels |
|--------------|----------------------|
| Read-only (read, list, find, grep, glob) | none, path-only, docker |
| Destructive (bash, write, edit) | path-only, docker |
| Network (web_search, web_fetch) | docker |
| MCP (mcp_call) | docker |

Configuration persists at `~/.tolu/permissions.json`.

---

## 4. Network Security

**Location**: `tolu-cowork-core/src/network/`

### End-to-End Encryption

Adapted from lunel's NaCl-based relay encryption pattern:

```
Client                              Server
  │                                    │
  │──── client_hello (publicKey) ─────►│
  │◄─── server_hello (publicKey) ──────│
  │                                    │
  │  Derive shared secret:              │
  │  nacl.box.before(remotePub,        │
  │                   localPriv)        │
  │                                    │
  │  Derive session keys via HKDF:      │
  │  rx = HKDF(shared, 'tolu-cowork-rx')│
  │  tx = HKDF(shared, 'tolu-cowork-tx')│
  │                                    │
  │◄════ nacl.secretbox(tx/rx) ═══════►│
```

- **Key Exchange**: NaCl box (Curve25519-XSalsa20-Poly1305)
- **Symmetric Encryption**: nacl.secretbox (XSalsa20-Poly1305)
- **Key Derivation**: HKDF-SHA256 with role-specific info strings
- **Session TTL**: 1 hour maximum, automatic cleanup
- **Key Zeroization**: Session keys zeroed on destruction

### TLS Configuration

- **Minimum Version**: TLS 1.3 (configurable to TLS 1.2)
- **Certificate Loading**: File-based cert/key/ca loading with validation
- **Self-Signed Certs**: Development-only certificate generation via manual DER/ASN.1 encoding
- **Certificate Validation**: Expiry, issuer, and subject checking

### mTLS Support

For enterprise deployments:

- **Client Certificate Verification**: Required client CA certificate
- **Mutual Authentication**: Both client and server present certificates
- **Certificate Pinning**: SHA-256 hash validation against known pins

### WebSocket Security

- **Origin Whitelist**: Default `http://localhost:*`, configurable
- **Frame Size Limit**: 1MB maximum (configurable)
- **Rate Limiting**: 100 messages/second per connection
- **Keepalive**: 30-second ping interval with configurable timeout

### Certificate Pinning (Phone Dispatch)

- **Global Pins**: SHA-256 hashes of expected certificate public keys
- **Per-Device Pins**: Device-specific pin sets for phone dispatch connections
- **Enforcement Mode**: Configurable — fail-closed or log-only

---

## 5. Remote Access Security

**Location**: `tolu-cowork-core/src/remote/`

### QR Pairing

Adapted from lunel's QR pairing with enhanced security:

- **Code Format**: 10-character alphanumeric (no ambiguous chars: 0/O/1/l/I)
- **Code TTL**: 5 minutes (reduced from lunel's 1 week for initial pairing)
- **Single Use**: Codes are consumed after successful pairing
- **Rate Limiting**: 5 pairing attempts per IP per hour

```
┌──────────┐                    ┌──────────┐
│   Phone   │                    │  Desktop  │
│  (App)    │                    │  (CLI)    │
└─────┬─────┘                    └─────┬─────┘
      │                                │
      │  Scan QR code (10 chars)       │
      │───────────────────────────────►│
      │                                │
      │  Validate code (5min TTL)      │
      │◄───────────────────────────────│
      │                                │
      │  Device info + fingerprint     │
      │───────────────────────────────►│
      │                                │
      │  Session token (64-byte hex)   │
      │◄───────────────────────────────│
      │                                │
```

### Session Management

- **Token Format**: 64-byte hex string from `crypto.randomBytes(64)`
- **Token TTL**: 24 hours default
- **Token Rotation**: Every 1 hour (configurable); new token issued, old invalidated
- **Revocation**: Per-token and per-device (all sessions) revocation
- **Cleanup**: Expired sessions removed on `cleanupExpiredSessions()`

### Device Trust Protocol

Three-level trust escalation:

| Level | How Earned | Permissions |
|-------|-----------|-------------|
| `untrusted` | Default | No access |
| `paired` | Successful QR pairing | Session-scoped access |
| `trusted` | 7 days since pairing + 5 sessions | Persistent access, elevated permissions |

Challenge-response authentication using Ed25519 signatures:

```
Server                              Device
  │                                    │
  │──── challenge (32 random bytes) ──►│
  │                                    │
  │  Device signs with Ed25519 key     │
  │                                    │
  │◄─── response (signature) ──────────│
  │                                    │
  │  Verify with stored public key     │
  │                                    │
```

### Secure Credential Storage

- **Encryption**: AES-256-GCM with scrypt-derived key
- **Key Derivation**: `scrypt(passphrase, salt, 16384, 8, 1, 32)`
- **Store Format**: `{ salt, iv, authTag, data }` — all base64-encoded
- **Location**: `~/.tolu/credentials.json`
- **Passphrase Rotation**: Re-encrypts all credentials with new passphrase

---

## 6. Tool Security

**Location**: `tolu-cowork-core/src/tools/`

### Command Blocking (BashTool)

The following dangerous commands are blocked regardless of sandbox level:

| Pattern | Reason |
|---------|--------|
| `rm -rf /` | Recursive root deletion |
| `rm -rf /*` | Recursive root deletion variant |
| `mkfs` | Filesystem formatting |
| `dd if=/dev/zero` | Disk wiping |
| `:(){ ::& };:` | Fork bomb |
| `chmod 000 /` | Permission destruction |
| `chown` on `/` | Ownership attacks |

### Resource Limits

- **Output Buffer**: 10MB per stdout/stderr stream (per pi-mono pattern)
- **Process Timeout**: Configurable per-command, default 120 seconds
- **AbortSignal**: All tools respect abort signals for graceful cancellation
- **Max Processes**: Docker sandbox limits via `--pids-limit`

### Path Validation

All file tools validate paths through the sandbox:

1. `path.resolve()` to normalize
2. Check against blacklist (`/etc/passwd`, `/root/.ssh`, etc.)
3. Verify within allowed roots (path sandbox)
4. Check read/write/execute permissions via SandboxManager

---

## 7. Data Protection

### At Rest

| Data | Encryption | Location |
|------|-----------|----------|
| API keys | AES-256-GCM | `~/.tolu/keys.json` |
| Device credentials | AES-256-GCM | `~/.tolu/credentials.json` |
| Master encryption key | Raw binary | `~/.tolu/master.key` (or env var) |
| Permissions | Plain JSON | `~/.tolu/permissions.json` |
| Audit log | Plain JSONL (sanitized) | `~/.tolu/audit.log` |

### In Transit

| Channel | Encryption |
|---------|-----------|
| gRPC (core ↔ clients) | TLS 1.3 or mTLS |
| WebSocket (remote) | TLS + E2E NaCl |
| LLM API calls | HTTPS (provider TLS) |

### In Memory

- Session keys zeroed on destruction
- API keys decrypted only when needed, never cached long-term
- Streaming buffers truncated at 10MB

---

## 8. Threat Model

### Threats Mitigated

| Threat | Mitigation |
|--------|-----------|
| **Malicious tool execution** | Docker sandbox isolation, command blocking, path restrictions |
| **API key leakage** | AES-256-GCM at rest, sanitization in logs, never returned by API |
| **Man-in-the-middle** | E2E encryption, TLS 1.3, certificate pinning |
| **Unauthorized remote access** | QR pairing, device trust protocol, session token rotation |
| **Resource exhaustion** | Rate limiting, Docker resource caps, output buffer limits |
| **Path traversal** | `path.resolve()` + blacklist + sandbox restrictions |
| **Privilege escalation** | `no-new-privileges` Docker flag, non-root user in container |
| **Session hijacking** | 64-byte tokens, 1-hour rotation, revocation support |

### Known Limitations

| Limitation | Mitigation |
|-----------|-----------|
| Single-process rate limiting | Redis integration planned for multi-instance |
| In-memory session store | Redis fallback for persistence across restarts |
| No RBAC | Permission system is tool-level only |
| Self-signed cert generation | Development-only; production must use proper CA |
| MCP transport stubbed | MCP security will follow same patterns when implemented |

---

## 9. Configuration Guide

### Minimum Security Config

```json
{
  "sandbox": { "level": "docker" },
  "security": {
    "auditLogging": true,
    "rateLimiting": true,
    "encryptionKey": "${TOLU_ENCRYPTION_KEY}"
  },
  "agent": {
    "maxTurns": 50,
    "toolExecution": "parallel"
  }
}
```

### Environment Variable Overrides

| Variable | Overrides | Required |
|----------|-----------|----------|
| `TOLU_API_KEY` | `provider.apiKey` | Yes |
| `TOLU_BASE_URL` | `provider.baseUrl` | No |
| `TOLU_MODEL` | `provider.model` | No |
| `TOLU_SANDBOX_LEVEL` | `sandbox.level` | No |
| `TOLU_ENCRYPTION_KEY` | `security.encryptionKey` | Recommended |
| `TOLU_LOG_LEVEL` | Logging verbosity | No |

---

## 10. Deployment Security

### Docker Compose

The `docker-compose.yml` provides:

- **Network Isolation**: `tolu-internal` network (no external access) for Redis/PostgreSQL; `tolu-external` for core service ports
- **Resource Limits**: CPU and memory caps on all services
- **Read-Only Filesystem**: Core service runs with read-only root filesystem, tmpfs for /tmp
- **No New Privileges**: `security_opt: no-new-privileges:true` on all containers
- **Non-Root User**: Core service runs as `tolu` user (not root)
- **Health Checks**: All services have health check endpoints
- **Sandbox Isolation**: Dedicated sandbox container with resource limits and pids-limit

### Secrets Management

1. **Never commit secrets**: Use `.env` file (gitignored) or environment variables
2. **Master encryption key**: Set `TOLU_ENCRYPTION_KEY` in production; auto-generated key is for development only
3. **Database passwords**: Change default passwords in `.env`
4. **Redis password**: Set `TOLU_REDIS_PASSWORD` to a strong value
5. **TLS certificates**: Mount certificate files, don't bake into image

### Production Checklist

- [ ] Set `TOLU_API_KEY` to your provider key
- [ ] Set `TOLU_ENCRYPTION_KEY` to a strong random value (32+ bytes)
- [ ] Change all default passwords in `.env`
- [ ] Set `sandbox.level` to `docker` in production
- [ ] Enable TLS with valid certificates (not self-signed)
- [ ] Set `TOLU_LOG_LEVEL` to `warn` or `error` in production
- [ ] Configure origin whitelist for WebSocket connections
- [ ] Set up certificate pinning for phone dispatch
- [ ] Review and customize tool permission levels
- [ ] Set up audit log retention and archival
- [ ] Configure Redis persistence for session data
- [ ] Review resource limits for your deployment size

---

## Module Reference

| Module | Location | Key Exports |
|--------|----------|-------------|
| Sandboxing | `src/sandbox/` | `SandboxManager`, `SandboxLevel`, `SandboxInstance` |
| Security | `src/security/` | `ApiKeyManager`, `RateLimiter`, `AuditLogger`, `PermissionSystem`, `RequestResponseSanitizer` |
| Network | `src/network/` | `E2EEncryption`, `TLSConfigurator`, `WebSocketSecurity`, `CertificatePinning` |
| Remote | `src/remote/` | `QRPairingManager`, `SessionManager`, `DeviceTrustManager`, `SecureCredentialStore` |
| Agent | `src/agent/` | `ToluAgent`, `AgentSession`, `ToolExecutor` |
| Tools | `src/tools/` | `ToluToolDefinition`, `ToolLoader`, `BashTool`, `FileTools` |
| Services | `src/services/` | `SkillsService`, `ProjectsService`, `SchedulerService`, `SubAgentsService` |
| Config | `src/config/` | `ConfigLoader`, `ToluConfigSchema` |
| Utils | `src/utils/` | `Logger`, stream helpers, formatters |

---

*This document covers the security architecture as implemented in Tolu Cowork v0.1.0. For questions or security concerns, open an issue at github.com/ToXMon/tolu.*
