---
name: "uiux-layout-advisor"
description: "Provide spacing, hierarchy, accessibility, and layout suggestions for UI/UX design. Reviews designs and suggests improvements for usability and visual balance."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["visual", "ui", "ux", "design", "accessibility", "layout"]
trigger_patterns:
  - "ui layout"
  - "ux advice"
  - "design review"
  - "layout suggestion"
  - "accessibility"
  - "spacing"
  - "hierarchy"
---

# UI/UX Layout Advisor

## When to Use
Activate when asked to review, improve, or design UI/UX layouts, wireframes, component spacing, or accessibility features.

## The Process

### Step 1: Understand the Context
- What type of interface? (web app, mobile, dashboard, landing page)
- Who are the users?
- What is the primary action/goal?

### Step 2: Analyze Layout Principles

#### Visual Hierarchy
- Primary content should be largest and highest contrast
- Secondary content supports but doesn't compete
- Tertiary content is smallest, lowest contrast

#### Spacing System
- Use 4px/8px base grid
- Consistent padding within components (8-16px)
- Consistent gaps between components (16-24px)
- Generous whitespace around key actions

#### Accessibility Checklist
- Color contrast ratio: 4.5:1 minimum (WCAG AA)
- Touch targets: minimum 44x44px
- Text: minimum 16px body, 12px for labels
- Focus indicators visible and clear
- Alt text for all images
- Keyboard navigation supported

### Step 3: Generate Recommendations

```markdown
## Layout Review: [Component/Page]

### Structure
- [Layout recommendation with reasoning]

### Spacing
- [Specific padding/margin values]

### Hierarchy
- [Visual weight adjustments]

### Accessibility
- [A11y improvements]

### Quick Wins
1. [Highest impact change]
2. [Second highest]
3. [Third]
```

## Constraints
- Always reference WCAG 2.1 AA standards
- Provide specific pixel values, not vague guidance
- Consider mobile-first when applicable
- Never sacrifice usability for aesthetics

