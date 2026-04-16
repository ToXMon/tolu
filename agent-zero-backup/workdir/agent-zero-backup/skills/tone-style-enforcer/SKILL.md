---
name: "tone-style-enforcer"
description: "Lock output to a specific brand or personal voice. Enforces consistent tone, style, vocabulary, and formatting across all generated content. Best for consistency at scale."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["writing", "tone", "style", "brand", "consistency", "voice"]
trigger_patterns:
  - "enforce tone"
  - "match tone"
  - "brand voice"
  - "writing style"
  - "consistent tone"
  - "style guide"
---

# Tone & Style Enforcer

## When to Use
Activate when asked to write or rewrite content in a specific tone, voice, or brand style. Use for maintaining consistency across team outputs.

## The Process

### Step 1: Capture the Style Profile
If the user provides a style reference (sample text, brand guide, voice description), extract:
- **Tone:** Formal/casual/playful/authoritative/etc.
- **Vocabulary:** Technical level, jargon, slang preferences
- **Sentence Structure:** Short punchy / flowing / varied
- **Perspective:** First person / second person / third person
- **Formatting:** Bullet preferences, heading style, paragraph length
- **Do's:** Specific patterns to follow
- **Don'ts:** Words or patterns to avoid

### Step 2: Build the Style Guide
Create a concise style profile in YAML format covering tone, vocabulary level, sentence style, perspective, do's, and don'ts.

### Step 3: Apply and Enforce
- Rewrite or generate content following the profile exactly
- After generating, self-check against the style guide
- Flag any deviations before presenting output

## Constraints
- Consistency is paramount — every sentence must pass the style check
- If no style reference is provided, ask for one before proceeding
- Never mix tones within a single piece unless explicitly asked

