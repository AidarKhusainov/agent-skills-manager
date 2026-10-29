#!/usr/bin/env python3
"""Validate the distributable Agent Skills Manager sources without running skills."""
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "agent-skills-manager"
VERSION = "0.2.0"
DISPLAY_NAME = "Agent Skills Manager"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validate_path(value: str, expected: str) -> None:
    check(isinstance(value, str) and value == "./" + expected, f"Unexpected relative path: {value}")
    check((ROOT / expected).exists(), f"Missing referenced path: {expected}")


def main() -> None:
    required = [
        "plugin.json", ".codex-plugin/plugin.json", "assets/icon.svg",
        "skills/manage/SKILL.md", "skills/manage/agents/openai.yaml",
        "README.md", "LICENSE", ".gitignore", ".agents/plugins/marketplace.json",
    ]
    for path in required:
        check((ROOT / path).is_file(), f"Required file missing: {path}")

    primary, compatible = read_json("plugin.json"), read_json(".codex-plugin/plugin.json")
    for manifest in (primary, compatible):
        check(manifest.get("name") == PACKAGE_NAME, "Internal plugin name changed")
        check(manifest.get("version") == VERSION, "Manifest version mismatch")
        check(bool(manifest.get("description")), "Description required")
        check(manifest.get("author", {}).get("name"), "Author name required")
        check("email" not in manifest.get("author", {}), "Author email must not be bundled")

    ui = primary["extensions"]["com.openai"]["interface"]
    check(ui == compatible["interface"], "Display metadata differs between manifests")
    check(ui.get("displayName") == DISPLAY_NAME, "Wrong public display name")
    check(ui.get("category") == "Developer Tools", "Unexpected category")
    check(bool(ui.get("capabilities")), "Capabilities required")
    check(bool(ui.get("defaultPrompt")), "Onboarding prompt required")
    for icon in ("logo", "composerIcon"):
        validate_path(ui[icon], "assets/icon.svg")
    validate_path(primary["extensions"]["com.openai"]["onboardingSkill"], "skills/manage/SKILL.md")
    validate_path(compatible["extensions"]["com.openai"]["onboardingSkill"], "skills/manage/SKILL.md")
    validate_path(compatible["skills"], "skills")


    # Local Git-backed catalog: exactly one safe, public, repo-root plugin entry.
    marketplace = read_json(".agents/plugins/marketplace.json")
    check(marketplace.get("name") == "agent-skills-manager", "Unexpected marketplace name")
    check(marketplace.get("interface", {}).get("displayName") == DISPLAY_NAME, "Marketplace display name mismatch")
    entries = marketplace.get("plugins")
    check(isinstance(entries, list) and len(entries) == 1, "Marketplace must expose exactly one plugin")
    entry = entries[0]
    check(entry.get("name") == PACKAGE_NAME, "Marketplace plugin name mismatch")
    check(entry.get("source") == {
        "source": "url",
        "url": "https://github.com/AidarKhusainov/agent-skills-manager.git",
        "ref": "main",
    }, "Marketplace must reference this repository's main branch")
    check(entry.get("policy") == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }, "Unexpected marketplace installation policy")
    check(entry.get("category") == ui["category"], "Marketplace category mismatch")

    skill_dir = ROOT / "skills"
    check(sorted(p.name for p in skill_dir.iterdir()) == ["manage"], "Only manage may be shipped")
    check(sorted(str(p.relative_to(skill_dir)) for p in skill_dir.rglob("SKILL.md")) == ["manage/SKILL.md"], "Unexpected additional skill")
    check(not (ROOT / "sources.json").exists(), "User collection state cannot be bundled")

    skill = (skill_dir / "manage/SKILL.md").read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", skill, re.DOTALL)
    check(frontmatter is not None, "SKILL.md needs YAML frontmatter")
    meta = yaml.safe_load(frontmatter.group(1))
    check(isinstance(meta, dict) and meta.get("name") == "manage", "Invalid skill name")
    check(isinstance(meta.get("description"), str) and meta["description"].strip(), "Description required")
    check('managed_by: "skills-manager-public"' in skill, "Legacy collection marker changed")
    openai = yaml.safe_load((skill_dir / "manage/agents/openai.yaml").read_text(encoding="utf-8"))
    check(openai["interface"]["display_name"] == DISPLAY_NAME, "Skill display name mismatch")
    check(bool(openai["interface"]["default_prompt"]), "Skill default prompt missing")
    ElementTree.parse(ROOT / "assets/icon.svg")
    print("OK: manifests, YAML, skill inventory, relative paths, SVG and privacy boundary")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError, yaml.YAMLError, ElementTree.ParseError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
