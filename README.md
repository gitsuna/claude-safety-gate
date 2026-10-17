# safety gate for Claude Code

free, open, 160 lines of Python. Claude stops and asks before it pushes, deploys, posts, sends, pays or deletes. new here? start with `QUICKSTART.md` (10 minutes).

**what this does for your business:** Claude can do real things on your computer. that is the point. but a few actions can hurt you in one click: a half-finished website goes live, an email goes to the wrong person, money moves, a folder of work disappears. the safety gate makes Claude stop and ask you before any of those. you stay the only one who can press the big buttons.

## what is in this folder

| file | what it is |
|---|---|
| `safety_gate.py` | the gate itself. a small Python script, 160 lines, no extra installs |
| `safety_gate_config.json` | the list of risky actions it watches. you can edit it |
| `settings-snippet-windows.json` | the lines that switch the gate on, for Windows |
| `settings-snippet-mac.json` | the same, for Mac |
| `gated-actions.md` | a plain-English list of what you never let an agent do alone. fill it in |
| `tests/` | tests you can run to prove it works. results in `TESTS.md` |
| `QUICKSTART.md` | the 10-minute install on one page |
| `CHANGELOG.md` | what changed in each version |

## how it works, in plain English

Claude Code has a feature called hooks. a hook is a small program Claude Code runs at a set moment. this one runs **before every tool call**, meaning before Claude runs a command, edits a file, or uses a connector.

the gate reads what Claude is about to do and checks it against your list:

- **nothing risky:** it stays silent. Claude carries on. you will not notice it.
- **risky, mode "ask":** Claude Code pauses and shows you a prompt with the reason. you choose allow or deny.
- **risky, mode "block":** the action is cancelled. Claude is told to tell you what it wanted to do, and you do it yourself.
- **anything goes wrong** (a broken config, a crash, Python missing): the action is blocked. this is called failing closed. a broken lock should keep the door shut, not swing it open.

## what it watches out of the box

1. **git push.** sending code to GitHub or similar. on many website setups, a push is a live deploy.
2. **deploys and publishes.** Vercel, Netlify, Cloudflare, Firebase, Heroku, `npm publish` and the like.
3. **public posts.** X, Facebook, Instagram, LinkedIn, Threads, Bluesky, Reddit, Slack and Discord webhooks.
4. **sending messages.** email by any common route (SMTP, the Google and Microsoft mail APIs, SendGrid, Mailgun, Resend, Postmark), texts (Twilio).
5. **payments.** Stripe, PayPal, Square, Lemon Squeezy, Gumroad, and any connector whose action names a charge, payment, invoice, purchase, refund or transfer.
6. **deleting files.** `rm`, `del`, `Remove-Item`, Python deletes, `git clean`, `git reset --hard`, and connector deletes.
7. **the gate itself.** Claude may not edit the gate, its config, or your Claude settings file without asking. otherwise it could switch the gate off.

connectors (the "mcp" tools you add to Claude, like an email or Google Drive connector) are matched by the action's name: anything named like send, reply, forward, post, publish, deploy, delete, trash, charge or purchase.

an eighth rule, **browser-actions**, is in the config but switched off. it asks before every click Claude makes in a browser. turn it on (`"enabled": true`) if you let Claude drive a browser while logged in to accounts that matter.

## install (10 minutes)

you need Python 3.8 or newer. check with `python --version` (Windows) or `python3 --version` (Mac). if it is missing, install it from python.org. on Windows, tick "Add python.exe to PATH" in the installer.

1. **find your Claude folder.** Windows: `C:\Users\<your name>\.claude\`. Mac: your home folder, then `.claude` (in Finder press Cmd+Shift+. to show hidden folders). if it does not exist, open Claude Code once and it will be created.
2. **make a `hooks` folder inside it** if there is not one.
3. **copy in** `safety_gate.py`, `safety_gate_config.json` and the `tests` folder.
4. **run the tests** (see TESTS.md, "run it yourself"). both suites should say all cases behaved as expected.
5. **open `settings.json`** in the `.claude` folder with a plain text editor (Notepad, TextEdit in plain text mode). if it does not exist, create it.
6. **paste the snippet** from `settings-snippet-windows.json` or `settings-snippet-mac.json`.
   - empty file: paste the whole snippet.
   - file already has content: add the `"hooks"` part inside the outer `{ }`, with a comma after the item before it. if there is already a `"hooks"` section, add the `PreToolUse` entry inside it. if unsure, paste your file and the snippet into a Claude chat and ask it to merge them. then paste the result back yourself.
   - Windows: replace `YOUR-WINDOWS-USERNAME` with your real folder name. use forward slashes `/` in the path.
7. **restart Claude Code.**
8. **live check.** ask Claude: "please delete the file test-delete-me.txt" (make an empty file with that name first). you should get a prompt mentioning SAFETY-GATE. deny it. the gate works.

## ask or block

- **"ask" (default)** is the friendly mode. you approve each risky action in the moment.
- **"block"** is the strict mode. Claude can never do these actions. it prepares everything, then hands you the exact command to run yourself.

use **block** if you ever run Claude Code with permission prompts turned off (sometimes called "skip permissions" or "bypass permissions" mode). an "ask" may not show a prompt in that mode, depending on your Claude Code version. block mode does not depend on prompts at all. to switch, open `safety_gate_config.json` and change `"mode": "ask"` to `"mode": "block"`.

## changing the list

open `safety_gate_config.json` in a text editor. each rule has:

- `name`: a short label you will see in the prompt.
- `why`: the plain-English reason, also shown in the prompt.
- `tools`: which Claude tools it watches. `Bash|PowerShell` means terminal commands. `mcp__.*` means connectors.
- `patterns`: what to look for. these are "regular expressions". the easy version: a plain word works, and `\\b` means "word edge". example, to gate a script called `send-invoices.py`, add `"send-invoices"` to a rule's patterns.
- `enabled`: `false` turns a rule off without deleting it.

after any change, run the tests again. a typo in the file makes the gate block everything until it is fixed. that is the fail-closed design working, not a bug.

## honest limits

- this is a seatbelt, not a vault door. it catches the normal ways an assistant does risky things. it reads the command, not the inside of every script. `python my-script.py` passes even if that script sends email. keep scripts that send, post or pay out of your business folder, or add their names to the patterns.
- it works only inside Claude Code. it does not watch the Claude website or phone app.
- it never replaces your own judgment. when the prompt appears, read it.

## if the gate gets in your way

- a prompt for something harmless: allow it. if it happens often, make that rule's pattern narrower.
- everything is suddenly blocked, but Claude can still read files: the config is broken. ask Claude to read `safety_gate_config.json` and find the error, then fix it yourself.
- everything is blocked, reading included: Python moved or the path in `settings.json` is wrong. Claude can't help from inside this state. fix the path in `settings.json` yourself (see TROUBLESHOOTING.md in the kit, or the install steps above), then restart Claude Code.
- to switch the gate off completely: remove the `PreToolUse` entry from `settings.json` and restart Claude Code. do this yourself, never through Claude.

---

## where this comes from

this gate is module 3 of 6 in **The One-Person OS by suna from sunabuilds**, a starter kit for running a one-person business on Claude. the gate stops Claude doing the wrong thing. the kit teaches it the right thing, for your business, every session: a router so Claude knows who you are, memory that carries decisions between sessions, loops for repeatable work, a knowledge vault and three skills. details at sunabuilds.ai/os.
