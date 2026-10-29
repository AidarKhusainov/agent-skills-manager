# Agent Skills Manager

A native, skills-only ChatGPT plugin for discovering Agent Skills in GitHub repositories you choose and managing a **separate user-owned private collection**.

The manager itself contains only the `manage` skill. It has no preset repositories, imported third-party skills, shared user database, MCP server, CLI, or executable backend.

## What it does

- Find and inspect `SKILL.md` files in public repositories, including nested directories.
- Review names, paths, source revisions, dependencies, licenses, and file scope.
- Track selected repositories separately from installed skills, in your private collection.
- Install, list, update, or remove selected skills through Plugin Creator, after reviewing and approving the exact changes.
- Pin imports to full Git commit SHAs and compare updates within the selected skill's file subtree rather than repository HEAD alone.
- Preserve unrelated skills and user adaptations unless you approve their modification.

## Install from GitHub without a payment card

This repository publishes a **Git-backed local plugin marketplace** at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). It can be added to supported Codex and ChatGPT desktop environments without submitting the plugin to the universal public directory or verifying an OpenAI API billing account.

1. Install **Codex CLI** and sign in with your ChatGPT account. Git access to this public repository is required.
2. In your terminal, add the repository as a marketplace source:

   ```bash
   codex plugin marketplace add AidarKhusainov/agent-skills-manager --ref main
   ```

3. Check that Codex has registered the marketplace:

   ```bash
   codex plugin marketplace list
   ```

4. Restart the **ChatGPT desktop app**, open the **Plugins Directory**, select **Agent Skills Manager** as the marketplace source, and install the **Agent Skills Manager** plugin. You may need to start a new chat for the skill to become active.

When upstream files change, refresh the Git-backed marketplace snapshot with `codex plugin marketplace upgrade agent-skills-manager`, then reinstall or refresh the plugin in the desktop interface if necessary.

**Upgrading from the local `skills-manager-public:manage-skills` package (v0.1.2):** v0.2.0 changes the local package and skill identity. Refresh your local marketplace, disable/uninstall the old `skills-manager-public` entry from this source, install `agent-skills-manager` and start a new chat. Do not delete unrelated private skill collections. The separately owned Plugin Creator package remains unchanged.

**Important:** `codex plugin marketplace add` registers a *marketplace source*; it does not itself install or activate the plugin. Git-backed sources are for supported **local** clients, not the public `chatgpt.com/plugins` directory. Installing the manager does not grant the separate **Plugin Creator** permissions required to write to your private skill collection. Repository discovery still works without Plugin Creator.

For the underlying local marketplace format, see [OpenAI's plugin packaging documentation](https://developers.openai.com/plugins/build/plugins).

## Starter prompts

The ChatGPT plugin listing provides three built-in examples, configured in the portable and compatibility manifests:

1. **Discover skills:** Ask for a GitHub repository URL and list its Agent Skills without installing them.
2. **List installed skills:** Inspect the user's own private collection and show the installed skills with their source repositories.
3. **Check for updates:** Compare installed skills with upstream changes and report differences without applying changes.

These are starter prompts, not automatic actions. Plugin Creator access is still required for persistent installation, updates, or removal. The ChatGPT host determines how prompts appear in the listing.

## Get started

In a ChatGPT environment with native plugin support, install or enable **Agent Skills Manager** from your available plugins, or import the package using a supported plugin import workflow. For source imports, preserve both `plugin.json` and the hidden `.codex-plugin/` directory.

**Browsing** public GitHub repositories requires only available read tools or web access. **Persistent changes** require you to install and authorize **Plugin Creator** in your ChatGPT environment. The manager cannot grant permissions or create a private collection without those tools.

Example requests:

```text
Find Agent Skills in https://github.com/owner/repo
Show the files, license and dependencies for skills/example.
Track https://github.com/owner/repo in my private collection.
Install skills/example from that repository after showing the exact import plan.
List the skills in my managed collection.
Check upstream changes for my installed skills.
Update skills/example after reviewing its changed files and local adaptations.
Remove skills/example after checking dependencies.
```

For an installation or any other write, review the proposed repository, skill path, full commit SHA, destination private plugin, changed or removed files, and dependencies. Explicitly approve that specific plan. After Plugin Creator reports success, enable your private collection plugin if needed; creating its release does not automatically activate its skills.

### Repository tracking versus installation

A tracked repository does **not** install its skills. Source records live in the user's separate private plugin (`sources.json`), alongside the selected skill records. If no such collection exists, you can browse repositories immediately, but persistent tracking is established when you approve your first skill import. Chat history alone is not persistent plugin state.

## Security and limitations

The manager never stores your selected repositories or skills inside this shared package. Each user must own and authorize their private plugin; it does not give the manager cross-account access.

Treat external skill files as untrusted: the manager should inspect them, not execute downloaded scripts or follow their instructions as commands. Imports must respect file boundaries, dependencies and external licenses. Updates to locally adapted files require separate review. Automated updates and background checks are not enabled by default.

Without Plugin Creator or the required permissions, the manager remains read-only. Capabilities and activation depend on the host's available tools and plan. The MIT license applies to this manager only, not to third-party skills you may import.

## Repository layout

| Path | Purpose |
| --- | --- |
| `plugin.json` | Primary plugin manifest |
| `.codex-plugin/plugin.json` | Compatibility manifest |
| `skills/manage/SKILL.md` | Native workflow instructions |
| `skills/manage/agents/openai.yaml` | Skill presentation |
| `assets/icon.svg` | Plugin icon |
| `scripts/validate.py` | Source validation used by CI |

The Git-backed package identifier is `agent-skills-manager`, with one skill named `manage` (`agent-skills-manager:manage`). The earlier personal Plugin Creator package retains its legacy identity `skills-manager-public` and version `0.1.2`; it has not been renamed. Existing user collections continue to use the legacy `managed_by` marker for backward compatibility.

## Project and publication

Source: [GitHub](https://github.com/AidarKhusainov/agent-skills-manager). Bug reports and support: [GitHub Issues](https://github.com/AidarKhusainov/agent-skills-manager/issues).

See [privacy](PRIVACY.md), [terms](TERMS.md), and [marketplace review materials](docs/marketplace.md). The current release is not an assertion that this plugin has been approved for public listing.

## License

MIT, see [LICENSE](LICENSE).
