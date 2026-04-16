# Tolu Cowork — Research Analysis: Building an Open-Source Claude Cowork Alternative

**Date**: 2026-04-15
**Objective**: Analyze three open-source repositories and propose an integration architecture for 'Tolu Cowork' — a desktop/mobile agent that replicates Claude Cowork features using any OpenAI-compatible API.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Claude Cowork Feature Mapping](#2-claude-cowork-feature-mapping)
3. [Repository 1: pi-mono](#3-repository-1-pi-mono)
4. [Repository 2: lunel](#4-repository-2-lunel)
5. [Repository 3: openclaude](#5-repository-3-openclaude)
6. [Feature Comparison Matrix](#6-feature-comparison-matrix)
7. [Integration Architecture: Tolu Cowork](#7-integration-architecture-tolu-cowork)
8. [Implementation Roadmap](#8-implementation-roadmap)
9. [Risks and Mitigations](#9-risks-and-mitigations)

---

## 1. Executive Summary

Three repositories form complementary layers for building Tolu Cowork:

| Repo | Role | Strength |
|------|------|----------|
| **pi-mono** | LLM Abstraction + Agent Runtime | 23+ provider unified API, modular agent core, extensible tools |
| **lunel** | Mobile/Desktop UI + Remote Access | React Native app, encrypted relay, Rust PTY, plugin system |
| **openclaude** | Coding Agent + Tool Ecosystem | 47+ tools, gRPC server, MCP, skills, multi-provider routing |

**Key Insight**: No single repo covers all Claude Cowork features, but together they provide 90%+ coverage:
- pi-mono gives the **LLM abstraction layer** (Claude Cowork's provider-agnostic core)
- openclaude gives the **tool ecosystem** (Skills, Connectors, Plugins, Sub-Agents, Scheduling)
- lunel gives the **multi-platform UI + remote access** (Desktop-native app, Dispatch from phone)

The remaining 10% (VM sandboxing, persistent project memory) requires greenfield development but has clear patterns to follow from pi-mono's pi-mom (Docker sandboxing) and openclaude's project/workspace system.

---

## 2. Claude Cowork Feature Mapping

Claude Cowork features and which repo(s) provide coverage:

| Claude Cowork Feature | Description | pi-mono | lunel | openclaude | Gap? |
|-----------------------|-------------|---------|-------|------------|------|
| **Desktop-native agent** | Sandboxed VM with file access | pi-tui (terminal), pi-web-ui (web) | Expo app (mobile/desktop), Rust PTY | CLI (terminal) | Need Electron/Tauri wrapper for true desktop |
| **Sandboxed VM file access** | Isolated filesystem for agent | pi-mom has Docker sandboxing | CLI has chroot-style path sandboxing | BashTool has sandbox mode | Need unified sandbox layer |
| **Skills** | Custom instruction files | Markdown skills + prompt templates | N/A | 13+ bundled skills, SkillTool | Covered by openclaude + pi-mono |
| **Connectors** | External service integrations | Extensions (TypeScript) | Plugin system (GPI) | MCP (8+ transports), 47+ tools | Covered by openclaude MCP + lunel GPI |
| **Plugins** | Bundled packages | npm-based extensions | App-side plugin registry | MCP servers, custom tools | Covered across all three |
| **Projects** | Persistent workspaces with memory | Session tree in TUI | Git workspace tracking | Project onboarding, context compaction | Need unified project persistence |
| **Scheduled Tasks** | Recurring automation | pi-mom has cron scheduling | N/A | ScheduleCronTool, TaskTool | Covered by openclaude |
| **Sub-Agents** | Parallel execution | Parallel tool execution in agent-core | N/A | AgentTool (3 isolation modes), TeamCreateTool | Covered by openclaude |
| **Dispatch** | Remote control from phone | RPC mode (JSONL) | QR pairing, encrypted relay | gRPC server | lunel + openclaude gRPC covers this |
| **Multi-provider LLM** | Any OpenAI-compatible API | 23+ providers, OpenAI compat layer | OpenCode + Codex backends | 9+ backends, 200+ models, agent routing | Well covered |

---

## 3. Repository 1: pi-mono

**Repository**: `github.com/badlogic/pi-mono`
**Author**: Mario Zechner | **License**: MIT | **Version**: 0.67.2
**Language**: TypeScript (strict, ESM, no `any`) | **Build**: tsgo (TS 7.0 native)

### 3.1 Purpose

Pi is an open-source, terminal-based coding agent framework built on a philosophy of **aggressive extensibility over built-in features**. Instead of baking in sub-agents, plan mode, permission popups, or MCP, pi provides a minimal core and lets users extend via TypeScript extensions, skills, prompt templates, themes, and shareable npm packages.

### 3.2 Architecture / Tech Stack

**7 packages** in a monorepo with lockstep versioning:

```
pi-mono/packages/
  ai/              -> @mariozechner/pi-ai          (unified LLM API)
  agent/           -> @mariozechner/pi-agent-core   (agent runtime)
  coding-agent/    -> @mariozechner/pi-coding-agent  (CLI coding agent)
  tui/             -> @mariozechner/pi-tui          (terminal UI lib)
  web-ui/          -> @mariozechner/pi-web-ui       (web components)
  mom/             -> @mariozechner/pi-mom          (Slack bot + sandboxing)
  pods/            -> @mariozechner/pi              (GPU pod manager)
```

**Build dependency chain**: `tui -> ai -> agent -> coding-agent -> mom -> web-ui -> pods`

**Key tech**: npm workspaces, Vitest, Biome, Node >=20.6

### 3.3 Core Features

- **pi-ai**: Unified streaming API for 23+ providers (OpenAI, Anthropic, Google, Bedrock, Mistral, OpenRouter, etc.) with lazy-loaded registry, cost tracking, OAuth flows, reasoning level abstraction
- **pi-agent-core**: Generic agent runtime with tool lifecycle hooks (before/after), parallel tool execution, steering/follow-up message queues, event-driven observation
- **pi-coding-agent**: CLI with interactive TUI, RPC mode (JSONL), JSON mode, print mode, SDK. 7 built-in tools (read, bash, edit, write, grep, find, ls) with pluggable operations for remote filesystems
- **pi-tui**: Custom terminal UI with differential rendering
- **pi-web-ui**: Lit/mini-lit web components for chat interfaces
- **pi-mom**: Slack bot with Docker sandboxing and cron scheduling
- **pi-pods**: GPU pod manager for vLLM deployments

### 3.4 LLM API Handling

pi-ai is the crown jewel — a unified multi-provider LLM API:

- **10 API transports**: openai-completions, openai-responses, azure-openai-responses, openai-codex-responses, anthropic-messages, bedrock-converse-stream, google-generative-ai, google-gemini-cli, google-vertex, mistral-conversations
- **23+ providers**: Including OpenRouter, Vercel AI Gateway, xAI, Groq, Cerebras, HuggingFace, and any custom OpenAI-compatible endpoint
- **Provider-agnostic event stream**: text, thinking, toolcall start/delta/end events
- **OpenAI compatibility layer**: Auto-detection for any `/v1` compatible server
- **Cost tracking**: Per-request input/output/cache costs in $/M tokens
- **Reasoning levels**: off/minimal/low/medium/high/xhigh abstraction
- **OAuth support**: GitHub Copilot, OpenAI Codex, Google Gemini CLI, Anthropic

### 3.5 File System Access

pi-coding-agent's tools use a **pluggable operations pattern**:

~~~typescript
const tools = [
  createReadTool(cwd, { operations: customReadOps }),
  createBashTool(cwd, { operations: customBashOps }),
  createEditTool(cwd),
  createWriteTool(cwd),
];
~~~

This means filesystem operations can be redirected to Docker containers, remote machines, or any custom backend — perfect for sandboxed VM file access.

### 3.6 Plugin/Extension System

- **TypeScript extensions**: Runtime-loaded from `~/.pi/agent/extensions/` or npm packages
- **Skills**: Markdown-based prompt templates with frontmatter metadata
- **Prompt templates**: Reusable prompt patterns
- **Themes**: Customizable UI themes
- Extension API provides hooks into agent lifecycle, tool registration, UI customization

### 3.7 Scheduling/Automation

- **pi-mom**: Has cron scheduling for automated Slack-triggered tasks
- **pi-coding-agent**: Print mode (`-p`) supports one-shot automation via pipes
- **No built-in general scheduler** — but pi-mom's cron pattern is reusable

### 3.8 Notable Dependencies

- `tsgo` — TypeScript native compiler (7.0 preview)
- `@anthropic-ai/sdk`, `openai` — Provider SDKs (lazy loaded)
- `@google-cloud/vertexai`, `@aws-sdk/client-bedrock-runtime` — Cloud providers
- `tweetnacl` — Encryption (for pi-mom)
- `dockerode` — Docker integration (for pi-mom sandboxing)

### 3.9 Integration Potential

- **With lunel**: RPC mode (`--mode rpc`) provides JSONL protocol — lunel can spawn pi as a subprocess and relay events to mobile app. Alternatively, use pi-ai directly as LLM backend via lunel's `AIProvider` interface.
- **With openclaude**: pi-ai can replace openclaude's provider layer for instant 23+ provider support. Or pi-agent-core can serve as the agent runtime with battle-tested tool execution.

---

## 4. Repository 2: lunel

**Repository**: `github.com/lunel-dev/lunel`
**License**: MIT
**Languages**: TypeScript/React Native (app+CLI), Bun (manager+proxy), Rust (PTY)

### 4.1 Purpose

Lunel is an **AI-powered mobile IDE** that pairs your phone to your local machine via QR code. It follows a "dumb client" architecture where the mobile app is purely a rendering layer — all business logic runs in the CLI on the developer's machine.

Two modes:
- **Lunel Connect**: Remote access to your PC for coding (no SSH needed)
- **Lunel Cloud**: Cloud sandbox development (coming soon)

### 4.2 Architecture / Tech Stack

**5 components**:

| Component | Tech | Lines | Purpose |
|-----------|------|-------|----------|
| **App** | Expo 54 / React Native | Large | Mobile client: CodeMirror 6 editor, Skia terminal, plugin system |
| **CLI** | Node.js | 3,578 | Workhorse: 11 message namespaces (fs, git, terminal, processes, ports, monitor, http, ai, proxy, editor) |
| **Manager** | Bun + SQLite | 4,263 | Session control plane: QR pairing, password gen, proxy assignment, rate limiting |
| **Proxy** | Bun | 1,460 | Encrypted WebSocket relay with NaCl E2E encryption |
| **PTY** | Rust (forked wezterm) | ~400 | Real terminal emulation at 24fps with cell-grid rendering |

### 4.3 Core Features

- **File Explorer + Editor**: CodeMirror 6 with syntax highlighting, multi-tab editing
- **Git Integration**: Status, commit, push, pull, diff, branch management from phone
- **Terminal Emulator**: Real PTY sessions via Rust binary, 24fps rendering, cell-grid (char + fg + bg)
- **Process Management**: Start/stop/restart processes, port scanning, system monitoring (CPU/memory/disk/battery)
- **QR Code Pairing**: Scan QR to connect — no SSH, no config
- **End-to-End Encryption**: NaCl Box (Curve25519-XSalsa20-Poly1305) between CLI and app
- **Plugin System**: GPI (Global Plugin Interface) for inter-plugin communication

### 4.4 LLM API Handling

Lunel has a **dual AI backend** system:
- **OpenCode**: Local HTTP + SSE backend
- **Codex**: JSON-RPC 2.0 child process
- Both are thin wrappers implementing a clean `AIProvider` interface

Adding a third backend (pi-ai or openclaude gRPC) requires implementing:

~~~typescript
interface AIProvider {
  init(): Promise<void>;
  sendMessage(msg: string, opts?: ChatOptions): Promise<ChatResponse>;
  streamMessage(msg: string, opts?: ChatOptions): AsyncIterable<ChatEvent>;
  abort(): void;
  dispose(): void;
}
~~~

### 4.5 File System Access

The CLI enforces **sandboxed filesystem access**:
- Lexical path resolution (`path.resolve(ROOT_DIR, requestedPath)`)
- Canonical path verification (`realpathSync` to resolve symlinks)
- Prefix check against canonicalized `ROOT_DIR`
- Error code `EACCES` for violations
- Real-time file change notifications to app

### 4.6 Plugin/Extension System

**GPI (Global Plugin Interface)** — Proxy-based inter-plugin communication:

| Plugin | APIs |
|--------|------|
| ai | Chat, streaming, abort |
| editor | Open, save, cursor, selection |
| terminal | Create, write, resize |
| browser | Navigate, URL tracking |
| explorer | File tree, create, delete |
| git | Status, commit, diff |
| processes | List, kill, start |
| ports | Scan, monitor |
| http | Fetch, request |
| tools | Execute custom tools |
| monitor | CPU, memory, disk |

### 4.7 Scheduling/Automation

No built-in scheduling. All operations are on-demand from the mobile app.

### 4.8 Notable Dependencies

- `expo` (~54) — React Native framework
- `@codemirror/view` 6 — Code editor
- `@shopify/react-native-skia` — Terminal rendering
- `tweetnacl` + `tweetnacl-util` — NaCl E2E encryption
- `better-sqlite3` — Manager session storage
- `ws` — WebSocket relay

### 4.9 Integration Potential

- **With pi-mono**: Add pi-ai as a third AI backend implementing `AIProvider`. Get instant multi-provider LLM support + tool calling. Or spawn pi in RPC mode and relay events.
- **With openclaude**: Use openclaude's gRPC server as AI backend. The gRPC bidirectional streaming maps to lunel's `AIProvider` interface. Works out-of-the-box in lunel's terminal.

---

## 5. Repository 3: openclaude

**Repository**: `github.com/Gitlawb/openclaude`
**License**: MIT
**Language**: TypeScript | **Runtime**: Bun/Node | **Build**: Bun

### 5.1 Purpose

OpenClaude is an **open-source, multi-provider coding-agent CLI** supporting 200+ models across 9+ backends. It originated from Claude Code's codebase but has been substantially modified to support multiple providers and open use. It provides a terminal-first workflow with prompts, tools, agents, MCP, slash commands, and streaming output.

### 5.2 Architecture / Tech Stack

**Key source structure**:

```
src/
  main.tsx          — 4,668-line entry (CLI parsing, provider init, session mgmt, TUI, tool orchestration)
  QueryEngine.ts    — Async generator pattern for query lifecycle
  Tool.ts           — Tool interface (~40 methods per tool)
  tools/            — 47+ tool implementations
  tools.ts          — Tool registration
  server/           — gRPC server (bidirectional streaming)
  proto/            — openclaude.proto (gRPC protocol definition)
  skills/           — 13+ bundled skills
  services/         — Provider adapters, auth, telemetry
  state/            — Reactive Store<T> state management
  vim/              — 5-module vim emulation
  voice/            — Native audio + WebSocket STT
  plugins/          — Plugin system
  tasks/            — Task scheduling system
```

### 5.3 Core Features

- **47+ built-in tools**: BashTool (sandboxing), FileEditTool (diff-based), AgentTool (3 isolation modes), MCPTool, WebSearchTool, WebFetchTool, GrepTool, GlobTool, SkillTool, WorkflowTool, LSPTool, TeamCreateTool, ScheduleCronTool, + 30 more
- **gRPC server mode**: Bidirectional streaming for headless integration (`Chat(stream ClientMessage) returns (stream ServerMessage)`)
- **Agent routing**: Different agents can use different models for cost optimization
- **MCP integration**: 8+ transport types, full Model Context Protocol support
- **Skills system**: 13+ bundled skills with lazy extraction
- **Voice input**: Native audio + WebSocket STT
- **Vim mode**: 5-module emulation (motions, operators, textObjects, transitions)
- **Context compaction**: Multi-strategy context window management
- **Cost tracking**: Token/cost/duration per provider with persistence
- **OpenTelemetry**: Traces + logs + metrics
- **Provider profiles**: Saved configurations in `.openclaude-profile.json`

### 5.4 LLM API Handling

OpenClaude supports **9+ provider backends** with 200+ models:

- **OpenAI-compatible**: Works with OpenAI, OpenRouter, DeepSeek, Groq, Mistral, LM Studio
- **Gemini**: API key, access token, or local ADC
- **GitHub Models**: Interactive onboarding
- **Codex OAuth**: Browser sign-in
- **Ollama**: Local inference
- **Atomic Chat**: Apple Silicon
- **Bedrock / Vertex / Foundry**: Cloud providers

**Agent routing** (in `settings.json`):

~~~json
{
  "agentModels": {
    "deepseek-chat": { "base_url": "...", "api_key": "..." },
    "gpt-4o": { "base_url": "...", "api_key": "..." }
  },
  "agentRouting": {
    "Explore": "deepseek-chat",
    "Plan": "gpt-4o",
    "default": "gpt-4o"
  }
}
~~

### 5.5 File System Access

- **FileEditTool**: Diff-based editing with undo support
- **FileReadTool**: Full file reading with line ranges
- **GrepTool**: Content search with regex support
- **GlobTool**: File pattern matching
- **BashTool**: Shell execution with sandboxing options
- **LSPTool**: Language server integration
- All tools respect project workspace boundaries

### 5.6 Plugin/Extension System

- **MCP servers**: Full Model Context Protocol support (8+ transports)
- **Custom tools**: Via `Tool.ts` interface with `buildTool()` factory
- **Skills**: Markdown-based task templates (13+ bundled)
- **Slash commands**: Extensible command system with feature gating
- **Custom agents**: AgentTool with worktree/remote/fork isolation

### 5.7 Scheduling/Automation

- **ScheduleCronTool**: Cron-based recurring task scheduling
- **TaskTool**: Task management and execution
- **WorkflowTool**: Multi-step workflow orchestration
- **TeamCreateTool**: Parallel agent teams

### 5.8 Notable Dependencies

- `@grpc/grpc-js` — gRPC server
- `@modelcontextprotocol/sdk` — MCP integration
- `react` + `ink` — Terminal UI rendering
- `web-tree-sitter` — Code parsing
- `duck-duck-scrape` — Free web search
- `sharp` — Image processing

### 5.9 Integration Potential

- **With lunel**: gRPC server as AI backend — lunel's mobile app becomes rich frontend. Maps `ServerMessage` events (TextChunk, ToolCallStart/Result, ActionRequired, FinalResponse) to lunel's `AIProvider` interface.
- **With pi-mono**: pi-ai can replace/extend openclaude's provider layer for 23+ provider support. pi-agent-core can supplement agent orchestration.

---

## 6. Feature Comparison Matrix

| Capability | pi-mono | lunel | openclaude |
|-----------|---------|-------|------------|
| **LLM Providers** | 23+ providers, 10 transports | 2 backends (OpenCode, Codex) | 9+ backends, 200+ models |
| **Agent Runtime** | pi-agent-core (events, hooks, steering) | None (delegates to backends) | QueryEngine (async generators) |
| **Tools** | 7 built-in (pluggable ops) | CLI ops (fs, git, terminal) | 47+ tools |
| **MCP** | No (explicit choice) | No | Full (8+ transports) |
| **gRPC Server** | No (RPC mode: JSONL) | No (WebSocket relay) | Yes (bidirectional streaming) |
| **Mobile UI** | No | Expo/React Native | No |
| **Web UI** | pi-web-ui (Lit components) | No | VS Code extension |
| **Terminal UI** | pi-tui (differential render) | Rust PTY (24fps cell grid) | ink (React terminal) |
| **Scheduling** | pi-mom cron | No | ScheduleCronTool + TaskTool |
| **Sub-Agents** | Parallel tool execution | No | AgentTool (3 isolation modes), TeamCreateTool |
| **Sandboxing** | pi-mom Docker | Path-based chroot | BashTool sandbox modes |
| **Encryption** | tweetnacl (pi-mom) | NaCl Box E2E | API key redaction |
| **Plugin System** | TS extensions + skills | GPI (11 plugin APIs) | MCP + custom tools + skills |
| **Voice Input** | No | No | Yes (native + WebSocket STT) |
| **Cost Tracking** | Per-request ($/M tokens) | No | Per-provider token/cost/duration |
| **OAuth** | GitHub, Google, OpenAI, Anthropic | No | Codex OAuth, GitHub Models |
| **Project System** | Session tree | Git workspace | Project onboarding + context compaction |
| **Skills** | Markdown + prompt templates | No | 13+ bundled skills |
| **Agent Routing** | Per-tool model selection | N/A | Per-agent model routing |
| **Context Mgmt** | transformContext hook | N/A | Multi-strategy compaction |

---

## 7. Integration Architecture: Tolu Cowork

### 7.1 Design Philosophy

Combine the **best layer from each repo**:

```
┌─────────────────────────────────────────────────────────┐
│                    Tolu Cowork                          │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  lunel/app   │  │ lunel/proxy  │  │ lunel/manager │  │
│  │  (UI Layer)  │  │ (E2E Relay)  │  │ (Sessions)    │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘  │
│         │                 │                  │          │
│  ┌──────┴─────────────────┴──────────────────┴───────┐  │
│  │              Tolu Cowork Core                      │  │
│  │  ┌───────────────────┐  ┌──────────────────────┐  │  │
│  │  │   pi-ai           │  │  openclaude/tools     │  │  │
│  │  │  (LLM Abstraction)│  │  (47+ Tools + MCP)    │  │  │
│  │  └────────┬──────────┘  └──────────┬────────────┘  │  │
│  │           │                        │               │  │
│  │  ┌────────┴────────────────────────┴─────────────┐ │  │
│  │  │         Tolu Agent Runtime                     │ │  │
│  │  │  (pi-agent-core + openclaude QueryEngine)      │ │  │
│  │  └───────────────────────┬────────────────────────┘ │  │
│  │                          │                          │  │
│  │  ┌───────────────────────┴────────────────────────┐ │  │
│  │  │         Tolu Services                           │ │  │
│  │  │  Skills | Projects | Schedule | Sub-Agents     │ │  │
│  │  │  (openclaude skills, tasks, agents)             │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────┘  │
│                          │                                │
│  ┌───────────────────────┴────────────────────────────┐   │
│  │              lunel/pty + lunel/cli                  │   │
│  │         (Local Execution + Terminal)               │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Layer Responsibilities

#### Layer 1: UI Layer (from lunel)

- **lunel/app**: React Native mobile/desktop app
  - CodeMirror 6 editor
  - Skia-rendered terminal
  - File explorer
  - AI chat interface
  - Plugin rendering
- **lunel/manager**: Session control plane
  - QR pairing for phone dispatch
  - Session management with reconnection
  - Rate limiting and auth
- **lunel/proxy**: Encrypted relay
  - NaCl E2E encryption
  - WebSocket relay for remote access
  - TCP tunnel forwarding

**Claude Cowork features covered**: Desktop-native agent, Dispatch (remote from phone)

#### Layer 2: LLM Abstraction (from pi-mono)

- **pi-ai**: Drop-in LLM provider layer
  - 23+ providers with unified API
  - OpenAI-compatible auto-detection
  - Streaming event protocol
  - Cost tracking per request
  - OAuth flows (GitHub, Google, OpenAI, Anthropic)
  - Reasoning level abstraction

**Claude Cowork features covered**: Multi-provider support ("any OpenAI-compatible API")

#### Layer 3: Tool Ecosystem (from openclaude)

- **47+ tools**: File editing, bash, grep, glob, agents, tasks, MCP, web search, voice
- **MCP integration**: 8+ transport types for Connectors
- **Skills system**: 13+ bundled skills for custom instructions
- **Agent routing**: Per-agent model selection for cost optimization

**Claude Cowork features covered**: Skills, Connectors, Plugins, Sub-Agents

#### Layer 4: Agent Runtime (hybrid)

- **pi-agent-core**: Agent lifecycle, tool hooks, parallel execution, steering/follow-up queues
- **openclaude QueryEngine**: Async generator query orchestration, context compaction
- **Combined**: Tolu Agent Runtime that merges both approaches

#### Layer 5: Services (from openclaude + new)

- **Scheduled Tasks**: ScheduleCronTool + TaskTool from openclaude
- **Projects**: Enhanced project persistence (new) building on openclaude's project onboarding + pi's session tree
- **Sub-Agents**: AgentTool + TeamCreateTool from openclaude
- **Memory**: New persistent memory layer (embeddings + vector store)

#### Layer 6: Execution (from lunel)

- **lunel/pty**: Rust PTY for real terminal sessions
- **lunel/cli**: Filesystem operations, git, process management
- **Sandboxing**: Docker-based (from pi-mom pattern) or path-based (from lunel CLI)

### 7.3 Data Flow

```
User (Phone/Desktop)
  │
  ├── Lunel App (React Native)
  │     ├── Editor → CLI → File System
  │     ├── Terminal → PTY (Rust) → Shell
  │     └── AI Chat → Tolu Core
  │
  ├── Tolu Core
  │     ├── User Message
  │     │     └── pi-ai → LLM Provider → Stream Response
  │     ├── Tool Calls
  │     │     └── openclaude/tools → Execute (fs/bash/web/mcp)
  │     ├── Sub-Agents
  │     │     └── AgentTool → New pi-ai session → Parallel execution
  │     ├── Skills
  │     │     └── SkillTool → Load skill template → Inject context
  │     └── Scheduled Tasks
  │           └── ScheduleCronTool → Timer → Trigger agent session
  │
  └── Results
        ├── Text → App Chat UI
        ├── File Changes → App Editor (auto-refresh)
        ├── Terminal Output → App Terminal
        └── Notifications → App Push
```

### 7.4 Key Integration Points

#### A. lunel ↔ openclaude (via gRPC)

~~~
Lunel CLI
  → spawn openclaude --grpc
  → gRPC bidirectional stream
  → map ServerMessage to lunel AIProvider events
  → relay to mobile app via encrypted WebSocket
```

OpenClaude's gRPC protocol events map to lunel:

| gRPC Event | lunel Handler |
|------------|---------------|
| TextChunk | AIProvider.streamMessage yield |
| ToolCallStart | Plugin notification |
| ToolCallResult | File change notification |
| ActionRequired | Push to app for approval |
| FinalResponse | Chat complete |
| ErrorResponse | Error display |

#### B. pi-ai ↔ openclaude (provider swap)

~~~
OpenClaude Tool System
  → pi-ai streamSimple()
  → Any of 23+ providers
  → Streaming events back to tools
```

Replace openclaude's provider adapters with pi-ai's unified API:

~~~typescript
// In openclaude's provider layer:
import { streamSimple } from "@mariozechner/pi-ai";

// Instead of provider-specific code, use pi-ai's abstraction
const stream = streamSimple({
  model: "gpt-4o",
  provider: "openrouter", // or any of 23+ providers
  messages: convertToLlmFormat(messages),
  reasoning: "medium",
});
~~

#### C. lunel ↔ pi-ai (direct backend)

~~~
lunel CLI (AIProvider)
  → pi-ai streamSimple()
  → Stream events to app
  → App renders in chat UI
```

Implement lunel's `AIProvider` using pi-ai:

~~~typescript
import { streamSimple } from "@mariozechner/pi-ai";

class ToluProvider implements AIProvider {
  async *streamMessage(msg: string, opts?: ChatOptions): AsyncIterable<ChatEvent> {
    const stream = streamSimple({
      model: this.model,
      provider: this.provider,
      messages: [{ role: "user", content: msg }],
    });
    for await (const event of stream) {
      if (event.type === "text_delta") yield { type: "text", content: event.delta };
      if (event.type === "toolcall_end") yield { type: "tool_result", ...event.toolCall };
      if (event.type === "done") yield { type: "complete" };
    }
  }
}
```

### 7.5 New Components (Greenfield)

These features don't exist in any repo and need new development:

#### 1. Desktop App Shell

- **Approach A**: Use lunel's Expo app with `expo-electron` or `@expo/electron`
- **Approach B**: Tauri shell wrapping lunel's web components + pi-web-ui
- **Recommendation**: Tauri for native feel, smaller binary, better security

#### 2. Unified Project System

- Persistent workspace configuration
- Cross-session memory (vector embeddings)
- Project-level skills and connectors
- Build on openclaude's project onboarding + pi's session tree

#### 3. VM Sandboxing

- Docker-based (pattern from pi-mom)
- Filesystem isolation (pattern from lunel CLI)
- Network isolation for agent tool calls
- Resource limits (CPU, memory, disk)

#### 4. Dispatch System

- lunel already provides phone-to-machine connectivity
- Add push notifications for scheduled task completion
- Add remote approval flow for sensitive operations
- Leverage lunel's QR pairing + encrypted relay

---

## 8. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Goal**: Get pi-ai + openclaude tools running inside lunel

1. Fork all three repos into `tolu-cowork/` monorepo
2. Create `packages/` structure:
   - `packages/llm/` — pi-ai (renamed, minimal)
   - `packages/tools/` — openclaude tools extracted
   - `packages/runtime/` — agent runtime (pi-agent-core + QueryEngine hybrid)
   - `packages/ui/` — lunel app
   - `packages/cli/` — lunel CLI + openclaude gRPC
3. Wire pi-ai as lunel's third AIProvider
4. Wire openclaude gRPC server into lunel CLI
5. Verify: Chat with any LLM from phone → tools execute locally

### Phase 2: Core Features (Weeks 5-8)

**Goal**: Skills, Projects, Sub-Agents

1. Port openclaude's SkillTool + 13+ skills
2. Port openclaude's AgentTool (sub-agent isolation)
3. Port openclaude's TeamCreateTool (parallel agents)
4. Build project persistence layer
5. Build context compaction (from openclaude)
6. Verify: Skills loaded, sub-agents running, projects persisting

### Phase 3: Scheduling & Dispatch (Weeks 9-12)

**Goal**: Scheduled Tasks, Remote Dispatch

1. Port ScheduleCronTool + TaskTool from openclaude
2. Add push notification support (FCM/APNs)
3. Build remote approval flow for sensitive operations
4. Add QR dispatch for triggering agents from phone
5. Verify: Cron tasks running, phone dispatch working

### Phase 4: Desktop + Sandboxing (Weeks 13-16)

**Goal**: Desktop-native experience, VM isolation

1. Build Tauri desktop shell
2. Integrate pi-web-ui + lunel app into desktop UI
3. Build Docker sandbox (from pi-mom pattern)
4. Add resource limits and network isolation
5. Verify: Desktop app running, sandboxed agent execution

### Phase 5: Polish & MCP (Weeks 17-20)

**Goal**: MCP Connectors, Plugin marketplace

1. Port full MCP support from openclaude (8+ transports)
2. Build plugin/connector discovery system
3. Add voice input (from openclaude)
4. Add cost tracking dashboard
5. Build installer/package for distribution

---

## 9. Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **License conflicts** | Medium | All three repos are MIT — no conflict |
| **pi-mono auto-closes PRs** | Low | Fork and maintain independently |
| **OpenClaude upstream divergence** | Medium | Pin to stable release, cherry-pick patches |
| **Lunel Expo app complexity** | Medium | Use Tauri for desktop, keep Expo for mobile only |
| **pi-ai + openclaude provider overlap** | Low | Use pi-ai as primary, openclaude as fallback for MCP-specific providers |
| **TypeScript version conflicts** | Medium | Use pi-mono's tsgo + strict ESM, migrate openclaude's Bun-specific code |
| **Rust PTY cross-platform** | Low | Already portable via portable-pty crate |
| **gRPC + WebSocket bridging** | Medium | lunel CLI acts as bridge — spawn openclaude gRPC, relay to app |
| **Context window management** | High | Use openclaude's compaction strategies + pi-agent-core's transformContext hook |
| **Sub-agent resource exhaustion** | Medium | Add resource limits from pi-mom Docker pattern |

---

## Appendix A: Detailed Per-Repo Analysis Files

Full deep-dive analysis for each repository is available in separate files:

- **pi-mono**: `/a0/usr/workdir/tolu-cowork/pi-mono-analysis.md` (695 lines)
- **lunel**: `/a0/usr/workdir/tolu-cowork/lunel-analysis.md` (705 lines)
- **openclaude**: `/a0/usr/workdir/tolu-cowork/openclaude-analysis.md` (782 lines)

## Appendix B: Quick Reference — Claude Cowork Feature Coverage

| Feature | Primary Source | Secondary Source | New Dev Needed |
|---------|---------------|-----------------|----------------|
| Desktop-native agent | lunel/app + Tauri | pi-web-ui | Yes (Tauri shell) |
| Sandboxed VM | pi-mom (Docker) | lunel CLI (paths) | Yes (unified sandbox) |
| Skills | openclaude (SkillTool) | pi-mono (skills) | No |
| Connectors | openclaude (MCP) | lunel (GPI plugins) | No |
| Plugins | openclaude (MCP) | lunel (GPI), pi-mono (extensions) | No |
| Projects | openclaude (onboarding) | pi-mono (session tree) | Yes (persistence) |
| Scheduled Tasks | openclaude (ScheduleCronTool) | pi-mom (cron) | No |
| Sub-Agents | openclaude (AgentTool) | pi-agent-core (parallel) | No |
| Dispatch | lunel (QR + relay) | openclaude (gRPC) | Yes (push notifications) |
| Multi-provider LLM | pi-ai (23+ providers) | openclaude (9+ backends) | No |
