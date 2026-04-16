# OpenClaude Repository — Comprehensive Architecture Report

Detailed analysis of 40 key source files/directories covering purpose, key types/interfaces, notable patterns, and inter-component connections.

---

## 1. `src/main.tsx` — Application Entry Point (~4668 lines)

**Purpose**: CLI entry point and orchestrator. Handles Commander.js CLI parsing, session initialization, provider configuration, and launching interactive REPL or headless/print mode.

**Key Patterns**:
- Side-effect imports (`startMdmRawRead()`, `startKeychainPrefetch()`) fire before module evaluation to parallelize I/O
- Dead code elimination via `feature('FLAG')` conditional requires — tree-shaken from external builds
- Lazy `require()` to break circular dependencies (teammate.ts ↔ AppState.tsx ↔ main.tsx)
- Extensive migration system for settings compatibility across versions

**Connections**: Imports from virtually every subsystem. Orchestrates: parse CLI → configure auth → setup permissions → initialize MCP → launch REPL or print mode.

---

## 2. `src/Tool.ts` — Tool Interface & Factory

**Purpose**: Defines the `Tool` type — the contract every tool implements. Foundational abstraction for all tools. Provides `buildTool()` factory with safe defaults.

**Key Types**:
- `Tool<Input, Output, P>` — ~40 methods: `call()`, `description()`, `prompt()`, `isEnabled()`, `isReadOnly()`, `isDestructive()`, `checkPermissions()`, `validateInput()`, rendering methods, `mapToolResultToToolResultBlockParam()`
- `ToolUseContext` — Context passed to every tool call: abort controller, app state, messages, file cache, MCP clients, permission context, progress callbacks
- `ToolResult<T>` — Output data + optional new messages + context modifiers
- `ToolPermissionContext` — Immutable permission rules (mode, allow/deny/ask rules)
- `ToolDef` / `buildTool()` — Partial definition + factory with fail-closed defaults
- `Tools` — `readonly Tool[]` alias
- `ValidationResult` — `{ result: true }` | `{ result: false, message, errorCode }`

**Notable Patterns**:
- `buildTool()` defaults: isEnabled→true, isConcurrencySafe→false, isReadOnly→false, checkPermissions→allow
- `shouldDefer`/`alwaysLoad` flags for ToolSearch (deferred loading for large tool pools)
- `maxResultSizeChars` controls disk persistence of large outputs

---

## 3. `src/tools.ts` — Tool Registry

**Purpose**: Central registry assembling the full tool pool. Combines built-in + MCP tools, applies deny rules, handles mode-specific filtering.

**Key Functions**:
- `getAllBaseTools()` — All possible built-in tools (feature-gated). Source of truth for tool catalog
- `getTools(permissionContext)` — Filtered by permissions and mode
- `assembleToolPool(permissionContext, mcpTools)` — Built-in + MCP, deduplicated, sorted for prompt-cache stability
- `filterToolsByDenyRules()` — Removes blanket-denied tools

**Notable Patterns**:
- Conditional `require()` for feature-gated tools
- Tool ordering matters for prompt caching — built-ins stay contiguous
- REPL mode hides primitives when REPL wrapper is active
- Simple mode restricts to Bash + Read + Edit

---

## 4. `src/context.ts` — LLM Context Management

**Purpose**: Constructs system/user context prepended to every conversation. Manages git status, CLAUDE.md files, system prompt injection.

**Key Functions**:
- `getSystemContext()` — Memoized: git status + cache-breaking injection
- `getUserContext()` — Memoized: CLAUDE.md content + current date
- `getGitStatus()` — Memoized: parallel git commands (branch, status, log, user.name)

**Notable Patterns**:
- All memoized via lodash — computed once per conversation
- Cache invalidation via `setSystemPromptInjection()`
- `--bare` skips auto-discovery but honors explicit `--add-dir`
- Git status truncated at 2000 chars

---

## 5. `src/QueryEngine.ts` — Query Orchestration

**Purpose**: Owns query lifecycle and session state. One QueryEngine per conversation; each `submitMessage()` is a new turn. Used by both headless/SDK and interactive paths.

**Key Class**: `QueryEngine`
- `submitMessage(prompt)` — Async generator yielding `SDKMessage` events
- `interrupt()` — Aborts current operation
- Manages `mutableMessages`, `totalUsage`, `permissionDenials`

**Key Types**:
- `QueryEngineConfig` — cwd, tools, commands, MCP clients, agents, budget limits, thinking config

**Notable Patterns**:
- Yields SDKMessage variants: assistant, user, progress, stream_event, attachment, system, tool_use_summary, result
- Handles structured output enforcement, max turns, max budget
- Snip compaction via injected callback (feature-gated)
- Standalone `ask()` function wraps QueryEngine for one-shot usage

---

## 6. `src/Task.ts` — Task System Types

**Purpose**: Defines task abstraction for background/foreground operations.

**Key Types**:
- `TaskType` — `'local_bash' | 'local_agent' | 'remote_agent' | 'in_process_teammate' | 'local_workflow' | 'monitor_mcp' | 'dream'`
- `TaskStatus` — `'pending' | 'running' | 'completed' | 'failed' | 'killed'`
- `TaskStateBase` — id, type, status, description, startTime, endTime, outputFile
- `Task` — Interface: `{ name, type, kill(taskId, setAppState) }`
- `TaskContext` — `{ abortController, getAppState, setAppState }`

**Notable Patterns**:
- Task IDs: type prefix (b/a/r/t/w/m/d) + 8 random alphanumeric chars
- Output stored to disk via `getTaskOutputPath()`

---

## 7. `src/tasks.ts` — Task Registry

**Purpose**: Registry of all task types, mirrors tools.ts pattern.

**Functions**: `getAllTasks()`, `getTaskByType(type)`
**Registered**: LocalShellTask, LocalAgentTask, RemoteAgentTask, DreamTask, LocalWorkflowTask (gated), MonitorMcpTask (gated)

---

## 8. `src/commands.ts` — Slash Commands (~767 lines)

**Purpose**: Registry of ~70+ slash commands for the CLI.

**Key Functions**:
- `getCommands()` — Memoized, returns all commands respecting feature flags
- `INTERNAL_ONLY_COMMANDS` — Stripped from external builds

**Notable Patterns**:
- Heavy conditional `require()` for feature-gated commands
- Skills, plugins, dynamic skill dirs contribute additional commands at runtime
- Lazy shim for `/insights` (113KB module)

---

## 9. `src/cost-tracker.ts` — Cost Tracking

**Purpose**: Tracks API costs, token usage, duration metrics. Provides formatting and session persistence.

**Key Functions**:
- `addToTotalSessionCost()` — Accumulates per-model costs including advisor overhead
- `formatTotalCost()` — Formatted display
- `saveCurrentSessionCosts()` / `restoreCostStateForSession()` — Persist to project config

**Key Types**: `StoredCostState` — Serialized: totalCostUSD, durations, line changes, model usage

---

## 10. `src/setup.ts` — Provider Setup

**Purpose**: Environment setup before first query. Node.js version check, UDS messaging, worktree creation, terminal backup, hook config, background jobs.

**Key Functions**: `setup(cwd, permissionMode, ...)`

**Notable Patterns**:
- Security: blocks `--dangerously-skip-permissions` as root (unless sandbox)
- Background jobs: session memory, context collapse, file-change watcher, attribution hooks
- Plugin pre-fetch skipped in bare/sync-plugin-install mode
- Hook config snapshot for tamper detection

---

## 11. `src/server/types.ts` — Server Types

**Key Types**:
- `ServerConfig` — port, host, authToken, idleTimeout, maxSessions, workspace
- `SessionState` — `'starting' | 'running' | 'detached' | 'stopping' | 'stopped'`
- `SessionInfo` — id, status, createdAt, workDir, process
- `SessionIndexEntry` — Persistent session metadata for cross-restart resume
- `connectResponseSchema` — Zod schema for POST /sessions response

---

## 12. `src/server/createDirectConnectSession.ts`

**Purpose**: Creates session on direct-connect server via POST /sessions.

**Key Types**: `DirectConnectError` — Custom error for connection failures
**Pattern**: Zod response validation, typed error throwing

---

## 13. `src/server/directConnectManager.ts`

**Purpose**: WebSocket connection manager for direct-connect server. Bidirectional message passing, permission requests, interrupt signals.

**Key Class**: `DirectConnectSessionManager`
- `connect()`, `sendMessage()`, `respondToPermissionRequest()`, `sendInterrupt()`, `disconnect()`

**Key Types**:
- `DirectConnectConfig` — `{ serverUrl, sessionId, wsUrl, authToken? }`
- `DirectConnectCallbacks` — `{ onMessage, onPermissionRequest, onConnected?, onDisconnected?, onError? }`

**Notable**: Newline-delimited JSON on WebSocket; filters control messages from SDK forwarding

---

## 14. `src/state/AppState.tsx` — React State Provider

**Purpose**: React context provider for global AppState store.

**Key Exports**:
- `AppStateProvider` — Creates store, wraps in AppStoreContext + MailboxProvider + VoiceProvider
- `useAppState(selector)` — Slice subscription via `useSyncExternalStore`
- `useSetAppState()` — setState without subscription
- `useAppStateMaybeOutsideOfProvider()` — Safe version returns undefined outside provider

**Notable**: React Compiler optimized; selector ref pattern avoids re-render loops

---

## 15. `src/state/store.ts` — Generic Store

**Purpose**: Minimal reactive store (similar to Zustand).

**Key Types**: `Store<T>` — `{ getState, setState, subscribe }`
**Key Function**: `createStore<T>(initialState, onChange?)`
**Pattern**: `Object.is` comparison in setState — same reference = no notification

---

## 16. `src/state/AppStateStore.ts` — AppState Type (~400 lines of types)

**Purpose**: Complete AppState type — central state tree.

**Key Fields**:
- **Core**: settings, verbose, mainLoopModel, toolPermissionContext
- **UI**: expandedView, isBriefOnly, footerSelection, coordinatorTaskIndex
- **Tasks**: tasks, agentNameRegistry, foregroundedTaskId
- **MCP**: mcp.clients, mcp.tools, mcp.commands, mcp.resources, mcp.pluginReconnectKey
- **Plugins**: plugins.enabled, plugins.disabled, plugins.errors, plugins.installationStatus
- **Multi-agent**: teamContext, standaloneAgentContext, inbox
- **Bridge/Remote**: replBridge*, remoteConnectionStatus
- **Speculation**: speculation (tagged union: idle | active)
- **Features**: fastMode, advisorModel, effortValue, thinkingEnabled
- **Computer Use**: computerUseMcpState (display, apps, grants)
- **REPL VM**: replContext (persistent VM context)

---

## 17. `src/services/api/` — API Client Layer

**Key Files**:

### `claude.ts` — Anthropic API Integration
- Constructs messages with beta headers, tool schemas, system prompts
- Handles streaming, token counting, cache management, model routing
- Beta headers: context management, effort, fast mode, prompt caching, structured outputs, task budgets

### `client.ts` — API Client Factory
- Creates configured `Anthropic` SDK instances
- Multi-provider: first-party, AWS Bedrock, GCP Vertex AI, Azure Foundry
- OAuth refresh, proxy config, custom headers

### `bootstrap.ts` — Initial Config Fetch
- Fetches from `/api/claude_cli/bootstrap`
- Caches additional model options from server

### Other: `errors.ts`, `withRetry.ts`, `filesApi.ts`, `logging.ts`, `agentRouting.ts`, `providerConfig.ts`

---

## 18. `src/services/mcp/` — Model Context Protocol

### `types.ts` — MCP Types
- `McpServerConfig` — Union of transports: stdio, sse, sse-ide, http, ws, ws-ide, sdk, claudeai-proxy
- `MCPServerConnection` — Union: Connected | Failed | NeedsAuth | Pending | Disabled
- `ScopedMcpServerConfig` — Config + scope (local/user/project/dynamic/enterprise/claudeai/managed)
- `MCPCliState` — Serialized state for CLI commands

### `client.ts` — MCP Client Management
- Manages connections, discovers tools/commands/resources
- Tool normalization and name mapping

### Other: `config.ts`, `auth.ts`, `doctor.ts`, `officialRegistry.ts`, `channelPermissions.ts`, `elicitationHandler.ts`, `xaaIdpLogin.ts`

---

## 19. `src/services/plugins/` — Plugin System

**Key Files**:
- `pluginCliCommands.ts` — CLI commands for plugin management
- `PluginInstallationManager.ts` — Background installation and marketplace management
- `pluginOperations.ts` — Core operations: load, enable, disable, validate

---

## 20. `src/skills/bundledSkills.ts` — Bundled Skill System

**Purpose**: Defines/registers skills shipping with the CLI binary.

**Key Types**: `BundledSkillDefinition` — name, description, aliases, whenToUse, allowedTools, model, getPromptForCommand, files?, context?

**Key Functions**: `registerBundledSkill()`, `getBundledSkills()`, `getBundledSkillExtractDir()`

**Notable**: Skills with `files` get lazy extraction (secure: O_NOFOLLOW|O_EXCL, 0o600 modes)

---

## 21. `src/skills/bundled/index.ts` — Bundled Skill Registration

**Registered Skills**: updateConfig, keybindings, debug, simplify, batch, loop
**Feature-gated**: dream (KAIROS), hunter (REVIEW_ARTIFACT), scheduleRemoteAgents (AGENT_TRIGGERS_REMOTE), claudeApi (BUILDING_CLAUDE_APPS), claudeInChrome (auto-enable), runSkillGenerator (RUN_SKILL_GENERATOR)

---

## 22. `src/tools/BashTool/` — Shell Command Execution

**Key Files**:
- `BashTool.tsx` — Main implementation: executes shell commands, sandboxing, timeout, progress
- `bashPermissions.ts` — Permission checking
- `bashSecurity.ts` — Security validations
- `commandSemantics.ts` — Result interpretation
- `readOnlyValidation.ts` — Read-only classification
- `sedEditParser.ts` — Sed edit detection
- `shouldUseSandbox.ts` — Sandbox decision
- `prompt.ts`, `UI.tsx` — Description and rendering

**Notable**: `isSearchOrReadBashCommand()` classifies for UI collapsing; background task auto-promotion; device file blocking; sandbox integration

---

## 23. `src/tools/FileEditTool/` — File Editing

**Key Files**:
- `FileEditTool.ts` — In-place editing with diff computation
- `types.ts` — Input (file_path + old_string + new_string) / Output (patch data) schemas
- `utils.ts` — String matching, patch generation, quote preservation
- `constants.ts`, `prompt.ts`, `UI.tsx`

**Notable**: 1 GiB max; concurrent edit protection; LSP diagnostic tracking; file history for undo

---

## 24. `src/tools/FileReadTool/` — File Reading

**Key Files**:
- `FileReadTool.ts` — Line ranges, image processing, PDF, notebooks
- `imageProcessor.ts` — Image detection, resizing, format conversion
- `limits.ts` — Token/byte limits

**Notable**: Device file blocking; PDF page extraction; image resize with token budget; `FILE_UNCHANGED_STUB` optimization; notebook cell reading

---

## 25. `src/tools/FileWriteTool/` — File Writing

**Key Files**: `FileWriteTool.ts`, `prompt.ts`, `UI.tsx`
**Notable**: Strict schema `{ file_path, content }`; git diff computation; same protections as FileEditTool

---

## 26. `src/tools/AgentTool/` — Sub-Agent Spawning

**Key Files**:
- `AgentTool.tsx` — Spawns sub-agents (local, remote, in-process teammate, fork)
- `runAgent.ts` — Agent execution loop
- `forkSubagent.ts` — Fork-based isolation
- `resumeAgent.ts` — Resume background agents
- `loadAgentsDir.ts` — Load from `.claude/agents/`
- `builtInAgents.ts`, `agentColorManager.ts`, `agentToolUtils.ts`, `agentMemory.ts`

**Notable**: Multiple isolation modes (worktree/remote/fork/in-process); auto-background after 120s; multi-agent with name-based addressing; coordinator mode integration

---

## 27. `src/tools/MCPTool/` — MCP Tool Wrapper

**Key Files**: `MCPTool.ts`, `prompt.ts`, `UI.tsx`, `classifyForCollapse.ts`

**Notable**: Passthrough input schema; `isMcp: true` flag; base implementation overridden by mcpClient.ts with actual name/schema/call; rich content support (string + content-block-array)

---

## 28. `src/tools/WebSearchTool/` — Web Search

**Key Files**: `WebSearchTool.ts`, `prompt.ts`, `UI.tsx`, `providers/` (pluggable providers)

**Notable**: Multi-provider (Anthropic server-side, Codex, custom); domain filtering; Firecrawl integration

---

## 29. `src/tools/WebFetchTool/` — Web Content Fetching

**Key Files**: `WebFetchTool.ts`, `utils.ts` (URL→markdown), `preapproved.ts`

**Notable**: Firecrawl for JS-rendered pages; prompt-based extraction; pre-approved host list; permission from URL hostname

---

## 30. `src/tools/GrepTool/` — Content Search

**Key Files**: `GrepTool.ts`, `prompt.ts`, `UI.tsx`

**Notable**: Direct ripgrep integration; rich params (pattern, path, glob, output_mode, context, type); concurrency-safe; read-only

---

## 31. `src/tools/GlobTool/` — File Pattern Matching

**Key Files**: `GlobTool.ts`, `prompt.ts`, `UI.tsx`

**Notable**: Concurrency-safe; read-only; results truncated at 100 files; duration tracking

---

## 32. `src/tools/SkillTool/` — Skill Invocation

**Key Files**: `SkillTool.ts`, `constants.ts`, `prompt.ts`, `UI.tsx`

**Notable**: Discovers commands from all sources; frontmatter parsing for metadata; fork-based execution isolation; plugin identifier parsing; skill usage telemetry

---

## 33. `src/tools/WorkflowTool/` — Workflow Execution

Feature-gated tool for predefined workflow scripts. Only `constants.ts` in base; implementation loaded via conditional require when `WORKFLOW_SCRIPTS` feature enabled.

---

## 34. `src/proto/openclaude.proto` — gRPC Protocol

**Purpose**: Bidirectional streaming RPC contract.

**Key Messages**:
- `ClientMessage` — ChatRequest | UserInput | CancelSignal
- `ServerMessage` — TextChunk | ToolCallStart | ToolCallResult | ActionRequired | FinalResponse | ErrorResponse
- `ActionRequired` — Permission prompt: CONFIRM_COMMAND or REQUEST_INFORMATION

**Notable**: `tool_use_id` correlation; session persistence via session_id; clean error model

---

## 35. `src/voice/voiceModeEnabled.ts` — Voice Feature Gate

**Key Functions**:
- `isVoiceGrowthBookEnabled()` — Kill-switch check (default: enabled)
- `hasVoiceAuth()` — Requires Anthropic OAuth
- `isVoiceModeEnabled()` — Combined: auth + GrowthBook

**Pattern**: Positive ternary for dead code elimination

---

## 36. `src/services/voice.ts` — Voice Recording

**Purpose**: Audio recording for push-to-talk. Native audio capture (cpal) with SoX/arecord fallback.

**Key Features**: Lazy NAPI module loading; platform-specific (CoreAudio/ALSA/WASAPI); silence detection; ALSA device probing

---

## 37. `src/services/voiceStreamSTT.ts` — Voice Stream STT

**Purpose**: WebSocket client for Anthropic voice_stream STT endpoint.

**Key Types**: `VoiceStreamCallbacks`, `VoiceStreamConnection`, `FinalizeSource`

**Notable**: Keep-alive every 8s; multi-layered timeout (noData 1.5s, safety 5s); OAuth WebSocket; JSON control + binary audio protocol

---

## 38. `src/screens/REPL.tsx` — Main Interactive UI

**Purpose**: Main React component for interactive REPL. Most complex UI component.

**Key Features**: Virtual scrolling message list; prompt input with vim mode; tool permission dialogs; background task navigation; session resume/compact; voice integration; direct connect; cost thresholds; swarm init; IDE selection

**Connections**: Uses hooks for every subsystem: useMergedTools, useMergedCommands, useMergedClients, useCanUseTool, useAppState, useMainLoopModel, useManagePlugins, useQueueProcessor, useMailboxBridge, etc.

---

## 39. `src/services/settingsSync/` — Settings Synchronization

**Key Files**:
- `index.ts` — Upload local to remote (interactive CLI), download remote to local (CCR). Incremental sync.
- `types.ts` — Sync data schemas, SYNC_KEYS

**Notable**: 500KB file limit; 10s timeout; 3 retries; cached download promise for dedup

---

## 40. `src/services/compact/` — Context Compaction

**Key Files**:
- `compact.ts` — Main logic: summarize history, create boundaries, preserve essential context
- `autoCompact.ts` — Auto-trigger on token usage
- `microCompact.ts` — Lightweight context reduction
- `snipCompact.ts` — Snip-based compaction (gated)
- `postCompactCleanup.ts` — Post-compaction cleanup

**Notable**: Pre/post compact hooks; compact boundary messages; fork-based agent for summarization; token budget management

---

## 41. `src/services/tools/` — Tool Execution Infrastructure

**Key Files**:
- `StreamingToolExecutor.ts` — Executes tools with concurrency control. Concurrent-safe run in parallel; non-concurrent get exclusive access. Results buffered in order.
- `toolExecution.ts` — Individual tool execution
- `toolOrchestration.ts` — Higher-level coordination
- `toolHooks.ts` — Pre/post execution hooks

**Key Class**: `StreamingToolExecutor`
- `addTool()`, `discard()`, TrackedTool with status: queued | executing | completed | yielded
- Sibling abort controller kills subprocesses when one Bash tool errors

---

## Architecture Overview

```
main.tsx (entry point)
├── setup.ts (environment setup)
├── commands.ts (slash command registry)
├── tools.ts (tool registry)
│   ├── Tool.ts (tool interface + buildTool factory)
│   └── tools/* (individual tool implementations)
│       ├── BashTool (shell execution)
│       ├── FileEditTool / FileReadTool / FileWriteTool (file ops)
│       ├── AgentTool (sub-agent spawning)
│       ├── MCPTool (MCP protocol tools)
│       ├── WebSearchTool / WebFetchTool (web operations)
│       ├── GrepTool / GlobTool (search operations)
│       ├── SkillTool (skill invocation)
│       └── WorkflowTool (workflow execution)
├── QueryEngine.ts (query lifecycle)
├── Task.ts / tasks.ts (task system)
├── context.ts (LLM context assembly)
├── cost-tracker.ts (usage/cost tracking)
├── state/
│   ├── AppStateStore.ts (AppState type)
│   ├── AppState.tsx (React provider)
│   └── store.ts (generic store)
├── server/ (direct-connect session management)
├── services/
│   ├── api/ (Anthropic/Bedrock/Vertex API clients)
│   ├── mcp/ (Model Context Protocol)
│   ├── plugins/ (plugin system)
│   ├── compact/ (context compaction)
│   ├── tools/ (tool execution infrastructure)
│   ├── settingsSync/ (cross-device sync)
│   └── voice.ts + voiceStreamSTT.ts (voice input)
├── skills/ (skill system)
├── proto/ (gRPC protocol)
├── screens/REPL.tsx (interactive UI)
└── voice/ (voice mode feature gating)
```

### Key Architectural Patterns

1. **Feature Gating**: `feature('FLAG')` + conditional `require()` enables dead code elimination
2. **Tool System**: `Tool` interface + `buildTool()` factory; `tools.ts` manages assembly/filtering
3. **State Management**: Generic `Store<T>` + React `useSyncExternalStore` for efficient slice subscriptions
4. **Permission System**: `ToolPermissionContext` (immutable rules) + `canUseTool()` + tool-specific `checkPermissions()` — layered security
5. **Task System**: Background tracking with disk-based output, type-prefixed IDs, lifecycle management
6. **MCP Integration**: Pluggable protocol with multiple transports, OAuth, resource management
7. **Multi-Agent**: Agent spawning with worktree/remote/fork isolation, team context, coordinator mode
8. **Context Management**: CLAUDE.md, git status, memory files, compaction for efficient context window usage
