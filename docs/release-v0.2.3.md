# Agent Skills Manager v0.2.3 — integration and release review

**Date:** 2026-10-29  
**State:** Source release candidate; **not published**. Merge, plugin installation, enablement and skill activation are separate operations.

## Integrated baseline

The release branch starts at `agent/validation-tests` (`cc31ca298f971bcaa789c60942db5e389cae2418`), which contains the work from the following **still-open** PRs:

| PR | Scope | Integration |
| --- | --- | --- |
| #1 | Native capabilities, persistence and architecture | Included through #4 |
| #2 | Pinned, metadata-only GitHub discovery | Included through #4 |
| #3 | Approval-gated, guarded collection operations | Included through #4 |
| #4 | DISCOVER / STATUS / MUTATE routing and short UX | Included in #5 ancestry |
| #5 | Manifest sync, source validator and 23 regression tests | Direct parent of release branch |

The release PR targets `master` and therefore includes this entire as-yet-unmerged stack. **Do not merge the individual overlapping PRs and the release PR independently without reconciling/closing superseded PRs.** Do not change the canonical marketplace to `main` as an unintended side effect.

## Cross-workflow checks

| Boundary | Expected invariant | Evidence / limit |
| --- | --- | --- |
| Discovery | Pinned Git tree + candidate SKILL.md metadata only | Read-only probe below; no Plugin Creator |
| Status | Accessible native/verified private inventory only; no inferred absence | Instructions reviewed; no user inventory accessed |
| Mutation | Selected dependencies and provenance checked; one plan/approval per batch; verified read-back | Specification reviewed; **write E2E not run** |
| No-op and concurrency | No release for unchanged effective state; guard and reconcile after uncertain writes | Code-independent agent contract; **write E2E not run** |
| Privacy | Public manager contains no private ledger/third-party skill; existing USER/PRIVATE collections untouched | Package validator and repository inspection |
| Lifecycle | Published, installed/enabled and active are independently verified | Explicitly separated in SKILL.md and operations.md |

`Locally modified` is a local-state flag, not an alternative upstream freshness state. The primary skill now states this consistently with the operations reference. No native write capability or transactional storage is implied by this documentation.

## Executed read-only discovery probe

**Source:** https://github.com/AidarKhusainov/skills  
**Ref:** `master` at full commit `56cb469463acda79921bf420eccf503881240d0b`  
**Tree:** `d5a0ed2f1a86b07008beeccddc29679770dde1f4`, `truncated: false`

Read repository metadata, resolve the commit, obtain the recursive tree and read the leading `SKILL.md` metadata for each of the four candidates. This minimal trace is **7 GitHub read actions, 0 write actions**, without full-repository download or Plugin Creator. Each candidate has valid nonempty `name` and `description`; no name collision was seen.

| Candidate | Skill directory | Metadata |
| --- | --- | --- |
| `clear-explanations` | `clear-explanations/` | Verified |
| `production-java-backend-development` | `production-java-backend-development/` | Verified |
| `strict-backend-code-review` | `strict-backend-code-review/` | Verified |
| `use-case-spec` | `use-case-spec/` | Verified |

A missing-directory path can be distinguished from an empty valid subtree using the complete tree listing. This probe is **read-only discovery E2E at the tool/data boundary**, not a tested installation or proof of how a future model will route every user utterance.

## Automated validation

The previous stacked PR #5 passed GitHub Actions [Validate plugin source](https://github.com/AidarKhusainov/agent-skills-manager/actions/runs/40860007915) on 2026-10-29: Python syntax check, 23 isolated unit tests and actual-package validation. **That result predates these release-branch edits.** The release PR must have an independent passing CI run before review completion.

Run locally or in CI:

```bash
python -m pip install -r requirements-validation.txt
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/validate.py
```

The release candidate adds three tests for `VERSION` mismatch, omission and malformed content, extending the fixture suite from 23 to **26 test definitions**. Test definitions are not counted as passes until CI reports them.

## v0.2.2 UX comparison

The baseline `master` `SKILL.md` (`v0.2.2`) is **1,682 whitespace-separated words**; the current release-branch version after the Codex provenance correction is **1,181** (~**30% fewer**). Earlier integration measurements (1,070 words) predate that correction. The shorter instruction explicitly routes discovery, status and mutation without requiring Plugin Creator for discovery or verified native operations.

| Dimension | v0.2.2 instructions | v0.2.3 candidate instructions |
| --- | --- | --- |
| Routine discovery | Repository browsing available, but first-use explanation steers toward Plugin Creator | Explicit minimal pinned tree/frontmatter path, no Creator or companion audit |
| Persistent installation | Plugin Creator private collection only | Verified native path first, UI handoff or optional verified private collection |
| Batch approval | Approval per concrete write; no explicit unified batch pipeline | One combined preflight, one approval per stable batch |
| Unchanged repeated operation | Described generally, no unified no-op gate | Explicit no-op and no unnecessary release |
| Status dimensions | Upstream/local status already distinguished | Distinction preserved and made explicit |

**Measured runtime impact:** not established for v0.2.2. The 7-read discovery trace is a v0.2.3 pathway observation, **not** a matched A/B agent benchmark. Counts of actual redundant questions, tool invocations, repeated reads and preparation steps across versions require paired conversations in the same environment.

## E2E execution and blockers

- **Read-only GitHub discovery:** PASS for the four real candidates above.
- **Plugin Creator missing / private storage unavailable:** instruction/fallback review PASS; actual agent/runtime behavior **NOT RUN**. Expected outcome is `Unavailable`, no fabricated empty collection and no replacement creation.
- **Install one/all, repeat, update, remove, concurrent change, partial failure and rejected plan:** **NOT RUN**. The user requires a separate explicit approval for concrete write operations. No disposable USER/PRIVATE test collection or approved write scope was provided, and no private collection was modified.
- **Native Codex filesystem installation and ChatGPT Skills UI upload/activation:** **NOT RUN** in this session. Read-only access to GitHub does not prove host write, persistence, installation or activation capabilities.
- For the full manual matrix, see [regression test plan](regression-test-plan.md); do not interpret its scenario definitions as executed E2E results.

## Migration notes

1. **Existing managed collections:** no migration. Preserve plugin identity, `sources.json` schema v1, `managed_by: "skills-manager-public"`, pinned SHAs and user adaptations. An inaccessible collection is **unknown/unavailable**, not deleted.
2. **Marketplace source:** `master` is canonical. Existing local marketplace registrations pinned to `main` may require explicit user-side re-registration with `--ref master`. Do not force-update `main` or assume local registrations migrate.
3. **Older local plugin identity:** `skills-manager-public:manage-skills` and `agent-skills-manager:manage` are different local entries. Replace only the manager entry if needed, not any private collection.
4. **Install/activation:** a GitHub merge, source tag, Plugin Creator published release and an enabled/active skill are distinct events; verify them separately.
5. **Release tooling:** update `VERSION` and both manifest versions together for future releases; the validator rejects mismatches.

## Release checklist (review gates)

- [x] Integrated source contains architecture, discovery, operations, UX and validation changes (#1–#5).
- [x] Read-only real-repository discovery and namespace/privacy boundary reviewed.
- [x] Release version is `0.2.3` in `VERSION` and both manifests.
- [x] Changelog, migration notes and E2E limitations documented.
- [ ] The **release PR's own** CI passes; inspect the final merge commit and all checks.
- [ ] Review the combined PR against `master` for changes, secrets, ownership and no duplicate integration.
- [ ] Execute separately approved isolated write-E2E (or formally accept/document the untested risk).
- [ ] Complete runtime UX A/B evaluation where both environments and permissions are available.
- [ ] Verify the target host's packaging, installation/enabling and activation independently.
- [ ] Obtain release approval; **only then** merge, tag/publish or update Plugin Creator if explicitly authorized.

**Release decision:** hold publication until review and applicable verification gates are satisfied. This PR deliberately neither publishes nor updates private user plugins.

## Final independent readiness audit (2026-10-29)

**Decision: NO-GO for publication until isolated mutation E2E has been executed.** This is an evidence gate, not evidence of data loss or an observed destructive failure.

| Check | Result | Evidence / boundary |
| --- | --- | --- |
| PR #6 combined diff / stacked PR integration | PASS | 20 paths against `master`; no duplicate file paths. The architecture/discovery files from #1/#2 match the release branch byte-for-byte. #1–#5 remain open and overlap. |
| Candidate source/package CI | PASS before final report edit; recheck latest HEAD | [Validate plugin source](https://github.com/AidarKhusainov/agent-skills-manager/actions) ran 26 unit tests and package validation after the workflow corrections. |
| Real GitHub discovery | PASS | `AidarKhusainov/skills` at `56cb469463acda79921bf420eccf503881240d0b`; 35 complete tree entries, 4 verified metadata candidates, no writes or Creator calls. |
| Unknown source / missing-ref API behavior | PASS at read-tool boundary only | A deliberately invalid GitHub ref returned HTTP 422; agent error wording was not executed as a runtime test. |
| RU intent routing and readable status | SPEC REVIEW ONLY | Modes checked against four Russian phrases; no autonomous agent runtime invoked. |
| Native Codex provenance | FIXED IN INSTRUCTIONS; E2E BLOCKED | Explicitly distinguish tracked vs untracked skills and pinned update skips; see `skills/manage/SKILL.md` and `skills/manage/references/operations.md`. No executable `gh` or `codex` was available in this test host. |
| Install / reinstall / update / remove | BLOCKED | No authorized real native installer/runtime and no disposable private collection in this session. Static validation and a fabricated mock are not a substitute. |
| Unauthorized write, concurrency and failure recovery | BLOCKED for agent runtime | Reviewed as conservative specification; permission-denied and write-timeout behavior not live-tested. |
| v0.2.2 vs v0.2.3 tool/question/time benchmark | BLOCKED | No paired equivalent runtimes; words are a static comparison only. |

New manual regression rows test native Codex provenance and pinned-update status. They are **not** counted as passing E2E. All mutations of user collections, production plugins, merges, tags and publication were excluded.

**Release gate:** test a deliberately disposable native Codex directory with a verified persistent installer or an expressly approved isolated USER/PRIVATE collection; capture before/after files, source pin, no-op release behavior, permission failure, read-back and local adaptation handling. Recheck CI at the final HEAD and obtain a separate publication decision.
