---
name: prompt-engineering-harness
version: 1.0.0
triggers:
  - "prompt engineering"
  - "improve prompt"
  - "craft prompt"
  - "prompt harness"
  - "prompting best practices"
requires: []
produces:
  - "improved prompts"
---

# Prompt Engineering Harness

A structured harness for engineering high-quality prompts in Agent Zero, extracted from Anthropic's official documentation and tutorial.

Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview

## Activation

Load this skill when:
- Writing or improving system prompts
- Crafting agent instruction sets
- Building prompt chains or multi-step agent workflows
- Debugging prompt quality issues
- Designing subordinate agent profiles

---

## Layer 1: Foundations (Always Apply)

### 1. Be Clear and Direct

State exactly what you want. Ambiguity is the enemy.

```
BAD:  "Help me with the data"
GOOD: "Extract all email addresses from the customer_records table where status='active' and return them as a JSON array."
```

### 2. Structure with XML Tags

XML tags let the model parse complex prompts without confusion. Wrap each content type separately.

```xml
<instructions>
  Analyze the sentiment of each review.
</instructions>
<reviews>
  <review id="1">Great product!</review>
  <review id="2">Terrible experience.</review>
</reviews>
<output_format>
  Return JSON: [{"id": "...", "sentiment": "positive|negative|neutral"}]
</output_format>
```

**Core tags for Agent Zero prompts:**
- `<instructions>` — What to do
- `<context>` — Background information and why it matters
- `<input>` or `<data>` — The actual content to process
- `<examples>` — Sample inputs/outputs wrapped in `<example>` tags
- `<constraints>` — What NOT to do or edge cases
- `<output_format>` — Exact format specification

### 3. Separate Data from Instructions

Never mix instructions with the data being processed. This is the #1 cause of misinterpretation.

```xml
<instructions>Summarize the document below in 3 bullet points.</instructions>
<document>
  {{document_text}}
</document>
```

### 4. Assign Roles

Give the model a persona to steer expertise, tone, and perspective.

```
You are a senior security auditor with 15 years of experience in smart contract
vulnerability assessment. You specialize in DeFi protocols and have found critical
bugs in major protocols.
```

### 5. Add Context (Explain WHY)

Explaining motivation behind instructions improves compliance.

```
When reviewing code, flag any use of unchecked external calls. These are the #1
cause of reentrancy attacks which have cost billions in DeFi exploits.
```

---

## Layer 2: Techniques (Apply Based on Task)

### 6. Use Examples (Few-Shot / Multishot)

3–5 examples produce the best results. Each example should be:
- **Relevant**: Mirror the actual use case
- **Diverse**: Cover edge cases, vary patterns
- **Structured**: Wrapped in `<example>` tags

```xml
<examples>
  <example>
    <input>"The meeting is at 3pm tomorrow"</input>
    <output>{"intent": "schedule", "time": "15:00", "offset": "+1day"}</output>
  </example>
  <example>
    <input>"Cancel my subscription"</input>
    <output>{"intent": "cancel", "target": "subscription"}</output>
  </example>
</examples>
```

### 7. Thinking Step-by-Step (Chain of Thought)

Ask the model to reason before answering. Two approaches:

**a) Implicit prompting:**
```
Think step by step before answering.
```

**b) Structured tags (manual CoT when extended thinking is off):**
```xml
Before answering, reason through the problem inside <thinking> tags.
Then provide your final answer inside <answer> tags.
```

### 8. Ask for Self-Checking

Append verification instructions to catch errors:

```
Before submitting your answer, verify:
1. All imports are used
2. No undefined variables
3. Return types match function signatures
4. Edge cases are handled
```

### 9. Control Output Format

Three methods:

**a) Say what TO do, not what NOT to do:**
```
GOOD: "Write in smooth prose paragraphs."
BAD:  "Don't use markdown."
```

**b) XML format indicators:**
```
Write each explanation inside <explanation> tags.
```

**c) Match prompt style to desired output:**
If you want concise output, write concise instructions.

### 10. Verbosity Control

```
Provide concise, focused responses. Skip non-essential context and keep examples minimal.
```

Positive examples of the desired length work better than negative instructions.

---

## Layer 3: Advanced Patterns

### 11. Prefer General Instructions Over Prescriptive Steps

```
BAD:  "Step 1: Read the file. Step 2: Parse lines. Step 3: Filter by X."
GOOD: "Extract all entries matching criteria X from the file. Think thoroughly about edge cases."
```

The model's reasoning often exceeds hand-written step plans. Trust the model to decompose.

### 12. Multishot + Thinking Combined

Use `<thinking>` tags INSIDE your few-shot examples to teach reasoning patterns:

```xml
<examples>
  <example>
    <input>Is 97 prime?</input>
    <thinking>97 is not divisible by 2, 3, 5, or 7. sqrt(97) ≈ 9.8, so I only need to check primes up to 9. Checked: 2, 3, 5, 7. None divide evenly.</thinking>
    <output>Yes, 97 is prime.</output>
  </example>
</examples>
```

### 13. Chaining Prompts

Break complex tasks into sequential prompts where each builds on the last:

```
Prompt 1: Analyze requirements → output: spec.json
Prompt 2: Generate code from spec.json → output: implementation
Prompt 3: Review implementation against spec.json → output: fixes
```

### 14. Agentic Coding Patterns

For autonomous coding tasks:
- **First context window**: Setup tasks (tests, scripts, project structure)
- **Subsequent windows**: Iterate on implementation
- **Write tests first** in a structured format (e.g., `tests.json`)
- **Don't add** unnecessary docstrings, comments, or type annotations to unchanged code
- **Don't add** error handling for impossible scenarios (only validate at system boundaries)
- **Don't create** abstractions for one-time operations or hypothetical future requirements

### 15. Extended/Adaptive Thinking Guidance

For agentic multi-step tasks:
```
After receiving tool results, carefully reflect on their quality and determine
optimal next steps before proceeding. Use your thinking to plan and iterate based
on this new information.
```

To reduce unnecessary thinking:
```
Extended thinking adds latency and should only be used when it will meaningfully
improve answer quality — typically for problems requiring multi-step reasoning.
When in doubt, respond directly.
```

### 16. Effort Calibration

- Replace blanket defaults with targeted instructions
- Remove over-prompting ("If in doubt, use X" causes overtriggering)
- Lower `effort` setting if the model is overly aggressive

---

## Layer 4: Anti-Patterns to Avoid

### ❌ Don't: Tell what NOT to do

```
BAD:  "Don't use bullet points. Don't write long paragraphs."
GOOD: "Write in concise, flowing prose paragraphs of 2-3 sentences each."
```

### ❌ Don't: Over-specify steps

```
BAD:  "First do X, then check Y, then if Z do W, otherwise..."
GOOD: "Think thoroughly and solve the problem optimally."
```

### ❌ Don't: Use prefilled responses (deprecated in Claude 4.6+)

Use explicit format instructions instead.

### ❌ Don't: Over-prompt tool usage

```
BAD:  "If in doubt, search the web. Always verify with a search."
GOOD: "Search the web when it would enhance your understanding of the problem."
```

### ❌ Don't: Mix instructions and data

Always separate with XML tags.

---

## Prompt Evaluation Checklist

Run this checklist against every prompt you write:

| # | Check | ✓ |
|---|-------|---|
| 1 | Is the task stated clearly and directly? | |
| 2 | Are instructions separated from data using XML tags? | |
| 3 | Is a role assigned when it would improve output? | |
| 4 | Is context provided for WHY instructions matter? | |
| 5 | Are 3-5 examples provided for non-trivial tasks? | |
| 6 | Are examples diverse and edge-case covering? | |
| 7 | Is the output format explicitly specified? | |
| 8 | Does the prompt say what TO do (not what NOT to do)? | |
| 9 | Is there a self-check/verification instruction? | |
| 10 | Is the prompt free of over-prescriptive step-by-step? | |
| 11 | Is verbosity appropriate to the task? | |
| 12 | For chains: does each prompt have a clear input/output contract? | |

---

## Quick Templates

### Template: Agent System Prompt

```xml
<role>
  You are a [role description with expertise and experience].
</role>

<task>
  [Clear, direct statement of what the agent should do]
</task>

<context>
  [Why this matters, background, constraints]
</context>

<instructions>
  1. [Primary instruction]
  2. [Secondary instruction]
  3. [Edge case handling]
</instructions>

<output_format>
  [Exact format specification]
</output_format>

<examples>
  <example>
    <input>[sample input]</input>
    <output>[expected output]</output>
  </example>
</examples>

<self_check>
  Before responding, verify:
  1. [Verification criterion 1]
  2. [Verification criterion 2]
</self_check>
```

### Template: Subordinate Agent Delegation

```xml
<role>You are a [specialist role]. Your job is to [specific task].</role>

<input>{{delegated_task}}</input>

<constraints>
  - Focus ONLY on [scope]
  - Return results as [format]
  - If blocked, report exactly what's blocking
</constraints>

<success_criteria>
  [What "done" looks like]
</success_criteria>
```

### Template: Prompt Chain Step

```xml
<chain_step number="N" total="M">
  <description>[What this step accomplishes]</description>
  <input_from_previous>{{step_N-1_output}}</input_from_previous>
  <instructions>[Step-specific instructions]</instructions>
  <output_to>step_N+1</output_to>
  <output_format>[Exact format for next step]</output_format>
</chain_step>
```

---

## Resources

| Resource | URL | Type |
|----------|-----|------|
| Anthropic Prompt Engineering Overview | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Official Docs |
| Prompting Best Practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Official Docs |
| Console Prompting Tools | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools | Official Docs |
| Interactive Tutorial (GitHub) | https://github.com/anthropics/prompt-eng-interactive-tutorial | Tutorial |
| Google Sheets Tutorial | https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8 | Lightweight Tutorial |
| Define Success & Build Evals | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Testing |
| Reduce Hallucinations | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Guardrails |
| Increase Output Consistency | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency | Guardrails |
| Prompt Caching | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | Performance |
| Extended Thinking | https://platform.claude.com/docs/en/build-with-claude/extended-thinking | Advanced |
| Tool Use Overview | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Tool Integration |
| Claude Console (Prompt Generator) | https://console.claude.com/dashboard | Interactive Tool |

---

## Agent Zero Integration Notes

This harness is designed for Agent Zero's prompt-driven architecture:

1. **System prompts** (`prompts/` directory): Apply Layer 1 (foundations) to all system prompt files
2. **Agent profiles** (`agents/`): Use the Agent System Prompt template for each profile
3. **Subordinate delegation**: Use the Delegation template when calling subordinates
4. **Skill instructions**: Structure SKILL.md files with XML-tagged sections
5. **Memory entries**: Use clear, direct formatting for saved knowledge
6. **Prompt chains**: Use chain step templates for multi-step workflows

The 12-point evaluation checklist should be run against any new prompt before deployment.
