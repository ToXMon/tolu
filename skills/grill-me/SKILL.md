---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
version: "1.0.0"
tags: ["planning", "design", "interview", "stress-test"]
trigger_patterns:
  - "grill me"
  - "stress test"
  - "stress-test"
  - "grill my plan"
  - "grill my design"
  - "challenge my assumptions"
  - "poke holes in"
  - "rip apart my plan"
---

# Grill Me

Relentless interview mode for plans, designs, and ideas. Walks down every branch of the decision tree, resolving dependencies one-by-one until shared understanding is reached.

## When to Use

- User wants to stress-test a plan or design
- User says "grill me" or similar trigger
- User wants assumptions challenged
- User needs help finding gaps in their thinking

## The Process

### Core Rules

1. **Ask one question at a time** — never dump a list
2. **Provide your recommended answer** for each question — don't just interrogate blindly
3. **Resolve dependencies first** — if question B depends on question A, ask A first
4. **Explore the codebase** when a question can be answered by reading code instead of asking the user
5. **Don't let the user off the hook** — if an answer is vague, push for specifics
6. **Track the decision tree** — keep mental (or written) map of resolved vs. open branches

### Interview Protocol

For each question:

1. **State the question clearly** — what decision or assumption needs resolving
2. **Explain why it matters** — what depends on this answer
3. **Give your recommendation** — what you'd choose and why
4. **Wait for the user's answer** — don't move on until resolved
5. **If the answer contradicts a prior decision, flag it** — surface conflicts immediately

### Decision Tree Walkdown

```
Root: What is the core goal?
├── Branch 1: Scope & Boundaries
│   ├── What's in scope?
│   ├── What's explicitly out of scope?
│   └── What are the non-negotiable constraints?
├── Branch 2: Architecture & Design
│   ├── What's the high-level structure?
│   ├── What are the key components?
│   └── How do they interact?
├── Branch 3: Edge Cases & Failure Modes
│   ├── What happens when X fails?
│   ├── What are the unlikely but catastrophic scenarios?
│   └── What's the recovery plan?
├── Branch 4: Trade-offs & Priorities
│   ├── Speed vs. correctness?
│   ├── Simplicity vs. flexibility?
│   └── Build vs. buy?
└── Branch 5: Validation & Success
    ├── How do you know it works?
    ├── What does "done" look like?
    └── What would make you throw it away?
```

### Adaptation Rules

- **If the user provides a document or codebase**, read it first and derive questions from the content rather than starting generic
- **If a question can be answered by exploring code**, explore the code instead of asking — report what you found and confirm with the user
- **If the user gets defensive**, acknowledge it but don't back off — reframe the question
- **If the user says "I don't know"**, that's valuable — mark it as an open question and explore why
- **If a branch is fully resolved**, say so explicitly and move on — don't re-plow settled ground

## Output Format

For each question, output:

> **Q{N}: {Question}**
>
> *Why this matters: {explanation of dependencies}*
>
> *My recommendation: {your suggested answer with reasoning}*

Then wait for the user's response before proceeding.

## Termination

The interview ends when:
- All branches of the decision tree are resolved
- The user explicitly says to stop
- A clear, shared understanding is reached

At termination, produce a summary of all decisions made and any remaining open questions.
