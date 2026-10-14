# safety gate for Claude Code, v1.0

first public release (2026-10-14). a small Python hook that makes Claude Code stop and ask before it pushes, deploys, posts, sends, pays or deletes.

## what is in it

- seven rules out of the box: git push, deploys and publishes, public posts, sending messages, payments, deleting files, and protecting the gate itself. an eighth, browser actions, ships switched off.
- ask mode (default) and block mode.
- fails closed: bad input, a missing or broken config, or a crash blocks the action. read-only tools keep working so Claude can help you fix it.
- core test suite (31 cases) and gated test suite (20 cases). results in TESTS.md.

## how to verify

run both test suites from the `tests` folder (Mac: use `python3`):

```
python run_tests.py
python run_gated_tests.py
```

the first should end with "31 of 31 cases behaved as expected", the second with "20 of 20 cases behaved as expected". if your numbers match, your gate works.

install steps are in QUICKSTART.md (10 minutes). MIT licensed.
