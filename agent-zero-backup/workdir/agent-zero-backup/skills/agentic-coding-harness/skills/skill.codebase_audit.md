---
name: codebase-audit
version: "1.0.0"
trigger: /audit
description: >
  Checks codebase against 0xSero standards: files >300 lines, dirs >20 files,
  `any` types, missing AGENTS.md, missing tests. Outputs AUDIT_REPORT.md.
---

# Codebase Audit

Slash command: `/audit`

## When activated:
When the user types `/audit` or says "audit codebase" or "check code health":

## Instructions

1. **Identify the project directory** — Use the current working directory or ask the user.

2. **Run the audit checks** — Execute each check via terminal commands:

### Check 1: Files exceeding 300 lines
```bash
find <project_dir> -type f \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' \) \
  ! -path '*/node_modules/*' ! -path '*/.git/*' ! -path '*/__pycache__/*' \
  ! -path '*/dist/*' ! -path '*/build/*' ! -path '*/venv/*' ! -path '*/.next/*' \
  -exec sh -c 'lines=$(wc -l < "$1"); if [ "$lines" -gt 300 ]; then echo "$lines $1"; fi' _ {} \; \
  | sort -rn
```

### Check 2: Directories exceeding 20 source files
```bash
find <project_dir> -type f \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' \) \
  ! -path '*/node_modules/*' ! -path '*/.git/*' ! -path '*/__pycache__/*' \
  | xargs dirname | sort | uniq -c | sort -rn | awk '$1 > 20'
```

### Check 3: `any` type usage
```bash
# TypeScript
find <project_dir> -type f \( -name '*.ts' -o -name '*.tsx' \) \
  ! -path '*/node_modules/*' ! -path '*/dist/*' \
  -exec grep -l ': any' {} \;

# Python
find <project_dir> -type f -name '*.py' \
  ! -path '*/venv/*' ! -path '*/__pycache__/*' \
  -exec grep -l 'Any' {} \;
```

### Check 4: Missing AGENTS.md files
```bash
python3 /a0/skills/agentic-coding-harness/instruments/agents_md_generator.py verify <project_dir>
```

### Check 5: Missing tests
```bash
# Find source files without corresponding test files
find <project_dir> -type f -name '*.py' ! -name 'test_*' ! -name '*_test.py' \
  ! -path '*/venv/*' ! -path '*/__pycache__/*' ! -path '*/tests/*' \
  | while read f; do
      base=$(basename "$f" .py)
      dir=$(dirname "$f")
      if ! find "$dir" -name "test_${base}.py" -o -name "${base}_test.py" | grep -q .; then
        echo "No test for: $f"
      fi
    done
```

3. **Generate AUDIT_REPORT.md** — Compile results:

```markdown
# Codebase Audit Report
Date: [date]
Project: [name]

## Summary
| Check | Count | Status |
|---|---|---|
| Files > 300 lines | [N] | [PASS/WARN/FAIL] |
| Dirs > 20 files | [N] | [PASS/WARN/FAIL] |
| `any` type usage | [N] | [PASS/WARN/FAIL] |
| Missing AGENTS.md | [N] | [PASS/WARN/FAIL] |
| Missing tests | [N] | [PASS/WARN/FAIL] |

## Details
### Files Exceeding 300 Lines
[list with line counts]

### Directories Exceeding 20 Files
[list with file counts]

### `any` Type Usage
[list files and occurrences]

### Missing AGENTS.md
[list directories]

### Missing Tests
[list source files without tests]

## Recommendations
[prioritized fix list]
```

4. **Save the report** — Write to `<project_dir>/AUDIT_REPORT.md`

5. **Display summary** — Show the summary table and top 3 priorities.

## Severity Levels

- **PASS** (green): 0 issues found
- **WARN** (yellow): 1-3 issues found
- **FAIL** (red): 4+ issues found

## Auto-fix Options

After audit, offer to:
- Generate missing AGENTS.md files: `/gen-docs`
- Split files exceeding 300 lines (manual review needed)
- Create test stubs for files missing tests
