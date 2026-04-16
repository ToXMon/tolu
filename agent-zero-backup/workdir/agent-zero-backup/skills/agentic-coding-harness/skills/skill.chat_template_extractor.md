---
name: chat-template-extractor
version: "1.0.0"
trigger: /extract-templates
description: >
  Extracts reusable prompt templates from current conversation history.
  Classifies, anonymizes, scores by reusability, and outputs a markdown library.
---

# Chat Template Extractor

Slash command: `/extract-templates`

## When activated:
When the user types `/extract-templates` or says "extract templates" or "save prompt templates":

## Instructions

1. **Run the extractor instrument**:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/chat_template_extractor.py extract \
     /a0/usr/chats templates/
   ```

2. **Review extracted templates** — Check the output for:
   - High-reusability templates (score > 0.7)
   - Category distribution (coding, debug, test, etc.)
   - Duplicate patterns that could be consolidated

3. **Score and rank** — Each template gets scored on:
   - **Generalizability**: How well does it apply beyond the original context?
   - **Structure**: Does it have clear steps, inputs, outputs?
   - **Placeholder density**: More {{placeholders}} = more reusable
   - **Category relevance**: Coding/debug/test templates score higher than general

4. **Output the template library** — Two files generated:
   - `templates/extracted_templates.json` — Machine-readable with metadata
   - `templates/PROMPT_TEMPLATES.md` — Human-readable library

5. **Highlight top templates** — Show the user the 3 most reusable templates:
   - Template ID and category
   - Reusability score
   - First 80 characters of the template
   - Suggestion for how to use it

## Template Categories

| Category | Description | Typical Score Boost |
|---|---|---|
| coding | Implementation tasks | +0.1 |
| debug | Bug fixing and tracing | +0.1 |
| test | Writing and running tests | +0.1 |
| build | Build and compile tasks | +0.1 |
| research | Information gathering | +0.0 |
| deploy | Deployment operations | +0.0 |
| refactor | Code restructuring | +0.0 |
| general | Uncategorized | +0.0 |

## Output Format

```
=== Extracted Templates ===
Total: [N] templates extracted

Top 3:
  [0.92] tmpl-abc123 (coding): "Build a {{feature}} endpoint that validates {{input}}..."
  [0.87] tmpl-def456 (debug): "Debug {{error_type}} in {{module}} by checking {{condition}}..."
  [0.81] tmpl-ghi789 (test): "Write integration tests for {{endpoint}} covering {{scenarios}}..."

Files:
  templates/extracted_templates.json
  templates/PROMPT_TEMPLATES.md
```

## List Existing Templates

To view previously extracted templates:
```bash
python3 /a0/skills/agentic-coding-harness/instruments/chat_template_extractor.py list templates/
```
