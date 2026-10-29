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

Read repository metadata, resolve the commit, obtain the recursive tree and read the leading `SKILL.md` metadata for each of the four candidates. This was a read-only repository inspection without a full-repository download, Plugin Creator use, or any collection mutation. Each candidate has valid nonempty `name` and `description`; no name collision was seen.

| Candidate | Skill directory | Metadata |
| --- | --- | --- |
| `clear-explanations` | `clear-explanations/` | Verified |
| `production-java-backend-development` | `production-java-backend-development/` | Verified |
| `strict-backend-code-review` | `strict-backend-code-review/` | Verified |
| `use-case-spec` | `use-case-spec/` | Verified |

A missing-directory path can be distinguished from an empty valid subtree using the complete tree listing. This probe is **read-only discovery E2E at the tool/data boundary**, not a tested installation or proof of how a future model will route every user utterance.

## Automated validation

PR #6 passed [Validate plugin source](https://github.com/AidarKhusainov/agent-skills-manager/actions/runs/40870894351) at `ae8b3ef0b1d7f81d1db7d0ef4caee3fe4271ab57` on 2026-10-29: Python syntax check, regression tests and actual-package validation. Recheck CI against the final commit after release-documentation edits.

Run locally or in CI:

```bash
python -m pip install -r requirements-validation.txt
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python scripts/validate.py
```

The release candidate adds tests for `VERSION` mismatch, omission and malformed content, extending the fixture suite from 23 to **26 test definitions**. The recorded PR #6 CI run passed them; the final branch head must also pass.

## Behavioral changes since v0.2.2

The manager now explicitly routes discovery, status and mutation, without requiring Plugin Creator for discovery or verified native operations.

| Dimension | v0.2.2 instructions | v0.2.3 candidate instructions |
| --- | --- | --- |
| Routine discovery | Repository browsing available, but first-use explanation steers toward Plugin Creator | Explicit minimal pinned tree/frontmatter path, no Creator or companion audit |
| Persistent installation | Plugin Creator private collection only | Verified native path first, UI handoff or optional verified private collection |
| Batch approval | Approval per concrete write; no explicit unified batch pipeline | One combined preflight, one approval per stable batch |
| Unchanged repeated operation | Described generally, no unified no-op gate | Explicit no-op and no unnecessary release |
| Status dimensions | Upstream/local status already distinguished | Distinction preserved and made explicit |

## E2E execution and blockers

- **Read-only GitHub discovery:** PASS for the four real candidates above.
- **Plugin Creator missing / private storage unavailable:** instruction/fallback review PASS; actual agent/runtime behavior **NOT RUN**. Expected outcome is `Unavailable`, no fabricated empty collection and no replacement creation.
- **Install one/all, repeat, update, remove, concurrent change, partial failure and rejected plan:** **NOT RUN**. No verified disposable collection or persistent native installer was available. No auxiliary test plugin was created and no user collection was modified.
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
- [ ] Final HEAD of **this PR** passes CI (previous HEAD `ae8b3ef` passed); inspect checks again after edits.
- [x] Review the combined PR against `master` for changed paths, stacked integration and ownership boundaries; PR #1–#5 overlap by design.
- [ ] Execute separately approved isolated write-E2E (or formally accept/document the untested risk).
- [ ] Verify the target host's packaging, installation/enabling and activation independently.
- [ ] Obtain release approval; **only then** merge, tag/publish or update Plugin Creator if explicitly authorized.

**Release decision:** hold publication until review and applicable verification gates are satisfied. This PR deliberately neither publishes nor updates private user plugins.

## Final independent readiness audit (2026-10-29)

**Decision: source changes can be reviewed for merge, but publication remains on hold pending an explicit release decision and evaluation of unexecuted isolated mutation E2E.** The missing E2E is a known verification limitation, not evidence of an observed destructive failure.

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

New manual regression rows test native Codex provenance and pinned-update status. They are **not** counted as passing E2E. All mutations of user collections, production plugins, merges, tags and publication were excluded.

**Remaining release gate:** when an isolated persistent native Codex directory or expressly authorized disposable USER/PRIVATE collection becomes available, verify install, repeat/no-op, update, removal, provenance, file preservation and error recovery against real state. Record any unavailable scenarios as `NOT RUN`; do not block source review on invented E2E success. Recheck CI at the final HEAD and obtain a separate publication decision.
