---
name: data-honesty-check
version: "1.0.0"
description: >
  Detect misleading statistics, visual distortions, and data integrity issues using the three-stage
  taxonomy (Collection, Processing, Presentation) from the Data Storytelling Bootcamp.
  Use when reviewing charts for honesty, checking data integrity, auditing visualizations for distortion,
  or evaluating whether a chart or dataset could mislead its audience.
  Triggers: "misleading", "honesty check", "data integrity", "distortion", "cherry-pick",
  "y-axis", "manipulation", "is this chart honest", "audit for honesty".
author: Tolu
trigger_patterns:
  - "is this chart misleading"
  - "check data integrity"
  - "audit this visualization for honesty"
  - "is this data honest"
  - "misleading chart"
  - "data distortion"
  - "cherry-picked data"
  - "y-axis manipulation"
  - "check for visual tricks"
  - "audit this statistic"
tags: ["data-storytelling", "ethics", "visualization", "audit"]
metadata:
  source: "Data Storytelling Bootcamp by Joy Hopkins, Data Society (April 2026)"
  core_frameworks: ["Misleading Statistics Taxonomy", "Consumer Defense Checklist"]
---

# Data Honesty Check Skill

## Purpose
Detect and prevent misleading visualizations and statistics through systematic integrity auditing.

## Core Principle
> "Numbers don't have to be fabricated to be misleading. If it's fabricated, it's not misleading, it's a lie."

Misleading data is usually *true* data presented in a way that creates false impressions. This skill catches that gap.

---

## Stage 1: Collection Integrity

Check how the data was gathered:

| Check | Red Flag | Example |
|-------|----------|--------|
| **Sample size** | Too small to support conclusions | Survey of 20 people generalized to millions |
| **Sampling bias** | Non-representative sample | Online poll excluding non-internet users |
| **Loaded questions** | Questions designed to produce a specific answer | "Don't you agree that...?" |
| **Self-selection bias** | Only motivated respondents participate | Customer satisfaction survey sent only to repeat buyers |
| **Survivorship bias** | Only successful cases visible | Investment fund showing only current funds, not closed ones |
| **Time period selection** | Window chosen to support a narrative | "Crime is up!" (comparing to unusually low year) |

---

## Stage 2: Processing Integrity

Check how the data was handled after collection:

| Check | Red Flag | Example |
|-------|----------|--------|
| **Duplicate data** | Inflated counts | Same survey response counted twice |
| **Outlier handling** | Outliers dropped without justification | Removing "bad" data points that contradict the story |
| **Aggregation level** | Granularity hides or creates patterns | Averages hiding bimodal distributions |
| **Missing data handling** | Gaps not disclosed | Dropping non-respondents instead of reporting response rate |
| **Calculation errors** | Wrong formula or method | Using mean for skewed data where median is appropriate |

**Key example:** Two sales reps with identical averages ($12K/month) but completely different patterns — one steady, one volatile. The aggregation hides the story.

**The Bill Gates bar problem:** If Bill Gates walks into a bar of 10 people, the *average* net worth rises 62%. The *median* barely changes. Averages lie when distributions are skewed.

---

## Stage 3: Presentation Integrity

Check how findings are communicated:

| Check | Red Flag | Example |
|-------|----------|--------|
| **Y-axis manipulation** | Not starting at zero without compelling reason | Chart showing dramatic change that's actually 2% |
| **Compressed x-axis** | Time axis distorted to exaggerate trends | Equal spacing for 1 year and 10 year intervals |
| **Inverted axes** | Y-axis inverted to flip the visual story | "Gun deaths went down!" (axes flipped, they went up) |
| **3D distortion** | Perspective makes near bars look bigger | 3D pie chart where front slice appears larger |
| **Dual axes** | Two unrelated scales implying correlation | Temperature and CO2 on dual axes with aligned peaks |
| **Cherry-picked range** | Favorable time window selected | Same data, different year ranges telling opposite stories |
| **Missing context** | No comparison or benchmark | "Revenue up 50%" (but market grew 80%) |
| **Correlation ≠ causation** | Implied causation from correlation | Ice cream sales and drowning both increase in summer |
| **Hidden findings** | Unfavorable results not shown | Clinical trial reporting only the positive endpoint |
| **Proportion distortion** | Visual area not proportional to value | Icon chart where twice the value gets 4x the visual area |

---

## Visual Distortion Detection Checklist

Run these specific checks on any chart:

- [ ] Y-axis starts at zero? If not, is there a documented compelling reason?
- [ ] Time axis has consistent intervals?
- [ ] No inverted axes creating false impressions?
- [ ] No 3D effects distorting proportions?
- [ ] No dual axes implying false correlation?
- [ ] Area and size proportional to values?
- [ ] Full data range shown (no cherry-picked windows)?
- [ ] Comparison/benchmark provided for context?
- [ ] Correlation explicitly NOT framed as causation?
- [ ] Unfavorable findings included alongside favorable ones?

---

## Consumer Defense Checklist

When *consuming* someone else's data presentation:

1. **Do the math** — Recalculate key numbers from the raw data
2. **Check the source** — Who collected it? What's their interest?
3. **Question the methodology** — How was it collected? What's the sample size?
4. **Cross-reference** — Does this match other sources?
5. **Look for what's missing** — What's NOT shown? What was excluded?

---

## Output Format

For each honesty audit:

```
DATA HONESTY REPORT

Overall Rating: [Clean / Caution / Misleading / Deceptive]

=== COLLECTION ISSUES ===
| # | Issue | Severity | Detail |

=== PROCESSING ISSUES ===
| # | Issue | Severity | Detail |

=== PRESENTATION ISSUES ===
| # | Issue | Severity | Detail |

=== VISUAL DISTORTIONS ===
| # | Distortion Type | Severity | Detail |

=== RECOMMENDATIONS ===
1. [Specific fix for each issue]

=== HONESTY VERDICT ===
[1-2 sentence summary of whether the visualization can be trusted and what to fix]
```

Severity levels: **Critical** (fundamentally changes the conclusion), **High** (significantly misleads), **Medium** (creates wrong impression but recoverable), **Low** (minor, could be unintentional).
