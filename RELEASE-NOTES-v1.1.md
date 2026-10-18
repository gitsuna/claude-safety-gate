# safety gate for Claude Code, v1.1

a fix release (2026-10-17). if you installed v1.0, please update: on a fresh Windows 11, the v1.0 settings line can stop the gate from running, or block every action.

## what changed

- **Windows fix.** the Windows settings snippet now starts Python directly, with no shell. the v1.0 line ended in `|| exit 2`, which Windows PowerShell 5.1 can't read. Claude Code no longer needs Git for Windows, and without it (and without PowerShell 7) it runs hooks in Windows PowerShell.
- **fail closed on timeouts and start failures.** both snippets now set `"onFailure": "block"`, so a gate that can't start, crashes or runs past its 20 seconds blocks the action instead of letting it through. needs Claude Code 2.1.295 or newer.
- **Monitor covered.** Monitor, the tool Claude uses to run commands in the background, now goes through every shell rule, same as Bash and PowerShell.
- README: the minimum Claude Code version, how to upgrade, a note on the desktop app's "Always allow" button, a note on auto mode, and how to tell a gate block (it says SAFETY-GATE) from Claude Code's own.

## how to update

1. copy the new `safety_gate.py` and the `tests` folder over the old ones.
2. the config: if you never edited `safety_gate_config.json`, copy the new one over it. if you did (for example you switched to block mode or added patterns), keep yours and add `|Monitor` after `PowerShell` in every rule whose `"tools"` line names PowerShell (7 rules). that keeps your mode and your patterns.
3. replace your `PreToolUse` entry in `settings.json` with the new snippet for your system.
4. run both test suites, restart Claude Code, and do the live check in QUICKSTART.md.

## how to verify

run both test suites from the `tests` folder (Mac: use `python3`):

```
python run_tests.py
python run_gated_tests.py
```

the first should end with "33 of 33 cases behaved as expected", the second with "20 of 20 cases behaved as expected". if your numbers match, your gate works.

MIT licensed.
