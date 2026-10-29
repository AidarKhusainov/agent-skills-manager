"""Executable validator regression tests; agent workflows have a separate manual plan."""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import validate  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.write("README.md", "# Manager\n")
        self.write("LICENSE", "MIT\n")
        self.write(".gitignore", ".env\n")
        self.write("VERSION", "0.2.3\n")
        self.write("assets/icon.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.write("skills/manage/SKILL.md", "---\nname: manage\ndescription: Safe skill discovery.\n---\n\n# New heading\nSee [operations](references/operations.md).\n")
        self.write("skills/manage/references/operations.md", "# Workflow details\n")
        self.write("skills/manage/agents/openai.yaml", 'interface:\n  display_name: Agent Skills Manager\n  short_description: Browse skills\n  default_prompt: Find skills\n')
        ui = {
            "displayName": "Agent Skills Manager", "shortDescription": "Browse skills",
            "longDescription": "Discover skills in selected GitHub repositories.",
            "developerName": "Aidar", "category": "Developer Tools",
            "capabilities": ["Discover skills"], "defaultPrompt": ["Discover skills in a repository"],
            "logo": "./assets/icon.svg", "composerIcon": "./assets/icon.svg",
        }
        core = {
            "name": "agent-skills-manager", "version": "0.2.3", "description": "Public manager",
            "author": {"name": "Aidar"}, "keywords": ["github"],
        }
        self.primary = dict(core, extensions={"com.openai": {"interface": ui, "onboardingSkill": "./skills/manage/SKILL.md"}})
        self.compat = dict(core, interface=copy.deepcopy(ui), skills="./skills",
                           extensions={"com.openai": {"onboardingSkill": "./skills/manage/SKILL.md"}})
        self.market = {
            "name": "agent-skills-manager", "interface": {"displayName": "Agent Skills Manager"},
            "plugins": [{"name": "agent-skills-manager", "category": "Developer Tools",
                         "source": {"source": "url", "url": "https://github.com/AidarKhusainov/agent-skills-manager.git", "ref": "master"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}}],
        }
        self.save_manifests()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def save_manifests(self):
        for name, value in (("plugin.json", self.primary), (".codex-plugin/plugin.json", self.compat),
                            (".agents/plugins/marketplace.json", self.market)):
            self.write(name, json.dumps(value, ensure_ascii=False, indent=2))

    def assert_rejected(self, message):
        with self.assertRaisesRegex(ValueError, message):
            validate(self.root)

    def test_valid_package_without_legacy_headings(self):
        validate(self.root)

    def test_version_change_is_allowed_when_manifests_match(self):
        self.primary["version"] = self.compat["version"] = "1.2.3"
        self.write("VERSION", "1.2.3\n")
        self.save_manifests()
        validate(self.root)

    def test_release_version_drift_rejected(self):
        self.primary["version"] = self.compat["version"] = "0.2.4"
        self.save_manifests()
        self.assert_rejected("does not match VERSION")

    def test_missing_release_version_file_rejected(self):
        (self.root / "VERSION").unlink()
        self.assert_rejected("Missing required file")

    def test_invalid_release_version_file_rejected(self):
        self.write("VERSION", "not-semver\n")
        self.assert_rejected("VERSION: invalid semantic version")

    def test_mismatched_versions_rejected(self):
        self.primary["version"] = "2.0.0"
        self.save_manifests()
        self.assert_rejected("Manifest mismatch: version")

    def test_bad_semver_rejected(self):
        self.primary["version"] = self.compat["version"] = "release-next"
        self.save_manifests()
        self.assert_rejected("semantic version")

    def test_ui_metadata_drift_rejected(self):
        self.compat["interface"]["shortDescription"] = "Other title"
        self.save_manifests()
        self.assert_rejected("UI metadata mismatch")

    def test_wrong_onboarding_path_rejected(self):
        self.primary["extensions"]["com.openai"]["onboardingSkill"] = "./skills/../private/SKILL.md"
        self.save_manifests()
        self.assert_rejected("Invalid package path")

    def test_marketplace_wrong_branch_rejected(self):
        self.market["plugins"][0]["source"]["ref"] = "main"
        self.save_manifests()
        self.assert_rejected("canonical release branch")

    def test_multiple_marketplace_entries_rejected(self):
        self.market["plugins"].append(copy.deepcopy(self.market["plugins"][0]))
        self.save_manifests()
        self.assert_rejected("exactly one")

    def test_unexpected_installed_skill_rejected(self):
        self.write("skills/private/SKILL.md", "---\nname: private\n---\n")
        self.assert_rejected("only the manager")

    def test_user_source_ledger_rejected_at_any_depth(self):
        self.write("skills/manage/references/sources.json", '{"repositories": []}')
        self.assert_rejected("User source ledger")

    def test_credential_artifact_rejected(self):
        self.write("data/.env", "API_TOKEN=dummy")
        self.assert_rejected("Credential-like file")

    def test_secret_pattern_rejected(self):
        self.write("docs/config.md", "example " + "gh" + "p_" + "A" * 30)
        self.assert_rejected("Possible credential")

    def test_symlink_rejected(self):
        (self.root / "docs").mkdir()
        (self.root / "docs/link").symlink_to(self.root / "README.md")
        self.assert_rejected("Symlink")

    def test_invalid_frontmatter_yaml_rejected(self):
        self.write("skills/manage/SKILL.md", "---\nname: [broken\n---\n")
        with self.assertRaises(Exception) as err:
            validate(self.root)
        self.assertIn("while parsing", str(err.exception))

    def test_missing_frontmatter_rejected(self):
        self.write("skills/manage/SKILL.md", "# Text alone\n")
        self.assert_rejected("frontmatter")

    def test_wrong_skill_name_rejected(self):
        self.write("skills/manage/SKILL.md", "---\nname: wrong\ndescription: Text\n---\n")
        self.assert_rejected("metadata name")

    def test_malformed_agent_yaml_rejected(self):
        self.write("skills/manage/agents/openai.yaml", "interface: [invalid\n")
        with self.assertRaises(Exception):
            validate(self.root)

    def test_missing_skill_reference_rejected(self):
        self.write("skills/manage/SKILL.md", "---\nname: manage\ndescription: Text\n---\n[missing](references/lost.md)\n")
        self.assert_rejected("Broken Markdown reference")

    def test_escaped_reference_outside_root_rejected(self):
        self.write("skills/manage/SKILL.md", "---\nname: manage\ndescription: Text\n---\n[bad](../../../../../etc/passwd)\n")
        self.assert_rejected("Broken Markdown reference")

    def test_external_urls_do_not_need_local_files(self):
        self.write("skills/manage/SKILL.md", "---\nname: manage\ndescription: Text\n---\n[GitHub](https://github.com/example/repo)\n")
        validate(self.root)

    def test_missing_required_file_rejected(self):
        (self.root / "README.md").unlink()
        self.assert_rejected("Missing required file")

    def test_invalid_svg_rejected(self):
        self.write("assets/icon.svg", "not svg")
        with self.assertRaises(Exception):
            validate(self.root)

    def test_duplicate_json_key_rejected(self):
        self.write("plugin.json", '{"name":"agent-skills-manager","name":"evil"}')
        self.assert_rejected("duplicate JSON key")


if __name__ == "__main__":
    unittest.main()
