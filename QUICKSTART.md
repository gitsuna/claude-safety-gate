# quickstart: the safety gate in 10 minutes

you need Claude Code 2.1.295 or newer (check with `claude --version`) and Python 3.8 or newer (check with `python --version` on Windows or `python3 --version` on Mac). upgrading from v1.0? see README.md, "upgrading from v1.0".

1. **find your Claude folder.** Windows: `C:\Users\<your name>\.claude\`. Mac: `~/.claude/`. no folder yet? open Claude Code once.
2. **make a `hooks` folder** inside it.
3. **copy in** `safety_gate.py`, `safety_gate_config.json` and the `tests` folder.
4. **run the tests** from the `tests` folder: `python run_tests.py` then `python run_gated_tests.py` (Mac: `python3`). both should end with "N of N cases behaved as expected".
5. **switch it on:** paste `settings-snippet-windows.json` or `settings-snippet-mac.json` into `.claude/settings.json`. Windows: replace `YOUR-WINDOWS-USERNAME` and use forward slashes. already have a settings file? see README.md, install step 6.
6. **restart Claude Code.**
7. **live check:** make an empty file called `test-delete-me.txt`, then ask Claude to delete it. you should see a prompt that mentions SAFETY-GATE. deny it. (in the desktop app the highlighted button may be "Always allow", so read before you click.)

that prompt is the gate working. from now on Claude asks before it pushes code, deploys, posts, sends a message, moves money or deletes files.

next: fill in `gated-actions.md` with your own accounts, and read "honest limits" in README.md so you know what a hook can and can't see.
