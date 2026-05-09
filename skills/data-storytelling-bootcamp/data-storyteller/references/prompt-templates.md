# Data Storytelling Prompt Templates

Reusable prompts extracted from the Data Storytelling Bootcamp.

---

## Template 1: Insight Statement Builder

```
Given raw analysis findings, produce an insight statement:
"The data shows [finding], which means [so what], and we should [action] because [outcome]."

Then answer:
- What is the single most important thing?
- What can the audience DO about it?
- Why should they care?
- What happens if they act? If they don't?
```

---

## Template 2: Data Story Constructor

```
Construct a data story from findings using this structure:

1. SETTING: Status quo before disruption (1-2 sentences)
2. HOOK: The anomaly/change/question (1-2 sentences)
3. BEATS: 3-4 data points building tension (ordered low→high)
4. INSIGHT: The single key finding ("aha moment")
5. OUTCOME: What we want to happen
6. ACTIONS: Specific steps the audience should take
7. MEASURES: How we track success

Constraint: ONE insight only. Narratives > charts alone for memorability.
```

---

## Template 3: Audience Translator

```
Take this data insight and produce versions for:

1. EXECUTIVE: Focus on outcomes, ROI, strategic implications. Use ARE: Authority=decision power, Reason=business context, Emotion=what's at stake.
2. TECHNICAL TEAM: Include methodology, data quality notes, confidence intervals. Direct, data-heavy.
3. GENERAL AUDIENCE: Plain language, relatable analogies, visual-first. One number, one chart, one action.

For each version: specify format (deck/infographic/report), word count target, and which beats to emphasize.
```

---

## Template 4: Chart Deconstruction

```
Analyze this visualization:

For each element:
- Does it serve the story? (Y/N)
- Can it be removed without loss? (Y/N)
- Is it redundant? (Y/N)

Checks:
- Y-axis starts at zero?
- Direct labels instead of legend?
- One highlight color + grayscale?
- Sorted by the dimension that matters?
- 3D effects present? (Remove unless dimension encodes meaning AND chart is interactive)

Output: Before/after specification with specific changes listed.
```

---

## Template 5: Data Integrity Pre-Check

```
Before presenting data, verify:

Collection: Sample size adequate? Sampling biased? Questions loaded?
Processing: Duplicates removed? Outliers examined (not blindly dropped)?
Presentation: Full context shown? Unfavorable findings included?

If any check fails, fix before proceeding.
```

---

## Template 6: Beat Ordering for Maximum Tension

```
Given these story beats (data points), reorder them for escalating tension:

Rule: Order from satisfying → unsatisfying → most dissatisfying.
Tension must never decrease between consecutive beats.

For each beat, explain:
- Emotional valence (positive/neutral/negative)
- Tension level (1-10)
- Why this order creates the strongest narrative arc
```
