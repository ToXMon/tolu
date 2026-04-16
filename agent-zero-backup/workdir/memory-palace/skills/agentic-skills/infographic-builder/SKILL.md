---
name: "infographic-builder"
description: "Generate sectioned, visual-friendly content summaries suitable for infographic layout. Creates structured content blocks with hierarchy, stats callouts, and visual cues."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["visual", "infographic", "design", "content", "presentation"]
trigger_patterns:
  - "infographic"
  - "visual summary"
  - "information graphic"
  - "visual content"
---

# Infographic Builder

## When to Use
Activate when asked to create infographic content, visual summaries, or information layouts for design tools.

## The Process

### Step 1: Parse the Source Material
- Extract key statistics, comparisons, timelines, and processes
- Identify the narrative arc (problem > data > insight > conclusion)
- Find quotable facts and figures

### Step 2: Structure the Infographic
Organize into sections:

```markdown
## Infographic: [Title]

### Header
- **Title:** [Bold, attention-grabbing headline]
- **Subtitle:** [Supporting context, 5-10 words]

### Section 1: The Problem/Context
- [Key stat or fact]
- [Supporting detail]
- Visual cue: [Icon suggestion: warning, globe, chart]

### Section 2: The Data
- **Stat Callout:** [Big number] — [What it means]
- **Comparison:** [A vs B in simple terms]
- [Supporting data point]

### Section 3: The Insight
- [Key takeaway]
- [Why it matters]

### Section 4: The Takeaway
- [Action item or conclusion]
- [CTA if applicable]

### Footer
- Sources: [List]
- Brand/logo placement note
```

### Step 3: Add Visual Cues
For each section, suggest:
- Icon type (from common sets: FontAwesome, Material)
- Color mood (warm/cool/alert/neutral)
- Layout direction (top-down, left-right, radial)

## Constraints
- Each section should be scannable in 3 seconds
- Maximum 6 sections per infographic
- Every claim needs a source
- Numbers should be humanized ("1 in 3" not "33.3%")

