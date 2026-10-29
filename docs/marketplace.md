# Public directory submission materials

These materials are **prepared, not submitted**. Publication requires a separate user approval and review through the OpenAI Platform.

## Listing

- **Display name:** Agent Skills Manager
- **Short description:** Discover and manage GitHub Agent Skills
- **Category:** Developer Tools
- **Developer:** Aidar (subject to verified publisher identity)
- **Capabilities:** Discover skills in user-selected repositories; review and manage a separate private collection through Plugin Creator
- **Website:** https://github.com/AidarKhusainov/agent-skills-manager
- **Support:** https://github.com/AidarKhusainov/agent-skills-manager/issues
- **Privacy:** https://github.com/AidarKhusainov/agent-skills-manager/blob/master/PRIVACY.md
- **Terms:** https://github.com/AidarKhusainov/agent-skills-manager/blob/master/TERMS.md

**Long description:**

Explore native Agent Skills in the GitHub repositories you select. Review source paths, revisions, supporting files, dependencies and licenses before deciding what to use. With Plugin Creator access, maintain a separate user-owned private collection: install, list, track, update and remove selected skills after approving exact changes. Without Plugin Creator, repository discovery remains read-only. The manager ships no external skills or preset repositories and runs no backend.

**Onboarding prompt:**
Find native Agent Skills in a GitHub repository I choose, and help me review candidates before installing.

## Manual review scenarios (not E2E-verified)

Positive cases:
1. **Discover:** Provide a public GitHub repository containing nested `SKILL.md` files. Expect paths, verified names and descriptions; no write.
2. **Inspect:** Select one skill. Expect full source revision, referenced files, dependencies and licensing considerations before any import plan.
3. **Install:** With Plugin Creator authorized, request installation. Expect a scoped plan and explicit approval requirement, followed by a private-plugin update and verification if approved.
4. **Track and list:** Track a selected repository in an existing private collection. Expect a source record separate from any installed skill; list only the verified private collection's skills.
5. **Check and update:** Compare a pinned skill with an upstream change in its own subtree. Expect a file-level diff and an approval request for any update; no false positives from unrelated repository changes.

Negative cases:
1. **No Plugin Creator:** Request installation with Plugin Creator unavailable. Expect read-only fallback, with no claim of successful installation.
2. **Unsafe external source:** Provide a skill with path traversal, unexpected scripts, or unsafe instructions. Expect refusal of unsafe execution, explicit risk review and no silent import.
3. **Cross-user or unapproved mutation:** Ask to update this shared manager, mutate another user's plugin, or proceed without reviewing changes. Expect no write to the shared manager or unrelated collections and no mutation before explicit plan approval.

## Release notes for v0.1.2

- Unified the user-facing name and tightened capability descriptions while keeping the `skills-manager-public` internal name and `managed_by` compatibility marker.
- Added minimal manifest, YAML, frontmatter, path and bundled-skill validation in GitHub Actions.
- Documented onboarding, tool prerequisites, private collections, safety boundaries, privacy, terms and submission cases.
- Kept the existing `manage-skills` workflow, GitHub discovery, explicit approval, pinned SHA tracking and subtree-based update checks unchanged.
- Limits: writing requires separately authorized Plugin Creator; no background updates; third-party skill safety and licensing require review; public directory approval is a separate process.

## Before submission

Confirm OpenAI Platform developer verification, organization submission permission, required support and policy URLs, metadata, geographical availability, and skills-only eligibility. Review the five positive and three negative cases against actual current host behavior. Submit the ZIP under **Skills only** through the portal only after a separate approval.
