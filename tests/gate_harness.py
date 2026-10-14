"""
gate_harness.py - shared helpers for the two test files. you never run
this one directly.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "..", "safety_gate.py")
REAL_CONFIG = os.path.join(HERE, "..", "safety_gate_config.json")


def ev(tool, **tool_input):
    """A fake Claude Code PreToolUse message."""
    return json.dumps({"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input})


def run(stdin, config_path=None):
    """Feed one message to the gate on stdin. returns PASS, ASK or BLOCK."""
    env = dict(os.environ)
    if config_path:
        env["SAFETY_GATE_CONFIG"] = config_path
    p = subprocess.run(
        [sys.executable, GATE], input=stdin, capture_output=True, text=True, env=env, timeout=20
    )
    if p.returncode == 2:
        return "BLOCK"
    if p.returncode == 0 and p.stdout.strip():
        try:
            d = json.loads(p.stdout)["hookSpecificOutput"]
            if d.get("permissionDecision") == "ask":
                return "ASK"
        except Exception:
            return "WEIRD"
    if p.returncode == 0:
        return "PASS"
    return "EXIT" + str(p.returncode)


def make_config(kind, tmpdir):
    """A temporary config for the error cases. never touches the real one."""
    if kind == "MISSING":
        return os.path.join(tmpdir, "does-not-exist.json")
    with open(REAL_CONFIG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    if kind == "BLOCK_MODE":
        cfg["mode"] = "block"
        text = json.dumps(cfg)
    elif kind == "BAD_REGEX":
        cfg["rules"][0]["patterns"] = ["(unclosed"]
        text = json.dumps(cfg)
    elif kind == "BAD_MODE":
        cfg["mode"] = "maybe"
        text = json.dumps(cfg)
    else:  # BROKEN_JSON
        text = json.dumps(cfg)[:-5]
    path = os.path.join(tmpdir, kind + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def report(results):
    """results: list of (label, expected, got). prints and returns exit code."""
    passed = 0
    for label, want, got in results:
        ok = want == got
        passed += ok
        print(("ok  " if ok else "FAIL") + "  " + label.ljust(44) + " expected " + want.ljust(5) + " got " + got)
    print()
    print("%d of %d cases behaved as expected" % (passed, len(results)))
    return 0 if passed == len(results) else 1
