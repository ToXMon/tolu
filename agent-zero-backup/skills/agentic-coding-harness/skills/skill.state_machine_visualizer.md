---
name: state-machine-visualizer
version: "1.0.0"
trigger: /diagram
description: >
  Generates ASCII state machine diagrams for data flows and module interactions.
  Saves diagrams to work_logs/state_machines/ for future reference.
---

# State Machine Visualizer

Slash command: `/diagram <module>`

## When activated:
When the user types `/diagram <module>` or says "diagram data flow" or "show state machine":

## Instructions

1. **Identify the target module** — Read the module's source files to understand:
   - Data models and types
   - State transitions
   - External dependencies
   - Event/message flows
   - API endpoints

2. **Analyze the code** — Look for:
   - State variables and enums
   - Transition functions
   - Event handlers
   - Database operations
   - API routes
   - Type definitions with state fields

3. **Generate the ASCII diagram** — Use this format:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   STATE_A   │────▶│   STATE_B   │────▶│   STATE_C   │
│  (initial)  │     │  (valid)    │     │  (complete) │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │                    │
                           ▼                    │
                    ┌─────────────┐             │
                    │   STATE_D   │◀────────────┘
                    │  (error)    │
                    └─────────────┘
```

4. **Add data flow annotations**:
```
┌──────────┐  submit()   ┌──────────┐  validate()  ┌──────────┐
│  Draft   │───────────▶│ Pending  │────────────▶│ Approved │
│          │            │          │             │          │
│ data: {} │            │ data: T  │             │ data: V  │
└──────────┘            └────┬─────┘             └──────────┘
                             │                        │
                      reject()                       │
                             ▼                        ▼
                      ┌──────────┐            ┌──────────┐
                      │ Rejected │            │ Complete │
                      │          │            │          │
                      │ reason:s │            │ result:R │
                      └──────────┘            └──────────┘
```

5. **Include a legend** explaining:
   - Box labels = states
   - Arrows = transitions with trigger functions
   - Annotations = data shape at each state
   - Initial state marked with `(initial)`
   - Terminal states marked with `(terminal)`

6. **Save the diagram**:
   ```bash
   mkdir -p work_logs/state_machines
   # Write to work_logs/state_machines/<module>-states.md
   ```

   The file should contain:
   - Module name and date
   - The ASCII diagram
   - State descriptions table
   - Transition table (from, to, trigger, guard condition)

7. **Display the diagram** in the response.

## Diagram File Format

```markdown
# State Machine: <module>
Date: YYYY-MM-DD
Source: <file paths analyzed>

## Diagram

[ASCII diagram here]

## States

| State | Description | Data Shape |
|---|---|---|
| Draft | Initial creation | { field: type } |
| Pending | Awaiting review | { field: type } |

## Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| Draft | Pending | submit() | data valid |
| Pending | Approved | validate() | rules pass |
```

## Tips for Accurate Diagrams

- Read the actual code, don't assume state names
- Check database schemas for state enums
- Look at test files for expected state transitions
- Identify side effects (notifications, webhooks) in transitions
- Note which transitions are reversible
