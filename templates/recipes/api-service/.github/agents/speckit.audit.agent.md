---
description: Audit the repository for consistency between code, API contract, tests, CI/build tooling, and documentation, and report or fix findings.
---

## Purpose

This agent performs the kind of repository-wide consistency audit that
caught real, previously undetected bugs in a past project: an OpenAPI
spec whose paths didn't match the actual routes at all, test/CI/Makefile
credential mismatches, a silently-broken CI health-check, and
infrastructure docs that described behavior the actual compose file
didn't implement. Run it periodically (e.g. before a release) and
whenever something "should just work" but doesn't.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).
If the user only wants specific checks (e.g. "nur die OpenAPI-Konsistenz
prüfen"), narrow the scope to those checks below.

## Checks to perform

Perform each applicable check (skip a check silently if the technology it
targets isn't used in this repository, e.g. skip OpenAPI checks if there
is no OpenAPI file):

1. **API contract parity**: Enumerate every route the application code
   actually registers (method + path) and every path/method documented in
   the API contract (OpenAPI/GraphQL schema/etc.). Report any route in
   code but not in the contract, and vice versa. Do this programmatically
   (parse the code's route registrations and the contract file), not by
   spot-reading a few endpoints.

2. **Dangling references**: If the contract uses `$ref`-style references
   (OpenAPI, JSON Schema), verify every reference resolves to a schema/
   response/parameter that actually exists in the document. Also flag
   schemas defined but never referenced anywhere (dead schemas).

3. **Credential and config consistency**: Compare database/service
   credentials and default ports across: test fixtures/conftest, the
   Makefile (or equivalent local dev tooling), the CI workflow file(s),
   `docker-compose.yml`, and `.env.example`. Flag any mismatch that would
   cause local tooling or CI to fail to connect, hang, or silently use
   different values than intended. Also flag version mismatches (e.g. a
   database image pinned to different major versions in different
   places).

4. **CI health**: Check whether CI has actually been passing on recent
   runs (e.g. via the platform's CLI, such as `gh run list`). A workflow
   that looks correct on paper can still be broken (e.g. a shell quoting
   bug in a health-check flag) and this often stays unnoticed because
   nobody watches CI once it "should" work. If CI is failing, identify
   the root cause before assuming any other check's findings are the
   only problem.

5. **Infrastructure docs vs. real behavior**: For any documented
   infrastructure behavior (tunnel setup, deployment commands, service
   startup), verify the actual configuration/command produces that
   behavior — don't just read the docs and the compose/config file
   side by side and assume consistency; if feasible, actually run the
   relevant container/command locally with a placeholder value and
   observe the real behavior, especially where a flag might silently
   change semantics (e.g. a "quick"/ephemeral vs. "named"/stable tunnel
   mode).

6. **Documentation structure**: Check for redundant or conflicting
   documentation files (e.g. multiple guides describing the same setup
   process with different, possibly outdated, instructions), dead
   internal links between docs, and stale references to files that no
   longer exist (e.g. a manifest or instructions file pointing at a
   deleted file). Prefer a single canonical operational document over
   many scattered ones; recommend archiving (not necessarily deleting)
   superseded docs with a clear marker that they're historical.

7. **Stale/leftover files**: Look for files that appear to be one-off
   artifacts with no active reference anywhere in the repo (e.g. leftover
   PR-description scratch files, old `NOTES.md` files, generated files
   that should have been gitignored). Confirm via search that nothing
   references them before flagging for removal.

## Reporting

Present findings grouped by severity:

- 🔴 Critical: contract/code mismatches, dangling references, broken CI,
  infra behavior contradicting its documentation — anything that causes
  incorrect behavior or is actively misleading.
- 🟡 Medium: version/credential mismatches, stale references, missing
  dev-dependency files — things that work today but are fragile or
  confusing.
- ✅ Already consistent: call out what was checked and found fine, so the
  user knows the audit was thorough rather than assuming silence means
  "not checked."

Do not silently fix anything without either (a) explicit user instruction
to do so, or (b) the user having already approved fixing findings from
this class of audit in the current conversation. When fixing, verify each
fix (e.g. re-run the test suite, actually start the affected container)
rather than assuming the fix is correct because it "looks right."

## Extension Hooks

If `.specify/extensions.yml` exists in the project root, check for hooks
under `hooks.before_audit` and `hooks.after_audit` following the same
enable/condition/optional rules used by the other speckit agents in this
project (skip conditions you cannot evaluate, run mandatory hooks and
wait for them, announce optional hooks without auto-running them). Skip
silently if the file doesn't exist or has no such hooks.
