# Agent Skills Manager

Manage, install, update, and remove Agent Skills from GitHub repositories.

Agent Skills Manager is an instruction-based ChatGPT plugin. It discovers native Agent Skills in repositories you choose and helps maintain a separate private collection through Plugin Creator. This repository contains the manager itself, with no bundled third-party skills or preset repositories.

## Features

- Discover nested `SKILL.md` files in a selected repository, branch, or directory.
- Review skill names, descriptions, supporting files, dependencies, and redistribution constraints before importing.
- Install selected skills into a separate user-owned private plugin after reviewing and approving the concrete changes.
- List installed skills and track selected sources independently of installed skills.
- Check updates within each selected skill directory and its declared dependencies, using pinned commit revisions.
- Review local adaptations before updating and check dependencies before removal.

## Requirements and usage

Use this package in a ChatGPT environment that supports native plugins and skills. Repository browsing requires available GitHub read tools or web browsing. Persistent installation, updates, and removal require Plugin Creator to be installed, accessible, and authorized for your private collection.

Enable the manager in ChatGPT, then provide a GitHub repository URL and ask, for example:

```text
Find Agent Skills in this GitHub repository: <repository URL>
Show the supporting files and dependencies for <skill path>.
Install the selected skill into my private collection.
List my installed skills.
Check whether my selected skills have upstream updates.
Update <skill name> after showing the proposed changes.
Remove <skill name> after checking its dependencies.
```

For an installation, the manager resolves the source and revision, presents the exact import scope, and requests approval before writing through Plugin Creator. A new private collection must also be installed and enabled by its owner for its skills to become active.

For source-based import, preserve the repository root layout, including the hidden `.codex-plugin` directory, and use the plugin import workflow supported by your host. This repository does not provide a CLI installer.

## Limitations and boundaries

- Installing this manager does not install any other skills or grant Plugin Creator permissions.
- Without Plugin Creator, the workflow is limited to browsing and reviewing candidates.
- User selections belong in the user's separate private collection, never in this shared manager.
- Source tracking is persisted only through approved private-collection changes; chat history alone is not persistent state.
- Imports, updates, and removals require approval of their concrete scope. There are no automatic updates or background jobs in this package.
- Tool availability, account permissions, plugin activation, and supported import flows depend on the host environment.
- External skills retain their own licenses. This repository's MIT license does not license any skills you later import.
- There is no bundled backend, MCP server, executable application, or dependency installation step.

## Source layout

| Path | Purpose |
| --- | --- |
| `plugin.json` | Root plugin manifest |
| `.codex-plugin/plugin.json` | Compatibility manifest |
| `assets/icon.svg` | Plugin icon |
| `skills/manage-skills/SKILL.md` | Native skill instructions |
| `skills/manage-skills/agents/openai.yaml` | Skill presentation metadata |

The source was exported from the current Plugin Creator release `0.1.1` (`pluginrel_6ae1ee72cd3881918f2cf3ff0e93da83`). The internal package name remains `skills-manager-public`; existing interface labels remain unchanged. The author's personal email was removed from both manifests for public distribution. Skill instructions, configuration behavior, and the icon are unchanged.

## License

MIT. See [LICENSE](LICENSE).
