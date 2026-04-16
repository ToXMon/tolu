# Lunel - Deep-Dive Architecture Analysis

**Repository**: `github.com/lunel-dev/lunel`
**Date**: 2025-04-15
**Analyst**: Agent Zero Deep Research

---

## 1. Purpose

Lunel is an **AI-powered mobile IDE and cloud development platform** that lets users code on their phone (iOS/Android/Web) and execute on their local machine or in cloud sandboxes. It positions itself as a no-SSH, QR-code-paired remote development environment with a "dumb client" architecture where the mobile app is a rendering layer and all heavy lifting happens on the CLI running on the developer's machine.

Two deployment modes:
- **Lunel Connect**: Remote access to your own machine (current, shipping)
- **Lunel Cloud**: Secure cloud sandboxes (coming soon, with `sandman` Go binary)

---

## 2. Architecture / Tech Stack

### Component Map

```
┌──────────────┐     WebSocket (encrypted)      ┌──────────────┐
│   Mobile App  │◄──────────────────────────────►│  Proxy Relay  │
│  (Expo/RN)    │     via Manager + Proxy        │  (Bun WS)     │
└──────────────┘                                 └──────┬───────┘
      │                                                 │
      │  ┌──────────┐    QR Pairing     ┌──────────┐   │
      └──►│ Manager  │◄─────────────────►│   CLI    │◄──┘
          │ (Bun+SQL)│    Session Codes  │ (Node.js)│
          └──────────┘                   └────┬─────┘
                                             │
                                    ┌────────┼────────┐
                                    │        │        │
                               ┌────┴───┐ ┌──┴──┐ ┌──┴──────┐
                               │ PTY    │ │ AI  │ │ Local   │
                               │ (Rust) │ │Back.│ │ FS/Git  │
                               └────────┘ └─────┘ └─────────┘
```

### 2.1 App (`app/`) — Expo/React Native Mobile Client

| Aspect | Detail |
|--------|--------|
| Framework | Expo 54, React Native 0.81.5, React 19.1 |
| Routing | Expo Router 6.x (file-based) |
| Code Editor | CodeMirror 6 (20+ language modes) rendered in WebView |
| Terminal | Custom cell-grid renderer (Skia + Canvas), data from Rust PTY |
| Fonts | 16+ Google Fonts families (DM Mono, JetBrains Mono, Fira Code, etc.) |
| Navigation | Bottom tabs + drawer via React Navigation 7 |
| Crypto | `react-native-libsodium` for NaCl encryption |
| Networking | `react-native-tcp-socket` (forked) for direct TCP |
| Over-the-air | `@hot-updater/react-native` for OTA updates |
| UI Libraries | Lucide, Phosphor, Iconoir icons; Skia for rendering |

**Key app directories:**
- `contexts/` — React contexts: ConnectionContext (WebSocket management), EditorContext, SessionRegistry, ThemeContext, AppSettingsContext
- `hooks/` — useApi (FS/git/process/ports/monitor/HTTP), useAI (dual backend AI), useFileSystem, useGit, useTerminal
- `plugins/` — Plugin system with registry, GPI (Global Plugin Interface), core and extra plugins
- `lib/transport/` — V2 encrypted transport (mirrors CLI transport layer)
- `components/editor/` — CodeMirror 6 wrapper in WebView

### 2.2 CLI (`cli/`) — Node.js Bridge

| Aspect | Detail |
|--------|--------|
| Runtime | Node.js >=18, TypeScript, ESM |
| Version | 0.1.114 |
| Binary | `npx lunel-cli` → `dist/index.js` |
| Size | ~3,578 lines in main `index.ts` + AI modules |
| Transport | WebSocket via `ws` library, V2 encrypted protocol with libsodium |

**Message Router Namespaces (10 total):**

| Namespace | Actions | Purpose |
|-----------|---------|---------|
| `system` | capabilities, ping | Version, platform, hostname |
| `fs` | ls, stat, read, write, mkdir, rm, mv, grep, create | Full filesystem CRUD |
| `git` | status, stage, unstage, commit, log, commitDetails, diff, branches, checkout, deleteBranch, pull, push, discard | Complete git integration |
| `terminal` | spawn, write, resize, kill, scroll | PTY terminal sessions |
| `processes` | list, spawn, kill, getOutput, clearOutput | Process management |
| `ports` | list, isAvailable, kill | Port scanning/management |
| `monitor` | system, cpu, memory, disk, battery | System monitoring |
| `http` | request | HTTP proxy via fetch |
| `ai` | backends, prompt, createSession, listSessions, getSession, deleteSession, getMessages, abort, agents, providers, setAuth, command, revert, unrevert, share, permission, questionReply, questionReject | Dual-backend AI |
| `proxy` | connect, getState, trackPort, untrackPort | TCP tunnel forwarding |
| `editor` | open, close, rename, delete | File change tracking |

### 2.3 Manager (`manager/`) — Session Control Plane

| Aspect | Detail |
|--------|--------|
| Runtime | Bun, TypeScript |
| Database | `bun:sqlite` (SQLite) |
| Size | ~4,263 lines |
| Purpose | Session orchestration, QR code generation, proxy assignment, reattach tokens, rate limiting, audit logging |

**Key responsibilities:**
- QR code generation (`/v2/qr` endpoint)
- Session assembly (pairing CLI and app via WebSocket handshake)
- Password generation and validation (timing-safe comparison)
- Proxy URL assignment (`/v2/proxy`)
- Reattach/resume tokens with generation counters
- Session state machine: `pending → active → app_offline_grace/cli_offline_grace → ended/expired`
- Dual-channel architecture: control + data WebSocket per session
- Rate limiting per IP/subnet
- Admin JWT authentication
- Gateway health monitoring (heartbeats every 15s)
- VM heartbeat tracking for cloud tier (sandman integration)
- Backup gateway registration for HA

### 2.4 Proxy (`proxy/`) — WebSocket Relay

| Aspect | Detail |
|--------|--------|
| Runtime | Bun, TypeScript |
| Size | ~1,460 lines |
| Purpose | Encrypted WebSocket relay between CLI and app, TCP tunnel forwarding |

**Key responsibilities:**
- V2 encrypted session WebSocket (`/v2/ws/cli`, `/v2/ws/app`)
- Proxy tunnel WebSocket (`/v1/ws/proxy`) for TCP port forwarding
- Session management with 7-day TTL
- Reconnect grace periods (7-day app, 5-minute CLI)
- Manager authority cache with readonly fallback
- Gateway control events (metrics, session events, commands)
- Proxy tunnel queue management (2MB/512 frames max per direction)
- Half-close protocol (fin/rst control frames)

### 2.5 PTY (`pty/`) — Rust Terminal Engine

| Aspect | Detail |
|--------|--------|
| Language | Rust 2021 edition |
| Version | 0.2.0 |
| Binary | `lunel-pty` |
| Size | ~213 lines (main.rs) + session.rs + protocol.rs |
| Dependencies | `portable-pty` 0.8, `wezterm-term` (forked), `wezterm-surface` (forked), `serde`/`serde_json` |

**Architecture:**
- JSON-line protocol over stdin/stdout
- Commands: `spawn`, `write`, `resize`, `kill`, `scroll`
- Events: `spawned`, `state` (cell grid), `exit`, `error`
- Render thread at 24 FPS with condvar notification
- Screen buffer as cell grid: char + fg color + bg color + attrs per cell
- Dirty-flag based rendering (only sends changed frames)
- Scrollback buffer (1000 lines)
- True color support with color palette
- Pre-built binaries downloaded from GitHub releases for linux-x64, macos-arm64, windows-x64

### 2.6 Sandman (`sandman/`) — Cloud Sandbox (Planned)

| Aspect | Detail |
|--------|--------|
| Language | Go |
| Status | Referenced in Makefile but not yet integrated |
| Purpose | Cloud sandbox management for Lunel Cloud tier |

---

## 3. Core Features and Capabilities

### 3.1 File Explorer and Editor
- Full filesystem CRUD: ls, stat, read, write, mkdir, rm, mv, grep, create
- Binary detection (null byte + non-printable ratio heuristic)
- Base64 encoding for binary files
- Path safety: all operations sandboxed to `ROOT_DIR` via `resolveSafePath()` with symlink/canonicalization checks
- Editor file tracking with fs.watch for real-time change notifications
- Gitignore-aware grep search
- CodeMirror 6 editor with 20+ language modes (JS, TS, Python, Rust, Go, Java, C#, C++, PHP, SQL, HTML, CSS, JSON, YAML, XML, Markdown, Elixir)

### 3.2 Git Integration
- Complete git workflow: status, stage/unstage, commit, log, diff, branches, checkout, pull, push, discard
- Porcelain parsing for structured status
- Ahead/behind tracking
- Commit details with per-file diffs
- Branch create/delete

### 3.3 Terminal Emulator
- Real PTY sessions via Rust binary using wezterm terminal emulation
- 24 FPS render loop with dirty-flag optimization
- Full cell grid rendering (char, fg, bg, attrs)
- True color support
- Scrollback buffer (1000 lines)
- Cursor styles, bracketed paste, mouse modes
- Multiple concurrent terminal sessions
- Auto-download of pre-built PTY binaries per platform

### 3.4 Process Management
- Spawn arbitrary processes with stdio capture
- Real-time stdout/stderr streaming to app
- Process kill, output retrieval, output clearing
- CWD and environment variable support

### 3.5 Port Management
- Active port listing (lsof on Unix, netstat on Windows)
- Port availability checking
- Process kill by port
- Auto-discovery of dev server ports (scanned every 30s)
- TCP tunneling through proxy for port access from mobile

### 3.6 System Monitoring
- CPU usage per core (delta-based)
- Memory info (total, used, free, percent)
- Disk info per mount point
- Battery status (macOS: pmset, Linux: sysfs, Windows: WMI)

### 3.7 HTTP Proxy
- Arbitrary HTTP requests from app through CLI
- Configurable method, headers, body, timeout
- Response includes status, headers, body, timing

### 3.8 TCP Tunnel Proxy
- Bidirectional TCP tunneling through WebSocket
- App can access local dev servers (e.g., localhost:3000) remotely
- Half-close protocol with fin/rst control frames
- Tunnel queue management (2MB max)
- Automatic port tracking and discovery
- Dual-stack localhost (IPv4 + IPv6) fallback

### 3.9 Session Management
- QR code pairing (10-char codes, 7-day TTL)
- Encrypted WebSocket with NaCl (libsodium) key exchange
- Session persistence across CLI restarts (config file per root directory)
- Reattach with generation counters
- Auto-reconnect with exponential backoff + jitter
- Graceful shutdown on SIGINT/SIGTERM

---

## 4. LLM API Handling

### Architecture: Dual AI Backend System

Lunel supports **two simultaneous AI backends** that run independently and are selected per-request by the app:

```
┌─────────────────────────────────────────────────┐
│                   AiManager                      │
│  (routes by `backend` field in each request)     │
├─────────────────────┬───────────────────────────┤
│  OpenCode Provider   │    Codex Provider          │
│  (@opencode-ai/sdk)  │    (codex app-server)      │
│  SSE event stream    │    JSON-RPC 2.0 stdin/out  │
│  Local HTTP server   │    Spawned child process   │
└─────────────────────┴───────────────────────────┘
```

### 4.1 OpenCode Backend

- **SDK**: `@opencode-ai/sdk` v1.3.15
- **Architecture**: Creates a local HTTP server (`createOpencodeServer`) on `127.0.0.1:random_port`, then connects via `createOpencodeClient`
- **Authentication**: Auto-generated Basic auth credentials (random 32-byte password)
- **Communication**: HTTP REST API for commands + SSE event stream for real-time updates
- **Prompt delivery**: Fire-and-forget via `/session/{id}/prompt_async` endpoint
- **Event streaming**: Continuous SSE loop with exponential backoff (500ms initial, 30s cap, max 20 retries)
- **State reconciliation**: On reconnect, refreshes sessions, pending permissions, pending questions, and session statuses
- **Supported operations**: create/list/get/delete sessions, get messages, prompt, abort, agents, providers, setAuth, command, revert, unrevert, share, permission replies, question replies

### 4.2 Codex Backend

- **Architecture**: Spawns `codex app-server` as a child process
- **Communication**: JSON-RPC 2.0 over stdin/stdout (line-delimited)
- **Thread/Turn model**: Maps Codex's thread/turn model onto Lunel's session/message model
- **Prompt delivery**: `turn/start` RPC call with reasoning effort and speed options
- **Event handling**: Processes notifications (`thread/started`, `turn/started`, `turn/completed`, `turn/failed`) and server requests (`item/*/requestApproval`)
- **Permission model**: Translates Codex permission requests (command execution, file changes) into Lunel's permission system
- **Model support**: Fetches available models via internal API, presents as single "codex" provider
- **Limitations**: No auth configuration, command execution, revert/unrevert, or structured user input support yet
- **Streaming text**: Overlap-aware text joining for progressive rendering

### 4.3 LLM Provider Details

Both backends are **thin wrappers** — they don't call LLM APIs directly. Instead:
- **OpenCode** delegates to the OpenCode runtime which manages its own LLM connections (supports multiple providers)
- **Codex** delegates to the Codex runtime which manages its own model connections

The app sends `model: { providerID, modelID }` and `backend: "opencode" | "codex"` to select which backend and model to use. Auth is configured per-provider via `ai.setAuth(providerId, key)` for OpenCode.

### 4.4 AI Event Flow

```
App → CLI (ai.prompt) → OpenCode/Codex → LLM Provider
                                               ↓
App ← CLI (ai.event) ← SSE/JSON-RPC events ← streaming tokens
```

Events include: `session.updated`, `session.status`, `session.idle`, `session.error`, `session_gc`, `permission.updated`, `permission.replied`, `question.asked`, `question.replied`, `question.rejected`, `prompt_error`, `sse_dead`

---

## 5. File System Access

### 5.1 Remote Filesystem via CLI

The CLI provides a complete remote filesystem API sandboxed to the directory where `lunel-cli` is invoked:

- **`ROOT_DIR`**: Resolved from `process.cwd()` via `realpathSync`
- **Path safety**: `resolveSafePath()` canonicalizes paths, resolves symlinks, and enforces `startsWith(ROOT_DIR)` prefix check
- **Binary handling**: Auto-detects binary files (null byte + 30% non-printable threshold), returns base64-encoded content
- **Gitignore-aware search**: Recursive grep respects `.gitignore` at each directory level

### 5.2 Editor File Tracking

When the app opens a file in the editor:
1. CLI registers the file with `trackEditorFile(path)`
2. Sets up `fs.watch` on the parent directory
3. Monitors mtime and size changes
4. Emits `editor.fileChanged` / `editor.fileDeleted` events to app
5. Suppresses self-inflicted events (1.5s suppression window after CLI writes)
6. Supports file rename and delete tracking

### 5.3 File Operations Summary

| Operation | Details |
|-----------|---------|
| `ls` | Directory listing with file sizes and mtimes |
| `stat` | File metadata + binary detection (8KB sample) |
| `read` | Full file read, auto-detect encoding (utf8/base64) |
| `write` | File write with auto-mkdir parents, supports utf8 and base64 |
| `mkdir` | Directory creation (recursive by default) |
| `rm` | File/directory removal (explicit `recursive` flag) |
| `mv` | Rename/move with tracked file migration |
| `grep` | Regex search across directory tree, gitignore-aware, 100 result cap |
| `create` | Create empty file or directory |

---

## 6. Plugin/Extension System

### 6.1 App Plugin Architecture

Lunel has a sophisticated plugin system in the mobile app:

**Core Plugins** (always loaded, cannot be removed):
- `ai` — AI chat interface
- `browser` — Web browser (WebView)
- `editor` — CodeMirror code editor
- `terminal` — Terminal emulator

**Extra Plugins** (always loaded, configurable visibility):
- `explorer` — File explorer
- `git` — Git integration
- `processes` — Process manager
- `ports` — Port manager
- `http` — HTTP client
- `tools` — Developer tools (JSON/XML format, base64, URL encode, hash, date conversion)
- `monitor` — System monitor

### 6.2 Plugin Types

~~~typescript
interface PluginDefinition {
  id: string;
  name: string;
  type: 'core' | 'extra';
  icon: ComponentType<IconProps>;
  component: ComponentType<PluginPanelProps>;
  allowMultipleInstances?: boolean;  // tabs
  api?: () => PluginAPI;             // exposed via GPI
}
~~~

### 6.3 GPI (Global Plugin Interface)

A Proxy-based inter-plugin communication system that provides type-safe API calls:

~~~typescript
// Usage:
await gPI.editor.openFile('/src/app.tsx')
await gPI.terminal.runCommand('npm run build')
await gPI.git.commit('fix: resolve bug')
await gPI.ai.sendMessage('explain this code')
~~~

**Registered GPI APIs**: editor, terminal, git, browser, ai, explorer, processes, http, ports, tools, monitor

### 6.4 Plugin Registry

Singleton registry pattern with `register()`, `unregister()`, `get()`, `getAll()`, `getByType()` methods. Plugins are loaded at app startup via `plugins/load.ts`.

### 6.5 Workspace State

Tracks open plugin tabs, active tab, and bottom bar configuration:
- Bottom bar: 2 rows × 6 slots for extra plugin shortcuts
- Multiple instances allowed per extra plugin
- Core plugins always have one instance

---

## 7. Scheduling/Automation

### No Built-in Scheduling

Lunel does **not** have a built-in scheduling or automation system. There is:
- No cron-like functionality
- No task scheduling
- No workflow automation
- No webhook triggers

The `sandman` Go component (planned) may introduce sandbox lifecycle management for the cloud tier, including VM heartbeats tracked by the manager.

### Reconnection Automation

The CLI does implement automatic reconnection:
- Exponential backoff with jitter (250ms base, 30s cap)
- Reattach via manager `/v2/reattach/claim` endpoint
- Session password persistence across CLI restarts
- Port sync every 30 seconds

---

## 8. Notable Dependencies

### CLI Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@opencode-ai/sdk` | 1.3.15 | OpenCode AI runtime client/server |
| `ws` | ^8.18.0 | WebSocket client for gateway connection |
| `libsodium-wrappers` | ^0.7.15 | NaCl encryption for V2 transport |
| `shelljs` | ^0.10.0 | Cross-platform shell commands (grep) |
| `qrcode-terminal` | ^0.12.0 | Terminal QR code rendering |
| `ignore` | ^6.0.2 | `.gitignore` parsing for file search |

### App Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@codemirror/*` | 6.x | Code editor engine (20+ language modes) |
| `@xterm/xterm` | ^5.5.0 | Terminal rendering types (cell grid data model) |
| `@shopify/react-native-skia` | ^2.5.3 | GPU-accelerated canvas rendering for terminal |
| `react-native-libsodium` | ^1.7.0 | NaCl encryption (mirrors CLI) |
| `react-native-tcp-socket` | forked | Direct TCP connections (custom fork) |
| `react-native-webview` | 13.15.0 | WebView for CodeMirror editor |
| `@lobehub/icons` | ^5.0.1 / ^2.4.0 | LLM provider icons (OpenAI, Anthropic, etc.) |
| `expo-camera` | ~17.0.9 | QR code scanning |
| `@hot-updater/react-native` | latest | OTA updates without app store review |

### PTY Dependencies

| Crate | Purpose |
|-------|---------|
| `portable-pty` 0.8 | Cross-platform PTY (Unix ptys, Windows ConPTY) |
| `wezterm-term` | Terminal emulation (forked from github.com/sohzm/wezterm) |
| `wezterm-surface` | Screen buffer rendering (forked) |
| `serde`/`serde_json` | JSON line protocol serialization |

### Build & Runtime

| Tool | Purpose |
|------|---------|
| **Bun** | Manager + Proxy runtime (zero deps) |
| **Node.js** | CLI runtime (>=18) |
| **Rust** | PTY binary (edition 2021) |
| **Go** | Sandman (planned, not integrated) |
| **Expo** | Mobile app build system (v54) |

---

## 9. Integration Scenarios

### 9.1 Integration with a Multi-Provider LLM Agent Framework (pi-mono-like)

**What pi-mono is**: A TypeScript monorepo with 7 packages providing a universal AI SDK (`pi-ai`), agent framework (`pi-agent-core`), coding agent (`pi-coding-agent`), TUI (`pi-tui`), web UI (`pi-web-ui`), orchestration (`pi-mom`), and extensible tools (`pi-pods`).

**Integration opportunities:**

#### A. Replace AI Backend Layer

Lunel's `cli/src/ai/` module could be extended to support `pi-ai` as a third backend alongside OpenCode and Codex:

~~~
AiManager
  ├── opencode (OpenCode SDK)
  ├── codex (Codex JSON-RPC)
  └── pi-ai (pi-mono SDK)  ← NEW
      ├── Multi-provider support via pi-ai's universal interface
      ├── Tool calling via pi-agent-core's tool framework
      └── Agent orchestration via pi-mom
~~~

**Implementation path:**
1. Create `cli/src/ai/pi-ai.ts` implementing the `AIProvider` interface
2. Import `@anthropic-ai/sdk`, `@openai/sdk`, etc. through `pi-ai`'s provider abstraction
3. Map pi-ai's message format to Lunel's `MessageInfo` type
4. Use pi-agent-core's tool execution for file operations instead of Lunel's built-in handlers
5. Pipe events through Lunel's `AiEventEmitter`

**Benefits:**
- Direct multi-provider LLM access (Anthropic, OpenAI, Google, etc.) without OpenCode/Codex middlemen
- Tool calling with structured outputs
- Agent orchestration (multi-step, multi-agent workflows)
- Reuse pi-pods tools ecosystem

#### B. App-Side Agent UI

The app's AI plugin could render pi-agent-core's streaming responses:
- Use pi-web-ui's React components adapted for React Native
- Display tool execution steps, file diffs, terminal commands
- Support pi-mom's multi-agent conversations

#### C. Protocol Bridging

Lunel's encrypted V2 WebSocket transport could carry pi-ai protocol messages:
- Extend the `ai` namespace with pi-specific actions
- Support pi-agent-core's tool permission model alongside OpenCode's
- Stream pi-ai events through the existing SSE→emitter pipeline

### 9.2 Integration with a Coding Agent CLI (openclaude-like)

**What openclaude is**: A terminal-based coding agent with multi-provider LLM support, tool system (47+ tools), skills, tasks, voice input, and gRPC server mode.

**Integration opportunities:**

#### A. openclaude as Lunel's Terminal Agent

The most natural integration: run openclaude inside Lunel's terminal emulator.

- User opens terminal tab in Lunel app
- Runs `openclaude` inside the PTY
- Gets full coding agent experience on mobile via Lunel's terminal renderer

**Already works today** — no code changes needed. Lunel's PTY is a real terminal that runs any CLI tool.

#### B. openclaude as Lunel's AI Backend

More deeply, openclaude's gRPC server mode could become a third AI backend:

~~~
AiManager
  ├── opencode (OpenCode SDK)
  ├── codex (Codex JSON-RPC)
  └── openclaude (gRPC)  ← NEW
      ├── Spawn `openclaude --grpc`
      ├── Communicate via gRPC protocol
      └── Use openclaude's tool system for file editing
~~~

**Implementation path:**
1. Create `cli/src/ai/openclaude.ts` implementing `AIProvider`
2. Spawn openclaude's gRPC server as child process
3. Connect via gRPC client (use `@grpc/grpc-js`)
4. Map openclaude's conversation model to Lunel's session/message model
5. Forward tool execution events (file reads/writes, terminal commands) as AI events

**Benefits:**
- 47+ built-in tools accessible from mobile
- Voice input via openclaude's voice module (triggered from phone)
- Skills system for reusable task templates
- Multi-provider LLM support with smart routing

#### C. Shared File System Access

openclaude and Lunel share the same local filesystem:
- openclaude reads/writes files → Lunel's editor file tracking detects changes
- Lunel's editor writes → openclaude's file watcher detects changes
- Both operate on the same git repository
- Lunel's `fs` namespace API could be exposed as an MCP server for openclaude to use

#### D. Lunel as openclaude's Mobile Frontend

The deepest integration would make Lunel the mobile UI for openclaude:

~~~
App (Lunel)
  → CLI (WebSocket)
    → openclaude (gRPC)
      → LLM Provider
        ↓
      Tool Execution
        → File changes (reflected in Lunel editor)
        → Terminal commands (shown in Lunel terminal)
        → Git operations (shown in Lunel git panel)
~~~

The app's AI plugin would render:
- openclaude's markdown output with syntax highlighting
- Tool execution cards (file edits with diff view, terminal commands with output)
- Task progress tracking
- Cost tracking (openclaude has built-in cost tracker)

---

## 10. Security Architecture

### V2 Encrypted Transport

```
CLI                              Proxy                           App
  │                                 │                              │
  │── client_hello (pubkey) ───────►│── relay ────────────────────►│
  │                                 │                              │
  │◄─ server_hello (pubkey) ────────│◄── relay ───────────────────│
  │                                 │                              │
  │── client_key (nonce+box+auth) ─►│── relay ────────────────────►│
  │                                 │                              │
  │◄─ server_ready (auth) ─────────│◄── relay ───────────────────│
  │                                 │                              │
  │═══ encrypted binary frames ═════│═══ relay (opaque) ═══════════│
```

- **Key exchange**: NaCl Box (Curve25519-XSalsa20-Poly1305)
- **Session keys**: Derived from shared secret with separate TX/RX keys
- **Binary framing**: Magic bytes `0x4C 0x32` ("L2") + type byte + ciphertext
- **Protocol version**: `v: 1` in all messages
- **Gateway**: Never sees plaintext content (end-to-end encrypted between CLI and app)

### Path Safety

All filesystem operations enforce:
- Lexical path resolution (`path.resolve(ROOT_DIR, requestedPath)`)
- Canonical path verification (`realpathSync` to resolve symlinks)
- Prefix check against canonicalized `ROOT_DIR`
- Error code `EACCES` for violations

### Session Security

- Session passwords: 67-character random strings (256 bytes of entropy)
- QR codes: 10-character alphanumeric codes
- Timing-safe comparison for password validation
- 7-day TTL on codes and reconnect grace periods
- Password revocation via manager `/v2/revoke`
- JWT admin tokens with 12-hour expiry

---

## 11. Key Design Decisions

### 11.1 "Dumb Client" Architecture

The app is intentionally a rendering layer — all business logic runs in the CLI on the developer's machine. This means:
- App can be lightweight and fast
- All data stays on the developer's machine
- App updates don't change functionality
- Works offline if app and CLI are on same network (future)

### 11.2 Dual AI Backend

Running OpenCode and Codex simultaneously provides:
- User choice between different AI coding assistants
- Graceful degradation if one fails to init
- Different strengths: OpenCode for general coding, Codex for deep reasoning

### 11.3 Rust PTY

Using a separate Rust binary for terminal emulation:
- Real PTY support (not xterm.js emulation)
- High-performance cell grid rendering
- No Node.js event loop blocking
- Portable across platforms (via `portable-pty`)

### 11.4 Encrypted Relay

End-to-end encryption between CLI and app:
- Gateway/proxy never sees plaintext
- Even if proxy is compromised, data is safe
- NaCl Box provides authenticated encryption

---

## 12. File Inventory

### Files Read for This Analysis

| File | Lines | Purpose |
|------|-------|---------|
| `README.md` | 96 | Project overview |
| `Makefile` | 120 | Build targets |
| `app/package.json` | ~170 | App dependencies |
| `cli/package.json` | ~35 | CLI dependencies |
| `manager/package.json` | ~12 | Manager config |
| `proxy/package.json` | ~12 | Proxy config |
| `pty/Cargo.toml` | ~20 | Rust dependencies |
| `cli/src/index.ts` | 3,578 | CLI main (full read) |
| `cli/src/ai/index.ts` | 144 | AI manager (full read) |
| `cli/src/ai/interface.ts` | 116 | AI provider interface (full read) |
| `cli/src/ai/opencode.ts` | 695 | OpenCode provider (full read) |
| `cli/src/ai/codex.ts` | 1,971 | Codex provider (partial, key sections) |
| `cli/src/transport/protocol.ts` | 163 | Protocol types (full read) |
| `cli/src/transport/v2.ts` | 497 | V2 transport (partial) |
| `proxy/src/index.ts` | 1,460 | Proxy server (partial) |
| `manager/src/index.ts` | 4,263 | Manager server (partial) |
| `pty/src/main.rs` | 213 | PTY main (full read) |
| `pty/src/protocol.rs` | ~70 | PTY protocol (full read) |
| `pty/src/session.rs` | 100+ | Terminal session (partial) |
| `app/plugins/types.ts` | ~80 | Plugin types (full read) |
| `app/plugins/load.ts` | ~10 | Plugin loader (full read) |
| `app/plugins/registry.ts` | ~80 | Plugin registry (full read) |
| `app/plugins/gpi.ts` | ~200 | GPI interface (full read) |
| `app/hooks/useAI.ts` | 60+ | AI hook (partial) |
| `app/hooks/useApi.ts` | 60+ | API hook (partial) |

---

## 13. Summary

Lunel is a well-architected mobile IDE with clean separation of concerns across five components. The "dumb client" approach keeps the app lightweight while the CLI does all the heavy lifting. The dual AI backend system (OpenCode + Codex) is extensible — adding a third backend implementing the `AIProvider` interface is straightforward. The plugin system with GPI provides a clean way for features to interoperate. The end-to-end encrypted transport via NaCl ensures security even through untrusted proxies.

The main integration vectors for external agent frameworks are:
1. **AI Backend**: Implement `AIProvider` interface to add new LLM providers
2. **Terminal**: Any CLI tool works out-of-the-box in the PTY
3. **File System**: Shared filesystem access with real-time change notifications
4. **Protocol**: Extensible namespace-based message protocol for new capabilities
