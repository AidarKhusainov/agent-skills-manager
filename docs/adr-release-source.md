# ADR: canonical marketplace release branch

**Status:** Accepted for this validation change (2026-10-29).

## Context

GitHub's default branch is `master`; at the start of this work `master` and `main` pointed to the same commit (`4bb479a2d8e4802338ec30a56facba8901fdf9ec`). The marketplace source and CLI examples referenced `main`, so a merged change to `master` could leave marketplace consumers on old instructions without an obvious error.

## Decision

Use `master` as the sole canonical Git-backed marketplace source; change `.agents/plugins/marketplace.json` to `ref: master` and align installation documentation and validation. Keep `main` as an optional legacy branch, not as a second release channel. Do not force push, delete, or silently synchronize either branch from CI.

## Consequences

- The marketplace tracks the same branch into which the primary PRs merge.
- A user who originally registered the marketplace with `--ref main` may need to re-add/update the source with `--ref master` using supported CLI UI controls; merely editing the catalog does not mutate a user's local registration.
- Before release, verify branch pointers and communicate any intentional divergence. If the project later adopts `main`, change source, documentation, validator and release workflow together.
- This ADR does not change `plugin.json` version, `sources.json` v1, private collection identity, or the workflow defined in PR #4.
