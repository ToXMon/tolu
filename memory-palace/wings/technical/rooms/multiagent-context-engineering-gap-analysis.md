# Multi-Agent Context Engineering Gap Analysis

Agent Zero vs. Cognition AI's Three Working Patterns

Date: 2026-04-22 | Status: Design Document

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Baseline](#architecture-baseline)
3. [Gap Map](#gap-map)
4. [Plugin Design: `_context_bridge`](#plugin-design-_context_bridge)
5. [Priority Phasing](#priority-phasing)
6. [Prompt Templates](#prompt-templates)
7. [Appendix: Source Code Reference](#appendix-source-code-reference)

---

## Executive Summary

Cognition AI identified three multi-agent patterns that outperform single-agent approaches. Agent Zero's architecture partially supports one (Manager->Child), but critical gaps prevent it from matching any of the three patterns effectively. This document maps exact code paths, designs a single plugin to close all gaps, and provides implementation-ready specifications.

**Key finding**: Agent Zero shares `AgentContext` between superior and subordinate (line 24 of `call_subordinate.py`), but the subordinate receives zero structured context about *what the superior knows*. The delegation is a raw text message into a blank-slate agent. Every Cognition pattern requires richer context transfer than this.

---

## Architecture Baseline

### Current Data Flow

```
User Message
    │
    ▼
Agent0.monologue()
    │
    ├── LoopData.extras_persistent  ← memories, solutions injected here
    ├── LoopData.extras_temporary   ← per-iteration context
    │
    ├── prepare_prompt()
    │   ├── message_loop_prompts_before extensions
    │   ├── system prompt assembly
    │   ├── message_loop_prompts_after extensions  ← recall_memories runs here
    │   └── extras rendered via agent.context.extras.md template
    │
    ├── LLM call with full prompt
    │
    ├── Tool execution (if any)
    │   │   └── call_subordinate.execute()
    │   │       ├── sub = Agent(number+1, config, self.agent.context)  ← SHARES context
    │   │       ├── sub.hist_add_user_message(UserMessage(message=raw_text))  ← ONLY text
    │   │       ├── sub.monologue()  ← subordinate runs its own loop
    │   │       └── result returned to superior
    │   │
    │   └── Loop continues until response tool called
    │
    └── Response to user
```

### State Isolation Model

| Data | Scope | Shared? | Mechanism |
|------|-------|---------|-----------|
| `AgentContext.data` | Conversation | YES | Shared dict, all agents in tree |
| `Agent.data` | Single agent | NO | Per-instance dict |
| `Agent.history` | Single agent | NO | Isolated, topic-based summarization |
| `LoopData.extras_persistent` | Single loop iteration | NO | Rebuilt each iteration |
| `LoopData.extras_temporary` | Single loop iteration | NO | Cleared each iteration |

### Extension Hook Points (relevant to this analysis)

```
agent_init                        ← agent created
system_prompt                     ← building system prompt
monologue_start                   ← agent loop begins
message_loop_start                ← each iteration begins
message_loop_prompts_before       ← before prompt assembly
message_loop_prompts_after        ← after prompt assembly (memories injected here)
before_main_llm_call             ← last chance to modify prompt
tool_execute_before               ← before any tool runs
tool_execute_after                ← after any tool completes
hist_add_before                   ← before adding to history
hist_add_tool_result              ← after tool result added
message_loop_end                  ← iteration complete
monologue_end                     ← agent loop complete
process_chain_end                 ← full chain done
```

Plus `@extensible` implicit hooks:
```
_functions/agent/Agent/monologue/start|end
_functions/agent/Agent/communicate/start|end
_functions/tools/call_subordinate/Delegation/execute/start|end
_functions/agent/AgentContext/_process_chain/start|end
```

---

## Gap Map

### Pattern 1: Clean-Context Review Loop

**Cognition's Model**: Coder writes code. Reviewer reviews with ZERO shared context. Reviewer gets only the diff, re-discovers needed context from scratch. Short context = better attention = catches more nuanced issues. Coder filters review findings against original instructions.

#### Current State in Agent Zero

Agent Zero has **no mechanism** for clean-context review. Both agents share `AgentContext`, and the subordinate receives a single raw text message with no structured context about what to review or how to feed findings back.

#### Required vs. What Exists

| Requirement | Current Status | Gap |
|-------------|---------------|-----|
| Reviewer gets only the diff/artifact | Subordinate gets raw text message | **CRITICAL**: No structured context packet |
| Reviewer has zero conversation history | Subordinate has blank history | OK (already works) |
| Coder filters review findings | No mechanism for superior to process structured findings | **HIGH**: No structured response format |
| Reviewer re-discovers context independently | Subordinate has no access to file system or tools beyond what's in the message | **MEDIUM**: Tools available but not guided |
| Separate model/temperature for reviewer | Profile system exists but no review-specific config | **LOW**: Can use profile system |

#### Code Paths Requiring Modification

1. **`call_subordinate.py` line 31**: `subordinate.hist_add_user_message(UserMessage(message=message, attachments=[]))` — needs structured context packet, not raw text.

2. **`call_subordinate.py` line 24**: `sub = Agent(self.agent.number + 1, config, self.agent.context)` — shared context is fine for data but the subordinate needs a way to operate independently.

3. **New extension needed at `tool_execute_before`**: When `call_subordinate` is about to run, intercept and build a structured context packet from the superior's state.

4. **New extension needed at `tool_execute_after`**: When `call_subordinate` returns, parse structured findings and inject them into the superior's loop_data.

5. **New prompt templates**: `context_bridge.review_request.md` and `context_bridge.review_findings.md`

#### Data Flow Needed

```
Superior (Coder)
    │
    ├── Knows: full conversation, task requirements, design decisions
    │
    ├── Calls call_subordinate with mode="review"
    │   └── Context bridge intercepts at tool_execute_before
    │       ├── Extracts: diff/artifact from superior's last tool result
    │       ├── Builds: structured review packet
    │       │   ├── artifact: the code/diff to review
    │       │   ├── criteria: what to look for
    │       │   ├── constraints: known limitations
    │       │   └── NO conversation history, NO memories
    │       └── Injects as UserMessage.system_message
    │
    ▼
Subordinate (Reviewer)
    │
    ├── Receives: clean review packet only
    ├── Runs: independent analysis with tools
    ├── Produces: structured findings JSON
    │
    ▼
Superior receives findings
    │
    ├── Context bridge at tool_execute_after
    │   ├── Parses structured findings
    │   ├── Injects into loop_data.extras_temporary["review_findings"]
    │   └── Superior's next LLM call sees findings as context
    │
    └── Superior filters against original requirements
```

---

### Pattern 2: Smart Friend (Weak-to-Strong Consultation)

**Cognition's Model**: Smaller/faster model runs the loop, calls out to frontier model when stuck. Works when both models are strong. Best communication: share full context fork, ask broad questions, let smart model decide what matters.

#### Current State in Agent Zero

Agent Zero has **no model routing**. A subordinate gets the same model as configured globally (via `_model_config` plugin). There is no mechanism for a fast agent to escalate specific questions to a smarter agent with full context.

#### Required vs. What Exists

| Requirement | Current Status | Gap |
|-------------|---------------|-----|
| Fast model runs main loop | Single global model config | **CRITICAL**: No per-delegation model override |
| Escalate to stronger model | No escalation mechanism | **CRITICAL**: No escalation trigger |
| Share full context fork | Context is shared but not forked | **HIGH**: No context snapshot mechanism |
| Ask broad questions | Subordinate gets narrow task message | **MEDIUM**: Message format too restrictive |
| Smart model decides what matters | No mechanism for subordinate to indicate relevance | **MEDIUM**: No structured response with confidence |

#### Code Paths Requiring Modification

1. **`call_subordinate.py` line 16**: `config = initialize_agent()` — needs option to override model for this specific subordinate instance.

2. **`call_subordinate.py` line 31**: Message needs to support `mode="consult"` with full context snapshot.

3. **New tool or extension**: An "escalation" mechanism where a subordinate can request stronger-model consultation mid-task.

4. **`agent.py` `AgentConfig`**: Needs optional model override fields.

5. **New prompt template**: `context_bridge.consult_request.md`

#### Data Flow Needed

```
Fast Agent (main loop)
    │
    ├── Hits complex problem
    ├── Calls call_subordinate with mode="consult", model="frontier"
    │   └── Context bridge:
    │       ├── Snapshots: full conversation history (compressed)
    │       ├── Snapshots: all extras_persistent
    │       ├── Snapshots: current loop_data state
    │       ├── Builds: consultation packet
    │       │   ├── context_snapshot: compressed history
    │       │   ├── question: specific problem
    │       │   ├── attempted: what was tried
    │       │   └── full_extras: all injected context
    │       └── Subordinate runs with frontier model
    │
    ▼
Strong Agent (consultant)
    │
    ├── Receives: full context fork
    ├── Decides: what's relevant from the context
    ├── Provides: targeted answer with reasoning
    │
    ▼
Fast Agent receives answer
    │
    └── Continues main loop with enhanced knowledge
```

---

### Pattern 3: Manager-to-Child Delegation

**Cognition's Model**: Manager splits work, spawns children, coordinates via internal MCP. Practical shape is map-reduce-and-manage. Hard problems: managers too prescriptive without deep codebase context, agents assume shared state when they don't, cross-agent communication doesn't happen by default.

#### Current State in Agent Zero

Agent Zero **partially supports** this pattern. The `call_subordinate` tool creates child agents with shared `AgentContext`. But cross-agent communication doesn't happen by default, managers can't coordinate multiple children, and there's no map-reduce pattern.

#### Required vs. What Exists

| Requirement | Current Status | Gap |
|-------------|---------------|-----|
| Manager splits work | Manual via prompt, no structured task decomposition | **MEDIUM**: Relies on LLM to decompose |
| Spawn multiple children | Sequential only, one subordinate at a time | **HIGH**: No parallel child spawning |
| Children share state | AgentContext.data is shared | OK (partially works) |
| Cross-agent communication | No mechanism | **CRITICAL**: Children can't talk to each other |
| Map-reduce coordination | No mechanism | **CRITICAL**: No result aggregation |
| Task status tracking | No mechanism | **HIGH**: No task board/state tracking |

#### Code Paths Requiring Modification

1. **`call_subordinate.py`**: Currently one subordinate at a time. Need parallel spawning capability.

2. **`AgentContext.data`**: Already shared, but needs structured keys for inter-agent communication.

3. **New tool**: `task_board` — shared task state accessible to all agents.

4. **New extension**: `message_loop_prompts_after` — inject task board state into each agent's context.

5. **New prompt templates**: Task decomposition, result aggregation, and coordination instructions.

#### Data Flow Needed

```
Manager Agent
    │
    ├── Decomposes task into subtasks
    ├── Writes subtasks to shared task_board (in AgentContext.data)
    │
    ├── Spawns Child 1
    │   ├── Child reads task_board, claims subtask
    │   ├── Child executes, writes results to task_board
    │   └── Child signals completion
    │
    ├── Spawns Child 2 (or parallel)
    │   ├── Child reads task_board, claims subtask
    │   ├── Can see Child 1's results (shared state)
    │   ├── Child executes, writes results to task_board
    │   └── Child signals completion
    │
    ▼
Manager Agent
    │
    ├── Reads all results from task_board
    ├── Aggregates, resolves conflicts
    └── Produces final output
```

---

## Plugin Design: `_context_bridge`

### Overview

A single plugin that addresses all three patterns through four components:

1. **Context Packets** — Structured data transfer between agents
2. **Context Bridge Extension** — Intercepts delegation, builds/injects context
3. **Task Board** — Shared state for multi-agent coordination
4. **Delegation Enhancer** — Enhanced call_subordinate with modes and model override

### File Structure

```
/a0/usr/plugins/_context_bridge/
├── plugin.yaml
├── default_config.yaml
├── README.md
│
├── helpers/
│   ├── __init__.py
│   ├── packets.py              # Context packet builders
│   ├── task_board.py            # Shared task board logic
│   └── model_override.py        # Per-delegation model config
│
├── tools/
│   ├── context_delegate.py      # Enhanced delegation tool (replaces call_subordinate usage)
│   └── task_board_tool.py       # Task board read/write tool for agents
│
├── extensions/
│   └── python/
│       ├── tool_execute_before/
│       │   └── _10_build_context_packet.py   # Intercept call_subordinate, inject context
│       ├── tool_execute_after/
│       │   └── _10_parse_subordinate_result.py # Parse structured results from subordinate
│       ├── message_loop_prompts_after/
│       │   └── _10_inject_task_board.py       # Inject task board state into agent context
│       ├── monologue_end/
│       │   └── _10_publish_results.py         # Publish agent results to task board
│       └── _functions/
│           └── tools/call_subordinate/Delegation/execute/start/
│               └── _10_enhanced_delegation.py  # Pre-hook for call_subordinate
│
├── prompts/
│   ├── agent.system.tool.context_delegate.md
│   ├── agent.system.tool.task_board_tool.md
│   ├── context_bridge.review_packet.md
│   ├── context_bridge.consult_packet.md
│   ├── context_bridge.task_decomposition.md
│   ├── context_bridge.review_findings_format.md
│   └── context_bridge.task_board_inject.md
│
└── webui/
    └── config.html              # Settings for context bridge
```

### plugin.yaml

```yaml
name: _context_bridge
title: Context Bridge
description: Structured context transfer between agents. Implements Cognition AI's three multi-agent patterns.
version: 1.0.0
settings_sections:
  - agent
per_project_config: false
per_agent_config: false
```

### default_config.yaml

```yaml
# Context Bridge Settings
context_bridge_enabled: true

# Review mode settings
review_mode_enabled: true
review_max_artifact_chars: 50000
review_include_criteria: true

# Consult mode settings
consult_mode_enabled: true
consult_snapshot_max_chars: 30000
consult_model_override: ""  # empty = use default

# Task board settings
task_board_enabled: true
task_board_max_tasks: 20
task_board_auto_claim: true

# Context packet settings
packet_max_history_chars: 10000
packet_include_extras: true
```

---

### Component 1: Context Packets (`helpers/packets.py`)

This module builds structured context packets for each delegation mode.

```python
# /a0/usr/plugins/_context_bridge/helpers/packets.py

"""
Context packet builders for multi-agent communication.

Each packet type corresponds to a Cognition AI pattern:
- ReviewPacket: Pattern 1 (clean-context review)
- ConsultPacket: Pattern 2 (smart friend consultation)
- TaskPacket: Pattern 3 (manager-child delegation)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class ReviewPacket:
    """Clean-context review packet (Pattern 1).
    
    Contains ONLY the artifact to review and review criteria.
    No conversation history, no memories, no prior context.
    """
    mode: str = "review"
    artifact: str = ""                    # The code/diff/document to review
    artifact_type: str = "code"           # code, diff, document, design
    criteria: list[str] = field(default_factory=list)  # What to look for
    constraints: list[str] = field(default_factory=list)  # Known limitations
    focus_areas: list[str] = field(default_factory=list)  # Specific areas to focus on
    severity_filter: str = "all"          # all, critical, high, medium
    
    def to_message(self) -> str:
        """Render as structured message for subordinate."""
        parts = ["## Review Task\n"]
        parts.append(f"**Mode**: Clean-context review (no prior conversation)\n")
        parts.append(f"**Artifact Type**: {self.artifact_type}\n")
        
        if self.criteria:
            parts.append("\n### Review Criteria")
            for c in self.criteria:
                parts.append(f"- {c}")
        
        if self.constraints:
            parts.append("\n### Known Constraints")
            for c in self.constraints:
                parts.append(f"- {c}")
        
        if self.focus_areas:
            parts.append("\n### Focus Areas")
            for a in self.focus_areas:
                parts.append(f"- {a}")
        
        parts.append(f"\n### Artifact to Review\n```")
        parts.append(self.artifact)
        parts.append("```")
        
        parts.append("\n### Response Format")
        parts.append("Respond with a JSON object with these fields:")
        parts.append("- `findings`: array of {severity, location, description, suggestion}")
        parts.append("- `summary`: brief overall assessment")
        parts.append("- `confidence`: 0-1 how confident you are in the review")
        
        return "\n".join(parts)


@dataclass
class ConsultPacket:
    """Smart friend consultation packet (Pattern 2).
    
    Contains FULL context fork: compressed history, all extras,
    current problem, and what was attempted.
    """
    mode: str = "consult"
    question: str = ""                    # The specific problem
    context_snapshot: str = ""            # Compressed conversation history
    attempted: list[str] = field(default_factory=list)  # What was tried
    extras_snapshot: dict[str, Any] = field(default_factory=dict)  # All injected context
    error_context: str = ""               # Error messages if relevant
    
    def to_message(self) -> str:
        """Render as structured message for consultant."""
        parts = ["## Consultation Request\n"]
        parts.append(f"**Mode**: Full-context consultation\n")
        
        parts.append(f"\n### Question\n{self.question}")
        
        if self.attempted:
            parts.append("\n### What Was Tried")
            for a in self.attempted:
                parts.append(f"- {a}")
        
        if self.error_context:
            parts.append(f"\n### Error Context\n```)\n{self.error_context}\n```")
        
        if self.context_snapshot:
            parts.append(f"\n### Conversation Context\n{self.context_snapshot}")
        
        if self.extras_snapshot:
            parts.append("\n### Additional Context")
            for key, value in self.extras_snapshot.items():
                parts.append(f"\n**{key}**:\n{value}")
        
        parts.append("\n### Response Format")
        parts.append("Provide your analysis and recommendation. Structure as:")
        parts.append("- `analysis`: your understanding of the problem")
        parts.append("- `recommendation`: specific steps to take")
        parts.append("- `code_suggestion`: any code to implement (if applicable)")
        parts.append("- `confidence`: 0-1 how confident you are")
        
        return "\n".join(parts)


@dataclass
class TaskPacket:
    """Manager-child task delegation packet (Pattern 3).
    
    Contains the specific subtask, shared context, and
    references to the task board for coordination.
    """
    mode: str = "task"
    task_id: str = ""                     # Reference to task board entry
    task_description: str = ""            # What to do
    task_context: str = ""                # Why this task exists
    shared_state_keys: list[str] = field(default_factory=list)  # AgentContext.data keys to read
    dependencies: list[str] = field(default_factory=list)  # Task IDs that must complete first
    expected_output: str = ""             # What the manager expects back
    
    def to_message(self) -> str:
        """Render as structured message for child agent."""
        parts = ["## Task Assignment\n"]
        parts.append(f"**Task ID**: {self.task_id}\n")
        parts.append(f"**Mode**: Task delegation with shared state\n")
        
        parts.append(f"\n### Task\n{self.task_description}")
        
        if self.task_context:
            parts.append(f"\n### Context\n{self.task_context}")
        
        if self.dependencies:
            parts.append(f"\n### Dependencies (complete before starting)")
            for d in self.dependencies:
                parts.append(f"- Task {d}")
        
        if self.shared_state_keys:
            parts.append(f"\n### Shared State (available in context)")
            for k in self.shared_state_keys:
                parts.append(f"- `{k}`")
        
        if self.expected_output:
            parts.append(f"\n### Expected Output\n{self.expected_output}")
        
        parts.append("\n### Instructions")
        parts.append("1. Read the task from the task board")
        parts.append("2. Check dependencies are complete")
        parts.append("3. Execute the task")
        parts.append("4. Write results back to the task board")
        parts.append("5. Return a summary to your superior")
        
        return "\n".join(parts)


def compress_history(history_text: str, max_chars: int = 10000) -> str:
    """Compress conversation history for context packets."""
    if len(history_text) <= max_chars:
        return history_text
    
    # Take first 20% (early context) and last 60% (recent context)
    # Leave 20% gap in the middle with a marker
    head_size = int(max_chars * 0.2)
    tail_size = int(max_chars * 0.6)
    
    head = history_text[:head_size]
    tail = history_text[-(len(history_text) - len(history_text) + tail_size):]
    # Simplify: just take the tail
    tail = history_text[-tail_size:]
    
    return f"{head}\n\n... [compressed: {len(history_text) - head_size - len(tail)} chars omitted] ...\n\n{tail}"


def build_packet_from_agent_state(
    agent, 
    mode: str,
    artifact: str = "",
    question: str = "",
    task_description: str = "",
    **kwargs
) -> str:
    """Build a context packet from an agent's current state.
    
    Args:
        agent: The superior agent building the packet
        mode: "review", "consult", or "task"
        artifact: For review mode - the code/diff to review
        question: For consult mode - the problem
        task_description: For task mode - the subtask
        **kwargs: Additional packet-specific fields
    
    Returns:
        Rendered packet as string
    """
    if mode == "review":
        packet = ReviewPacket(
            artifact=artifact or kwargs.get("artifact", ""),
            artifact_type=kwargs.get("artifact_type", "code"),
            criteria=kwargs.get("criteria", []),
            constraints=kwargs.get("constraints", []),
            focus_areas=kwargs.get("focus_areas", []),
            severity_filter=kwargs.get("severity_filter", "all"),
        )
        return packet.to_message()
    
    elif mode == "consult":
        history_text = agent.history.output_text()
        compressed = compress_history(
            history_text, 
            max_chars=kwargs.get("max_history_chars", 10000)
        )
        
        # Capture current extras
        extras = {}
        if hasattr(agent, 'loop_data') and agent.loop_data:
            extras = {
                k: str(v) for k, v in {
                    **agent.loop_data.extras_persistent,
                    **agent.loop_data.extras_temporary,
                }.items()
            }
        
        packet = ConsultPacket(
            question=question,
            context_snapshot=compressed,
            attempted=kwargs.get("attempted", []),
            extras_snapshot=extras,
            error_context=kwargs.get("error_context", ""),
        )
        return packet.to_message()
    
    elif mode == "task":
        packet = TaskPacket(
            task_id=kwargs.get("task_id", ""),
            task_description=task_description,
            task_context=kwargs.get("task_context", ""),
            shared_state_keys=kwargs.get("shared_state_keys", []),
            dependencies=kwargs.get("dependencies", []),
            expected_output=kwargs.get("expected_output", ""),
        )
        return packet.to_message()
    
    else:
        raise ValueError(f"Unknown packet mode: {mode}")
```

---

### Component 2: Context Bridge Extension

#### `tool_execute_before/_10_build_context_packet.py`

Intercepts `call_subordinate` before execution to inject structured context.

```python
# /a0/usr/plugins/_context_bridge/extensions/python/tool_execute_before/_10_build_context_packet.py

from helpers.extension import Extension
from usr.plugins._context_bridge.helpers.packets import build_packet_from_agent_state


class BuildContextPacket(Extension):
    """
    Intercepts call_subordinate before execution.
    
    If the agent's delegation message contains a context_bridge mode marker,
    rebuilds the message as a structured context packet.
    
    Mode markers:
    - [mode:review] — triggers ReviewPacket
    - [mode:consult] — triggers ConsultPacket  
    - [mode:task] — triggers TaskPacket
    
    These markers are set by the context_delegate tool or by the
    enhanced_delegation @extensible pre-hook.
    """
    
    async def execute(self, **kwargs):
        if not self.agent:
            return
        
        tool_name = kwargs.get("tool_name", "")
        if tool_name != "call_subordinate":
            return
        
        # Check if context bridge mode is active
        bridge_mode = self.agent.data.get("_context_bridge_mode", "")
        if not bridge_mode:
            return
        
        bridge_config = self.agent.data.get("_context_bridge_config", {})
        
        # Build the structured packet
        packet_text = build_packet_from_agent_state(
            agent=self.agent,
            mode=bridge_mode,
            **bridge_config
        )
        
        # Inject into the tool's message argument
        # The call_subordinate tool reads message from self.args
        tool_args = kwargs.get("tool_args", {})
        if isinstance(tool_args, dict):
            tool_args["message"] = packet_text
            kwargs["tool_args"] = tool_args
        
        # Clear the mode so it doesn't persist
        self.agent.data.pop("_context_bridge_mode", None)
        self.agent.data.pop("_context_bridge_config", None)
```

#### `tool_execute_after/_10_parse_subordinate_result.py`

Parses structured results from subordinates and injects into superior's context.

```python
# /a0/usr/plugins/_context_bridge/extensions/python/tool_execute_after/_10_parse_subordinate_result.py

import json
from helpers.extension import Extension
from helpers import dirty_json


class ParseSubordinateResult(Extension):
    """
    After call_subordinate returns, check if the result contains
    structured findings (JSON). If so, inject them into the
    superior's loop_data.extras_temporary for the next LLM call.
    """
    
    async def execute(self, **kwargs):
        if not self.agent:
            return
        
        tool_name = kwargs.get("tool_name", "")
        if tool_name != "call_subordinate":
            return
        
        # Get the tool result
        response = kwargs.get("response", None)
        if not response or not hasattr(response, 'message'):
            return
        
        result_text = response.message
        
        # Try to parse as JSON (structured findings)
        parsed = dirty_json.try_parse(result_text)
        if not isinstance(parsed, dict):
            return  # Not structured, leave as-is
        
        # Check if this looks like structured findings
        mode = parsed.get("mode", "")
        if mode == "review":
            findings = parsed.get("findings", [])
            summary = parsed.get("summary", "")
            confidence = parsed.get("confidence", 0)
            
            # Format for injection into superior's context
            findings_text = self._format_review_findings(findings, summary, confidence)
            
            # Inject into extras_temporary so next LLM call sees it
            if hasattr(self.agent, 'loop_data') and self.agent.loop_data:
                self.agent.loop_data.extras_temporary["review_findings"] = findings_text
        
        elif mode == "consult":
            analysis = parsed.get("analysis", "")
            recommendation = parsed.get("recommendation", "")
            code_suggestion = parsed.get("code_suggestion", "")
            confidence = parsed.get("confidence", 0)
            
            consult_text = self._format_consult_result(
                analysis, recommendation, code_suggestion, confidence
            )
            
            if hasattr(self.agent, 'loop_data') and self.agent.loop_data:
                self.agent.loop_data.extras_temporary["consult_result"] = consult_text
    
    def _format_review_findings(self, findings: list, summary: str, confidence: float) -> str:
        parts = ["## Review Findings\n"]
        parts.append(f"**Summary**: {summary}")
        parts.append(f"**Confidence**: {confidence:.0%}\n")
        
        if findings:
            # Group by severity
            by_severity = {}
            for f in findings:
                sev = f.get("severity", "info")
                by_severity.setdefault(sev, []).append(f)
            
            for severity in ["critical", "high", "medium", "low", "info"]:
                if severity in by_severity:
                    parts.append(f"\n### {severity.upper()}")
                    for finding in by_severity[severity]:
                        loc = finding.get("location", "unknown")
                        desc = finding.get("description", "")
                        sug = finding.get("suggestion", "")
                        parts.append(f"- **{loc}**: {desc}")
                        if sug:
                            parts.append(f"  - Suggestion: {sug}")
        
        return "\n".join(parts)
    
    def _format_consult_result(
        self, analysis: str, recommendation: str, 
        code_suggestion: str, confidence: float
    ) -> str:
        parts = ["## Consultation Result\n"]
        parts.append(f"**Confidence**: {confidence:.0%}\n")
        parts.append(f"### Analysis\n{analysis}")
        parts.append(f"\n### Recommendation\n{recommendation}")
        if code_suggestion:
            parts.append(f"\n### Code Suggestion\n```\n{code_suggestion}\n```")
        return "\n".join(parts)
```

---

### Component 3: Task Board (`helpers/task_board.py`)

Shared state for multi-agent coordination.

```python
# /a0/usr/plugins/_context_bridge/helpers/task_board.py

"""
Task board for multi-agent coordination (Pattern 3).

Uses AgentContext.data as the backing store, so all agents
in the conversation tree share the same task board.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"
    BLOCKED = "blocked"


TASK_BOARD_KEY = "_context_bridge_task_board"


@dataclass
class TaskEntry:
    id: str
    description: str
    status: str = TaskStatus.PENDING
    assigned_to: str = ""          # Agent name (e.g., "A1", "A2")
    result: str = ""               # Task result text
    dependencies: list[str] = field(default_factory=list)  # Task IDs
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at


def get_board(context_data: dict) -> dict[str, TaskEntry]:
    """Get the task board from shared context data."""
    raw = context_data.get(TASK_BOARD_KEY, {})
    board = {}
    for tid, entry in raw.items():
        if isinstance(entry, dict):
            board[tid] = TaskEntry(**entry)
        elif isinstance(entry, TaskEntry):
            board[tid] = entry
    return board


def save_board(context_data: dict, board: dict[str, TaskEntry]):
    """Save the task board to shared context data."""
    context_data[TASK_BOARD_KEY] = {
        tid: asdict(entry) for tid, entry in board.items()
    }


def add_task(
    context_data: dict,
    description: str,
    dependencies: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TaskEntry:
    """Add a task to the board."""
    board = get_board(context_data)
    task = TaskEntry(
        id=str(uuid.uuid4())[:8],
        description=description,
        dependencies=dependencies or [],
        metadata=metadata or {},
    )
    board[task.id] = task
    save_board(context_data, board)
    return task


def claim_task(context_data: dict, task_id: str, agent_name: str) -> TaskEntry | None:
    """Claim a pending task."""
    board = get_board(context_data)
    task = board.get(task_id)
    if not task or task.status != TaskStatus.PENDING:
        return None
    
    # Check dependencies
    for dep_id in task.dependencies:
        dep = board.get(dep_id)
        if not dep or dep.status != TaskStatus.COMPLETE:
            return None  # Dependencies not met
    
    task.status = TaskStatus.CLAIMED
    task.assigned_to = agent_name
    task.updated_at = datetime.utcnow().isoformat()
    save_board(context_data, board)
    return task


def update_task(
    context_data: dict,
    task_id: str,
    status: str | None = None,
    result: str | None = None,
) -> TaskEntry | None:
    """Update a task's status and/or result."""
    board = get_board(context_data)
    task = board.get(task_id)
    if not task:
        return None
    
    if status:
        task.status = status
    if result is not None:
        task.result = result
    task.updated_at = datetime.utcnow().isoformat()
    save_board(context_data, board)
    return task


def get_available_tasks(context_data: dict) -> list[TaskEntry]:
    """Get tasks that are pending and have met dependencies."""
    board = get_board(context_data)
    available = []
    for task in board.values():
        if task.status != TaskStatus.PENDING:
            continue
        deps_met = all(
            board.get(dep_id, TaskEntry(id="", description="")).status == TaskStatus.COMPLETE
            for dep_id in task.dependencies
        )
        if deps_met:
            available.append(task)
    return available


def get_task_summary(context_data: dict) -> str:
    """Get a text summary of the task board for injection into prompts."""
    board = get_board(context_data)
    if not board:
        return ""
    
    parts = ["## Task Board\n"]
    
    # Group by status
    by_status = {}
    for task in board.values():
        by_status.setdefault(task.status, []).append(task)
    
    for status in [TaskStatus.PENDING, TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS,
                   TaskStatus.COMPLETE, TaskStatus.FAILED, TaskStatus.BLOCKED]:
        tasks = by_status.get(status, [])
        if tasks:
            parts.append(f"\n### {status.upper()} ({len(tasks)})")
            for t in tasks:
                assigned = f" → {t.assigned_to}" if t.assigned_to else ""
                deps = f" [depends: {', '.join(t.dependencies)}]" if t.dependencies else ""
                parts.append(f"- **{t.id}**: {t.description}{assigned}{deps}")
    
    return "\n".join(parts)
```

---

### Component 4: Enhanced Delegation Tool (`tools/context_delegate.py`)

```python
# /a0/usr/plugins/_context_bridge/tools/context_delegate.py

from helpers.tool import Tool, Response


class ContextDelegate(Tool):
    """
    Enhanced delegation tool that supports Cognition AI's three patterns.
    
    Modes:
    - "review": Clean-context review (Pattern 1). Subordinate gets ONLY the artifact.
    - "consult": Full-context consultation (Pattern 2). Subordinate gets context fork.
    - "task": Task delegation with shared state (Pattern 3). Subordinate reads task board.
    - "default": Standard delegation (backward compatible).
    
    Usage from agent JSON:
    {
        "tool_name": "context_delegate",
        "tool_args": {
            "mode": "review",
            "artifact": "<code to review>",
            "criteria": ["security", "performance"],
            "profile": "developer",
            "reset": false
        }
    }
    """
    
    async def execute(self, **kwargs):
        from agent import Agent, UserMessage
        from initialize import initialize_agent
        from usr.plugins._context_bridge.helpers.packets import build_packet_from_agent_state
        from usr.plugins._context_bridge.helpers.task_board import (
            add_task, claim_task, update_task, get_board
        )
        from usr.plugins._context_bridge.helpers.model_override import apply_model_override
        
        mode = kwargs.get("mode", "default")
        message = kwargs.get("message", "")
        reset = str(kwargs.get("reset", "false")).lower().strip() == "true"
        profile = kwargs.get("profile", "")
        model = kwargs.get("model", "")
        
        # Build context packet based on mode
        if mode != "default":
            packet_kwargs = {}
            
            if mode == "review":
                packet_kwargs = {
                    "artifact": kwargs.get("artifact", message),
                    "artifact_type": kwargs.get("artifact_type", "code"),
                    "criteria": kwargs.get("criteria", []),
                    "constraints": kwargs.get("constraints", []),
                    "focus_areas": kwargs.get("focus_areas", []),
                }
            elif mode == "consult":
                packet_kwargs = {
                    "question": kwargs.get("question", message),
                    "attempted": kwargs.get("attempted", []),
                    "error_context": kwargs.get("error_context", ""),
                    "max_history_chars": kwargs.get("max_history_chars", 10000),
                }
            elif mode == "task":
                # Create task on board first
                task = add_task(
                    self.agent.context.data,
                    description=kwargs.get("task_description", message),
                    dependencies=kwargs.get("dependencies", []),
                )
                packet_kwargs = {
                    "task_id": task.id,
                    "task_description": kwargs.get("task_description", message),
                    "task_context": kwargs.get("task_context", ""),
                    "shared_state_keys": kwargs.get("shared_state_keys", []),
                    "dependencies": kwargs.get("dependencies", []),
                    "expected_output": kwargs.get("expected_output", ""),
                }
            
            message = build_packet_from_agent_state(
                agent=self.agent,
                mode=mode,
                **packet_kwargs
            )
        
        # Create or reuse subordinate
        if (
            self.agent.get_data(Agent.DATA_NAME_SUBORDINATE) is None
            or reset
        ):
            config = initialize_agent()
            
            if profile:
                config.profile = profile
            
            # Apply model override if specified
            if model:
                config = apply_model_override(config, model)
            
            sub = Agent(self.agent.number + 1, config, self.agent.context)
            sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
            self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub)
        
        subordinate: Agent = self.agent.get_data(Agent.DATA_NAME_SUBORDINATE)
        subordinate.hist_add_user_message(UserMessage(message=message, attachments=[]))
        
        # Run subordinate
        result = await subordinate.monologue()
        subordinate.history.new_topic()
        
        # If task mode, update the task board
        if mode == "task" and "task" in dir():
            update_task(
                self.agent.context.data,
                task_id=task.id,
                status="complete",
                result=result,
            )
        
        return Response(message=result, break_loop=False)
    
    def get_log_object(self):
        return self.agent.context.log.log(
            type="subagent",
            heading=f"icon://communication {self.agent.agent_name}: Context-Aware Delegation",
            content="",
            kvps=self.args,
        )
```

---

### Component 5: Task Board Tool (`tools/task_board_tool.py`)

```python
# /a0/usr/plugins/_context_bridge/tools/task_board_tool.py

from helpers.tool import Tool, Response
from usr.plugins._context_bridge.helpers.task_board import (
    add_task, claim_task, update_task, get_board,
    get_available_tasks, get_task_summary,
)


class TaskBoardTool(Tool):
    """
    Task board tool for multi-agent coordination.
    
    Methods:
    - list: Show all tasks
    - add: Create a new task
    - claim: Claim an available task
    - update: Update task status/result
    - summary: Get board summary
    """
    
    async def execute(self, **kwargs):
        if not self.method:
            return Response(message="Error: method required (list, add, claim, update, summary)", break_loop=False)
        
        context_data = self.agent.context.data
        
        if self.method == "list":
            return self._list(context_data)
        elif self.method == "add":
            return self._add(context_data, kwargs)
        elif self.method == "claim":
            return self._claim(context_data, kwargs)
        elif self.method == "update":
            return self._update(context_data, kwargs)
        elif self.method == "summary":
            return self._summary(context_data)
        else:
            return Response(message=f"Unknown method: {self.method}", break_loop=False)
    
    def _list(self, context_data: dict) -> Response:
        board = get_board(context_data)
        if not board:
            return Response(message="Task board is empty.", break_loop=False)
        
        summary = get_task_summary(context_data)
        return Response(message=summary, break_loop=False)
    
    def _add(self, context_data: dict, kwargs: dict) -> Response:
        description = kwargs.get("description", "")
        if not description:
            return Response(message="Error: description required", break_loop=False)
        
        task = add_task(
            context_data,
            description=description,
            dependencies=kwargs.get("dependencies", []),
            metadata=kwargs.get("metadata", {}),
        )
        return Response(
            message=f"Task created: {task.id} - {task.description}",
            break_loop=False,
        )
    
    def _claim(self, context_data: dict, kwargs: dict) -> Response:
        task_id = kwargs.get("task_id", "")
        if not task_id:
            # Auto-claim next available
            available = get_available_tasks(context_data)
            if not available:
                return Response(message="No available tasks to claim.", break_loop=False)
            task_id = available[0].id
        
        task = claim_task(context_data, task_id, self.agent.agent_name)
        if not task:
            return Response(
                message=f"Could not claim task {task_id}. It may be already claimed or dependencies not met.",
                break_loop=False,
            )
        return Response(
            message=f"Claimed task {task.id}: {task.description}",
            break_loop=False,
        )
    
    def _update(self, context_data: dict, kwargs: dict) -> Response:
        task_id = kwargs.get("task_id", "")
        status = kwargs.get("status", "")
        result = kwargs.get("result", "")
        
        task = update_task(context_data, task_id, status=status, result=result)
        if not task:
            return Response(message=f"Task {task_id} not found.", break_loop=False)
        return Response(
            message=f"Task {task.id} updated: status={task.status}",
            break_loop=False,
        )
    
    def _summary(self, context_data: dict) -> Response:
        summary = get_task_summary(context_data)
        return Response(message=summary or "Task board is empty.", break_loop=False)
```

---

### Model Override Helper (`helpers/model_override.py`)

```python
# /a0/usr/plugins/_context_bridge/helpers/model_override.py

"""
Per-delegation model override for Pattern 2 (Smart Friend).

Allows specifying a different model for a subordinate without
changing the global model configuration.
"""

from __future__ import annotations

from typing import Any


# Map of shorthand names to model identifiers
MODEL_ALIASES = {
    "frontier": "openai/gpt-4.1",
    "fast": "openai/gpt-4.1-mini",
    "smart": "anthropic/claude-sonnet-4-20250514",
    "coding": "zai_coding/glm-5.1",
    "reasoning": "openai/o3",
}


def resolve_model_name(name: str) -> str:
    """Resolve a model alias to its full identifier."""
    return MODEL_ALIASES.get(name, name)


def apply_model_override(config, model: str) -> Any:
    """
    Apply a model override to an AgentConfig.
    
    This modifies the config's additional dict to include
    a model override that the _model_config plugin can read.
    
    Args:
        config: AgentConfig instance
        model: Model name or alias
    
    Returns:
        Modified AgentConfig
    """
    resolved = resolve_model_name(model)
    config.additional["model_override"] = resolved
    return config
```

---

### Task Board Injection Extension

```python
# /a0/usr/plugins/_context_bridge/extensions/python/message_loop_prompts_after/_10_inject_task_board.py

from helpers.extension import Extension
from usr.plugins._context_bridge.helpers.task_board import get_task_summary


class InjectTaskBoard(Extension):
    """
    Injects task board state into every agent's context.
    This ensures all agents in a multi-agent workflow
    can see the current state of all tasks.
    """
    
    async def execute(self, loop_data=None, **kwargs):
        if not self.agent:
            return
        
        # Check if task board is enabled and has entries
        summary = get_task_summary(self.agent.context.data)
        if not summary:
            return  # No tasks, don't inject anything
        
        # Inject into extras_persistent so it persists across iterations
        if loop_data:
            loop_data.extras_persistent["task_board"] = summary
```

---

### Data Flow Diagrams

#### Pattern 1: Clean-Context Review

```
┌─────────────────────────────────────────────────────────────┐
│ SUPERIOR (Coder)                                            │
│                                                             │
│  ┌──────────────┐     ┌──────────────────────┐             │
│  │ History       │     │ LoopData             │             │
│  │ (full conv)   │     │  extras_persistent   │             │
│  │              │     │  extras_temporary    │             │
│  └──────┬───────┘     └──────────┬───────────┘             │
│         │                        │                         │
│         │   context_delegate     │                         │
│         │   mode="review"        │                         │
│         │                        │                         │
│  ┌──────▼────────────────────────▼───────────┐             │
│  │ packets.build_packet_from_agent_state()    │             │
│  │                                            │             │
│  │  INPUT: artifact from args                 │             │
│  │  INPUT: criteria from args                 │             │
│  │  NOT INCLUDED: history, memories, extras   │             │
│  └──────────────────┬─────────────────────────┘             │
│                     │                                       │
└─────────────────────┼───────────────────────────────────────┘
                      │ ReviewPacket.to_message()
                      │ (clean, no context)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ SUBORDINATE (Reviewer)                                      │
│                                                             │
│  ┌──────────────┐     ┌──────────────────────┐             │
│  │ History       │     │ LoopData             │             │
│  │ (only review  │     │  (no memories from   │             │
│  │  packet)      │     │   superior)          │             │
│  └──────┬───────┘     └──────────┬───────────┘             │
│         │                        │                         │
│         ▼                        ▼                         │
│     Runs independent analysis with tools                    │
│     Produces structured JSON findings                       │
│                     │                                       │
│                     │ JSON: {mode, findings, summary, conf} │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ SUPERIOR (Coder) — receives findings                        │
│                                                             │
│  parse_subordinate_result extension:                        │
│  ┌───────────────────────────────────────────┐              │
│  │ Parse JSON findings                       │              │
│  │ Inject into loop_data.extras_temporary    │              │
│  │ ["review_findings"]                       │              │
│  └───────────────────────────────────────────┘              │
│                     │                                       │
│                     ▼                                       │
│  Next LLM call sees findings as context                     │
│  Superior filters against original requirements             │
└─────────────────────────────────────────────────────────────┘
```

#### Pattern 2: Smart Friend Consultation

```
┌─────────────────────────────────────────────────────────────┐
│ FAST AGENT (main loop)                                      │
│                                                             │
│  context_delegate mode="consult" model="frontier"           │
│                     │                                       │
│  ┌──────────────────▼─────────────────────────┐             │
│  │ ConsultPacket:                              │             │
│  │  - question: specific problem               │             │
│  │  - context_snapshot: compressed history     │  ← FULL CTX │
│  │  - attempted: what was tried                │             │
│  │  - extras_snapshot: all injected context    │  ← FULL CTX │
│  │  - error_context: error messages            │             │
│  └──────────────────┬─────────────────────────┘             │
│                     │                                       │
└─────────────────────┼───────────────────────────────────────┘
                      │ ConsultPacket.to_message()
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ STRONG AGENT (consultant, different model)                  │
│                                                             │
│  Receives FULL context fork                                 │
│  Decides what's relevant                                    │
│  Produces: {analysis, recommendation, code, confidence}     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ FAST AGENT — receives consultation result                   │
│  consult_result injected into extras_temporary              │
│  Continues main loop with enhanced knowledge                │
└─────────────────────────────────────────────────────────────┘
```

#### Pattern 3: Manager-Child with Task Board

```
┌─────────────────────────────────────────────────────────────┐
│ MANAGER AGENT                                               │
│                                                             │
│  1. Decomposes task                                         │
│  2. task_board_tool:add for each subtask                    │
│  3. AgentContext.data["_context_bridge_task_board"] = {...}  │
│                                                             │
│  ┌─────────────────────────────────────────────┐            │
│  │ Task Board (in shared AgentContext.data)     │            │
│  │                                              │            │
│  │ T1: [pending]  Parse HTML files              │            │
│  │ T2: [pending]  Extract metadata   [dep: T1]  │            │
│  │ T3: [pending]  Build search index  [dep: T2]  │            │
│  └──────────────────────────┬──────────────────┘            │
│                             │                               │
│  ┌──────────┐        ┌──────▼──────┐                        │
│  │ Child 1  │        │  Child 2    │  (sequential or         │
│  │ claims   │        │  waits for  │   parallel)             │
│  │ T1       │        │  T1 to done │                         │
│  └────┬─────┘        └──────┬──────┘                        │
│       │                      │                               │
│  ┌────▼──────────────────────▼────┐                         │
│  │ inject_task_board extension    │                         │
│  │ (every agent sees board state) │                         │
│  └───────────────────────────────┘                          │
│                             │                               │
│  ┌──────────────────────────▼──────────────────┐           │
│  │ Manager reads all results, aggregates         │           │
│  │ task_board_tool:list → see all completed work │           │
│  └──────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘

Key: AgentContext.data is SHARED, so all agents see the same task board.
     Each agent's inject_task_board extension reads from shared state.
```

---

## Priority Phasing

### Phase 1: Foundation (Highest Impact, Lowest Complexity)

**Estimate**: 2-3 days

| Component | Files | Impact | Complexity |
|-----------|-------|--------|------------|
| Context packet builder | `helpers/packets.py` | HIGH | LOW |
| Enhanced delegation tool | `tools/context_delegate.py` | HIGH | LOW |
| Review mode (Pattern 1) | Packet + tool + prompt | HIGH | LOW |
| Consult mode (Pattern 2) | Packet + tool + prompt | HIGH | MEDIUM |

**Rationale**: The packet builder and enhanced delegation tool unlock Patterns 1 and 2 immediately. Review mode alone (clean-context code review) is the single highest-value pattern. Consult mode adds model routing for hard problems. Neither requires the task board.

**Implementation order**:
1. `helpers/__init__.py` — empty
2. `helpers/packets.py` — packet builders with all three modes
3. `tools/context_delegate.py` — enhanced delegation
4. `prompts/agent.system.tool.context_delegate.md` — tool documentation
5. `prompts/context_bridge.review_packet.md` — review format instructions
6. `prompts/context_bridge.consult_packet.md` — consult format instructions
7. `plugin.yaml` + `default_config.yaml`

**Testing**: Manual test with developer profile. Delegate a code review task with `mode="review"`. Verify subordinate receives clean context. Verify structured findings parse back.

---

### Phase 2: Task Board (Medium Impact, Medium Complexity)

**Estimate**: 2-3 days

| Component | Files | Impact | Complexity |
|-----------|-------|--------|------------|
| Task board logic | `helpers/task_board.py` | MEDIUM | MEDIUM |
| Task board tool | `tools/task_board_tool.py` | MEDIUM | LOW |
| Task board injection | `extensions/.../inject_task_board.py` | MEDIUM | LOW |
| Task mode packets | (in existing packets.py) | MEDIUM | LOW |
| Task decomposition prompt | `prompts/context_bridge.task_decomposition.md` | MEDIUM | MEDIUM |

**Rationale**: Task board enables Pattern 3. The shared `AgentContext.data` already provides the mechanism; the task board just structures it. Dependency tracking and auto-claiming are the key features.

**Implementation order**:
1. `helpers/task_board.py` — task board CRUD operations
2. `tools/task_board_tool.py` — agent-facing tool
3. `extensions/.../message_loop_prompts_after/_10_inject_task_board.py`
4. `prompts/agent.system.tool.task_board_tool.md`
5. `prompts/context_bridge.task_decomposition.md`
6. `prompts/context_bridge.task_board_inject.md`

**Testing**: Create a multi-step task decomposition. Verify children can claim tasks, see each other's results, and the manager can aggregate.

---

### Phase 3: Result Parsing & Refinement (Lower Impact, Lower Complexity)

**Estimate**: 1-2 days

| Component | Files | Impact | Complexity |
|-----------|-------|--------|------------|
| Result parsing extension | `extensions/.../parse_subordinate_result.py` | MEDIUM | MEDIUM |
| Model override helper | `helpers/model_override.py` | LOW | LOW |
| @extensible pre-hook | `extensions/.../Delegation/execute/start/...` | LOW | MEDIUM |
| Settings UI | `webui/config.html` | LOW | MEDIUM |

**Rationale**: Structured result parsing makes Patterns 1 and 2 smoother but isn't strictly required — the raw text result still works. Model override enables proper smart-friend routing. The @extensible hook allows intercepting existing `call_subordinate` calls without requiring agents to use `context_delegate`.

**Implementation order**:
1. `extensions/.../tool_execute_after/_10_parse_subordinate_result.py`
2. `helpers/model_override.py`
3. `extensions/.../tool_execute_before/_10_build_context_packet.py`
4. `extensions/.../_functions/tools/call_subordinate/Delegation/execute/start/_10_enhanced_delegation.py`
5. `webui/config.html`

---

### Phase 4: Advanced Patterns (Future)

- **Parallel child spawning**: Requires changes to `call_subordinate.py` core logic
- **Cross-agent messaging**: MCP-style communication between siblings
- **Dynamic model routing**: Automatic escalation based on failure patterns
- **Context window budgeting**: Allocate token budgets per agent based on task complexity
- **Result quality scoring**: Auto-evaluate subordinate output quality

---

## Prompt Templates

### `agent.system.tool.context_delegate.md`

```markdown
## context_delegate tool

Delegate tasks to a subordinate agent with structured context transfer.

### Usage

{
    "tool_name": "context_delegate",
    "tool_args": {
        "mode": "<mode>",
        "message": "<task description>",
        "profile": "<agent_profile>",
        "reset": false,
        "model": "<model_alias>"
    }
}

### Modes

#### "review" — Clean-Context Review
Subordinate receives ONLY the artifact and review criteria. No conversation history, no memories.
Use for: code review, document review, design critique.

{
    "tool_name": "context_delegate",
    "tool_args": {
        "mode": "review",
        "artifact": "<code or diff to review>",
        "artifact_type": "code",
        "criteria": ["security", "performance", "correctness"],
        "constraints": ["must work with Python 3.11"],
        "focus_areas": ["error handling", "edge cases"],
        "profile": "developer"
    }
}

#### "consult" — Full-Context Consultation
Subordinate receives your full conversation context (compressed) plus the question.
Use for: getting a second opinion, solving hard problems, design decisions.

{
    "tool_name": "context_delegate",
    "tool_args": {
        "mode": "consult",
        "question": "<specific question or problem>",
        "attempted": ["tried X", "tried Y"],
        "error_context": "<error message if relevant>",
        "model": "frontier",
        "profile": "researcher"
    }
}

#### "task" — Task Delegation with Shared State
Subordinate receives a task from the shared task board. Other agents can see results.
Use for: parallelizable work, multi-step processes, map-reduce patterns.

{
    "tool_name": "context_delegate",
    "tool_args": {
        "mode": "task",
        "task_description": "<what to do>",
        "task_context": "<why this task exists>",
        "dependencies": ["<task_id>", ...],
        "expected_output": "<what format>",
        "profile": "developer"
    }
}

#### "default" — Standard Delegation
Backward-compatible with existing call_subordinate behavior.

{
    "tool_name": "context_delegate",
    "tool_args": {
        "mode": "default",
        "message": "<task description>",
        "profile": "developer"
    }
}

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| mode | string | Delegation mode: review, consult, task, default |
| message | string | Task description (for default mode) |
| profile | string | Agent profile to use |
| reset | boolean | Reset subordinate (new instance) |
| model | string | Model alias or identifier for subordinate |
| artifact | string | Code/diff to review (review mode) |
| artifact_type | string | Type: code, diff, document, design |
| criteria | string[] | Review criteria (review mode) |
| constraints | string[] | Known constraints (review mode) |
| focus_areas | string[] | Areas to focus on (review mode) |
| question | string | Question to ask (consult mode) |
| attempted | string[] | What was tried (consult mode) |
| error_context | string | Error messages (consult mode) |
| task_description | string | Task description (task mode) |
| task_context | string | Why task exists (task mode) |
| dependencies | string[] | Required task IDs (task mode) |
| expected_output | string | Expected output format (task mode) |
```

### `agent.system.tool.task_board_tool.md`

```markdown
## task_board_tool

Interact with the shared task board for multi-agent coordination.

### Methods

#### task_board_tool:list
Show all tasks and their status.

{
    "tool_name": "task_board_tool",
    "tool_args": {"": ""}
}

#### task_board_tool:add
Create a new task.

{
    "tool_name": "task_board_tool",
    "tool_args": {
        "description": "<task description>",
        "dependencies": ["<task_id>", ...],
        "metadata": {"<key>": "<value>"}
    }
}

#### task_board_tool:claim
Claim an available task. Omit task_id to auto-claim the next available.

{
    "tool_name": "task_board_tool",
    "tool_args": {
        "task_id": "<id or empty for auto>"
    }
}

#### task_board_tool:update
Update a task's status or result.

{
    "tool_name": "task_board_tool",
    "tool_args": {
        "task_id": "<id>",
        "status": "in_progress",
        "result": "<result text>"
    }
}

#### task_board_tool:summary
Get a formatted summary of the task board.

{
    "tool_name": "task_board_tool",
    "tool_args": {}
}

### Task States

pending → claimed → in_progress → complete
                                      → failed
                   → blocked
```

### `context_bridge.task_board_inject.md`

```markdown
{{summary}}

---
*Task board state is shared across all agents. Use task_board_tool to interact with it.*
```

### `context_bridge.task_decomposition.md`

```markdown
## Task Decomposition Guide

When breaking a complex task into subtasks for multi-agent delegation:

### Rules
1. Each subtask should be independently executable
2. Define clear inputs and expected outputs for each subtask
3. Mark dependencies explicitly
4. Keep subtasks small enough to fit in a single context window
5. Each subtask should produce a result that can be aggregated

### Decomposition Pattern

1. **Map tasks**: Parallel work that can run simultaneously
   - Same operation on different data
   - Independent investigations
   - Competing approaches

2. **Reduce tasks**: Aggregation of map results
   - Merge findings
   - Pick best approach
   - Synthesize insights

3. **Manage tasks**: Coordination and quality control
   - Review results
   - Handle failures
   - Final integration

### Creating Tasks

Use `task_board_tool:add` for each subtask, then delegate with `context_delegate` mode="task".

### Example

Original: "Analyze the codebase for performance issues and fix them"

Decomposed:
- T1: Profile the codebase and identify bottlenecks (map)
- T2: Research optimization approaches for top 3 bottlenecks (map)
- T3: Implement optimizations for bottleneck #1 (depends: T1, T2)
- T4: Implement optimizations for bottleneck #2 (depends: T1, T2)
- T5: Run benchmarks and verify improvements (reduce, depends: T3, T4)
```

### `context_bridge.review_findings_format.md`

```markdown
## Review Response Format

When performing a clean-context review, structure your findings as:

```json
{
    "mode": "review",
    "findings": [
        {
            "severity": "critical|high|medium|low|info",
            "location": "file:line or section",
            "description": "what the issue is",
            "suggestion": "how to fix it"
        }
    ],
    "summary": "brief overall assessment",
    "confidence": 0.85
}
```

### Severity Levels
- **critical**: Will cause failures or security vulnerabilities
- **high**: Significant issues that should be fixed before merging
- **medium**: Issues that affect quality but aren't blockers
- **low**: Minor improvements, style issues
- **info**: Observations, not necessarily issues

### Guidelines
- Focus on correctness, security, performance, and maintainability
- Each finding should be specific and actionable
- Include location information (file, line, function)
- Provide a fix suggestion for every finding
- Be honest about confidence level
```

---

## Appendix: Source Code Reference

### `call_subordinate.py` (full, 55 lines)

```python
from agent import Agent, UserMessage
from helpers.tool import Tool, Response
from initialize import initialize_agent
from extensions.python.hist_add_tool_result import _90_save_tool_call_file as save_tool_call_file

class Delegation(Tool):
    async def execute(self, message="", reset="", **kwargs):
        if (
            self.agent.get_data(Agent.DATA_NAME_SUBORDINATE) is None
            or str(reset).lower().strip() == "true"
        ):
            config = initialize_agent()
            agent_profile = kwargs.get("profile", kwargs.get("agent_profile", ""))
            if agent_profile:
                config.profile = agent_profile
            sub = Agent(self.agent.number + 1, config, self.agent.context)  # SHARES context
            sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
            self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub)

        subordinate: Agent = self.agent.get_data(Agent.DATA_NAME_SUBORDINATE)
        subordinate.hist_add_user_message(UserMessage(message=message, attachments=[]))  # RAW TEXT ONLY

        result = await subordinate.monologue()
        subordinate.history.new_topic()

        additional = None
        if len(result) >= save_tool_call_file.LEN_MIN:
            hint = self.agent.read_prompt("fw.hint.call_sub.md")
            if hint:
                additional = {"hint": hint}

        return Response(message=result, break_loop=False, additional=additional)
```

### Key `agent.py` Structures

```python
# LoopData (line 326)
class LoopData:
    def __init__(self, **kwargs):
        self.iteration = -1
        self.system = []
        self.user_message: history.Message | None = None
        self.history_output: list[history.OutputMessage] = []
        self.extras_temporary: OrderedDict[str, history.MessageContent] = OrderedDict()
        self.extras_persistent: OrderedDict[str, history.MessageContent] = OrderedDict()
        self.last_response = ""
        self.params_temporary: dict = {}
        self.params_persistent: dict = {}
        self.current_tool = None

# Agent.__init__ (line 350)
class Agent:
    DATA_NAME_SUPERIOR = "_superior"
    DATA_NAME_SUBORDINATE = "_subordinate"
    DATA_NAME_CTX_WINDOW = "ctx_window"

    @extension.extensible
    def __init__(self, number, config, context=None):
        self.config = config
        self.context = context or AgentContext(config=config, agent0=self)
        self.number = number
        self.agent_name = f"A{self.number}"
        self.history = history.History(self)
        self.last_user_message = None
        self.intervention = None
        self.data = {}  # PER-AGENT isolated dict
        extension.call_extensions_sync("agent_init", self)

# prepare_prompt (line 537)
    @extension.extensible
    async def prepare_prompt(self, loop_data: LoopData) -> list[BaseMessage]:
        await extension.call_extensions_async("message_loop_prompts_before", self, loop_data=loop_data)
        loop_data.system = await self.get_system_prompt(self.loop_data)
        loop_data.history_output = self.history.output()
        await extension.call_extensions_async("message_loop_prompts_after", self, loop_data=loop_data)
        
        system_text = "\n\n".join(loop_data.system)
        extras = history.Message(False, content=self.read_prompt(
            "agent.context.extras.md",
            extras=dirty_json.stringify({**loop_data.extras_persistent, **loop_data.extras_temporary}),
        )).output()
        loop_data.extras_temporary.clear()
        # ... build full_prompt from system + history + extras
```

### recall_memories Injection Point

```python
# _50_recall_memories.py (line 221-228)
# This is where memories get injected into extras_persistent:
        if memories_txt:
            extras["memories"] = self.agent.parse_prompt(
                "agent.system.memories.md", memories=memories_txt
            )
        if solutions_txt:
            extras["solutions"] = self.agent.parse_prompt(
                "agent.system.solutions.md", solutions=solutions_txt
            )
```

---

## Summary

Agent Zero's multi-agent architecture has one critical gap: **context transfer between agents is a raw text message into a blank-slate subordinate**. The shared `AgentContext.data` provides the infrastructure for shared state, but nothing structures or populates it.

The `_context_bridge` plugin closes this gap with:

1. **Context packets** that structure what gets transferred (review=clean, consult=full, task=shared)
2. **Enhanced delegation** with mode selection and model override
3. **Task board** for multi-agent coordination via shared state
4. **Result parsing** that feeds structured findings back to superiors

Phase 1 (review + consult modes) delivers 80% of the value with 20% of the complexity. The task board (Phase 2) unlocks full map-reduce patterns. Result parsing and model routing (Phase 3) polish the experience.
