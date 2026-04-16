---
name: "source-validation"
description: "Score source credibility, detect bias, and filter relevance. Evaluates reliability of information sources for research integrity."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["research", "validation", "credibility", "bias", "fact-checking"]
trigger_patterns:
  - "validate source"
  - "check credibility"
  - "fact check"
  - "source reliability"
  - "bias detection"
  - "evaluate source"
---

# Source Validation Skill

## When to Use
Activate when asked to evaluate, validate, or assess the credibility of information sources. Use during research to ensure quality and reduce bias.

## The Process

### Step 1: Identify Source Metadata
- **Author:** Who wrote it? Credentials?
- **Publication:** Where was it published? Reputation?
- **Date:** When was it published? Still relevant?
- **Type:** Primary research, opinion piece, news, blog, social media
- **URL/DOI:** Verifiable link

### Step 2: Credibility Scoring (0-10 each)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Author Expertise | 25% | Relevant credentials and track record |
| Publication Quality | 20% | Peer-reviewed? Editorial standards? |
| Recency | 15% | How current is the information |
| Citations/References | 15% | Does it cite sources? |
| Methodology | 15% | Is the approach sound? |
| Transparency | 10% | Conflicts of interest disclosed? |

### Step 3: Bias Detection
- **Financial bias:** Funded by interested parties?
- **Political bias:** Ideological framing?
- **Confirmation bias:** Cherry-picked data?
- **Survivorship bias:** Only showing successes?
- **Selection bias:** Unrepresentative sample?

### Step 4: Generate Report

```markdown
## Source Validation: [Source Title]

### Overall Score: [X]/10
- Credibility: [score]/10
- Relevance: [score]/10
- Bias Risk: [Low/Medium/High]

### Breakdown
| Criterion | Score | Notes |
|-----------|-------|-------|
| Author | [X]/10 | [Notes] |
| Publication | [X]/10 | [Notes] |
| Recency | [X]/10 | [Notes] |
| Citations | [X]/10 | [Notes] |
| Methodology | [X]/10 | [Notes] |
| Transparency | [X]/10 | [Notes] |

### Bias Assessment
- [Detected bias type]: [Explanation]

### Recommendation
[Use with confidence / Use with caution / Avoid / Cross-reference needed]
```

## Constraints
- Never accept a single source as definitive truth
- Flag all potential biases, even if minor
- Score objectively, not based on personal agreement with conclusions

