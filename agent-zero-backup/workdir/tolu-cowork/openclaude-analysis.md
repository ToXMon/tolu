# OpenClaude - Deep-Dive Architecture Analysis

**Repository**: `github.com/Gitlawb/openclaude`
**Version**: 0.3.0
**Date**: 2025-04-15
**Analyst**: Agent Zero Deep Research

---

## 1. Purpose

OpenClaude is an **open-source, multi-provider coding-agent CLI** that lets developers use any LLM backend (OpenAI, Gemini, DeepSeek, Ollama, Anthropic, Codex, Bedrock, Vertex, etc.) with a single terminal-first workflow. It provides tool-driven coding workflows with bash execution, file editing, grep/glob, agent delegation, task management, MCP (Model Context Protocol), slash commands, skills, voice input, and streaming output.

Key differentiators:
- Provider-agnostic: works with 200+ models across cloud and local backends
- Agent routing: different agents can use different models for cost/quality optimization
- Headless gRPC server mode for integration into other applications
- Voice input via native audio capture + WebSocket STT
- Vim mode, skills system, plugin architecture, and extensive slash commands

---

## 2. Architecture / Tech Stack

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        User Interface                         │
│  REPL.tsx (Ink/React TUI) │ gRPC Server │ VS Code Extension  │
└─────────────┬────────────────────────┬───────────────┬───────┘
              │                        │               │
┌─────────────▼────────────────────────▼───────────────▼───────┐
│                      QueryEngine.ts                           │
│         (async generator, tool loop orchestration)            │
├──────────────────────────────────────────────────────────────┤
│                      Tool Registry                            │
│  BashTool, FileEditTool, FileReadTool, FileWriteTool,         │
│  GrepTool, GlobTool, AgentTool, MCPTool, WebSearchTool,       │
│  WebFetchTool, SkillTool, WorkflowTool, + 30 more tools       │
├──────────────────────────────────────────────────────────────┤
│                    Services Layer                              │
│  api/ (multi-provider) │ mcp/ │ plugins/ │ compact/ │ voice   │
│  skills/ │ tasks/ │ tools/ │ cost-tracker │ settingsSync        │
├──────────────────────────────────────────────────────────────┤
│                    Context System                              │
│  System prompt │ CLAUDE.md │ git status │ session memory      │
├──────────────────────────────────────────────────────────────┤
│                    Provider Layer                              │
│  Anthropic │ OpenAI-compat │ Gemini │ Codex │ Ollama │ Bedrock│
│  Vertex │ Foundry │ Atomic Chat │ GitHub Models               │
└──────────────────────────────────────────────────────────────┘
```

### 2.1 Entry Point (`src/main.tsx` — 4668 lines)

The monolithic entry point handles:
- CLI argument parsing (commander.js)
- Provider initialization and configuration
- Session management (new vs resume)
- TUI rendering (Ink/React)
- Query dispatch pipeline
- Tool execution orchestration
- Permission system
- Cost tracking hooks
- Voice mode activation
- gRPC server startup

### 2.2 Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Language | TypeScript (ESM), Bun build |
| TUI | React 19 + Ink (react-reconciler) |
| CLI | Commander.js 12 |
| LLM SDK | @anthropic-ai/sdk 0.81, @anthropic-ai/bedrock-sdk, @anthropic-ai/vertex-sdk, @anthropic-ai/foundry-sdk |
| OpenAI Compat | Custom openaiShim.ts (Anthropic-to-OpenAI adapter) |
| gRPC | @grpc/grpc-js + @grpc/proto-loader |
| MCP | @modelcontextprotocol/sdk 1.29 |
| Search | duck-duck-scrape, @mendable/firecrawl-js |
| Voice | Native audio + WebSocket STT |
| File Watching | chokidar 4 |
| Image Processing | sharp |
| Schema Validation | zod 3.25, ajv 8 |
| Markdown | marked 15, turndown (HTML→MD) |
| Terminal | xss (sanitization), cli-highlight, ansi-tokenize |
| Observability | OpenTelemetry (traces + logs + metrics) |
| Testing | Bun test |

### 2.3 Source Directory Structure

```
src/
├── main.tsx              # 4668-line entry point
├── Tool.ts               # Tool interface (802 lines, ~40 methods)
├── tools.ts              # Tool registry (combines built-in + MCP)
├── tools/                # 47 tool implementations
│   ├── BashTool/         # Shell execution with sandboxing
│   ├── FileEditTool/     # Diff-based file editing
│   ├── FileReadTool/     # File reading with line ranges
│   ├── FileWriteTool/    # File creation/overwrite
│   ├── GrepTool/         # Regex search (ripgrep)
│   ├── GlobTool/         # File globbing (picomatch)
│   ├── AgentTool/        # Sub-agent delegation
│   ├── MCPTool/          # MCP server passthrough
│   ├── WebSearchTool/    # Web search (DDG/Firecrawl)
│   ├── WebFetchTool/     # HTTP fetch + HTML→MD
│   ├── SkillTool/        # Skill execution
│   ├── WorkflowTool/     # Multi-step workflows
│   ├── TaskCreateTool/   # Background task creation
│   ├── LSPTool/          # Language Server Protocol
│   ├── MonitorTool/      # System monitoring
│   ├── REPLTool/         # Embedded REPL
│   ├── ConfigTool/       # Configuration management
│   ├── TodoWriteTool/    # Todo list management
│   ├── TeamCreateTool/   # Team/teammate creation
│   └── ... (27 more tool dirs)
├── QueryEngine.ts        # Query lifecycle (async generator)
├── Task.ts / tasks.ts    # Background task system
├── tasks/                # Task implementations
│   ├── LocalAgentTask/   # Local sub-agent
│   ├── LocalShellTask/   # Local shell execution
│   ├── RemoteAgentTask/  # Remote agent (API-based)
│   ├── DreamTask/        # Background dreaming
│   ├── InProcessTeammateTask/  # Teammate in same process
│   └── MonitorMcpTask/   # MCP server monitoring
├── commands.ts           # 70+ slash commands
├── context.ts            # LLM context management
├── cost-tracker.ts       # Token/cost tracking
├── setup.ts              # Environment bootstrap
├── services/
│   ├── api/              # Multi-provider API layer (40+ files)
│   ├── mcp/              # Model Context Protocol (20+ files)
│   ├── plugins/          # Plugin management
│   ├── compact/          # Context compaction
│   ├── tools/            # StreamingToolExecutor
│   ├── voice.ts          # Voice input system
│   ├── voiceStreamSTT.ts # WebSocket STT
│   ├── skills/           # (top-level, not here)
│   ├── settingsSync/     # Cross-device sync
│   └── ... (24 subdirs)
├── skills/
│   ├── bundled/          # 13+ bundled skills
│   └── bundledSkills.ts  # Lazy extraction + registry
├── server/               # gRPC server
│   ├── types.ts
│   ├── createDirectConnectSession.ts
│   └── directConnectManager.ts
├── proto/                # gRPC protocol definition
│   └── agent.proto
├── screens/              # TUI screens
│   ├── REPL.tsx          # Main interactive UI
│   ├── Doctor.tsx        # System diagnostics
│   └── ResumeConversation.tsx
├── state/                # Reactive state management
│   ├── AppState.tsx      # React context
│   ├── AppStateStore.ts  # State type definitions
│   └── store.ts          # Generic Store<T>
├── vim/                  # Vim emulation (5 modules)
├── voice/                # Voice mode toggle
└── utils/                # 350+ utility files
```

---

## 3. Core Features and Capabilities

### 3.1 Multi-Provider LLM Support

OpenClaude supports 9+ provider backends:

| Provider | Auth Method | Transport |
|----------|-------------|-----------|
| Anthropic Claude | API key | @anthropic-ai/sdk |
| OpenAI-compatible | API key + base URL | Custom openaiShim |
| Gemini | API key / ADC / OAuth | google-auth-library |
| Codex | OAuth / secure storage | codexShim |
| Codex OAuth | Browser sign-in | codexOAuth |
| Ollama | None (local) | OpenAI-compatible |
| Bedrock | AWS credentials | @anthropic-ai/bedrock-sdk |
| Vertex | GCP credentials | @anthropic-ai/vertex-sdk |
| Foundry | API key | @anthropic-ai/foundry-sdk |
| Atomic Chat | Local | Apple Silicon |
| GitHub Models | OAuth | /onboard-github |

**Agent Routing**: Different agents can use different models. Configured in `~/.claude/settings.json` with `agentModels` and `agentRouting` keys.

**Provider Profiles**: Saved to `.openclaude-profile.json` for quick switching via `/provider` command.

### 3.2 Tool System (47+ Tools)

Tools implement the `Tool` interface (~40 methods) defined in `src/Tool.ts`:

**Core Tools:**

| Tool | Purpose | Key Features |
|------|---------|-------------|
| BashTool | Shell command execution | Sandboxing, background promotion, timeout, working directory |
| FileReadTool | Read file contents | Line ranges, binary detection, syntax highlighting |
| FileEditTool | Edit files via diff | Diff computation, concurrent edit protection, undo support |
| FileWriteTool | Create/overwrite files | Auto-mkdir, encoding support |
| GrepTool | Regex search | ripgrep-based, file filtering, context lines |
| GlobTool | File pattern matching | picomatch-based, recursive |
| AgentTool | Delegate to sub-agents | 3 isolation modes: worktree, remote, fork. Agent definitions from `.claude/agents/` |
| MCPTool | MCP server passthrough | Wraps any MCP tool as native tool |
| WebSearchTool | Web search | DuckDuckGo (free) or Firecrawl (paid) |
| WebFetchTool | HTTP fetch + HTML→MD | Raw HTTP or Firecrawl scrape |
| SkillTool | Execute skills | Lazy-loaded bundled skills |
| WorkflowTool | Multi-step workflows | Orchestrates tool sequences |
| TaskCreateTool | Background task creation | Detached execution |
| LSPTool | Language Server Protocol | Diagnostics, definitions, references |
| MonitorTool | System monitoring | CPU, memory, processes |
| REPLTool | Embedded REPL | Interactive code execution |
| ConfigTool | Configuration management | Read/write settings |
| TodoWriteTool | Todo tracking | Progress tracking |
| PowerShellTool | PowerShell execution | Windows-specific |
| NotebookEditTool | Jupyter notebook editing | Cell manipulation |
| ScheduleCronTool | Cron scheduling | Background scheduled tasks |
| TeamCreateTool | Team creation | Multi-agent teams |
| BriefTool | Context briefing | Summarization |
| TungstenTool | Tungsten integration | External service |
| SleepTool | Delay execution | Timing control |
| VerifyPlanExecutionTool | Plan verification | Execution checking |

**Tool Execution Architecture:**
- `StreamingToolExecutor` manages concurrency control
- `toolHooks.ts` provides pre/post execution hooks
- `toolOrchestration.ts` coordinates multi-tool workflows
- Permission system: tools require user approval based on mode (auto-plan, auto-accept, interactive)

### 3.3 Task System

Background task system with type-prefixed IDs:

| Task Type | Purpose |
|-----------|---------|
| LocalAgentTask | Sub-agent in local process with worktree isolation |
| LocalShellTask | Shell command execution with guards |
| RemoteAgentTask | Agent via API (cloud tier) |
| DreamTask | Background processing/dreaming |
| InProcessTeammateTask | Teammate in same process |
| MonitorMcpTask | MCP server health monitoring |

### 3.4 Skills System

13+ bundled skills with lazy file extraction:

| Skill | Purpose |
|-------|---------|
| batch | Batch operations |
| claudeApiContent | Claude API content generation |
| claudeApi | Claude API interaction |
| claudeInChrome | Chrome integration |
| debug | Debugging assistance |
| keybindings | Keybinding management |
| loop | Loop/retry patterns |
| scheduleRemoteAgents | Remote agent scheduling |
| simplify | Code simplification |
| stuck | Unstuck assistance |
| updateConfig | Configuration updates |
| verifyContent | Content verification |

Skills are loaded from `src/skills/bundled/` with lazy extraction via `bundledSkills.ts`. Custom skills can be loaded from `.claude/skills/` directories.

### 3.5 MCP (Model Context Protocol)

Full MCP implementation with 8+ transport types:
- Stdio transport (local processes)
- SSE transport (server-sent events)
- WebSocket transport
- In-process transport
- VS Code SDK transport
- OAuth-authenticated transport
- Claude.ai transport
- Custom channel-based transports

MCP features:
- `MCPConnectionManager.tsx` — React hook for connection lifecycle
- Tool passthrough via `MCPTool`
- Resource reading via `ReadMcpResourceTool`
- Auth management via `McpAuthTool`
- Doctor/health checking via `doctor.ts`
- Official registry support
- Permission management via `channelPermissions.ts`

### 3.6 Voice Input

- `voiceModeEnabled.ts` — Toggle state
- `voice.ts` — Main voice service (native audio capture)
- `voiceStreamSTT.ts` — WebSocket-based speech-to-text streaming
- `voiceKeyterms.ts` — Keyword detection for voice commands

### 3.7 Vim Mode

5-module Vim emulation:
- `motions.ts` — Cursor motions (h, j, k, l, w, b, etc.)
- `operators.ts` — Text operators (d, y, c, etc.)
- `textObjects.ts` — Text objects (iw, i", etc.)
- `transitions.ts` — Mode transitions
- `types.ts` — Type definitions

### 3.8 Slash Commands (70+)

Defined in `src/commands.ts`, feature-gated with dead code elimination:

Categories include: provider management, session control, task management, agent routing, configuration, MCP management, plugin commands, skill commands, debug commands, and more.

### 3.9 Cost Tracking

`cost-tracker.ts` tracks:
- Token usage (input/output/cache)
- API costs per provider
- Duration metrics
- Persistence across sessions
- Hook integration for real-time updates

### 3.10 Context Compaction

Sophisticated context management to handle long conversations:
- `compact.ts` — Main compaction logic
- `microCompact.ts` — Small context reductions
- `autoCompact.ts` — Automatic triggering
- `sessionMemoryCompact.ts` — Session memory preservation
- `snipCompact.ts` — Snippet-based compaction
- `grouping.ts` — Message grouping for compaction
- `apiMicrocompact.ts` — API-aware micro compaction
- Time-based configuration via `timeBasedMCConfig.ts`

---

## 4. LLM API Handling

### 4.1 Multi-Provider Architecture

```
User Prompt
    │
    ▼
QueryEngine.ts (async generator)
    │
    ▼
services/api/client.ts
    │
    ├─► Anthropic SDK (@anthropic-ai/sdk)
    │      ├── Direct API
    │      ├── Bedrock (@anthropic-ai/bedrock-sdk)
    │      ├── Vertex (@anthropic-ai/vertex-sdk)
    │      └── Foundry (@anthropic-ai/foundry-sdk)
    │
    ├─► OpenAI Shim (openaiShim.ts)
    │      ├── OpenAI direct
    │      ├── OpenRouter
    │      ├── DeepSeek
    │      ├── Groq
    │      ├── Mistral
    │      ├── LM Studio
    │      └── Any /v1 compatible
    │
    ├─► Codex Shim (codexShim.ts)
    │      ├── Codex CLI auth
    │      ├── Codex OAuth
    │      └── Codex secure storage
    │
    ├─► Gemini (google-auth-library)
    │      ├── API key
    │      ├── Access token
    │      └── ADC (Application Default Credentials)
    │
    └─► Ollama
           └── OpenAI-compatible (localhost:11434/v1)
```

### 4.2 API Client Details

`services/api/client.ts` is the central API abstraction:
- Handles streaming responses (SSE for Anthropic, streaming for OpenAI-compat)
- Tool call/response cycle management
- Retry logic via `withRetry.ts`
- Rate limit handling
- Prompt cache break detection
- Usage tracking (token counting)
- Error normalization across providers

### 4.3 OpenAI Shim

`openaiShim.ts` adapts OpenAI-format API calls to work within OpenClaude's Anthropic-native tool calling architecture:
- Maps OpenAI function calling to Anthropic tool use format
- Handles schema differences between providers
- `openaiSchemaSanitizer.ts` cleans tool schemas for different providers
- `reasoningLeakSanitizer.ts` prevents reasoning tokens from leaking
- `toolArgumentNormalization.ts` normalizes tool arguments across providers

### 4.4 Codex Shim

`codexShim.ts` provides Codex-specific adaptation:
- OAuth flow via `codexOAuth.ts`
- Secure credential storage
- Usage tracking via `codexUsage.ts`
- Shared OAuth state via `codexOAuthShared.ts`

### 4.5 Context Injection

`context.ts` builds the LLM context:
- System prompt construction
- `CLAUDE.md` file injection (project-specific instructions)
- Git status information
- Working directory context
- Session memory integration
- Notification system for context events

---

## 5. File System Access

### 5.1 FileReadTool
- Read file contents with optional line ranges
- Binary detection (returns base64 or skips)
- Large file handling with truncation
- File state caching via `FileStateCache`

### 5.2 FileWriteTool
- Create new files or overwrite existing
- Auto-creates parent directories
- UTF-8 and binary encoding support
- Integration with file state cache

### 5.3 FileEditTool
- Diff-based editing (insert, replace, delete)
- Uses `diff` library for diff computation
- Concurrent edit protection (detects external modifications)
- Undo support via file history
- Line-number based addressing
- Snippet-based matching for robust edits

### 5.4 GrepTool
- Regex-based search using ripgrep (`rg`)
- File type filtering
- Context line inclusion
- Max results limiting
- `.gitignore` respect

### 5.5 GlobTool
- File pattern matching using `picomatch`
- Recursive directory scanning
- Pattern syntax: `**/*.ts`, `src/**/*.js`, etc.

### 5.6 Path Safety
- Working directory scoping
- `ignore` package for `.gitignore` patterns
- Permission-based access control

---

## 6. Plugin/Extension System

### 6.1 Plugin Architecture

`services/plugins/` contains:
- `PluginInstallationManager.ts` — Plugin lifecycle management
- `pluginOperations.ts` — Install, uninstall, update operations
- `pluginCliCommands.ts` — CLI commands for plugin management

### 6.2 Plugin Types

Plugins can provide:
- Custom slash commands
- MCP server configurations
- Custom tools
- Output styles
- Agent definitions
- Hook scripts

### 6.3 Agent Definitions

`AgentTool/loadAgentsDir.ts` loads agent definitions from `.claude/agents/` directories:
- Each agent has a definition file specifying name, description, instructions
- Agents can be routed to different models
- Isolation modes: worktree (safe), remote (API), fork (process)

### 6.4 MCP as Extension Point

MCP servers serve as the primary extension mechanism:
- Any MCP-compatible server can be added
- Tool passthrough via `MCPTool`
- Resource access via `ReadMcpResourceTool`/`ListMcpResourcesTool`
- Auth via `McpAuthTool`

---

## 7. Scheduling/Automation

### 7.1 Cron Scheduling

`ScheduleCronTool` enables cron-like scheduling of tasks:
- Background execution at specified intervals
- Integration with task system

### 7.2 Background Tasks

Tasks run in background with:
- Detached execution
- Output buffering
- Progress tracking
- Stop/kill support

### 7.3 Remote Agent Scheduling

`skills/bundled/scheduleRemoteAgents.ts` enables:
- Scheduling remote agents for background work
- Batch processing of multiple agents

### 7.4 Dream Task

`DreamTask.ts` enables background processing/dreaming:
- Runs when system is idle
- Can perform background analysis or improvements

### 7.5 Auto-Compaction

`autoCompact.ts` automatically compacts context when it grows too large:
- Threshold-based triggering
- Time-based configuration
- Session memory preservation

---

## 8. Notable Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `@anthropic-ai/sdk` | 0.81.0 | Anthropic Claude API |
| `@anthropic-ai/bedrock-sdk` | 0.26.4 | AWS Bedrock integration |
| `@anthropic-ai/vertex-sdk` | 0.14.4 | GCP Vertex AI integration |
| `@anthropic-ai/foundry-sdk` | 0.2.3 | Anthropic Foundry integration |
| `@grpc/grpc-js` | ^1.14.3 | gRPC server for headless mode |
| `@grpc/proto-loader` | ^0.8.0 | Proto file loading |
| `@modelcontextprotocol/sdk` | 1.29.0 | MCP protocol implementation |
| `react` | 19.2.4 | TUI rendering via Ink |
| `react-reconciler` | 0.33.0 | Custom React renderer |
| `commander` | 12.1.0 | CLI argument parsing |
| `zod` | 3.25.76 | Schema validation |
| `ajv` | 8.18.0 | JSON schema validation |
| `chokidar` | 4.0.3 | File watching |
| `sharp` | ^0.34.5 | Image processing |
| `ws` | 8.20.0 | WebSocket (voice STT, MCP) |
| `diff` | 8.0.3 | Diff computation for FileEditTool |
| `marked` | 15.0.12 | Markdown parsing |
| `turndown` | 7.2.2 | HTML to Markdown conversion |
| `duck-duck-scrape` | ^2.2.7 | Free web search |
| `@mendable/firecrawl-js` | 4.18.1 | Paid web search/fetch |
| `google-auth-library` | 9.15.1 | Gemini/Google auth |
| `axios` | 1.15.0 | HTTP client |
| `undici` | 7.24.6 | HTTP/1.1 client |
| `execa` | 9.6.1 | Process execution |
| `picomatch` | 4.0.4 | Glob pattern matching |
| `ignore` | 7.0.5 | .gitignore parsing |
| `lru-cache` | 11.2.7 | Caching |
| `yaml` | 2.8.3 | YAML parsing |

### Observability

| Package | Purpose |
|---------|---------|
| `@opentelemetry/api` | Trace/metric/log API |
| `@opentelemetry/sdk-trace-node` | Node.js tracing |
| `@opentelemetry/sdk-logs` | Log collection |
| `@opentelemetry/sdk-metrics` | Metric collection |
| `@opentelemetry/exporter-trace-otlp-grpc` | OTLP trace export |
| `@opentelemetry/exporter-logs-otlp-http` | OTLP log export |

---

## 9. gRPC Server (Headless Mode)

### Protocol Definition

`src/proto/agent.proto` defines:

~~~protobuf
service AgentService {
  rpc Chat(stream ClientMessage) returns (stream ServerMessage);
}
~~~

**Bidirectional streaming protocol:**

Client messages:
- `ChatRequest` — Initial prompt with working directory, model, session ID
- `UserInput` — Response to agent prompts (confirmations, answers)
- `CancelSignal` — Stop generation

Server messages:
- `TextChunk` — Streaming text tokens
- `ToolCallStart` — Agent started using a tool
- `ToolCallResult` — Tool returned a result
- `ActionRequired` — Agent needs user decision (confirm/info)
- `FinalResponse` — Completion with token stats
- `ErrorResponse` — Error with code

### Server Implementation

- `createDirectConnectSession.ts` — REST endpoint for session creation
- `directConnectManager.ts` — WebSocket bidirectional communication manager
- `scripts/start-grpc.ts` — Server startup script
- `scripts/grpc-cli.ts` — Test CLI client

---

## 10. Integration Scenarios

### 10.1 Integration with a Multi-Provider LLM Agent Framework (pi-mono-like)

**What pi-mono is**: A TypeScript monorepo with packages for universal AI SDK, agent framework, coding agent, TUI, web UI, orchestration, and extensible tools.

**Integration opportunities:**

#### A. Provider Layer Replacement

OpenClaude already has robust multi-provider support. pi-mono could:
- Use OpenClaude's `openaiShim.ts` pattern for provider normalization
- Integrate pi-ai's provider abstraction as an alternative to OpenClaude's custom shims
- Use OpenClaude's agent routing for cost optimization

#### B. Tool System Integration

- Expose pi-pods tools as OpenClaude tools via MCP
- Use OpenClaude's `StreamingToolExecutor` for pi-agent-core tool execution
- Map pi-agent-core's tool interface to OpenClaude's `Tool` interface

#### C. Agent Orchestration

- pi-mom orchestration via OpenClaude's `AgentTool` (worktree isolation)
- Multi-agent coordination using OpenClaude's `TeamCreateTool`
- pi-coding-agent as an OpenClaude agent definition

#### D. gRPC Bridge

- pi-mono's TUI/web UI could connect to OpenClaude's gRPC server
- Bidirectional streaming for real-time tool execution visualization
- Session persistence via gRPC session IDs

### 10.2 Integration with Lunel (Mobile IDE)

**What Lunel is**: AI-powered mobile IDE with Expo/React Native app, CLI bridge, proxy relay, and Rust PTY.

**Integration opportunities:**

#### A. Out-of-the-Box: Terminal Mode

OpenClaude runs in Lunel's terminal emulator with zero code changes:
- User opens terminal in Lunel app
- Runs `openclaude` in the PTY
- Full coding agent experience on mobile
- File changes reflected in Lunel's editor via file tracking

#### B. AI Backend Integration

OpenClaude as Lunel's third AI backend:

~~~
Lunel AiManager
  ├── opencode (OpenCode SDK)
  ├── codex (Codex JSON-RPC)
  └── openclaude (gRPC)  ← NEW
      ├── Spawn OpenClaude gRPC server
      ├── Bidirectional streaming via gRPC
      └── 47+ tools + multi-provider support
~~~

Implementation path:
1. Create `cli/src/ai/openclaude.ts` implementing `AIProvider`
2. Spawn `openclaude --grpc` as child process
3. Connect via `@grpc/grpc-js` client
4. Map gRPC `ChatRequest`/`ServerMessage` to Lunel's session/message model
5. Route tool execution events (TextChunk, ToolCallStart/Result, ActionRequired) through Lunel's `AiEventEmitter`

Benefits:
- 47+ tools accessible from mobile (bash, file editing, web search, agents)
- Multi-provider LLM support
- Voice input from phone → OpenClaude's voice system
- Skills system for reusable task templates
- MCP integration for extended tool ecosystem

#### C. Shared File System

- Both operate on same local filesystem
- OpenClaude's `FileEditTool` writes → Lunel's editor file tracking detects changes
- Lunel's editor writes → OpenClaude's `FileReadTool` reads latest
- Git operations shared between both

#### D. Lunel as OpenClaude's Mobile UI

~~~
Lunel App (React Native)
  → CLI (WebSocket)
    → OpenClaude (gRPC)
      → Any LLM Provider
        ↓
      Tool Execution
        → File changes (Lunel editor auto-refresh)
        → Terminal commands (shown in Lunel terminal)
        → Web search (shown in Lunel browser tab)
~~~

---

## 11. Security Architecture

### Permission System

Three permission modes:
- **Interactive** — Every tool call requires approval
- **Auto-plan** — Plan mode auto-approves reads, requires approval for writes
- **Auto-accept** — All tools auto-approved (dangerous)

### Tool Validation

- `ValidationResult` type: `{ result: true }` or `{ result: false, message, errorCode }`
- `CanUseToolFn` callback for dynamic permission checks
- Denial tracking via `DenialTrackingState`
- Tool permission rules by source

### API Security

- Secure credential storage for Codex OAuth
- API key redaction in logs
- Rate limit handling
- CORS headers for gRPC server

---

## 12. Key Design Patterns

### 12.1 Async Generator Pattern

`QueryEngine.ts` uses async generators for the query lifecycle:
- Yield streaming tokens
- Handle tool calls via yield*/delegate
- Clean cancellation via AbortController

### 12.2 Feature Gating

Slash commands use feature gating with dead code elimination:
- Commands conditionally available based on config
- Unused command paths eliminated at build time

### 12.3 Fail-Closed Defaults

Tool defaults are fail-closed:
- If permission check fails, deny by default
- If validation fails, return error (not empty)
- If provider fails, report error (not silent)

### 12.4 Reactive State

`store.ts` provides a minimal generic `Store<T>` with:
- `get()`/`set()` methods
- `subscribe()` for change notification
- Integration with React via `useSyncExternalStore`

### 12.5 Tool Isolation

AgentTool provides three isolation levels:
- **Worktree** — Git worktree for safe file isolation
- **Remote** — API-based execution (no local access)
- **Fork** — Process-level isolation

---

## 13. Summary

OpenClaude is a comprehensive, multi-provider coding agent CLI built on a modular architecture with 47+ tools, MCP integration, gRPC server mode, voice input, vim emulation, skills system, and extensive provider support. Its key strengths are:

1. **Provider agnosticism** — Works with any LLM via adapter shims
2. **Tool richness** — 47+ built-in tools covering file I/O, shell execution, web access, agents, tasks, MCP
3. **gRPC server** — Headless mode enables integration with any application
4. **Agent routing** — Cost-optimal model selection per agent/task
5. **Extensibility** — MCP servers, plugins, skills, custom agents, custom tools

The most natural integration with Lunel is via the gRPC server, where Lunel's mobile app becomes a rich frontend for OpenClaude's full coding agent capabilities. The gRPC bidirectional streaming protocol maps cleanly to Lunel's `AIProvider` interface.
