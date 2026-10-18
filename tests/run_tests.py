#!/usr/bin/env python3
"""
run_tests.py - core checks for the safety gate.

run it from anywhere:
    python run_tests.py        (Windows)
    python3 run_tests.py       (Mac / Linux)

each case feeds a fake Claude Code message into safety_gate.py on stdin and
checks what comes back: PASS (allowed), ASK (paused for your approval) or
BLOCK (cancelled). this file covers safe actions, deleting files (also through
the Monitor tool, which runs commands in the background), guarding the gate
itself, and every fail-closed error path. the push, deploy, post,
send and payment cases live in run_gated_tests.py. it changes nothing on
your computer: the error cases use temporary config files that are deleted
afterwards.
"""

import json
import sys
import tempfile

from gate_harness import ev, make_config, report, run

CASES = [
    ("read a file", ev("Read", file_path="notes/plan.md"), "PASS"),
    ("list files", ev("Bash", command="ls -la"), "PASS"),
    ("git status", ev("Bash", command="git status"), "PASS"),
    ("git log", ev("Bash", command="git log --oneline -5"), "PASS"),
    ("write a draft file", ev("Write", file_path="drafts/welcome-email.md", content="hi"), "PASS"),
    ("run a local script", ev("Bash", command="python scripts/report.py"), "PASS"),
    ("connector read", ev("mcp__notes__search_pages", query="pricing"), "PASS"),
    ("word 'remove' inside a file name is fine", ev("Bash", command="cat remove-list.md"), "PASS"),
    ("Monitor watching a log", ev("Monitor", command="tail -f logs/app.log"), "PASS"),
    ("rm -rf", ev("Bash", command="rm -rf old-drafts"), "ASK"),
    ("rm after &&", ev("Bash", command="cd tmp && rm notes.txt"), "ASK"),
    ("Remove-Item", ev("PowerShell", command="Remove-Item -Recurse .\\old"), "ASK"),
    ("del on Windows", ev("PowerShell", command="del notes.txt"), "ASK"),
    ("python shutil.rmtree", ev("Bash", command='python -c "import shutil; shutil.rmtree(\'x\')"'), "ASK"),
    ("git reset --hard", ev("Bash", command="git reset --hard HEAD~1"), "ASK"),
    ("git clean", ev("Bash", command="git clean -fd"), "ASK"),
    ("Monitor running rm -rf", ev("Monitor", command="rm -rf build"), "ASK"),
    ("connector delete_file", ev("mcp__drive__delete_file", id="123"), "ASK"),
    ("edit the gate itself", ev("Edit", file_path="/home/me/.claude/hooks/safety_gate.py", old_string="a", new_string="b"), "ASK"),
    ("write settings.json", ev("Write", file_path="C:\\Users\\me\\.claude\\settings.json", content="{}"), "ASK"),
    ("shell edit of the gate config", ev("Bash", command="echo {} > ~/.claude/hooks/safety_gate_config.json"), "ASK"),
    ("not JSON on stdin", "this is not json", "BLOCK"),
    ("empty stdin", "", "BLOCK"),
    ("JSON without tool_name", json.dumps({"tool_input": {"command": "ls"}}), "BLOCK"),
    ("JSON list instead of object", "[1, 2, 3]", "BLOCK"),
]

CONFIG_CASES = [
    ("block mode: rm is blocked, not asked", "BLOCK_MODE", ev("Bash", command="rm -rf old"), "BLOCK"),
    ("block mode: safe command still passes", "BLOCK_MODE", ev("Bash", command="git status"), "PASS"),
    ("missing config: Bash blocked", "MISSING", ev("Bash", command="ls"), "BLOCK"),
    ("missing config: Write blocked", "MISSING", ev("Write", file_path="a.md", content="x"), "BLOCK"),
    ("missing config: Read still allowed", "MISSING", ev("Read", file_path="a.md"), "PASS"),
    ("broken config JSON: blocked", "BROKEN_JSON", ev("Bash", command="ls"), "BLOCK"),
    ("bad pattern in config: blocked", "BAD_REGEX", ev("Bash", command="ls"), "BLOCK"),
    ("unknown mode in config: blocked", "BAD_MODE", ev("Bash", command="ls"), "BLOCK"),
]


def main():
    results = [(label, want, run(stdin)) for label, stdin, want in CASES]
    with tempfile.TemporaryDirectory() as tmp:
        for label, kind, stdin, want in CONFIG_CASES:
            results.append((label, want, run(stdin, make_config(kind, tmp))))
    sys.exit(report(results))


if __name__ == "__main__":
    main()
