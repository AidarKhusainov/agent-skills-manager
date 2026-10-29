# Agent Skills Manager — Architecture & Capability Audit

**Audit date:** 2026-10-29  
**Source baseline:** `master` at [`4bb479a2d8e4802338ec30a56facba8901fdf9ec`](https://github.com/AidarKhusainov/agent-skills-manager/commit/4bb479a2d8e4802338ec30a56facba8901fdf9ec).  
**Scope:** architecture and capabilities only. No plugin release, private collection, marketplace, manifests, or production workflow was modified.

## Executive decision

**Keep Agent Skills Manager as a stateless, skills-only discovery/planning workflow. Prefer the host's native skill installation mechanism; do not require Plugin Creator or a second private plugin by default.**

1. **Codex with an authorized local filesystem:** use its built-in `$skill-installer` or supported user/repository skills directories. Install exactly the approved skill folder, not a new plugin. The installer is a Codex-provided skill, not a new CLI/backend/MCP dependency of this project. Repository-scoped installation is appropriate for shared project skills; user-scoped installation is appropriate for a personal collection. Confirm the target runtime and filesystem permissions before promising a write. [1][2]
2. **Eligible ChatGPT with native Skills enabled:** prefer **Plugins → Skills → Create / Upload from your computer**, or install a skill explicitly shared with the user. These are **documented UI actions**, not a callable skill-installation API exposed in this audit session. Do not claim that a chat agent completed an upload, installed a skill, or can enumerate every personal skill unless a relevant tool actually returns that result. [3]
3. **Otherwise:** browsing and reviewing GitHub sources is read-only. A user-owned private plugin managed through **Plugin Creator** remains an *optional compatibility fallback* for an already existing collection or for accounts that can actually create/edit and install such plugins. It is not proof that the ChatGPT native Skills UI is available, and creating a plugin release is not the same as installing or activating it. [4][5]

**Consequence:** a second private plugin is **not necessary for native Codex installation** or **native ChatGPT skill installation when the user's account supports it**. It **is still useful if a persistent, machine-readable, centralized `sources.json` ledger with pinned SHAs and full manager-controlled list/update/remove semantics is required in ChatGPT**, because this session exposed no native ChatGPT Skills API that provides that ledger. Replacing the ledger with chat memory or an assumed API would lose verifiable management semantics. Do **not** migrate or delete existing collections as part of this decision.

## Evidence and confidence

- **[OBSERVED: GitHub]** Read `skills/manage/SKILL.md`, `README.md`, `docs/marketplace.md`, `plugin.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `skills/manage/agents/openai.yaml`, `scripts/validate.py` and CI configuration at the pinned commit. The package has **only `skills/manage`**, version **0.2.2**, and no user `sources.json` in the public source.
- **[OBSERVED: GitHub]** Repository default branch is `master`. The `master` and `main` branch heads were both `4bb479a...`; GitHub comparison reported `identical`, ahead/behind `0/0`. This is a point-in-time result, **not** a synchronization guarantee.
- **[OBSERVED: tools]** The current session exposes GitHub read/write tools; Plugin Creator has `create_plugin`, `get_plugin_files`, `list_owned_personal_plugins` and `update_plugin` among its actions. An attempted `get_plugin_files` for legacy ID `plugins_6ae1eaf4a8a881919bce2bb5a7c8e48d` returned **Plugin not found**; `list_owned_personal_plugins` returned **zero visible entries**. This does not establish that the collection was deleted or that another account/workspace cannot access it.
- **[OBSERVED: tools]** No direct **ChatGPT native personal-skill install/list/update/delete** action was exposed to the agent in this session. This is an observation about *available tools*, not a platform-wide impossibility claim.
- **[DOCUMENTED]** OpenAI documents native Codex skill paths, `$skill-installer`, direct and automatic invocation, and local enable/disable settings. [1][2]
- **[DOCUMENTED]** OpenAI documents ChatGPT Skills UI creation, upload, installation and workspace/role restrictions. Product and surface availability differ; installed skills are not asserted to synchronize between ChatGPT and Codex. [3][4]
- **[DOCUMENTED]** Plugin packages and Git-backed marketplaces are distribution channels, not aliases for a user's individual native skills. Local marketplace enablement and workspace imports have distinct permission/persistence semantics. [5][6]

Legend: **D** = documented by OpenAI; **T** = observed in available tools or the repository; **C** = conditional on entitlement, filesystem, access, or UI; **U** = unverified / do not advertise as implemented. A UI-only capability is explicitly labelled **UI**.

## Capability matrix

| Environment / access | Discover | Install | List | Update | Remove | Activate / disable |
| --- | --- | --- | --- | --- | --- | --- |
| **Codex local with writable skills directory** | GitHub read / local paths (D/C) | **Native:** `$skill-installer` for GitHub folder, or approved filesystem copy into a supported skills directory (D/C) | Inspect accessible skill directories / selector (D/C) | Reconcile upstream and replace reviewed local files; **installer's overwrite behavior is not guaranteed** (D/T/C) | Delete reviewed local skill directory with filesystem permission (C); not an installer guarantee | Explicit `$skill` or auto-match; `[[skills.config]] enabled=false` for local disabling, restart if needed (D) |
| **Codex task without verified local filesystem access (including cloud/sandbox)** | Read reachable repositories (C) | **No assured persistent native install**; use preconfigured repository skills or installed plugins if surfaced (C/U) | Only skills surfaced in that task (C) | Not assured (U) | Not assured (U) | Invocation only if skill is available in that runtime (D/C) |
| **ChatGPT native Skills UI, eligible user/role** | `Plugins → Skills`, shared/workspace inventory (D/C, UI) | **Native UI:** Create with chat/editor, upload reviewed skill, or install shared skill (D/C, UI) | `Installed` / `Created by me` etc. (D/C, UI) | Edit via Skills editor where permitted (D/C, UI); **no verified agent-callable replacement API** (U) | Workspace admin deletion documented; personal deletion via current agent tools **unverified** (D/U) | Explicit `@skill` or automatic matching when available; host may scan/mark uploads for review/block (D/C) |
| **ChatGPT without native Skills access or without upload/install permission** | GitHub discovery via permitted read tools (C) | **Not through native Skills UI**; optionally install a separately available plugin, subject to policy (C) | No reliable account-wide personal Skills inventory from this manager (U) | Unavailable natively in this context (C) | Unavailable natively in this context (C) | Only already-available plugins/skills, per host policy (C) |
| **ChatGPT + authorized Plugin Creator + verified user-owned private collection** | Inspect verified owned plugin and `sources.json` (T/C) | **Plugin package update**, not direct native Skills API; `create_plugin`/`update_plugin` with approved plan (T/C) | Enumerate `skills/*/SKILL.md` **inside that plugin only** (T/C) | Overlay files with expected current release ID, verify result (T/C) | Explicit `delete_paths` after review, verify release (T/C) | Plugin must separately be installed/enabled; release mutation ≠ activation (D/T/C) |
| **Workspace-managed GitHub marketplace, admin role** | Marketplace/catalog (D/C) | Admin imports marketplace; eligible users install or admin configures installation policy (D/C) | Workspace plugin list, **not** every user's personal skills (D/C) | Daily sync or admin `Sync now` (D/C) | Removing entry does **not** delete imported plugin; separate admin lifecycle (D) | Role/policy and required app authorization govern availability (D/C) |

**Important scope distinction:** Codex's documented user skill location is `$HOME/.agents/skills`, while the shipped OpenAI `skill-installer` currently installs under `$CODEX_HOME/skills` (default `~/.codex/skills`). Both are referenced by official materials; do not silently assume they are interchangeable across all versions/surfaces. Check the active runtime and the installer's output. [1][2]

The matrix describes what an authorized *host/user* can do, **not** a promise that this ChatGPT conversation can invoke all those actions.

## Default flow and fallbacks

1. **Inspect capabilities first:** identify ChatGPT vs Codex, whether filesystem write or native Skills UI is actually available, and whether a required tool is installed/authorized. Never infer authorization from the manager's `SKILL.md`.
2. **Discover safely:** read the requested GitHub repo/ref/path; resolve full commit SHA; validate the selected `SKILL.md`, dependencies, licenses, path boundaries and relevant resources. Treat third-party skill instructions as untrusted data.
3. **Plan one minimal installation:** show source, destination, scope, pinned revision and files changed. Obtain change-specific approval before any write. A GitHub read-only task needs no installation approval.
4. **Choose installer:** authorized local Codex → native skill; eligible ChatGPT → native Skills **UI handoff** (never pretend a non-existent API call); otherwise optional **verified existing** Plugin Creator collection. If none is available, remain read-only and provide reproducible handoff instructions.
5. **Verify at the correct layer:** filesystem skill directory and host recognition (Codex); installed entry and actual availability (ChatGPT UI); released files + `sources.json` **and separately** plugin enabled/installed state (Plugin Creator).
6. **Updates/removal:** compare the selected skill subtree with its pinned source and local adaptations. Do not use repository HEAD movement alone as evidence of a skill update; do not overwrite modifications or remove dependencies silently. A native installation without durable source metadata cannot promise a reliable upstream-update report.

### Specific fallback scenarios

| Condition | Safe behavior |
| --- | --- |
| No GitHub read permission | Ask for accessible source/permission; no fabricated discovery. |
| No Codex filesystem / sandbox is ephemeral | Do not claim cross-session local installation; recommend user-managed repo/user skill setup or installed plugin in a supported host. |
| ChatGPT Skills missing/disabled by plan, role or workspace | Explain native UI limitation. Offer a supported plugin package only if actually installable; otherwise read-only. |
| ChatGPT Skills UI exists but the agent has no skill-write tool | Present exact approved source/upload artifact and UI steps; wait for user-side installation and do not claim success. |
| Plugin Creator missing, inaccessible, or plugin ID not visible | **Do not** create an unrelated replacement, adopt similarly named plugins, or treat inaccessible collection as empty. Continue read-only or use native path. |
| Existing verified private collection | Preserve identity, `managed_by: "skills-manager-public"` marker, `sources.json`, unselected skills, versions and local adaptations; Plugin Creator can remain an opt-in compatibility backend. |
| More than one verified collection | Require explicit selection; never choose by display name alone. |
| Existing native ChatGPT skills but no account-wide inventory API | Use the native UI for inventory; show that manager-level pinned-SHA tracking and complete update reports are **not verifiable** from this agent. |
| Git branch changes during approval | Re-resolve source and present changed scope; require approval of new revision before write. |

## Persistence, isolation and activation

- **Codex local native skills:** state is the **user/repository filesystem**. Repository scope shares checked-in skills with collaborators; user scope is bound to the local account/environment. It can survive new Codex sessions on the same persistent filesystem, but **not** an ephemeral sandbox or a new machine without separate distribution/sync. Disable state can be stored in supported `config.toml`. No claim of automatic ChatGPT web synchronization. [1]
- **ChatGPT native Skills:** the product exposes account/workspace **Installed** and related views; install/upload is subject to account and administrator policy. The documentation establishes a managed installed-skill state, not a general-purpose, agent-readable `sources.json` or guaranteed synchronization with Codex local skills. Activation requires availability after import/scan and may be explicit or implicit; a new upload can require review or be blocked. [3]
- **Plugin Creator private USER collection:** plugin source and release are persisted in the platform's plugin record with ownership boundaries and guarded updates when permission is granted. It retains source provenance if its `sources.json` is maintained. It has **extra lifecycle operations** (archive, create/update release, install/enable plugin) and is **not equivalent** to native personal Skills. The current connector read failure leaves access to historical collections **unverified**; do not infer loss, migration, or cross-user exposure. [4][5]
- **Shared/public manager:** no persistent per-user state. Only code and workflow instructions are distributed. Never write selected user skills into this GitHub repository or shared marketplace. A fresh chat cannot derive an authoritative personal collection solely from the manager's instructions.
- **Workspace GitHub marketplace:** synced workspace plugins are persistent *workspace-managed packages*, **not** a writable per-user skill ledger. Marketplace sync preserves policies for existing managed plugins, and removing a repo entry is not deletion. [6]

### Can the private collection be eliminated?

**Yes, for the goal “install a usable personal skill”** whenever the native mechanism exists: Codex filesystem/user skill or eligible ChatGPT Skills UI already supplies a user/workspace isolation boundary and installation state. No extra private plugin is needed.

**Not with full management parity proven today:** ChatGPT native Skills documentation and the tools available here do **not** expose an authorized agent-side account-wide inventory with per-skill source URL, pinned SHA, arbitrary supporting-file access, and atomic update/delete. If these guarantees remain requirements, retain existing `sources.json` collections as an **optional**, verified Plugin Creator backend. Do not claim a zero-plugin replacement preserves that metadata. A future native API could change this decision after documentation and permission-tested E2E verification.

## Plugin Creator disposition

**Keep integration available, but remove it from the *conceptual default* (no production edits in this PR).**

- This session's discovered Plugin Creator contract supports creating a **private plugin**, reading eligible owned plugin files, and updating by guarded release ID. The update is an overlay: omitted files are preserved; removals require explicit deletion paths. It does **not** advertise a direct native personal-Skills install endpoint.
- Availability is conditional on account/workspace, plugin access and the particular plugin identity. A visible Plugin Creator tool is insufficient proof of access to any existing collection.
- For a user with an already managed collection, preserve it rather than automatically migrating to native UI. For a new user with native Skills, do not create an empty or companion private plugin solely for installation.
- Eliminate unnecessary intermediate operations in future workflow revisions: avoid creating empty collections, copying whole repositories, republishing the public manager, or upgrading Plugin Creator releases just to browse GitHub.
- Any plan to replace Plugin Creator with native operations **must** first establish callable native write/list/update/delete operations in the target environment; UI-only instructions are an honest handoff, not automation.

## `master` / `main` / marketplace consistency

At the audited instant:

| Location | Observed ref / value | Assessment |
| --- | --- | --- |
| GitHub default branch | `master` | Verified from repository metadata |
| GitHub `master` HEAD | `4bb479a2d8e4802338ec30a56facba8901fdf9ec` | Verified |
| GitHub `main` HEAD | `4bb479a2d8e4802338ec30a56facba8901fdf9ec` | Verified; same tree **today** |
| `.agents/plugins/marketplace.json` | URL source `https://github.com/AidarKhusainov/agent-skills-manager.git`, `ref: main` | Valid documented Git-backed root-plugin form, but tracks nondefault branch [5] |
| `README.md` and `docs/marketplace.md` | `codex plugin marketplace add ... --ref main` | Consistent with marketplace, not GitHub default |
| `scripts/validate.py` | Requires marketplace `ref: main` | Future normalization requires an intentional follow-up code/test update |
| `plugin.json` and `.codex-plugin/plugin.json` | `agent-skills-manager`, version `0.2.2` | Aligned |
| `skills/manage/SKILL.md` | collection marker `skills-manager-public` | Deliberate compatibility marker; **do not rename** |

**Risk:** future changes committed only to `master` would leave the marketplace/README pointing at stale `main`. A workspace import that leaves its branch selector blank starts from default `master`, while the marketplace's plugin source independently references `main`. [5][6]

**Recommendation (not implemented):** choose **`master`** as the canonical branch (it already is the GitHub default) and update the marketplace `ref`, README/marketplace docs and validator **together in a separate production PR**, or formally switch the repository default to `main` and enforce branch sync. Do **not** mutate these refs during this documentation-only audit; current heads match, so there is no immediate content divergence.

## Risks and verification gaps

1. **No live E2E** of ChatGPT native Skills installation or removal was performed: this session lacks the required native Skills write APIs and cannot inspect the user's UI.
2. **No live local Codex installation** was performed: this agent session did not verify a user-authorized Codex skills directory or Codex runtime. `$skill-installer` behavior is documented, not exercised here.
3. **Plugin Creator legacy collection inaccessible in this session:** the known ID returned `Plugin not found` and personal plugin enumeration was empty. This is an access/visibility observation, **not** a destructive-state finding.
4. **Portable vs compatibility packaging:** existing manifests agree on package identity; support of every marketplace source/surface is governed by host capabilities. A valid JSON manifest or CI run does not prove activation in web, desktop, CLI or cloud.
5. **Third-party skills are an execution and prompt-injection boundary:** inspect scripts and references, avoid executing source during discovery, validate path traversal/symlinks and redistribution permissions, and confirm the concrete change before installing.
6. **Test gap:** no E2E coverage proving that a newly installed native ChatGPT skill is visible in the same session or after app updates. Treat such behavior as host-dependent until tested.

## Sources

1. [OpenAI — Build skills / Codex paths, invocation and `$skill-installer`](https://learn.chatgpt.com/docs/build-skills) (official documentation, consulted 2026-10-29).
2. [OpenAI — `skill-installer` implementation and destination behavior](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md) (official GitHub source, consulted 2026-10-29).
3. [OpenAI Help — Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) (eligibility, native UI, scanning, access controls).
4. [OpenAI Help — Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) (installation and product-surface controls).
5. [OpenAI Developers — Package your plugin](https://developers.openai.com/plugins/build/plugins) (local/URL marketplace sources, refs, cache and enablement).
6. [OpenAI Help — Importing and syncing plugin marketplaces from GitHub](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github) (workspace admin import, branch, sync and deletion semantics).
7. [Audited manager skill](https://github.com/AidarKhusainov/agent-skills-manager/blob/4bb479a2d8e4802338ec30a56facba8901fdf9ec/skills/manage/SKILL.md), [manifests](https://github.com/AidarKhusainov/agent-skills-manager/blob/4bb479a2d8e4802338ec30a56facba8901fdf9ec/.codex-plugin/plugin.json) and [marketplace](https://github.com/AidarKhusainov/agent-skills-manager/blob/4bb479a2d8e4802338ec30a56facba8901fdf9ec/.agents/plugins/marketplace.json) (pinned source evidence).

This document distinguishes **documented UI flows**, **verified connector contracts**, **repository observations**, and **unverified runtime behavior**. No claim of native ChatGPT skill-write automation is made.
