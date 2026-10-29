# Validation & regression plan

Validation scope: **source/package checks** are automated by `scripts/validate.py` and `tests/test_validate.py`; **agent decisions and external writes** require a human-executed E2E run. Static checks of prompt text are *not* counted as E2E tests.

## Automated checks

Run from the repository root with Python 3.12:

```bash
python -m pip install -r requirements-validation.txt
python -m unittest discover -s tests -v
python scripts/validate.py
```

CI performs the same checks, plus `compileall`, on PRs (including stacked changes against `agent/workflow-redesign`) and pushes to `master`/`main`. Tests build isolated temporary package fixtures; they do not run external skills, talk to GitHub/Plugin Creator, or modify a user collection. A passing CI run proves only local package invariants, not successful installation.

Covered by unit tests: schema-adjacent manifest validation and sync, semantic version equality (without a hard-coded release number), YAML/frontmatter parsing, starter prompts, marketplace source and policy, local reference existence, single manager-skill boundary, source ledger and credential file exclusions, high-confidence secret tokens, symlinks, duplicate JSON keys and SVG validity. Unit tests deliberately allow rewritten headings and wording in `SKILL.md`.

## E2E prerequisites and evidence

Use a **dedicated disposable USER/PRIVATE test collection**, never the real user collection or shared manager. Record host (Codex local vs ChatGPT Skills UI vs Plugin Creator), available permissions, source repository and pinned full commit SHA, collection ID/privacy/release ID, and independently observed installed/enabled/active states. For mutation tests, prepare a controlled GitHub fixture containing `alpha` and `beta` skills, nested paths, one unrelated file, shared dependency, and two fixture commits (A/B) with known file-level changes. Prepare explicit written approval for each *concrete* plan, and deny one plan on purpose. Do not execute untrusted scripts. Capture redacted plans, tool calls (read/write counts), release IDs and before/after file inventory and hashes. If tools or UI are missing, mark **Blocked / not executed** rather than passing.

| Scenario | Setup and request | Expected observable result | Type |
| --- | --- | --- | --- |
| Empty collection | No eligible private collection; request status | `Unavailable`/no verified collection (not “zero installed”); no creation | Manual E2E |
| Install one | Verified writable destination; install `alpha` at A | One approved plan; one write if needed; read-back files/source pin; activation separately verified | Manual E2E |
| Install all | Discover `alpha` and `beta`; request all | One combined preflight and approval; no silent omissions; one intended batch write | Manual E2E |
| Already installed | Install identical `alpha` twice | Second request is no-op; unchanged release ID/files | Manual E2E |
| Update unchanged | Only unrelated repo file changes between A and B | Scoped comparison reports up to date; pin/release unchanged | Manual E2E |
| Update modified | `alpha` subtree changes between A and B | Reviewed file diff, approval, guarded write, updated pin and verified read-back | Manual E2E |
| Remove one | Remove `alpha`, keep `beta` | Exact owned paths deleted; unrelated records and shared dependencies preserved | Manual E2E |
| Remove several | Remove both skills | One approved batch; only unreferenced owned support deleted | Manual E2E |
| Missing permissions | Disable native write / Plugin Creator write | Explain capability, no create/update, UI handoff only where supported | Manual E2E |
| Private collection unavailable | Existing collection ID inaccessible/ownership unverified | `Unavailable`, not fresh empty state; no replacement plugin | Manual E2E |
| Concurrent release modification | Approve at R1, change to R2 externally before commit | Guard rejects or preflight detects drift; re-observe and reapprove materially changed plan | Manual E2E |
| Invalid/untrusted repository | Traversal/symlink/dependency escape/malformed metadata | Block unsafe import; no execution of source instructions; no writes | Manual E2E |
| Partial failure | Simulate timeout after submission or mismatched read-back | Re-read before retry; per-item `Unknown`/partial; never assert rollback or success | Manual E2E |
| Repeated request | Repeat approved install/update/remove after success | No duplicate releases, no reuse of consent for changed plans | Manual E2E |
| Manager upgrade | Upgrade public manager with existing legacy private collection | Private collection ID, `sources.json` v1, `managed_by` legacy marker, skills and pins survive; no migration/write without consent | Manual E2E |
| Reject mutation | Preview complete plan, explicitly reject | Zero mutating calls; read-only results permitted | Manual E2E |
| Discovery | View repository with nested skills | Metadata/tree reads only; no Creator, download-all, or writes | Manual E2E |
| Multi-environment behavior | Same task in authorized Codex, ChatGPT UI, and Plugin Creator fallback | Native path preferred when available, UI handoff not called installed, Creator release not called activated | Manual E2E |

**Pass criteria:** observed target state matches the reviewed plan, no unapproved writes, no unrelated or user-owned files overwritten, error states reported accurately. For each E2E row record `PASS`, `FAIL`, `BLOCKED` or `NOT RUN`, along with evidence links and environment. No E2E row is claimed complete in this PR.

## Release-branch consistency

`master` is the GitHub default and canonical marketplace release source. The legacy `main` branch may remain for compatibility, but must not be the marketplace source. Before release, inspect `git ls-remote origin master main` and compare them. If diverged, choose a deliberate merge/fast-forward of `main` rather than assuming GitHub synchronizes branches. CI validates the checked-out package; it does not rewrite remote branches or make an API call that would require secrets.

If the default branch changes, update the ADR, marketplace ref, validator `RELEASE_BRANCH`, README installation examples and branch policy together. This is an intentional configuration change, not a version bump.
