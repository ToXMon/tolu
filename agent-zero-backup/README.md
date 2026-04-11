# 🔄 Agent Zero Daily Backup

This directory contains the automated daily backup of the Agent Zero instance.

## What's Backed Up

| Directory | Source | Description |
|-----------|--------|-------------|
| `agents/` | `/a0/usr/agents/` | Agent profiles and configurations |
| `knowledge/` | `/a0/usr/knowledge/` | Knowledge base (fragments, solutions, main) |
| `memory-export/` | `/a0/tmp/memory.sqlite` | Memory database snapshot |
| `plugins/` | `/a0/usr/plugins/` | Installed plugins and configs |
| `prompts/` | `/a0/prompts/` | Prompt templates and overrides |
| `skills/` | `/a0/usr/skills/` | Custom skills (SKILL.md files) |
| `workdir/` | `/a0/usr/workdir/` | Working directory files |

## Restore Instructions

To restore to a fresh Agent Zero instance:

```bash
# Copy each backup directory to its Agent Zero path
cp -r agents/ /a0/usr/agents/
cp -r knowledge/ /a0/usr/knowledge/
cp -r plugins/ /a0/usr/plugins/
cp -r skills/ /a0/usr/skills/
cp -r prompts/ /a0/prompts/
cp memory-export/memory.sqlite /a0/tmp/memory.sqlite
# Workdir files selectively as needed
```
