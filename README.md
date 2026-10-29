# Agent Skills Manager

A native, skills-only ChatGPT plugin for discovering Agent Skills in GitHub repositories you choose and managing a **separate user-owned private collection**.

The manager itself contains only the `manage-skills` skill. It has no preset repositories, imported third-party skills, shared user database, MCP server, CLI, or executable backend.

## What it does

- Find and inspect `SKILL.md` files in public repositories, including nested directories.
- Review names, paths, source revisions, dependencies, licenses, and file scope.
- Track selected repositories separately from installed skills, in your private collection.
- Install, list, update, or remove selected skills through Plugin Creator, after reviewing and approving the exact changes.
- Pin imports to full Git commit SHAs and compare updates within the selected skill's file subtree rather than repository HEAD alone.
- Preserve unrelated skills and user adaptations unless you approve their modification.

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
| `skills/manage-skills/SKILL.md` | Native workflow instructions |
| `skills/manage-skills/agents/openai.yaml` | Skill presentation |
| `assets/icon.svg` | Plugin icon |
| `scripts/validate.py` | Source validation used by CI |

The stable internal package name remains `skills-manager-public`. The user-facing name is **Agent Skills Manager**. Source and releases should match after each update.

## Project and publication

Source: [GitHub](https://github.com/AidarKhusainov/agent-skills-manager). Bug reports and support: [GitHub Issues](https://github.com/AidarKhusainov/agent-skills-manager/issues).

See [privacy](PRIVACY.md), [terms](TERMS.md), and [marketplace review materials](docs/marketplace.md). The current release is not an assertion that this plugin has been approved for public listing.

## License

MIT, see [LICENSE](LICENSE).
