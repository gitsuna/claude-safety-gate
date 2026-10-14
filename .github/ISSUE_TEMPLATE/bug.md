---
name: bug report
about: the gate did something you did not expect, or a test failed
title: ""
labels: bug
---

## what happened

tell us what you asked Claude to do, what the gate did, and what you expected instead.

## your setup

- operating system and version (for example Windows 11, macOS 15):
- Python version (`python --version` on Windows, `python3 --version` on Mac):
- Claude Code version (`claude --version`):
- mode in `safety_gate_config.json` (ask or block):

## failing test

if a test failed, paste the failing line from `run_tests.py` or `run_gated_tests.py` here, for example:

```
FAIL  rm -rf    expected ASK   got PASS
```

and the last line of the run ("N of M cases behaved as expected").

please remove any private paths, names or keys before posting.
