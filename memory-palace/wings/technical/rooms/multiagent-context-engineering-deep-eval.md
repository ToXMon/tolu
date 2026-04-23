# Deep Evaluation: Multi-Agent Context Engineering for Agent Zero

Critical analysis layer on top of the gap analysis document.
Date: 2026-04-22 | Status: Deep Evaluation

---

## Corrections to the Gap Analysis

The initial gap analysis (multiagent-context-engineering-gap-analysis.md) correctly identifies the three patterns and their gaps but makes several architectural mistakes in the proposed plugin design.

### Correction 1: Don't Duplicate call_subordinate — Extend It

**Problem**: The `context_delegate` tool (Component 4 in the analysis) duplicates nearly all of `call_subordinate.py`'s logic: agent creation, profile setting, subordinate registration, monologue execution, topic sealing. This creates a maintenance burden and diverges from core framework updates.

**Fix**: Use the `@extensible` decorator on `Delegation.execute`. The path is:
```
_functions/tools/call_subordinate/Delegation/execute/start/_10_context_bridge.py
```

This hook fires BEFORE `Delegation.execute()` runs. It can modify `data["kwargs"]` (the args passed to execute), which includes `message` and `reset`. So we can rewrite the message into a structured packet BEFORE the subordinate receives it, without duplicating any agent creation logic.

**Why the analysis missed this**: It proposed `tool_execute_before/_10_build_context_packet.py` as a named extension hook, but the agent sets `_context_bridge_mode` in `agent.data` which requires a separate tool to set. This is fragile — it depends on the LLM using `context_delegate` instead of `call_subordinate`. The `@extensible` approach works regardless of which tool the LLM calls.

### Correction 2: Model Override Should Use _model_config Plugin

**Problem**: The `model_override.py` helper (Component in analysis) hardcodes model aliases and sets `config.additional["model_override"]`. But the actual model resolution happens in `/a0/plugins/_model_config/extensions/python/_functions/agent/Agent/get_chat_model/start/_10_model_config.py`, which reads from plugin config, not `config.additional`.

**Fix**: Instead of a separate helper, the `@extensible` pre-hook on `Delegation.execute` should:
1. Read the model from the delegation args
2. Set a per-agent override in `agent.data["_model_override"]`
3. Register an `agent_init` extension that reads this override and configures the model

OR better: create a dedicated `@extensible` hook on `Agent.get_chat_model` for the subordinate, which reads from `agent.data["_model_override"]`. This is exactly how the existing `_model_config` plugin works.

### Correction 3: Context Rot Is Bidirectional

**Problem**: The analysis focuses on context rot in the superior ("long conversation degrades attention") but misses that the subordinate ALSO accumulates context rot during its own monologue loop.

**Insight from Cognition**: The review loop works because the reviewer starts clean. But if the reviewer loops for 20+ iterations reading files and running tools, it accumulates its own context rot. The fix isn't just clean starting context — it's also **iteration budgeting**.

**Fix**: The `@extensible` pre-hook should set a `max_iterations` limit on the subordinate's monologue loop. This can be done via `agent.data["_max_iterations"]`, checked by a `message_loop_start` extension.

### Correction 4: Task Board Sequential-Only Problem

**Problem**: The task board (Component 3) correctly uses `AgentContext.data` as shared state, but `call_subordinate` only supports ONE subordinate at a time. The manager can't spawn Child 1, then spawn Child 2 while Child 1 runs.

**Fix for now**: Accept sequential execution. The task board still adds value because:
1. It provides structured task decomposition
2. Children can see completed siblings' results
3. The manager gets a clean aggregation point

**Future**: Parallel spawning requires changes to `call_subordinate.py` core. This is Phase 4 and correctly identified in the analysis.

---

## Revised Architecture: `_context_bridge` Plugin

### Core Insight

The plugin should be **invisible to the LLM** when possible. Instead of requiring the LLM to call `context_delegate` instead of `call_subordinate`, the plugin should intercept `call_subordinate` and enhance it automatically based on profile and context.

### Revised File Structure

```
/a0/usr/plugins/_context_bridge/
├── plugin.yaml
├── default_config.yaml
├── README.md
│
├── helpers/
│   ├── __init__.py
│   ├── packets.py              # Context packet builders (keep from analysis)
│   └── task_board.py            # Shared task board (keep from analysis)
│
├── tools/
│   └── task_board_tool.py       # Agent-facing task board operations
│
│
├── extensions/python/
│   │
│   │  # PATTERN 1 & 2: Intercept delegation
│   ├── _functions/tools/call_subordinate/Delegation/execute/start/
│   │   └── _10_context_bridge.py      # Pre-hook: build packet, set model override
│   │
│   │  # PATTERN 1: Parse structured results
│   ├── tool_execute_after/
│   │   └── _10_parse_subordinate_result.py  # Parse review/consult results
│   │
│   │  # PATTERN 3: Task board injection
│   ├── message_loop_prompts_after/
│   │   └── _10_inject_task_board.py   # Inject task board into every agent
│   │
│   │  # Iteration budgeting (anti-context-rot)
│   ├── message_loop_start/
│   │   └── _20_check_iteration_budget.py  # Enforce max iterations on subordinates
│   │
│   │  # Model override for subordinates
│   ├── _functions/agent/Agent/get_chat_model/start/
│   │   └── _10_subordinate_model_override.py  # Read model override from agent.data
│   │
│   │  # Agent profile for reviewer
│   └── system_prompt/
│       └── _20_reviewer_prompt.py     # Inject review-specific instructions when profile=reviewer
│
├── prompts/
│   ├── agent.system.tool.task_board_tool.md
│   ├── context_bridge.review_packet.md
│   ├── context_bridge.consult_packet.md
│   ├── context_bridge.task_decomposition.md
│   └── context_bridge.task_board_inject.md
│
├── agents/
│   └── reviewer/
│       ├── agent.yaml               # Reviewer profile
│       └── prompts/
│           └── agent.system.main.role.md  # Review-specific role
│
└── webui/
    └── config.html
```

### Key Differences from Original Analysis

| Aspect | Original Analysis | Revised Design |
|--------|------------------|----------------|
| New delegation tool | `context_delegate.py` (duplicates call_subordinate) | `@extensible` pre-hook on Delegation.execute |
| Model override | Separate helper with hardcoded aliases | `@extensible` hook on Agent.get_chat_model |
| Trigger mechanism | LLM must call `context_delegate` | Automatic when profile matches or args contain mode |
| Context rot | Only addressed at transfer time | Iteration budgeting on subordinates |
| Reviewer profile | Generic `developer` profile | Dedicated `reviewer` profile with clean-context instructions |
| Tool count | 2 new tools (context_delegate + task_board) | 1 new tool (task_board only) |

---

## Implementation: The @extensible Pre-Hook

This is the single most important file. It intercepts `call_subordinate` before it runs.

```python
# extensions/python/_functions/tools/call_subordinate/Delegation/execute/start/
# _10_context_bridge.py

from helpers.extension import Extension
from helpers.plugins import get_plugin_config


class ContextBridgeHook(Extension):
    """
    Intercepts call_subordinate.execute() BEFORE it runs.
    
    Detects delegation mode from profile name or explicit args,
    then rewrites the message into a structured context packet.
    
    Also handles:
    - Model override for smart-friend pattern
    - Iteration budgeting for anti-context-rot
    - Reviewer profile auto-detection
    """
    
    async def execute(self, **kwargs):
        data = kwargs.get("data", {})
        if not data:
            return
        
        fn_args = data.get("args", [])
        fn_kwargs = data.get("kwargs", {})
        
        # The Delegation.execute receives: self, message="", reset="", **kwargs
        # fn_kwargs has: message, reset, profile, and any custom args
        
        config = get_plugin_config("_context_bridge", self.agent)
        if not config or not config.get("context_bridge_enabled", True):
            return
        
        profile = fn_kwargs.get("profile", fn_kwargs.get("agent_profile", ""))
        message = fn_kwargs.get("message", "")
        
        # Detect mode
        mode = self._detect_mode(profile, fn_kwargs)
        if not mode:
            return  # Standard delegation, no enhancement
        
        # Build packet
        from usr.plugins._context_bridge.helpers.packets import build_packet_from_agent_state
        
        packet = build_packet_from_agent_state(
            agent=self.agent,
            mode=mode,
            artifact=fn_kwargs.get("artifact", ""),
            question=fn_kwargs.get("question", message),
            task_description=fn_kwargs.get("task_description", message),
            criteria=fn_kwargs.get("criteria", []),
            constraints=fn_kwargs.get("constraints", []),
            focus_areas=fn_kwargs.get("focus_areas", []),
            attempted=fn_kwargs.get("attempted", []),
            error_context=fn_kwargs.get("error_context", ""),
        )
        
        # Rewrite the message — the subordinate will receive this instead
        fn_kwargs["message"] = packet
        data["kwargs"] = fn_kwargs
    
    def _detect_mode(self, profile: str, kwargs: dict) -> str:
        """Detect delegation mode from profile or explicit mode arg."""
        # Explicit mode
        mode = kwargs.get("mode", "")
        if mode:
            return mode
        
        # Profile-based detection
        profile_modes = {
            "reviewer": "review",
            "review": "review",
        }
        return profile_modes.get(profile.lower(), "")
    
    def _set_model_override(self, kwargs: dict):
        """Set model override for smart-friend pattern."""
        model = kwargs.get("model", "")
        if model:
            # Store in agent.data for the get_chat_model hook to read
            # This applies to the SUBORDINATE being created
            self.agent.data["_subordinate_model_override"] = model
    
    def _set_iteration_budget(self, kwargs: dict):
        """Set iteration budget for anti-context-rot."""
        max_iter = kwargs.get("max_iterations", 0)
        if max_iter:
            self.agent.data["_subordinate_max_iterations"] = max_iter
        elif kwargs.get("mode", "") == "review":
            # Default budget for review: 10 iterations
            self.agent.data["_subordinate_max_iterations"] = 10
```

---

## Implementation: Iteration Budget

```python
# extensions/python/message_loop_start/_20_check_iteration_budget.py

from helpers.extension import Extension
from helpers.tool import Response


class CheckIterationBudget(Extension):
    """
    Enforces maximum iteration count on subordinate agents.
    
    Prevents context rot by forcing the subordinate to produce
    a response within a budget of iterations.
    
    The budget is set by the @extensible pre-hook on Delegation.execute
    and stored in agent.data["_max_iterations"].
    """
    
    async def execute(self, loop_data=None, **kwargs):
        if not self.agent or not loop_data:
            return
        
        max_iter = self.agent.data.get("_max_iterations", 0)
        if max_iter <= 0:
            return  # No budget set
        
        if loop_data.iteration >= max_iter:
            # Force the agent to respond on this iteration
            # by injecting a nudge into extras_temporary
            loop_data.extras_temporary["_budget_warning"] = (
                "## ITERATION BUDGET EXHAUSTED\n"
                f"You have reached your maximum of {max_iter} iterations.\n"
                "You MUST call the response tool NOW with your current findings.\n"
                "Do not attempt any more tool calls. Summarize what you have."
            )
```

---

## Implementation: Model Override Hook

```python
# extensions/python/_functions/agent/Agent/get_chat_model/start/
# _10_subordinate_model_override.py

from helpers.extension import Extension


class SubordinateModelOverride(Extension):
    """
    When a subordinate agent is created with a model override,
    this hook reads the override from agent.data and short-circuits
    the model resolution.
    
    Works with the existing _model_config plugin by setting
    the model before _model_config's hook runs.
    """
    
    async def execute(self, **kwargs):
        if not self.agent:
            return
        
        override = self.agent.data.get("_model_override", "")
        if not override:
            return
        
        # Resolve aliases
        aliases = {
            "frontier": "openai/gpt-4.1",
            "fast": "openai/gpt-4.1-mini",
            "smart": "anthropic/claude-sonnet-4-20250514",
            "reasoning": "openai/o3",
        }
        resolved = aliases.get(override, override)
        
        # Set in config.additional so _model_config picks it up
        if hasattr(self.agent, 'config') and self.agent.config:
            self.agent.config.additional["chat_model"] = resolved
```

---

## Implementation: The Reviewer Profile

```yaml
# agents/reviewer/agent.yaml
title: Reviewer
description: Agent specialized in clean-context code and design review.
context: Use this agent for code review, design critique, security audit, or any task
  where a fresh set of eyes on an artifact is more valuable than full conversation context.
```

```markdown
<!-- agents/reviewer/prompts/agent.system.main.role.md -->

## Your role
You are a specialized review agent. You receive artifacts (code, diffs, documents)
with NO prior conversation context. This is by design — your clean context lets you
spot issues that agents deep in a long conversation miss.

## Review Process
1. Read the artifact carefully from scratch
2. Re-discover context by examining the codebase with your tools
3. Identify issues grouped by severity: critical, high, medium, low
4. For each issue: location, description, suggestion
5. Provide a summary and confidence score

## Output Format
Always end with a JSON block:
```json
{
  "mode": "review",
  "findings": [
    {"severity": "critical", "location": "file.py:L42", "description": "...", "suggestion": "..."}
  ],
  "summary": "Brief overall assessment",
  "confidence": 0.85
}
```

## Principles
- Never assume the original author's intent — question everything
- If you don't have enough context, investigate before flagging
- Security issues always get severity bumped one level
- Prefer specific, actionable suggestions over vague warnings
```

---

## Revised Priority Phasing

### Phase 1: Review Loop (3-4 days)

Highest impact. Unlocks Cognition Pattern 1.

| Component | Hook Point | What It Does |
|-----------|-----------|-------------|
| Packet builder | `helpers/packets.py` | ReviewPacket with to_message() |
| Pre-hook | `_functions/.../Delegation/execute/start` | Detect review mode, build packet, set budget |
| Result parser | `tool_execute_after` | Parse structured findings, inject into extras |
| Iteration budget | `message_loop_start` | Force response after N iterations |
| Reviewer profile | `agents/reviewer/` | Clean-context review specialist |
| Prompt templates | `prompts/` | Review packet format, findings format |

**Verification**: Delegate a code review with `profile="reviewer"`. Confirm subordinate receives only the artifact. Confirm structured findings parse back into superior's context.

### Phase 2: Smart Friend (2-3 days)

Medium impact. Unlocks Cognition Pattern 2.

| Component | Hook Point | What It Does |
|-----------|-----------|-------------|
| Model override | `_functions/.../get_chat_model/start` | Read override from agent.data |
| Consult packet | `helpers/packets.py` | ConsultPacket with context fork |
| Mode detection | (in Phase 1 pre-hook) | Detect consult mode from args |

**Verification**: Delegate with `mode="consult", model="frontier"`. Confirm subordinate gets full context fork and runs on different model.

### Phase 3: Task Board (2-3 days)

Medium impact. Unlocks Cognition Pattern 3.

| Component | Hook Point | What It Does |
|-----------|-----------|-------------|
| Task board logic | `helpers/task_board.py` | CRUD on AgentContext.data |
| Task board tool | `tools/task_board_tool.py` | Agent-facing operations |
| Board injection | `message_loop_prompts_after` | All agents see current board state |
| Task packet | `helpers/packets.py` | TaskPacket with dependency refs |
| Task decomposition prompt | `prompts/` | Guide manager to decompose |

**Verification**: Create 3 subtasks with dependencies. Spawn children sequentially. Confirm each sees completed siblings' results via task board.

---

## Open Questions for Implementation

1. **How does the pre-hook access the subordinate's agent.data?** The `@extensible` hook on `Delegation.execute` fires in the SUPERIOR's context. The subordinate hasn't been created yet (it's created on line 24 of call_subordinate.py). So model override and iteration budget need to be set AFTER the subordinate is created. This might require also hooking `agent_init` to propagate these settings.

2. **Should the task board persist across conversations?** Currently `AgentContext.data` is ephemeral. For Cognition's manager pattern ("a week of work"), we need persistence. This could use the existing memory system or a file-based store.

3. **How to handle the profile detection for review mode?** The pre-hook checks `profile` in kwargs, but the LLM might not always pass `profile="reviewer"`. Should we also detect review intent from the message content? This risks false positives.

4. **Context fork for consult mode: how much to compress?** The analysis suggests 10K chars of history. But the utility LLM call in `_50_recall_memories.py` shows the pattern — use a utility model to summarize. Should the consult packet do the same, or is raw truncation sufficient?

---

## The Deepest Insight

Cognition's post ends with: "The open problems are all communication problems."

Agent Zero's architecture already solves the HARD part — isolated history, shared state, profile-based specialization. What's missing is the THIN LAYER of structured communication between agents:

1. **Packet format** — What shape does the message take? (ReviewPacket, ConsultPacket, TaskPacket)
2. **Response format** — What shape does the answer take? (Structured JSON findings)
3. **State sharing** — Where do agents write shared state? (Task board in AgentContext.data)
4. **Context budget** — How long should each agent run? (Iteration limits)

None of these require changes to the core framework. All four can be implemented as a single plugin with extensions at existing hook points. The plugin is a communication protocol, not a new agent architecture.
