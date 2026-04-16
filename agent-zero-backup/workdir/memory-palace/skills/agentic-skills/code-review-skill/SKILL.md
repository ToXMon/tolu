---
name: "code-review-skill"
description: "Handle bug detection, optimization suggestions, and style enforcement in code reviews. Provides structured review with severity ratings and fix suggestions."
version: "1.0.0"
author: "Tolu Memory Palace"
tags: ["coding", "review", "quality", "bugs", "optimization", "best-practices"]
trigger_patterns:
  - "code review"
  - "review code"
  - "check code"
  - "code quality"
  - "find bugs"
  - "review pull request"
---

# Code Review Skill

## When to Use
Activate when asked to review code, check for bugs, optimize code quality, or evaluate a pull request.

## The Process

### Step 1: Identify Context
- **Language:** What programming language?
- **Purpose:** What does this code do?
- **Scope:** Single function, module, or full project?
- **Priority:** Security, performance, readability, or all?

### Step 2: Run the Review Checklist

#### Bug Detection
- Off-by-one errors
- Null/undefined handling
- Race conditions
- Resource leaks (unclosed files, connections)
- Type mismatches
- Unhandled edge cases

#### Security
- Input validation
- SQL injection / XSS risks
- Hardcoded secrets
- Insecure dependencies
- Authentication/authorization gaps

#### Performance
- Unnecessary loops or iterations
- Memory-heavy operations
- Missing caching opportunities
- Inefficient queries
- Blocking operations that could be async

#### Readability
- Clear naming conventions
- Appropriate abstractions
- Consistent formatting
- Meaningful comments (not redundant ones)
- Single responsibility per function

#### Testing
- Are there tests?
- Do tests cover edge cases?
- Are mocks appropriate?
- Is test coverage adequate?

### Step 3: Generate Review Report

```markdown
## Code Review: [File/Module]

### Summary
- **Issues Found:** [count]
- **Severity Breakdown:** Critical: [n] | Warning: [n] | Info: [n]
- **Overall Quality:** [1-10]

### Critical Issues
#### 1. [Issue Title]
**Line(s):** [line numbers]
**Problem:** [Description]
**Fix:** [Suggested fix with code]

### Warnings
#### 1. [Issue Title]
**Line(s):** [line numbers]
**Problem:** [Description]
**Suggestion:** [Suggested improvement]

### Info and Suggestions
- [Improvement suggestion]

### Positive Notes
- [What's done well]
```

## Constraints
- Always provide actionable fixes, not just problems
- Severity must match actual impact
- Don't nitpick style unless it affects readability
- Consider the codebase context (prototype vs production)

