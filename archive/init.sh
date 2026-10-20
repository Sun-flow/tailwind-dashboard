#!/usr/bin/env bash
# init.sh — Initialize the agent workspace
# Usage: bash .agents/scripts/init.sh
# Last updated: 2026-10-19

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
echo "=== Agent Workspace Init ==="
echo "Root: $ROOT"

# 1. Verify .agents structure
echo ""
echo "--- Agent Rules ---"
if [ -d "$ROOT/.agents/rules" ]; then
    echo "✅ .agents/rules/ exists"
    for f in "$ROOT/.agents/rules/"*.md; do
        name="$(basename "$f")"
        [ "$name" = "*.md" ] && echo "   (no .md files)" && break
        echo "   ✅ $name"
    done
else
    echo "⚠️  .agents/rules/ missing"
fi

# 2. Check resources
echo ""
echo "--- Resources ---"
if [ -d "$ROOT/resources" ]; then
    echo "✅ resources/ exists"
    for f in "$ROOT/resources/"*.md; do
        name="$(basename "$f")"
        [ "$name" = "*.md" ] && echo "   (no .md files)" && break
        echo "   ✅ $name"
    done
else
    echo "ℹ️  resources/ not present"
fi

# 3. Check memory-bank (not yet initialized)
echo ""
echo "--- Memory Bank ---"
if [ -d "$ROOT/memory-bank" ]; then
    echo "✅ memory-bank/ exists — has been initialized"
else
    echo "ℹ️  memory-bank/ not present — will be generated when directed"
fi

# 4. Check for AGENTS.md
echo ""
echo "--- Entry Point ---"
if [ -f "$ROOT/AGENTS.md" ]; then
    echo "✅ AGENTS.md found"
else
    echo "❌ AGENTS.md missing"
fi

# 3. Check core dependencies
echo ""
echo "--- Dependencies ---"
if command -v python3 &>/dev/null; then
    echo "✅ python3 $(python3 --version 2>&1)"
else
    echo "❌ python3 not found"
fi

if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Flask installed"
else
    echo "⚠️  Flask not installed — run: pip3 install flask"
fi

echo ""
echo "=== Init Complete ==="