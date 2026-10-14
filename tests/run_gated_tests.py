#!/usr/bin/env python3
"""
run_gated_tests.py - checks the push, deploy, post, send and payment rules.

run it from anywhere:
    python run_gated_tests.py        (Windows)
    python3 run_gated_tests.py       (Mac / Linux)

nothing here sends, posts, pays or pushes. each case is only a fake
message fed to safety_gate.py on stdin, and the gate's answer is checked.
the commands inside the cases are never run.

why this is a separate file: some security tools (including other safety
hooks) refuse to run any script whose text contains real posting or
payment addresses, even in a test. if that happens to you, that is the
other tool doing its job. run this file yourself in a terminal, outside
Claude, and compare with TESTS.md.
"""

import sys
import tempfile

from gate_harness import ev, make_config, report, run

CASES = [
    ("git commit mentioning push is fine", ev("Bash", command='git commit -m "push the new pricing page"'), "PASS"),
    ("git push", ev("Bash", command="git push origin main"), "ASK"),
    ("git push with -C and extra spaces", ev("Bash", command="git -C ./site    push"), "ASK"),
    ("git push chained in PowerShell", ev("PowerShell", command="git add .; git commit -m x; git push"), "ASK"),
    ("connector push_files", ev("mcp__github__push_files", repo="site"), "ASK"),
    ("vercel deploy", ev("Bash", command="npx vercel --prod"), "ASK"),
    ("npm run deploy", ev("Bash", command="npm run deploy"), "ASK"),
    ("npm publish", ev("Bash", command="npm publish"), "ASK"),
    ("gh pr merge", ev("Bash", command="gh pr merge 12"), "ASK"),
    ("post to X api", ev("Bash", command="curl -X POST https://api.x.com/2/tweets -d '{}'"), "ASK"),
    ("slack webhook", ev("Bash", command="curl -X POST https://hooks.slack.com/services/T0/B0/x"), "ASK"),
    ("connector create_post", ev("mcp__social__create_post", text="hello world"), "ASK"),
    ("connector send_email", ev("mcp__mail__send_email", to="a@example.com", body="hi"), "ASK"),
    ("python mail library", ev("Bash", command='python -c "import smtplib"'), "ASK"),
    ("PowerShell Send-MailMessage", ev("PowerShell", command="Send-MailMessage -To a@example.com"), "ASK"),
    ("text message api", ev("Bash", command="curl https://api.twilio.com/2010-04-01/Accounts"), "ASK"),
    ("stripe api call", ev("Bash", command="curl https://api.stripe.com/v1/charges -d amount=500"), "ASK"),
    ("connector create_payment", ev("mcp__pay__create_payment", amount=47), "ASK"),
]

CONFIG_CASES = [
    ("block mode: git push is blocked", "BLOCK_MODE", ev("Bash", command="git push"), "BLOCK"),
    ("block mode: send email is blocked", "BLOCK_MODE", ev("mcp__mail__send_email", to="a@example.com"), "BLOCK"),
]


def main():
    results = [(label, want, run(stdin)) for label, stdin, want in CASES]
    with tempfile.TemporaryDirectory() as tmp:
        for label, kind, stdin, want in CONFIG_CASES:
            results.append((label, want, run(stdin, make_config(kind, tmp))))
    sys.exit(report(results))


if __name__ == "__main__":
    main()
