---
name: extract-chat-templates
version: "1.0.0"
trigger: /extract-templates (end-of-session)
description: >
  End-of-session template extraction with top 3 highlights and generalization suggestions.
  Run before closing a session to capture reusable patterns.
---

# Extract Chat Templates (End-of-Session)

## When to use
Run this at the end of every coding session to:
- Capture reusable prompt patterns discovered during the session
- Build a library of proven prompt templates
- Score templates by reusability for future prioritization
- Suggest generalizations for narrow prompts

## Execution Steps

### Step 1: Run the Template Extractor

```bash
python3 /a0/skills/agentic-coding-harness/instruments/chat_template_extractor.py extract \
  /a0/usr/chats templates/
```

### Step 2: Review Top 3 Highlights

From the extracted templates, identify the top 3 by reusability score. For each:

1. **Show the template** with its category and score
2. **Identify the pattern** — What makes this template reusable?
3. **Suggest generalization** — How could it apply to other contexts?

Example analysis:
```
### Highlight 1: Auth Implementation Pattern (score: 0.92)
Template: "Build {{auth_type}} for {{app_framework}} with {{storage}}..."
Pattern: Multi-step implementation with clear inputs/outputs
Generalization: Works for any middleware/flow implementation
  - Could apply to: rate limiting, logging, caching middleware
  - Replace auth-specific terms with {{middleware_type}}
```

### Step 3: Generalization Suggestions

For each top template, suggest:

1. **Broader category** — What family of tasks does this belong to?
2. **Parameter extraction** — Which specifics should become {{placeholders}}?
3. **Edge cases to document** — What conditions might break this pattern?
4. **Composable patterns** — Can this template chain with others?

### Step 4: Update Template Library

```bash
python3 /a0/skills/agentic-coding-harness/instruments/chat_template_extractor.py list templates/
```

Verify the new templates are saved and accessible.

### Step 5: Session Template Summary

Output:
```
=== Template Extraction Summary ===
Session date: [date]
Templates extracted: [count]
New templates: [count not previously seen]

Top 3:
  1. [score] [category] [brief description]
  2. [score] [category] [brief description]
  3. [score] [category] [brief description]

Generalization opportunities:
  - [opportunity 1]
  - [opportunity 2]

Files:
  templates/extracted_templates.json
  templates/PROMPT_TEMPLATES.md
```

### Step 6: Log Template Extraction

```bash
python3 /a0/skills/agentic-coding-harness/instruments/session_logger.py log \
  "templates" "Extracted [N] templates, top: [description]" "" "" "review-generalize-top-3"
```
