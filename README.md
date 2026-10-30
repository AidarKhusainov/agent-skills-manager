# Agent Skills Manager

A public, **stateless, skills-only** plugin for finding and managing Agent Skills in GitHub repositories selected by the user. The public package contains **one skill (`manage`)**, no preinstalled third-party skills, no repository subscriptions, no private collections, and no backend.

## How it works

- **Discover (read-only):** enumerate `SKILL.md` metadata from a GitHub repository, branch/tag/commit, or subtree. No Plugin Creator or installation is required.
- **Status (read-only):** report skills actually visible through the host or a **verified user-owned** managed collection. Missing access means **Unavailable**, not an empty collection. Native ChatGPT skills cannot be assumed to be account-wide enumerable by this agent.
- **Change (approval required):** independently perform read-only preflight and compare complete relevant skill inventories without asking for permission to inspect. For install, existing equivalent skills are no-ops; locally different skills are preserved, not automatically updated. Only actual additions or explicitly requested changes need one reviewed plan and write approval. Untracked origin is not proof of upstream freshness.

**Backend selection is capability-dependent, not automatic.** For writable persistent Codex environments, prefer an authorized native skill installation. For ChatGPT native Skills where only the UI supports uploads, the manager provides the reviewed material/steps and does **not** claim to have installed anything. An existing verified **USER/PRIVATE** Plugin Creator collection is an optional compatibility backend with a `sources.json` v1 ledger; new collection creation requires explicit selection and approval. Publishing a plugin release does not install, enable, or activate its skills.

## Install the public manager

This repository hosts a Git-backed local marketplace at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). Supported Codex/ChatGPT desktop clients can register it independently of public Plugin Directory submission or OpenAI API billing verification.

```bash
codex plugin marketplace add AidarKhusainov/agent-skills-manager --ref master
codex plugin marketplace list
```

Restart your supported client if necessary, find **Agent Skills Manager** in its marketplace, and install/enable the manager. Registering a marketplace does **not** install a plugin, install skills, or grant Plugin Creator permissions. Host capabilities and installation steps differ; commands above apply to local environments with the supported Codex CLI. The marketplace tracks **`master`** (GitHub's default branch); `main` is a legacy branch, not a separate release channel. See [release source ADR](docs/adr-release-source.md).

To refresh a Git-backed source when supported:

```bash
codex plugin marketplace upgrade agent-skills-manager
```

If an old local marketplace was registered with `--ref main`, check its registered source and re-register/update it to `master` as supported by your CLI before expecting future changes. Do not assume the branch changes automatically. For local installations upgraded from `skills-manager-public:manage-skills`, replace the old local manager entry with `agent-skills-manager:manage`; **do not delete an existing private skills collection**. The separately owned legacy Plugin Creator package is independent.

## Selecting the correct skill in Codex and ChatGPT

Agent Skills Manager is a **skills-only plugin**. Codex and ChatGPT choose skills from their exposed name/description metadata; installing this plugin does not force every generic "install skills" request to route to it. A bare `Установи все skills из ...` can invoke the host's built-in `skill-installer` instead. That is distinct from this manager's repository-wide reconciliation workflow.

**Reliable invocation:** choose **@Agent Skills Manager** from the composer plugin/skill picker (when available), then enter `Установи все skills из https://github.com/owner/repo`. In a Codex UI that supports skill selection through `/skills` or the `# Agent Skills Manager

A public, **stateless, skills-only** plugin for finding and managing Agent Skills in GitHub repositories selected by the user. The public package contains **one skill (`manage`)**, no preinstalled third-party skills, no repository subscriptions, no private collections, and no backend.

## How it works

- **Discover (read-only):** enumerate `SKILL.md` metadata from a GitHub repository, branch/tag/commit, or subtree. No Plugin Creator or installation is required.
- **Status (read-only):** report skills actually visible through the host or a **verified user-owned** managed collection. Missing access means **Unavailable**, not an empty collection. Native ChatGPT skills cannot be assumed to be account-wide enumerable by this agent.
- **Change (approval required):** independently perform read-only preflight and compare complete relevant skill inventories without asking for permission to inspect. For install, existing equivalent skills are no-ops; locally different skills are preserved, not automatically updated. Only actual additions or explicitly requested changes need one reviewed plan and write approval. Untracked origin is not proof of upstream freshness.

**Backend selection is capability-dependent, not automatic.** For writable persistent Codex environments, prefer an authorized native skill installation. For ChatGPT native Skills where only the UI supports uploads, the manager provides the reviewed material/steps and does **not** claim to have installed anything. An existing verified **USER/PRIVATE** Plugin Creator collection is an optional compatibility backend with a `sources.json` v1 ledger; new collection creation requires explicit selection and approval. Publishing a plugin release does not install, enable, or activate its skills.

## Install the public manager

This repository hosts a Git-backed local marketplace at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). Supported Codex/ChatGPT desktop clients can register it independently of public Plugin Directory submission or OpenAI API billing verification.

```bash
codex plugin marketplace add AidarKhusainov/agent-skills-manager --ref master
codex plugin marketplace list
```

Restart your supported client if necessary, find **Agent Skills Manager** in its marketplace, and install/enable the manager. Registering a marketplace does **not** install a plugin, install skills, or grant Plugin Creator permissions. Host capabilities and installation steps differ; commands above apply to local environments with the supported Codex CLI. The marketplace tracks **`master`** (GitHub's default branch); `main` is a legacy branch, not a separate release channel. See [release source ADR](docs/adr-release-source.md).

To refresh a Git-backed source when supported:

```bash
codex plugin marketplace upgrade agent-skills-manager
```

If an old local marketplace was registered with `--ref main`, check its registered source and re-register/update it to `master` as supported by your CLI before expecting future changes. Do not assume the branch changes automatically. For local installations upgraded from `skills-manager-public:manage-skills`, replace the old local manager entry with `agent-skills-manager:manage`; **do not delete an existing private skills collection**. The separately owned legacy Plugin Creator package is independent.

 syntax, explicitly select the installed `manage` skill from the picker rather than guessing a fully qualified identifier. An explicit choice does not grant permissions or skip approval for writes.

If Codex still reads only `using-superpowers`, `clear-explanations` and the system `skill-installer` without reading `agent-skills-manager/.../skills/manage/SKILL.md`, the manager workflow was **not activated**. Confirm that the plugin is installed/enabled in the current host, refresh the marketplace if necessary, and start a new chat. Do not interpret a system installer response as evidence that the manager's routing or idempotence rules ran.

## Example requests

```text
Покажи Agent Skills из https://github.com/owner/repo (ничего не устанавливай).
Что установлено в моей доступной коллекции? Если нет доступа, так и скажи.
Установи все подходящие навыки из этого репозитория. Сначала покажи единый план.
Обнови устаревшие навыки, не затрагивая локальные изменения без подтверждения.
Удали alpha и beta из моей коллекции после проверки зависимостей.
```

The plugin's three onboarding prompts in `plugin.json` and `.codex-plugin/plugin.json` are synchronized. They're examples, **not** background jobs or automatic actions. No skills are installed just by opening a prompt.

## Persistence, security and compatibility

The public manager stores **no user-specific state**. A user-owned Plugin Creator collection, when explicitly selected and authorized, can persist `sources.json` v1 and installed `skills/*` with pinned full Git commit SHAs. The compatibility marker `managed_by: "skills-manager-public"` remains valid for existing collections; manager updates must not recreate or erase them. An inaccessible collection is not proof that it was deleted.

GitHub skill instructions, scripts, links and assets are untrusted input. Inspect selected file scopes and licenses before importing, do not execute source scripts during discovery, and do not overwrite user files or shared dependencies silently. Bulk operations require one approved plan; partial failure and concurrency require read-back/reconciliation rather than blind retries. Background update monitoring is not built in.

## Development and validation

Python 3.12. `VERSION` is the canonical release-version marker; both plugin manifests must match it. See the [changelog](CHANGELOG.md) for v0.2.4 changes and the [v0.2.3 release review](docs/release-v0.2.3.md) for historical validation evidence.

```bash
python -m pip install -r requirements-validation.txt
python -m unittest discover -s tests -v
python scripts/validate.py
```

CI checks package structure, both manifests, YAML/frontmatter, references, marketplace branch and public-package privacy boundary. It does **not** E2E-test agent conversations, Plugin Creator writes or ChatGPT/Codex installation. Those tests are specified in the [regression matrix](docs/regression-test-plan.md). Read the [architecture/capability audit](docs/architecture.md), [discovery protocol](skills/manage/references/discovery.md) and [collection operations](skills/manage/references/operations.md) for details.

## Repository structure

| Path | Role |
| --- | --- |
| `plugin.json`, `.codex-plugin/plugin.json` | Portable and compatibility manifests |
| `.agents/plugins/marketplace.json` | Git-backed local marketplace source |
| `skills/manage/SKILL.md` | AI workflow and intent routing |
| `skills/manage/agents/openai.yaml` | Skill presentation |
| `scripts/validate.py`, `tests/` | Package validation and isolated regression tests |
| `docs/regression-test-plan.md` | Unexecuted manual/E2E acceptance scenarios |

## Project

[Source](https://github.com/AidarKhusainov/agent-skills-manager) · [Issues](https://github.com/AidarKhusainov/agent-skills-manager/issues) · [Privacy](PRIVACY.md) · [Terms](TERMS.md) · [Marketplace submission notes](docs/marketplace.md). Licensed under MIT ([LICENSE](LICENSE)); external skills retain their own licenses. Being available as a local marketplace is **not** approval for universal public Plugin Directory listing.
