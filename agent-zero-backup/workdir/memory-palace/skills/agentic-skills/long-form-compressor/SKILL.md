---
name: "long-form-compressor"
description: "Condense dense long-form material into key points, TLDRs, and executive summaries. Extracts the signal from noise. Best for research digestion and quick overviews."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["writing", "summary", "compression", "tldr", "executive summary"]
trigger_patterns:
  - "summarize"
  - "compress"
  - "tldr"
  - "executive summary"
  - "condense"
  - "key points"
  - "brief overview"
---

# Long-Form to Summary Compressor

## When to Use
Activate when asked to summarize, condense, or extract key points from long-form content — articles, reports, documents, transcripts, or research papers.

## Compression Levels

### Level 1: TLDR (1-3 sentences)
The absolute core message. What would you tell someone in an elevator?

### Level 2: Key Points (5-8 bullets)
The main arguments, findings, or takeaways. No fluff.

### Level 3: Executive Summary (1-2 paragraphs)
A structured overview with context, key findings, and implications.

### Level 4: Structured Summary (detailed)
Organized by sections with sub-headings, each with a 1-2 sentence distillation.

## The Process

### Step 1: Parse the Source
- Identify the thesis/main argument
- Extract supporting evidence and data points
- Note conclusions and recommendations

### Step 2: Filter Signal from Noise
- Remove filler, repetition, and tangents
- Keep only novel or important information
- Preserve critical numbers, names, and dates

### Step 3: Generate at Requested Level
- Default to Level 2 (Key Points) if no level specified
- Maintain the original author's intent
- Use clear, direct language

## Output Format
```markdown
## TLDR
[1-3 sentences]

## Key Points
- [Point 1]
- [Point 2]

## Notable Details
- [Specific data, quotes, or findings worth preserving]

## Bottom Line
[One sentence: what should the reader do or think after reading this?]
```

## Constraints
- Never add information not in the source
- Preserve nuance — don't oversimplify complex arguments
- Always include the source context (who, what, when)

