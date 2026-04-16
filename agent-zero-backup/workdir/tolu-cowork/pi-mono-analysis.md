# Pi-Mono Deep-Dive Analysis

**Repository**: github.com/badlogic/pi-mono  
**Author**: Mario Zechner  
**License**: MIT  
**Version**: 0.67.2 (lockstep across all packages)  
**Analyzed**: 2026-04-15

---

## 1. Purpose

Pi ("Shitty Coding Agent") is an open-source, terminal-based coding agent framework. Its core philosophy is **aggressive extensibility over built-in features** -- instead of baking in sub-agents, plan mode, permission popups, MCP, or background bash, pi provides a minimal core and lets users extend it via TypeScript extensions, skills (markdown-based prompts), prompt templates, themes, and shareable npm packages.

The monorepo ships:
- A **unified multi-provider LLM streaming API** (pi-ai)
- An **agent runtime with tool calling and state management** (pi-agent-core)
- An **interactive coding agent CLI** with TUI, RPC mode, JSON mode, print mode, and SDK (pi-coding-agent)
- A **terminal UI library** with differential rendering (pi-tui)
- **Web UI components** for AI chat interfaces (pi-web-ui)
- A **Slack bot** that delegates to the coding agent (pi-mom)
- A **GPU pod management CLI** for vLLM deployments (pi-pods)

---

## 2. Architecture / Tech Stack

### Monorepo Structure

```
pi-mono/
  packages/
    ai/              -> @mariozechner/pi-ai          (unified LLM API)
    agent/           -> @mariozechner/pi-agent-core   (agent runtime)
    coding-agent/    -> @mariozechner/pi-coding-agent  (CLI coding agent)
    tui/             -> @mariozechner/pi-tui          (terminal UI lib)
    web-ui/          -> @mariozechner/pi-web-ui       (web components)
    mom/             -> @mariozechner/pi-mom          (Slack bot)
    pods/            -> @mariozechner/pi              (GPU pod manager)
```

### Build Order Dependency Chain

```
tui -> ai -> agent -> coding-agent -> mom -> web-ui -> pods
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | TypeScript (strict, ESM only, no `any`) |
| Build | `tsgo` (TypeScript native preview 7.0) for most packages; `tsc` for web-ui |
| Linting | Biome 2.3.5 |
| Testing | Vitest (unit), Node test runner (TUI) |
| Runtime | Node >=20.6 (or Bun compiled binary) |
| Package Mgmt | npm workspaces |
| Versioning | Lockstep -- all packages share the same version |

### Package Dependency Graph

```
pi-ai (zero deps on other pi packages)
  ^
  |
pi-agent-core (depends on pi-ai)
  ^
  |
pi-coding-agent (depends on pi-ai, pi-agent-core, pi-tui)
  ^
  |
pi-mom (depends on pi-ai, pi-agent-core, pi-coding-agent)
pi-web-ui (depends on pi-ai, pi-tui, peer: lit/mini-lit)
pi-pods (depends on pi-agent-core)
```

---

## 3. Core Features and Capabilities

### 3.1 Pi-AI: Unified LLM API

**Supported APIs (10 known)**:
| API | Transport |
|-----|----------|
| `openai-completions` | HTTP SSE |
| `openai-responses` | HTTP SSE |
| `azure-openai-responses` | HTTP SSE |
| `openai-codex-responses` | HTTP SSE |
| `anthropic-messages` | HTTP SSE |
| `bedrock-converse-stream` | AWS SDK |
| `google-generative-ai` | HTTP SSE |
| `google-gemini-cli` | OAuth CLI |
| `google-vertex` | HTTP SSE |
| `mistral-conversations` | HTTP SSE |

**Supported Providers (23+)**:
amazon-bedrock, anthropic, openai, azure-openai, openai-codex, google, google-gemini-cli, google-antigravity, google-vertex, github-copilot, xai, groq, cerebras, openrouter, vercel-ai-gateway, zai, mistral, minimax, minimax-cn, huggingface, opencode, opencode-go, kimi-coding, plus any OpenAI-compatible custom provider.

**Default models per provider**: claude-opus-4-6, gpt-5.4, gemini-2.5-pro, etc.

**Key capabilities**:
- Streaming and complete (non-streaming) APIs
- `streamSimple()` / `completeSimple()` with reasoning level abstraction (off/minimal/low/medium/high/xhigh)
- Automatic model discovery and metadata generation (`scripts/generate-models.ts`)
- Cost tracking per request (input/output/cache-read/cache-write in $/M tokens)
- Context window and max token metadata per model
- Provider-agnostic event stream protocol (text/thinking/toolcall start/delta/end events)
- OpenAI-compatible provider support with auto-detection and compatibility layer (`OpenAICompletionsCompat`)
- OAuth support for GitHub Copilot, OpenAI Codex, Google Gemini CLI, Anthropic, Google Antigravity
- Prompt cache retention preferences (none/short/long)
- Session-based caching for compatible backends
- Proxy support via `proxy-agent`
- Custom payload inspection/replacement via `onPayload` hook

### 3.2 Pi-Agent-Core: Agent Runtime

**Agent class** (`Agent`):
- Stateful wrapper: owns transcript, tools, model, system prompt, thinking level
- Event-driven lifecycle: `agent_start`, `agent_end`, `turn_start`, `turn_end`, `message_start/update/end`, `tool_execution_start/update/end`
- Subscribe pattern for UI observation
- Steering message queue (delivered mid-run after tool execution)
- Follow-up message queue (delivered after agent finishes)
- Queue modes: `"all"` or `"one-at-a-time"`
- Abort support via `AbortController`

**Tool lifecycle hooks**:
- `beforeToolCall` -- can block execution with `{ block: true, reason }`
- `afterToolCall` -- can override content, details, isError
- Tool execution modes: `"sequential"` or `"parallel"` (default)

**AgentTool interface**:
- `name`, `description`, `label`, `parameters` (TypeBox schema)
- `prepareArguments()` -- pre-validation shim
- `execute()` -- receives toolCallId, validated params, abort signal, and update callback for streaming partial results

**Extensible message types** via declaration merging on `CustomAgentMessages`

**Context management**:
- `convertToLlm()` -- transforms AgentMessage[] to LLM-compatible Message[]
- `transformContext()` -- pre-conversion hook for context window management, pruning
- `getApiKey()` -- dynamic key resolution (for OAuth token refresh)

### 3.3 Pi-Coding-Agent: The CLI

**Modes of operation**:
1. **Interactive mode** -- Full TUI with editor, model selector, session tree, keyboard shortcuts
2. **Print mode** (`-p`) -- Output response to stdout and exit; supports piped stdin
3. **JSON mode** (`--mode json`) -- Stream all events as JSON lines
4. **RPC mode** (`--mode rpc`) -- JSONL stdin/stdout protocol for process integration
5. **SDK** -- Programmatic embedding via `createAgentSession()` or `createAgentSessionRuntime()`

**Built-in tools**:
| Tool | Description | Type |
|------|-------------|------|
| `read` | Read file contents with line ranges, image support, auto-resize | Coding |
| `bash` | Execute shell commands with timeout, streaming output | Coding |
| `edit` | Line-range file editing (patch-style) | Coding |
| `write` | Create/overwrite files | Coding |
| `grep` | Search file contents | Read-only |
| `find` | Find files by name | Read-only |
| `ls` | List directory contents | Read-only |

**Session management**:
- JSONL-based session files with tree structure (entries have `id` + `parentId`)
- Branching: create alternate conversation branches from any point
- Forking: create new sessions from branches
- Compaction: automatic or manual context compression via summarization
- Export to HTML with syntax highlighting
- Share via GitHub gist

**Message queue** (unique feature):
- Steering messages: delivered after current assistant turn's tool calls finish
- Follow-up messages: delivered after agent completes all work
- Configurable delivery modes

### 3.4 Pi-TUI: Terminal UI Library

Custom terminal rendering library with:
- Differential rendering (only update changed cells)
- Text editor component with autocomplete, multi-line, paste handling
- Component system (Container, Text, etc.)
- Theme support
- East Asian width handling
- Markdown rendering via `marked`
- Optional native FFI via `koffi`

### 3.5 Pi-Web-UI: Web Components

Reusable web components for AI chat interfaces:
- Built on Lit / mini-lit web components
- Tailwind CSS styling
- Document viewers: PDF (pdfjs-dist), DOCX (docx-preview), XLSX (sheetjs)
- Image/file handling
- Integration with LM Studio SDK and Ollama for local models

### 3.6 Pi-Mom: Slack Bot

Slack bot that delegates messages to pi coding agent:
- Slack Socket Mode integration
- Sandbox execution: host or Docker container
- Per-channel agent runners
- File download/upload support
- Uses `@anthropic-ai/sandbox-runtime` for sandboxing
- Cron-based scheduling via `croner` library
- Channel store for state persistence

### 3.7 Pi-Pods: GPU Pod Manager

CLI for managing vLLM deployments on GPU pods:
- SSH-based remote management
- Model configuration
- Pod lifecycle commands
- Prompt testing against deployed models

---

## 4. LLM API Handling

### Abstraction Architecture

```
User code
  |
  v
stream() / complete() / streamSimple() / completeSimple()  (stream.ts)
  |
  v
api-registry.ts -- getApiProvider(model.api)
  |
  v
Lazy-loaded provider module (register-builtins.ts)
  |
  v
Provider-specific stream function
  |
  v
LLM SDK (openai, anthropic, google-genai, mistral, aws-bedrock)
```

### Provider Registration System

Providers are registered via `registerApiProvider()` with lazy loading:

```typescript
// Each provider is a separate subpath export in package.json
"./anthropic": { import: "./dist/providers/anthropic.js" }
"./openai-completions": { import: "./dist/providers/openai-completions.js" }
// ... etc
```

**Lazy loading pattern**: Provider modules are dynamically `import()`ed on first use. A cached promise ensures subsequent calls reuse the loaded module. This keeps startup fast.

**Source-based unregistration**: `unregisterApiProviders(sourceId)` allows bulk removal, enabling plugin hot-loading.

### Unified Event Stream Protocol

All providers emit events through `AssistantMessageEventStream`:

```
start -> [text_start -> text_delta* -> text_end]?
       -> [thinking_start -> thinking_delta* -> thinking_end]?
       -> [toolcall_start -> toolcall_delta* -> toolcall_end]?
       -> done | error
```

### Message Types

- `UserMessage`: text + optional images, timestamp
- `AssistantMessage`: text + thinking + tool calls, usage, stop reason, cost
- `ToolResultMessage`: text + optional images, error flag, details

### How Providers Are Called

Each provider implements:
1. `streamXxx()` -- provider-specific options, raw streaming
2. `streamSimpleXxx()` -- maps `SimpleStreamOptions` (with `reasoning` level) to provider-specific parameters

The provider converts unified Context/Message types to provider-native formats, calls the SDK, parses responses, and emits standardized events.

### Custom Provider Support

OpenAI-compatible providers are supported via `openai-completions` API with `OpenAICompletionsCompat` overrides:
- `supportsStore`, `supportsDeveloperRole`, `supportsReasoningEffort`
- `reasoningEffortMap` -- map pi reasoning levels to provider-specific values
- `thinkingFormat` -- openai/openrouter/zai/qwen formats
- `maxTokensField` -- max_completion_tokens vs max_tokens
- OpenRouter and Vercel AI Gateway routing preferences

Extensions can register entirely new providers (custom APIs, OAuth flows).

---

## 5. File System Access

### Tool-Level Abstraction: Pluggable Operations

Each file tool defines an operations interface that can be overridden:

```typescript
// Read tool
interface ReadOperations {
  readFile: (absolutePath: string) => Promise<Buffer>;
  access: (absolutePath: string) => Promise<void>;
  detectImageMimeType?: (absolutePath: string) => Promise<string | null>;
}

// Bash tool  
interface BashOperations {
  exec: (command, cwd, { onData, signal, timeout, env }) => Promise<{ exitCode };
}
```

**Default implementations** use local filesystem (`fs.readFile`, `child_process.spawn`). **Custom implementations** can delegate to remote systems (SSH, Docker, etc.).

### Factory Functions

Every tool has both a singleton (`readTool`, `bashTool`) and a factory (`createReadTool(cwd, options)`, `createBashTool(cwd, options)`). Factories accept:
- `cwd` -- working directory for path resolution
- `options` -- including custom `operations`

### Path Resolution

All tools use `resolveReadPath()` / `path-utils.ts` to resolve relative paths against the session's working directory.

### Truncation

Output truncation is handled by `truncate.ts`:
- `DEFAULT_MAX_LINES` and `DEFAULT_MAX_BYTES` constants
- `truncateHead()`, `truncateTail()`, `truncateLine()` functions
- Truncation metadata returned in tool details for UI rendering

### Sandboxing (Pi-Mom)

The `mom` package supports:
- **Host execution** -- run directly on the host
- **Docker execution** -- run commands inside a Docker container
- Uses `@anthropic-ai/sandbox-runtime` for sandboxed tool execution

### File Mutation Queue

`withFileMutationQueue()` wraps tools to serialize file mutations (read, edit, write) to prevent race conditions when tools execute in parallel.

---

## 6. Plugin/Extension System

### Architecture

Extensions are **TypeScript modules** loaded at runtime via `@mariozechner/jiti` (a fork with virtual module support for Bun binaries).

```
Extension lifecycle:
1. Discovery: scan ~/.pi/agent/extensions/, .pi/extensions/, pi-packages
2. Loading: jiti compiles TS -> JS with module aliasing
3. Registration: extension's default function receives ExtensionAPI
4. Runtime: hooks fire on agent events
```

### ExtensionAPI Capabilities

An extension can:
- **Register tools** (`registerTool`) -- add LLM-callable tools with TypeBox schemas
- **Register commands** (`registerCommand`) -- add slash commands with keybindings
- **Register CLI flags** (`registerFlag`) -- add command-line arguments
- **Subscribe to events** (`on(event, handler)`) -- lifecycle, tool calls, messages
- **Access UI context** (`ctx.ui`) -- dialogs, selectors, editors, notifications, widgets, overlays
- **Override tools** -- replace built-in tool implementations
- **Custom compaction** -- replace summarization logic
- **Custom editor** -- replace the input editor
- **Custom footer/header** -- replace status bar components
- **Status lines** -- add persistent status indicators
- **Message rendering** -- custom renderers for specific message types
- **Access session state** -- read/write session, model, messages

### Extension Events

```typescript
"session_start" | "session_end"
| "user_message" | "user_bash"
| "assistant_message"
| "tool_call" | "tool_result"
| "compact" | "compact_summary"
```

### Skills System

Skills follow the **Agent Skills standard** (agentskills.io):
- Markdown files with YAML frontmatter (`name`, `description`, `disable-model-invocation`)
- Placed in `~/.pi/agent/skills/`, `~/.agents/skills/`, `.pi/skills/`, or `.agents/skills/`
- Auto-discovered walking up from cwd to root
- Respect `.gitignore`/`.ignore`/`.fdignore`
- Invoked via `/skill:name` or auto-loaded when matching user request

### Pi Packages

Shareable bundles distributed via npm or git:
```json
{
  "pi": {
    "extensions": ["./extensions"],
    "skills": ["./skills"],
    "prompts": ["./prompts"],
    "themes": ["./themes"]
  }
}
```

Install commands: `pi install npm:@foo/pi-tools`, `pi install git:github.com/user/repo`

### Hook Points for Extension Authors

The coding-agent exposes a `./hooks` subpath export with:
- Event bus subscription
- Tool definition wrappers
- Extension lifecycle hooks

---

## 7. Scheduling/Automation

### Built-in: No Native Scheduling

Pi's philosophy explicitly excludes built-in scheduling. The recommendation is to use external tools.

### Pi-Mom: Slack-Based Automation

The `mom` package provides the closest thing to built-in scheduling:
- **Cron-based scheduling** via the `croner` library (dependency in mom's package.json)
- **Slack-triggered execution** -- messages in Slack channels trigger coding agent runs
- **Per-channel state** -- each Slack channel gets its own agent runner
- **Sandbox execution** -- Docker container isolation for untrusted code

### RPC Mode for External Orchestration

The RPC protocol enables external schedulers to drive pi:
```bash
pi --mode rpc
```
Commands: `prompt`, `steer`, `follow_up`, `abort`, `new_session`, `set_model`, `compact`, `bash`, etc.

### SDK for Programmatic Scheduling

```typescript
const { session } = await createAgentSession({ ... });
await session.prompt("Run the test suite");
```

---

## 8. Notable Dependencies

### Runtime Dependencies

| Package | Used By | Purpose |
|---------|---------|--------|
| `@anthropic-ai/sdk` | pi-ai | Anthropic Claude API |
| `openai` | pi-ai | OpenAI API (v6.26) |
| `@google/genai` | pi-ai | Google Generative AI |
| `@mistralai/mistralai` | pi-ai | Mistral API |
| `@aws-sdk/client-bedrock-runtime` | pi-ai | Amazon Bedrock |
| `@sinclair/typebox` | pi-ai, pi-agent-core | JSON Schema type builder |
| `ajv` + `ajv-formats` | pi-ai | JSON Schema validation |
| `zod-to-json-schema` | pi-ai | Zod schema conversion |
| `partial-json` | pi-ai | Streaming JSON parsing |
| `proxy-agent` | pi-ai | HTTP proxy support |
| `undici` | pi-ai, coding-agent | HTTP client |
| `chalk` | pi-tui, coding-agent | Terminal colors |
| `marked` | pi-tui | Markdown rendering |
| `diff` | coding-agent, mom | Diff generation for edit tool |
| `glob` | coding-agent | File globbing |
| `ignore` | coding-agent | .gitignore parsing |
| `minimatch` | coding-agent | Pattern matching |
| `yaml` | coding-agent | YAML parsing |
| `uuid` | coding-agent | Unique IDs |
| `@mariozechner/jiti` | coding-agent | Runtime TS compilation for extensions |
| `proper-lockfile` | coding-agent | File locking |
| `@slack/socket-mode` + `@slack/web-api` | pi-mom | Slack integration |
| `@anthropic-ai/sandbox-runtime` | pi-mom | Sandboxed execution |
| `croner` | pi-mom | Cron scheduling |
| `lit` / `@mariozechner/mini-lit` | pi-web-ui | Web components |
| `pdfjs-dist` | pi-web-ui | PDF viewing |
| `docx-preview` | pi-web-ui | DOCX viewing |
| `xlsx` | pi-web-ui | Spreadsheet viewing |
| `@lmstudio/sdk` | pi-web-ui | LM Studio local model integration |
| `ollama` | pi-web-ui | Ollama local model integration |
| `koffi` | pi-tui (optional) | Native FFI |
| `@silvia-odwyer/photon-node` | coding-agent | Image processing (WASM) |

### Dev Dependencies

| Package | Purpose |
|---------|--------|
| `@biomejs/biome` 2.3.5 | Linting + formatting |
| `@typescript/native-preview` 7.0 | tsgo (native TS compiler) |
| `typescript` 5.9+ | Type checking |
| `vitest` | Testing |
| `concurrently` | Parallel dev server management |
| `husky` | Git hooks |

---

## 9. Integration Scenarios

### 9a. Integration with a Mobile IDE Platform (Lunel-like)

**Lunel** is a React Native mobile IDE with a Rust PTY, TypeScript proxy/manager, and mobile app. Integration points:

#### Option 1: RPC Mode (Recommended for mobile)

```
Mobile App -> Manager -> Proxy -> pi --mode rpc (child process)
                                    stdin/stdout JSONL
```

**Why RPC mode**:
- Language-agnostic JSONL protocol over stdin/stdout
- No Node.js dependency in the mobile app itself
- Full agent control: prompt, steer, follow_up, abort, set_model, compact, bash
- Event streaming: agent_start/end, turn_start/end, message_update, tool_execution events
- Extension UI forwarding: RPC supports `extension_ui_request`/`extension_ui_response` for remote UI

**Protocol flow**:
1. Spawn `pi --mode rpc` as child process
2. Send JSON commands on stdin
3. Read JSON events on stdout
4. Handle `extension_ui_request` events for UI interactions (select, confirm, input)
5. Respond with `extension_ui_response`

**Key RPC commands needed**:
```json
{ "type": "prompt", "message": "..." }
{ "type": "abort" }
{ "type": "get_state" }
{ "type": "set_model", "provider": "anthropic", "modelId": "claude-sonnet-4-20250514" }
{ "type": "get_messages" }
{ "type": "new_session" }
{ "type": "switch_session", "sessionPath": "..." }
```

#### Option 2: SDK Embedding (Node.js native)

For platforms with a Node.js runtime:

```typescript
import { createAgentSession, SessionManager } from "@mariozechner/pi-coding-agent";

const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  // Custom tools with remote operations
  tools: [createReadTool(cwd, { operations: remoteReadOps })],
});

session.subscribe(async (event, signal) => {
  // Forward events to mobile app
  sendToApp(serializeEvent(event));
});

await session.prompt("Fix the bug in app.tsx");
```

#### Option 3: Custom Tools for Remote File System

Override `ReadOperations`, `BashOperations`, etc. to delegate to the mobile device's file system:

```typescript
const sshReadOps: ReadOperations = {
  readFile: (path) => sshExec(`cat ${path}`),
  access: (path) => sshExec(`test -r ${path}`),
};
```

**Key considerations for mobile IDE integration**:
- Session management: Use `SessionManager.inMemory()` or custom storage
- File operations: Override tool operations to work with device filesystem
- UI: Build React Native components that consume `AgentEvent` stream
- Streaming: Subscribe to `message_update` events for real-time rendering
- Cost tracking: `AssistantMessage.usage` provides token counts and costs
- Image support: `UserMessage` and `ToolResultMessage` support image content

### 9b. Integration with a Multi-Provider Coding Agent (OpenClaude-like)

**OpenClaude** is a multi-provider coding agent with tools, services, plugins, voice, vim mode, etc. Integration points:

#### Option 1: Use pi-ai as the LLM abstraction layer

Replace OpenClaude's provider logic with pi-ai's unified API:

```typescript
import { stream, streamSimple, completeSimple } from "@mariozechner/pi-ai";
import { models } from "@mariozechner/pi-ai"; // auto-generated model catalog

// Provider-agnostic streaming
const eventStream = streamSimple(model, {
  systemPrompt: "You are a coding assistant.",
  messages: [...],
  tools: [...],
}, { reasoning: "medium" });

for await (const event of eventStream) {
  if (event.type === "text_delta") handleText(event.delta);
  if (event.type === "toolcall_end") handleToolCall(event.toolCall);
  if (event.type === "done") handleComplete(event.message);
}
```

**Benefits for OpenClaude**:
- Instant support for 23+ providers without maintaining provider-specific code
- Automatic model catalog with cost tracking
- Unified thinking/reasoning level abstraction
- OAuth flows for GitHub Copilot, Google, OpenAI Codex
- OpenRouter/Vercel AI Gateway routing preferences
- Provider-specific compatibility handled automatically

#### Option 2: Use pi-agent-core as the agent runtime

```typescript
import { Agent } from "@mariozechner/pi-agent-core";

const agent = new Agent({
  streamFn: streamSimple,
  convertToLlm: myMessageConverter,
  transformContext: myContextPruner,
  beforeToolCall: myPermissionGate,
  afterToolCall: myOutputFilter,
  toolExecution: "parallel",
});

// Register OpenClaude's tools
agent.state.tools = [myCustomTools];

// Subscribe to events for UI
agent.subscribe((event, signal) => { ... });

// Run
await agent.run(userMessage);
```

**Benefits for OpenClaude**:
- Battle-tested agent loop with parallel tool execution
- Steering and follow-up message queues
- Abort support with proper cleanup
- Before/after tool call hooks for permission gates
- Custom message types via declaration merging

#### Option 3: Use pi-coding-agent as a subprocess

Spawn pi in RPC mode and use OpenClaude as the orchestration layer:

```typescript
const piProcess = spawn("pi", ["--mode", "rpc"]);
// Send prompts, receive events, relay to OpenClaude's UI
```

#### Option 4: Use pi-coding-agent's tool implementations

Import individual tools from pi-coding-agent:

```typescript
import { 
  createReadTool, createBashTool, createEditTool, createWriteTool,
  createGrepTool, createFindTool, createLsTool 
} from "@mariozechner/pi-coding-agent";

// Use with custom operations for sandbox/container execution
const tools = [
  createReadTool(cwd, { operations: dockerReadOps }),
  createBashTool(cwd, { operations: dockerBashOps }),
  createEditTool(cwd),
  createWriteTool(cwd),
];
```

**Key considerations for multi-provider agent integration**:
- **Model registry**: pi-ai's `ModelRegistry` handles auto-discovery from provider APIs
- **Custom providers**: Add via `~/.pi/agent/models.json` or extensions with custom auth
- **Tool extensibility**: pi's tools are designed for composition and override
- **Extension system**: Could wrap OpenClaude's plugins as pi extensions
- **No MCP dependency**: Pi explicitly avoids MCP in favor of direct tool implementations and skills

---

## Summary

Pi-mono is a well-architected, modular coding agent framework with clean separation of concerns:

1. **pi-ai** provides the LLM abstraction -- the most mature and portable layer
2. **pi-agent-core** provides the agent runtime -- generic enough for any agent use case
3. **pi-coding-agent** provides the full coding experience -- extensible via TypeScript extensions
4. **pi-tui** enables the rich terminal interface
5. **pi-web-ui** enables browser-based chat interfaces
6. **pi-mom** demonstrates Slack integration with sandboxing
7. **pi-pods** manages self-hosted model deployments

The architecture favors **composition over configuration**, **extensibility over built-in features**, and **TypeScript-native runtime loading** over static compilation. The pluggable operations pattern on tools, the lazy-loaded provider registry, and the event-driven agent lifecycle make it highly adaptable for integration into other platforms.
