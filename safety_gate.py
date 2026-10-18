#!/usr/bin/env python3
"""
safety_gate.py - a PreToolUse hook for Claude Code.

the free safety gate from "The One-Person OS by suna from sunabuilds".
plain-english explanation in
README.md, next to this file.

what it does
- Claude Code runs this script before every tool call and sends it a small
  JSON message on stdin (the tool name and what the tool is about to do).
- the script checks that against the rules in safety_gate_config.json.
- no rule matches: it exits 0 and says nothing. the action goes ahead.
- a rule matches, mode "ask": it tells Claude Code to stop and ask you
  first. you see the reason and click allow or deny.
- a rule matches, mode "block": it exits with code 2. the action is
  cancelled and Claude is told why. you do the action yourself.

fail closed
- if anything goes wrong (bad JSON in, missing or broken config file, a
  bad pattern, any crash), the script blocks the action with exit code 2.
- the only exception: the read-only tools listed in READ_ONLY_TOOLS still
  pass on an error, so Claude can still read files and help you fix it.
- the settings.json snippet sets "onFailure": "block", so a gate that
  can't start, crashes or runs out of time blocks the action too.

limits (honest)
- this is a pattern guard. it catches the normal ways an agent deploys,
  posts, sends, pays, deletes or pushes. a determined attacker with access
  to your computer can get around any pattern list. treat it as a seatbelt,
  not a vault door.

standard library only. works on Windows, Mac and Linux with Python 3.8+.
"""

import json
import os
import re
import sys

CONFIG_NAME = "safety_gate_config.json"
READ_ONLY_TOOLS = {"Read", "Glob", "Grep", "LS"}
SHELL_TOOLS = {"Bash", "PowerShell", "Monitor"}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
MARK = "SAFETY-GATE"


def block(reason):
    """Exit code 2 = Claude Code cancels the tool call and shows the reason."""
    sys.stderr.write(MARK + ": " + reason + "\n")
    sys.exit(2)


def ask(reason):
    """Tell Claude Code to pause and ask the owner before running the tool."""
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": MARK + ": " + reason,
        }
    }
    sys.stdout.write(json.dumps(out))
    sys.exit(0)


def flatten(obj):
    """Turn any JSON value into one string, so patterns can scan it."""
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return " ".join(str(k) + " " + flatten(v) for k, v in obj.items())
    if isinstance(obj, (list, tuple)):
        return " ".join(flatten(x) for x in obj)
    return str(obj)


def load_config():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.environ.get("SAFETY_GATE_CONFIG") or os.path.join(here, CONFIG_NAME)
    with open(path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    mode = cfg.get("mode", "ask")
    if mode not in ("ask", "block"):
        raise ValueError('config "mode" must be "ask" or "block"')
    rules = cfg.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError('config needs a non-empty "rules" list')
    compiled = []
    for rule in rules:
        if not rule.get("enabled", True):
            continue
        name = rule["name"]
        tools = re.compile(rule.get("tools", ".*"))
        pats = [re.compile(p, re.IGNORECASE) for p in rule["patterns"]]
        if not pats:
            raise ValueError("rule " + name + " has no patterns")
        compiled.append((name, rule.get("why", name), tools, pats))
    return mode, compiled


def text_to_scan(tool, tool_input):
    """What the rules look at, per tool type."""
    if tool in SHELL_TOOLS:
        return str(tool_input.get("command") or flatten(tool_input))
    if tool in WRITE_TOOLS:
        # the path is what matters: is Claude editing the gate itself?
        return str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
    # MCP tools, WebFetch, everything else: the tool name plus all its inputs
    return tool + " " + flatten(tool_input)


def main():
    raw = sys.stdin.read()
    tool = ""
    try:
        event = json.loads(raw)
        if not isinstance(event, dict):
            raise ValueError("hook input is not a JSON object")
        tool = str(event.get("tool_name", ""))
        tool_input = event.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            tool_input = {"value": tool_input}
        if not tool:
            raise ValueError("hook input has no tool_name")
        mode, rules = load_config()
        text = text_to_scan(tool, tool_input)
        # collapse runs of whitespace so "git    push" still matches
        text = re.sub(r"\s+", " ", text)
        for name, why, tools, pats in rules:
            if not tools.fullmatch(tool):
                continue
            for pat in pats:
                if pat.search(text):
                    reason = (
                        "gated action [" + name + "]: " + why + ". "
                        "this needs the owner's approval. "
                        "Claude: do not retry, reword or work around this. "
                        "tell the owner exactly what you want to run and why."
                    )
                    if mode == "block":
                        block(reason)
                    ask(reason)
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as exc:  # fail closed
        if tool in READ_ONLY_TOOLS:
            sys.exit(0)
        block(
            "the safety gate hit an error and blocked this action to stay safe ("
            + type(exc).__name__ + ": " + str(exc)[:200] + "). "
            "the owner should check safety_gate_config.json and the hook path."
        )


if __name__ == "__main__":
    main()
