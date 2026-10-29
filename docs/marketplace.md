# Marketplace listing and review notes

**Status:** Git-backed local marketplace source; public Plugin Directory submission is **not** implied. Review and publication require a separate process.

## Metadata

- **Display name:** Agent Skills Manager
- **Short description:** Discover and manage GitHub Agent Skills
- **Category:** Developer Tools
- **Developer:** Aidar (publisher identity subject to platform verification)
- **Website:** https://github.com/AidarKhusainov/agent-skills-manager
- **Support:** https://github.com/AidarKhusainov/agent-skills-manager/issues
- **Privacy:** https://github.com/AidarKhusainov/agent-skills-manager/blob/master/PRIVACY.md
- **Terms:** https://github.com/AidarKhusainov/agent-skills-manager/blob/master/TERMS.md

**Description:** Discover Agent Skills from repositories the user selects. Show read-only inventory/status when actually accessible. With verified native filesystem permissions, prepare and apply approved native changes; when ChatGPT Skills is UI-only, provide manual installation guidance. An authorized existing USER/PRIVATE Plugin Creator collection may be used for persistent source-ledger management as a fallback. No shared user state, background process, backend or bundled third-party skills.

## Onboarding examples

1. Discover skills from a GitHub repository URL without installing anything.
2. Show the accessible installed skills and identify inventories that cannot be verified.
3. Check updates without applying them, and prepare an approval-gated plan only if requested.

The portable and compatibility manifests share one set of prompts, capabilities, names and icons. These are example interactions, not an auto-executing workflow.

## Distribution and compatibility

The local marketplace catalog `.agents/plugins/marketplace.json` uses the canonical **`master`** branch:

```bash
codex plugin marketplace add AidarKhusainov/agent-skills-manager --ref master
```

`main` existed with identical contents at the initial 2026-10-29 branch check, but GitHub does not keep the two refs synchronized automatically. See [ADR](adr-release-source.md). The source release candidate is **0.2.3** in both manifests and `VERSION`; a GitHub PR or merge alone does not publish, install or activate a plugin release. The Git-backed package identity is `agent-skills-manager:manage`; the private-collection legacy marker `managed_by: "skills-manager-public"` and `sources.json` v1 compatibility are retained. Upgrading the manager must not replace a user's private collection.

## Validation boundaries

`python scripts/validate.py` and `python -m unittest discover -s tests -v` check static source/package invariants, not agent behavior. Manual installation, permissions, invalid sources, idempotency, concurrency, partial failures, upgrading and actual activation need verified external execution. See [E2E regression matrix](regression-test-plan.md). None of those E2E cases is claimed to have passed as part of this source-only change.

Before submitting to any public directory, verify current developer/publisher requirements, skills-only eligibility, permission model, metadata and privacy/terms links, and run the E2E matrix in the actual target environments. Never portray an unverified Plugin Creator release as an installed/activated skill.
