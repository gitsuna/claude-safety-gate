# safety gate for Claude Code, v1.2

a fix release (2026-11-22). if you have v1.1, please update: one way of deleting files from PowerShell got past the delete rule.

## what changed

- **one more way of deleting is covered.** the delete-files rule now also stops .NET delete calls made from PowerShell, such as `[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory(...)` and `[System.IO.Directory]::Delete(...)`. in v1.1 they passed the gate. found by testing three commands from real data-loss reports on Anthropic's issue tracker; the other two (an rm with a wildcard, a find with -delete) were already stopped.
- core test suite: 36 cases (3 new, the three reported commands). gated suite unchanged at 20 cases.
- README: a hook's ask normally shows a prompt in auto mode, and Claude Code's own safety check can say no first.
- `safety_gate.py` and both settings snippets are unchanged since v1.1.

## how to update

1. copy the new `tests` folder over the old one.
2. the config: if you never edited `safety_gate_config.json`, copy the new one over it. if you did, keep yours and add this line to the delete-files rule's patterns, right after the `find ... -delete` line:

```
"::delete(directory|file)?\\s*\\(",
```

3. run both test suites, restart Claude Code, and do the live check in QUICKSTART.md.

## how to verify

run both test suites from the `tests` folder (Mac: use `python3`):

```
python run_tests.py
python run_gated_tests.py
```

the first should end with "36 of 36 cases behaved as expected", the second with "20 of 20 cases behaved as expected". if your numbers match, your gate works.

MIT licensed.
