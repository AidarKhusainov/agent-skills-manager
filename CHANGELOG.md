# Changelog

## [0.2.4] - 2026-10-30 (proposed)

### Fixed
- Complete read-only installation preflight without additional confirmation to inspect files or prepare a plan; host permission prompts still apply.
- Treat install and update as distinct requests: no automatic update of existing local skills, metadata adoption or forced overwrites.
- Report equivalent existing skills as no-change and local adaptations as `Locally modified — preserved`, reserving `Conflict` for actual proposed colliding writes.
- Distinguish line-ending-only differences from substantive changes, and avoid claiming complete equality or source provenance from partial comparisons.

### Validation
- Expand the manual agent E2E matrix for preflight, repeat installs, untracked/equivalent content, local edits and incomplete comparisons.
- Source and package validation run in CI; these additions are behavioral instructions, not automatically verified agent E2E.


## [0.2.3] - 2026-10-29 (release candidate)

### Changed
- Integrate the architecture and capability audit (#1), pinned read-only GitHub discovery (#2), safe collection operations (#3), and simplified DISCOVER/STATUS/MUTATE UX (#4).
- Preserve the validation and regression work from #5, including native-first capability routing, stateless distribution and no-op behavior.
- Use `master` as the canonical marketplace source while retaining `main` only for legacy compatibility.
- Clarify that upstream freshness and `Locally modified` are independent status dimensions.

### Validation
- Introduce `VERSION` as the authoritative source-release marker and validate both manifests against it; extend regression fixtures for drift and malformed/missing release markers.
- Record read-only GitHub discovery evidence on `AidarKhusainov/skills`; document unexecuted, permission-gated mutation tests separately.
- Document release checklist, migration guidance, the comparison with v0.2.2, and verification boundaries in [release notes](docs/release-v0.2.3.md).

### Compatibility and security
- Preserve `sources.json` schema v1 and `managed_by: "skills-manager-public"`; do not migrate or touch any existing user collection.
- The public manager still ships only `skills/manage`, without bundled third-party skills or user data.
- No plugin publication, private-collection mutation or automatic activation is part of this source release.
