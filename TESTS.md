# safety gate test results

this is the record of how the gate behaved when it was tested before release. you can re-run the same tests on your own computer in under a minute (see "run it yourself" at the bottom). if your numbers match, your gate works.

## how the tests work

each test is a fake message, the same shape Claude Code sends before a tool runs. it goes into `safety_gate.py` on stdin. the test checks the answer:

- **PASS** means the gate allowed it (exit code 0, no output).
- **ASK** means the gate paused it for your approval (exit code 0, a JSON "ask" answer).
- **BLOCK** means the gate cancelled it (exit code 2, a reason on stderr).

nothing in any test is actually run. the commands are just text inside the fake messages.

## core suite: `tests/run_tests.py`

run on 2026-10-13, Windows 11, Python 3.14. result: **31 of 31 cases behaved as expected, exit 0.**

```
ok    read a file                                  expected PASS  got PASS
ok    list files                                   expected PASS  got PASS
ok    git status                                   expected PASS  got PASS
ok    git log                                      expected PASS  got PASS
ok    write a draft file                           expected PASS  got PASS
ok    run a local script                           expected PASS  got PASS
ok    connector read                               expected PASS  got PASS
ok    word 'remove' inside a file name is fine     expected PASS  got PASS
ok    rm -rf                                       expected ASK   got ASK
ok    rm after &&                                  expected ASK   got ASK
ok    Remove-Item                                  expected ASK   got ASK
ok    del on Windows                               expected ASK   got ASK
ok    python shutil.rmtree                         expected ASK   got ASK
ok    git reset --hard                             expected ASK   got ASK
ok    git clean                                    expected ASK   got ASK
ok    connector delete_file                        expected ASK   got ASK
ok    edit the gate itself                         expected ASK   got ASK
ok    write settings.json                          expected ASK   got ASK
ok    shell edit of the gate config                expected ASK   got ASK
ok    not JSON on stdin                            expected BLOCK got BLOCK
ok    empty stdin                                  expected BLOCK got BLOCK
ok    JSON without tool_name                       expected BLOCK got BLOCK
ok    JSON list instead of object                  expected BLOCK got BLOCK
ok    block mode: rm is blocked, not asked         expected BLOCK got BLOCK
ok    block mode: safe command still passes        expected PASS  got PASS
ok    missing config: Bash blocked                 expected BLOCK got BLOCK
ok    missing config: Write blocked                expected BLOCK got BLOCK
ok    missing config: Read still allowed           expected PASS  got PASS
ok    broken config JSON: blocked                  expected BLOCK got BLOCK
ok    bad pattern in config: blocked               expected BLOCK got BLOCK
ok    unknown mode in config: blocked              expected BLOCK got BLOCK

31 of 31 cases behaved as expected
```

what this proves:

- normal work (reading, listing, git status, writing drafts, running a local script) is not slowed down.
- deleting files, by any of the common routes on Windows, Mac or inside Python, stops and asks.
- Claude cannot quietly edit the gate, its config, or your Claude settings.
- **fail closed:** bad input, an empty message, a missing config, a broken config, a bad pattern or a wrong mode all block the action. only the read-only tools (Read, Glob, Grep, LS) keep working, so Claude can still read files and help you fix the problem.
- block mode turns every "ask" into a hard block.

## gated suite: `tests/run_gated_tests.py`

this file covers git push, deploys, public posts, sending email and texts, and payments. 20 cases.

run on 2026-10-14, Windows 11, by hand in PowerShell outside Claude. result: **20 of 20 cases behaved as expected, exit 0.** (the build machine runs its own, stricter safety hook that refuses to let an agent run this file, because its text names real posting, mail and payment routes. that is the correct behavior for that hook, so the run was done by hand.)

run it yourself (step below): you should see the same 20 of 20. if you do not, see "if a test fails".

## run it yourself

1. open a terminal (Windows: PowerShell. Mac: Terminal).
2. go to the tests folder, for example: `cd ~/.claude/hooks/tests` (or wherever you put this repo's `tests` folder).
3. run the core suite: Windows `python run_tests.py`, Mac `python3 run_tests.py`.
4. run the gated suite: Windows `python run_gated_tests.py`, Mac `python3 run_gated_tests.py`.
5. both should end with "N of N cases behaved as expected".

the tests use `safety_gate.py` and `safety_gate_config.json` from the folder one level up. keep the `tests` folder next to them.

## if a test fails

- a FAIL line names the case. open `safety_gate_config.json` and look at the rule for that kind of action.
- if you changed the config, a FAIL may be what you intended (for example you turned a rule off). that is fine. update your own notes.
- if you did not change anything, paste the FAIL line into Claude and ask it to explain. Claude may read the files but cannot edit them without asking you, because of the protect-the-gate rule.

## what the tests do not prove

- the hook only sees what Claude Code shows it. a command hidden inside a script file (for example `python deploy.py` where the script deploys) looks like "run a local script" and passes. keep risky scripts out of your business folder, or name them clearly and add a pattern for them.
- whether your Claude Code version shows the "ask" prompt in every permission mode. see README.md, "ask or block".
