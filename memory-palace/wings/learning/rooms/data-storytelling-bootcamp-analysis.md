# Data Storytelling & Visualization Bootcamp — Comprehensive Analysis
## 4-Day Course by Joy Hopkins, Data Society (April 28 – May 1, 2026)

---

# DAY 1: Foundations — Data Types, Audience Analysis, Chart Anatomy

## Key Topics
- Defining data visualization (making data visual for digestibility)
- Exploratory vs. Explanatory data analysis
- Data type taxonomy (Qualitative → Nominal/Ordinal; Quantitative → Discrete/Continuous)
- The Who → What → How decision framework
- Tool landscape overview (Excel, Tableau, Power BI, Python, R, Canva, Flourish)
- Chart anatomy (7 components: title, axes, grid lines, data series, legend, markers, trend lines)
- Color accessibility (red-green colorblindness; orange-blue as safe default)

## Core Frameworks
1. **Who → What → How**: Audience first, message second, chart type last
2. **Exploratory vs Explanatory Spectrum**: Self-directed discovery vs audience-directed communication
3. **Data Classification Hierarchy**: Qualitative/Quantitative → Nominal/Ordinal/Discrete/Continuous
   - Litmus test: "Would you average it?" → Quantitative. "Staircase vs ramp" for discrete vs continuous.
   - Zip codes are numbers but qualitative (nominal).

## Key Principles
- One chart, one message
- Audience only knows what you tell them
- Everything in a chart must serve the story
- Decision-making skill > tool knowledge
- Paper/pencil sketch before opening any tool
- Consider multiple charts over one complex chart
- Not everything needs to be a chart

## Real-World Examples
- Challenger Space Shuttle disaster (1986): Original incomprehensible charts vs Tufte's redesign (temperature vs damage)
- Uber/Lyft vs Taxi chart: Hyperbolic titles, missing context, data ethics lesson
- Sales Rep table showing identical sums/averages but different monthly patterns

## Exercises
- Activity 1: Data type identification from commodity price report
- Activity 2: Chart anatomy labeling and critique

---

# DAY 2: Chart Types, Selection, and Decluttering

## Key Topics
- Deep dive into 12+ chart types (bar, line, area, pie, donut, heat map, scatter, bubble, box plot, histogram, tree map, waterfall, map)
- Four data relationship categories: Comparison, Composition, Distribution, Relationship
- Choosing the right visualization for your data
- Step-by-step chart decluttering workflow
- "Do I even need a chart?" test

## Core Frameworks
1. **Four Data Relationship Categories**:
   - Comparison → bar charts, line charts
   - Composition → pie charts, stacked area, tree maps, waterfall
   - Distribution → histograms, box plots
   - Relationship → scatter plots, bubble charts
2. **Chart Selection Decision Framework**: Data type → Relationship type → Variables count → Data points count → Grouping needs → Time display needs
3. **Decluttering Workflow**: Remove 3D → Remove background → Remove borders → Remove gridlines → Add direct labels → One highlight color + grayscale → Reduce decimal precision

## Key Rules by Chart Type
- Bar charts: qualitative data only
- Line charts: continuous data only ("if you can rearrange x-axis labels, don't use a line chart")
- Pie charts: max 4-5 slices, part-to-whole only
- Donut charts: avoid even more than pie (removes the central angles being compared)
- Area charts: only when line represents a composite
- Box plots: univariate, show summary stats, include n
- Histograms: show shape of distribution, bins are adjustable
- Tree maps: Joy's favorite for composition; "brains do better with rectangles than pie slices"

## Key Principles
- Ink on the page should mean something
- Cognitive load is the enemy
- 3D is almost never justified
- If you can take it out without losing the story, take it out
- "No relationship is a relationship" — null findings are still findings
- "It is an art informed by science"

## Real-World Examples
- Birthday heat map (months × days)
- Bubble chart of presidential speeches (4 dimensions)
- Olympic medals histogram (right-skewed distribution)
- Federal budget area chart (NASA spending over time)
- Expense chart decluttering demo (before/after)

## Exercises
- 10-question survey at start for later analysis
- Chart identification (10 charts, identify type and data type)
- Polling questions on relationship types
- Story + visualization planning (10 survey questions → what story, what chart)

---

# DAY 3: Visual Design, Common Mistakes, and Misleading Data

## Key Topics
- Cognitive load framework (every visual element costs brain power)
- 11-point visual design checklist
- Color theory (sequential, diverging, categorical schemes)
- 7 common mistakes in data visualization
- Misleading statistics taxonomy (collection, processing, presentation)
- Visual distortions (y-axis manipulation, compressed x-axis, inverted axes, 3D distortion, dual-axis false correlations)
- Hans Rosling Gapminder video analysis

## Core Frameworks
1. **Cognitive Load Framework**: Every element costs processing; that processing could go toward understanding the actual point
2. **11-Point Visual Design Checklist**: Light backgrounds, meaningful sorting, grouping, direct labels, size = importance, color with meaning, natural reading order, data gap marking, closed regions, color, labels
3. **Misleading Statistics Taxonomy**: Collection (sample size, biased sampling, loaded questions) → Processing (duplicates, ignoring outliers) → Presentation (hiding context, omitting findings)
4. **3D Chart Acceptance Criteria**: Third dimension must encode meaning AND chart must be interactive
5. **Consumer Defense Checklist**: Do math, check source, question methodology, cross-reference

## Key Principles
- "Numbers don't have to be fabricated to be misleading. If it's fabricated, it's not misleading, it's a lie."
- "You need a really, really, really compelling reason to not start your y-axis at zero."
- "There is no single ideal."
- "A pie chart is for comparing part to whole, and that's it."
- Direct labeling > separate legends
- Sort by the dimension that matters for the story
- Color as accent, not foundation
- "There's no rule that says you've got to get it all in one visualization."

## Real-World Examples
- NYT COVID radial chart (gained month-to-month comparison, lost trend visibility)
- Bill Gates bar example (outlier distorting average)
- Steubenville, Ohio income (Buffett/Winfrey moving there raises average 62%)
- Spurious Correlations website (tylervigen.com)
- Hans Rosling 200 Countries (120,000 numbers via progressive revelation)

## Exercises
- NYT COVID graph analysis (gains/losses of different chart forms)
- Survey data visualization critique (10 student-created charts evaluated)
- Visual distortion identification (y-axis tricks, compressed axes, false correlations)
- Company sales trajectory trick (same data, different year selections = different stories)

---

# DAY 4: Storytelling with Data — Putting It All Together

## Key Topics
- What is data storytelling (insight + persuasion + narrative + visuals)
- 5-step iterative storytelling process
- 7-part story structure
- ARE audience engagement framework
- Communication types (direct vs indirect)
- Storyboarding and plotting
- Format selection (slide deck, infographic, report, interactive, hybrid)
- Visualization gallery review and critique

## Core Frameworks
1. **5-Step Iterative Storytelling Process**:
   - Refine Insight → Tailor to Audience → Outline → Storyboard → Format
   - Can go back any number of steps, but must re-execute forward if returning to Step 1

2. **7-Part Story Structure**:
   - Setting (status quo) → Hook (disruption) → Beats (data points building tension) → Insight ("aha moment" — the MIDDLE) → Outcome → Actions → Measures
   - "The insight is not the end. It's the middle."

3. **ARE Audience Engagement Framework**:
   - Authority (decision power, hierarchy)
   - Reason (domain knowledge, data literacy)
   - Emotion (pre-existing beliefs, what matters to THEM)

4. **"Why Story?" Framework**: Stories help when insights are unpleasant, disruptive, unexpected, complicated, risky, or costly

5. **Communication Type Framework**: Direct (presenter controls pacing, flexible, can ad-lib) vs Indirect (audience controls pacing, must anticipate questions, permanent)

6. **Format Selection Matrix**: Slide deck (<50 words/slide), Infographic (stands alone), Report (text-heavy with appendix), Interactive (user-driven), Hybrid

7. **Data Relationships for Beats**: Comparison, drill-down, zoom-out, composition, distribution

## Key Principles
- One insight per story
- Narratives are more memorable than charts alone
- Context makes data stick
- Never dump information — build progressively
- Build suspense from slide to slide
- Low-tech storyboard first (paper, wireframes)
- Format affects story shape — can't just break a document into slides
- Readability > aesthetics
- Everyone tells stories — it's everyone's responsibility

## Real-World Examples
- Hans Rosling "200 Countries" (information sequencing technique)
- David McCandless "Mountains Out of Molehills" (hidden twin-peak pattern in video game coverage)
- SelfieCity project (interactive data story)
- Napoleon's March (pretty but poor at information)
- Florence Nightingale mortality data
- US Federal Budget tree map
- Disney gender dialogue analysis
- Solar Eclipse map (stunning but insufficient context)

## Exercises
- Audience-specific storytelling: Same insight framed for Marketing Team vs Head of Technical Support
- Story structure deconstruction: Breaking down McCandless TED talk into Setting/Hook/Beats/Insight/Action

---

# SYNTHESIS

## Top 10 Most Actionable Concepts → AI Agent Skills/Prompts

### 1. The Who-What-How Decision Engine
A universal pre-visualization checklist that forces audience-first thinking before any chart is made.
- **AI Skill**: Given a dataset and intended message, output the audience profile, core message, and recommended visualization type with justification.

### 2. The 5-Step Data Storytelling Process
Refine Insight → Tailor to Audience → Outline → Storyboard → Format (iterative, can return to any step).
- **AI Skill**: Walk users through each step, asking the right questions, producing deliverables at each stage.

### 3. The 7-Part Story Structure
Setting → Hook → Beats → Insight → Outcome → Actions → Measures. The insight is the MIDDLE, not the end.
- **AI Prompt Template**: Given a finding, construct a complete data story following this structure.

### 4. ARE Audience Analysis Framework
Authority, Reason, Emotion — with sub-factors for goals, timing, data literacy, power structures.
- **AI Skill**: Profile any audience along these three dimensions and recommend framing, complexity, and delivery format.

### 5. Chart Type Selection Engine
Data type (qual/quant) × Relationship type (comparison/composition/distribution/relationship) → Recommended chart(s).
- **AI Skill**: Given dataset metadata and a question to answer, recommend the optimal chart type with alternatives.

### 6. Chart Decluttering Audit
Systematic removal: 3D → background → borders → gridlines → add direct labels → grayscale + one accent → reduce precision.
- **AI Skill**: Given a description or image of a chart, produce a decluttered version specification.

### 7. Cognitive Load Audit
Every element costs brain power. If removing it doesn't hurt the story, remove it.
- **AI Prompt**: Review visualization and flag every element that doesn't directly serve the story.

### 8. Misleading Data Detector
Three-stage check: Collection (sample size, bias, loaded questions) → Processing (duplicates, outlier handling) → Presentation (y-axis, missing context, cherry-picking).
- **AI Skill**: Given a chart or dataset description, flag potential misleading elements.

### 9. Beat Ordering for Maximum Tension
Order data points from satisfying → unsatisfying → most dissatisfying. Never let tension decrease.
- **AI Prompt**: Given story beats, reorder for escalating tension and explain the optimal sequence.

### 10. Insight Refinement Protocol
Raw finding → What's the single most important thing? → What can the audience DO? → Why should they care? → What if they act? What if they don't?
- **AI Prompt**: Transform raw analysis findings into actionable, audience-ready insights.

---

## Reusable Templates & Formulas

### Template 1: Insight Statement Formula
```
The data shows [finding], which means [so what], and we should [action] because [outcome].
```

### Template 2: Data Story Construction Prompt
```
Given a dataset and analysis finding, construct a data story:
1. SETTING: Status quo before disruption (1-2 sentences)
2. HOOK: The anomaly/change/question (1-2 sentences)
3. BEATS: 3-4 data points building tension (ordered low→high tension)
4. INSIGHT: The single key finding ("aha moment")
5. OUTCOME: What we want to happen
6. ACTIONS: Specific steps the audience should take
7. MEASURES: How we track success

Constraint: ONE insight only.
```

### Template 3: Audience Analysis Checklist
```
AUTHORITY: Decision power? Hierarchy? Empowered to act?
REASON: Domain knowledge? Data literacy? Metrics they care about?
EMOTION: Pre-existing beliefs? What matters to THEM? Timing?

Output: Framing recommendation + Complexity level + Delivery format
```

### Template 4: Visualization Audit
```
For each element in the chart:
- Does it serve the story? (Y/N)
- Can it be removed without loss? (Y/N)
- Is it redundant with another element? (Y/N)
Remove all Y answers.

Check:
- Y-axis starts at zero? (If not, compelling reason?)
- Direct labels instead of legend?
- One highlight color + grayscale?
- Sorted meaningfully?
```

### Template 5: Chart Type Decision Tree
```
1. Qualitative or Quantitative data?
2. Relationship type: Comparison | Composition | Distribution | Relationship?
3. How many variables? How many data points?
4. Need grouping? Need time display?
5. Could this be a simple number or sentence instead?
```

### Template 6: Data Integrity Pre-Check
```
Collection: Sample size adequate? Sampling biased? Questions loaded?
Processing: Duplicates removed? Outliers examined (not blindly dropped)?
Presentation: Full context shown? Unfavorable findings included?
```

---

## Potential Agent Personalities/Specializations

### 1. Data Story Architect
Specializes in the 5-step storytelling process. Takes raw analysis findings and produces complete data stories with the 7-part structure. Asks ARE questions about the audience. Outputs storyboards.
- **Trigger phrases**: "help me tell a story with this data", "turn this analysis into a presentation", "create a data story"

### 2. Visualization Doctor
Specializes in chart critique and decluttering. Given a chart (description or image), diagnoses issues and prescribes fixes. Applies cognitive load framework, decluttering workflow, and accessibility standards.
- **Trigger phrases**: "review this chart", "improve this visualization", "declutter my chart", "audit this visualization"

### 3. Audience Translator
Specializes in adapting the same data story for different audiences. Takes one insight and produces versions for executives, technical teams, general public, and mixed audiences.
- **Trigger phrases**: "adapt this for executives", "present this to marketing", "same data different audience"

### 4. Misleading Data Detective
Specializes in detecting and preventing misleading visualizations and statistics. Checks for y-axis manipulation, cherry-picking, correlation vs causation, outlier distortion, and presentation bias.
- **Trigger phrases**: "is this chart misleading", "check for data integrity", "audit this visualization for honesty"

### 5. Chart Type Advisor
Specializes in recommending optimal chart types based on data types, relationship types, and audience needs. Applies the Who→What→How framework.
- **Trigger phrases**: "what chart should I use", "best visualization for this data", "which chart type"

---

## Complete Tool Reference from All 4 Days

| Tool | Category | When Mentioned |
|------|----------|----------------|
| Excel | Spreadsheet | Days 1-3 ("use of Excel will not be going away") |
| Tableau | BI Platform | Days 1-2 |
| Power BI | BI Dashboard | Days 1-3 |
| Python | Programming | Days 1-2 (Joy's primary tool) |
| R + RStudio | Programming | Day 1 |
| Seaborn | Python Library | Day 1 (Joy's EDA go-to) |
| Plotly/Plotly Express | Python Library | Days 1, 3 |
| Bokeh | Python Library | Day 1 (interactive) |
| Matplotlib | Python Library | Day 1 (underlying engine) |
| Canva | Infographic | Days 1, 3-4 (Joy's go-to for infographics) |
| Flourish | Data Story | Days 1, 3 |
| Figma | Design | Day 3 |
| Napkin AI | Infographic | Day 3 (participant mention) |
| Google Charts | Free Tool | Day 1 |
| PowerPoint | Presentation | Day 1 |
| Gapminder | Data/Tools | Days 3-4 (data available for download) |

---

## Master Principles Collection (All 4 Days)

1. Who comes first. Always. Before what, before how.
2. One chart = one message. One story = one insight.
3. Audience only knows what you tell them.
4. Everything in the chart must serve the story.
5. Cognitive load is the enemy — reduce relentlessly.
6. Ink on the page should mean something.
7. If you can remove it without losing the story, remove it.
8. Decision-making > tool knowledge.
9. Sketch on paper before opening any tool.
10. Start with the question, not the chart type.
11. Y-axis starts at zero unless you have a really compelling reason.
12. 3D is almost never justified.
13. Pie charts are for part-to-whole only, max 4-5 slices.
14. Orange-blue is the safest color combination.
15. Direct labels > separate legends.
16. Sort by the dimension that matters.
17. Context makes data stick.
18. Build suspense progressively — never dump information.
19. The insight is the middle of the story, not the end.
20. Format affects story shape.
21. Narratives beat charts alone for memorability.
22. Everyone is responsible for storytelling.
23. Numbers don't have to be fabricated to be misleading.
24. There is no single ideal — develop defaults, change when needed.
25. It is an art informed by science.
