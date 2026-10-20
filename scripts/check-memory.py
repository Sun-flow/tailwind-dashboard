"""Check the memory bank for drift: broken paths, unmapped files, missing dates and size budgets.

Usage: python3 scripts/check-memory.py   (exits 1 if anything needs fixing)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "memory-bank"
ENTRY_FILES = [ROOT / "AGENTS.md", ROOT / "CLAUDE.md"]

# Line budgets from memory-bank/README.md; log.md is budgeted in entries instead.
LINE_BUDGETS = {"README.md": 120, "context.md": 100, "status.md": 80, "notes.md": 100}
LOG_MAX_ENTRIES = 15

# Paths the docs name on purpose before they exist.
PLANNED_PATHS = {"archive/memory-bank/log-archive.md"}

PATH_EXTENSIONS = (".md", ".py", ".js", ".html", ".txt", ".json", ".png", ".sh", ".css")
CODE_SPAN = re.compile(r"`([^`\s]+)`")


def looks_like_path(token):
    if token.startswith(("http", "@", "-")) or "*" in token or "..." in token:
        return False
    return token.endswith("/") or token.lower().endswith(PATH_EXTENSIONS)


def path_exists(token, doc):
    token = token.split("#")[0]
    return any((base / token).exists() for base in (ROOT, BANK, doc.parent))


def main():
    problems = []
    bank_files = sorted(BANK.glob("*.md"))

    for doc in ENTRY_FILES + bank_files:
        if not doc.exists():
            problems.append(f"{doc.relative_to(ROOT)} is missing")
            continue
        for token in CODE_SPAN.findall(doc.read_text(encoding="utf-8")):
            if looks_like_path(token) and token not in PLANNED_PATHS and not path_exists(token, doc):
                problems.append(f"{doc.relative_to(ROOT)}: `{token}` doesn't exist")

    readme = (BANK / "README.md").read_text(encoding="utf-8")
    for f in bank_files:
        text = f.read_text(encoding="utf-8")
        if f"| `{f.name}` |" not in readme:
            problems.append(f"memory-bank/{f.name} isn't in the map in memory-bank/README.md")
        if "Last updated" not in text:
            problems.append(f"memory-bank/{f.name} has no 'Last updated' line")
        budget = LINE_BUDGETS.get(f.name)
        lines = len(text.splitlines())
        if budget and lines > budget:
            problems.append(f"memory-bank/{f.name} is {lines} lines (budget {budget}): trim or split it")

    log = BANK / "log.md"
    if log.exists():
        entries = sum(1 for line in log.read_text(encoding="utf-8").splitlines() if line.startswith("### "))
        if entries > LOG_MAX_ENTRIES:
            problems.append(f"memory-bank/log.md has {entries} entries (max {LOG_MAX_ENTRIES}): "
                            "move the oldest to archive/memory-bank/log-archive.md")

    for p in problems:
        print(f"FAIL  {p}")
    print(f"{'OK' if not problems else f'{len(problems)} problem(s)'}: "
          f"checked {len(bank_files)} memory files and {len(ENTRY_FILES)} entry files")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
