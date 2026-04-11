#!/bin/bash
#
# Tolu Memory Palace — Daily Backup Script
# Syncs Agent Zero state to the tolu GitHub repository
#
# Usage: bash /a0/usr/workdir/tolu/scripts/daily-backup.sh
#

set -e

REPO_DIR="/a0/usr/workdir/tolu"
BACKUP_DIR="$REPO_DIR/agent-zero-backup"
LOG_FILE="$REPO_DIR/BACKUP-LOG.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')

echo "🔄 Starting Tolu backup at $TIMESTAMP"

# Ensure we're in the repo directory
cd "$REPO_DIR"

# Ensure git credentials are configured
git config user.name "Tolu Backup Bot" 2>/dev/null || true
git config user.email "tolu-backup@agent-zero.local" 2>/dev/null || true

# ─── Sync Agent Zero State ─────────────────────────────────────

echo "📦 Syncing Agent Zero directories..."

# 1. Knowledge base
rsync -a --delete /a0/usr/knowledge/ "$BACKUP_DIR/knowledge/" 2>/dev/null || echo "⚠️  knowledge sync had issues"

# 2. Agent profiles
rsync -a --delete /a0/usr/agents/ "$BACKUP_DIR/agents/" 2>/dev/null || echo "⚠️  agents sync had issues"

# 3. Custom skills
rsync -a --delete /a0/usr/skills/ "$BACKUP_DIR/skills/" 2>/dev/null || echo "⚠️  skills sync had issues"

# 4. User plugins
rsync -a --delete /a0/usr/plugins/ "$BACKUP_DIR/plugins/" 2>/dev/null || echo "⚠️  plugins sync had issues"

# 5. Workdir files (excluding tolu repo itself and other large/temp items)
mkdir -p "$BACKUP_DIR/workdir"
rsync -a --delete \
  --exclude='tolu/' \
  --exclude='venv/' \
  --exclude='__pycache__/' \
  --exclude='node_modules/' \
  --exclude='.git/' \
  /a0/usr/workdir/ "$BACKUP_DIR/workdir/" 2>/dev/null || echo "⚠️  workdir sync had issues"

# 6. Custom prompts (user overrides only - skip framework defaults)
if [ -d /a0/prompts ]; then
  mkdir -p "$BACKUP_DIR/prompts"
  # Only copy files that differ from the framework defaults
  rsync -a /a0/prompts/ "$BACKUP_DIR/prompts/" 2>/dev/null || echo "⚠️  prompts sync had issues"
fi

# 7. Memory database export (FAISS index + metadata)
MEMORY_DIR="/a0/usr/memory"
if [ -d "$MEMORY_DIR" ]; then
  mkdir -p "$BACKUP_DIR/memory-export"
  rsync -a --delete "$MEMORY_DIR/" "$BACKUP_DIR/memory-export/" 2>/dev/null || echo "⚠️  memory export had issues"
  echo "✅ Memory database exported"
else
  echo "ℹ️  No memory directory found at $MEMORY_DIR"
fi

# ─── Update MANIFEST timestamp ─────────────────────────────────

if command -v python3 &>/dev/null; then
  python3 -c "
import json
m = json.load(open('$REPO_DIR/MANIFEST.json'))
m['last_backup'] = '$TIMESTAMP'
json.dump(m, open('$REPO_DIR/MANIFEST.json','w'), indent=2)
print('✅ MANIFEST.json updated')
" 2>/dev/null || echo "⚠️  MANIFEST update failed"
fi

# ─── Git Commit & Push ──────────────────────────────────────────

echo "📝 Committing changes to git..."
git add -A

# Only commit if there are changes
if git diff --cached --quiet; then
  echo "✅ No changes to commit — backup is up to date"
else
  git commit -m "🔄 Daily backup — $TIMESTAMP"
  echo "🚀 Pushing to GitHub..."
  git push origin main
  echo "✅ Backup pushed to GitHub"
fi

# ─── Update Backup Log ──────────────────────────────────────────

echo "- **$TIMESTAMP** — Daily backup completed" >> "$LOG_FILE"

echo ""
echo "🎉 Tolu backup complete at $(date '+%Y-%m-%d %H:%M:%S %Z')"
