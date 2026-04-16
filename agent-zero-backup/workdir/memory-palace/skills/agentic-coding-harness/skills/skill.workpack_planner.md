---
name: workpack-planner
version: "1.0.0"
trigger: /workpack
description: >
  Break any goal into structured workpack files (scope.md, rules.md, task-XXXX.md)
  for long autonomous coding runs of 12-16 hours. Outputs ready-to-queue command sequence.
---

# Workpack Planner

Slash command: `/workpack <goal>`

## Activation

When the user types `/workpack <goal>` or asks to "create a workpack" or "plan autonomous work":

## Instructions

1. **Clarify the goal** — Extract the primary objective from the user's description. If the goal is vague, make reasonable assumptions and document them.

2. **Generate the workpack structure** using the workpack_generator instrument:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/workpack_generator.py create <project_dir> "<goal>" [max_tasks]
   ```

3. **Create a PRD** (if the project has no PRD yet) — Generate a `prd.json` in the project root following the Ralph format:
   ```json
   {
     "project": "ProjectName",
     "branchName": "feature/<descriptive-name>",
     "description": "Clear one-line objective",
     "userStories": [
       {
         "id": "US-001",
         "title": "Story title",
         "description": "As a <role>, I need <capability> so that <outcome>.",
         "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
         "priority": 1,
         "passes": false,
         "notes": ""
       }
     ]
   }
   ```

4. **Write the scope.md** — Define:
   - Objective in one clear sentence
   - Architecture constraints (300 lines/file, 20 files/dir, no `any` types)
   - Success criteria (all tests pass, AGENTS.md updated, no regressions)
   - Task summary with priorities

5. **Write the rules.md** — Define autonomous execution constraints:
   - No questions, no stops
   - One task per iteration
   - Commit on green
   - Update AGENTS.md after changes
   - File/directory size limits

6. **Write individual task files** — Each task-XXXX.md contains:
   - Status: pending
   - Priority number
   - Description framed as user action
   - Acceptance criteria with concrete inputs/outputs
   - Files to create/modify
   - Verification steps

7. **Output the execution plan** — Show:
   - Number of tasks generated
   - Estimated complexity per task
   - Recommended execution order
   - Ready-to-queue command for starting autonomous run

## Task Sizing Rules

- Each task must be completable in one context window
- Tasks should be small: "Add database column" not "Build the dashboard"
- Maximum 8 tasks per workpack (split larger goals into multiple workpacks)
- Each task has clear acceptance criteria with pass/fail conditions

## PRD-First Pattern (from Ralph)

For fresh builds or builds without a PRD:
1. Generate PRD from the user's goal description
2. Convert PRD user stories into task-XXXX.md files
3. Each task maps to one or more user stories
4. Tasks are ordered by priority (foundations first)
5. Stop condition: all user stories have `passes: true`

## Output Format

```
Workpack created: .workpack/
  scope.md   — Overall objective and constraints
  rules.md   — Autonomous execution rules
  progress.txt — Append-only learnings log
  task-0001.md — [Title] (priority: 1)
  task-0002.md — [Title] (priority: 2)
  ...

PRD created: prd.json
  [N] user stories defined
  Branch: feature/<name>

Ready to execute:
  python3 /a0/skills/agentic-coding-harness/instruments/workpack_generator.py next <project_dir>
```
