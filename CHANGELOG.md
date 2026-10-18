# changelog

## v1.1 (2026-10-17)

- **Windows fix.** the Windows settings snippet now starts Python directly (`"command": "python"` with the script in `"args"`), with no shell. the v1.0 line ended in `|| exit 2`, which Windows PowerShell 5.1 can't read. Claude Code no longer needs Git for Windows, and without it (and without PowerShell 7) it runs hooks in Windows PowerShell, so on a fresh Windows 11 the v1.0 line either never ran the gate or blocked every action, depending on the Claude Code version.
- **fail closed on timeouts and start failures.** both snippets set `"onFailure": "block"`. without it, a hook that times out or can't start lets the action through. needs Claude Code 2.1.295 or newer.
- **Monitor covered.** Monitor, the tool Claude uses to run commands in the background, now goes through every shell rule, same as Bash and PowerShell.
- README: minimum Claude Code version, "upgrading from v1.0", a note on the desktop app's "Always allow" button, a note on auto mode, and how to tell a gate block (it says SAFETY-GATE) from Claude Code's own.
- core test suite: 33 cases (2 new, for Monitor). gated suite unchanged at 20 cases.

## v1.0 (2026-10-14)

- first public release.
- seven rules out of the box: git push, deploys and publishes, public posts, sending messages, payments, deleting files, and protecting the gate itself. an eighth, browser actions, ships switched off.
- ask mode (default) and block mode.
- fails closed: bad input, a missing or broken config, or a crash blocks the action. read-only tools keep working so Claude can help you fix it.
- core test suite (31 cases) and gated test suite (20 cases). results in TESTS.md.
