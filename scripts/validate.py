#!/usr/bin/env python3
"""Validate the distributable Agent Skills Manager sources without running skills."""
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "skills-manager-public"
VERSION = "0.1.2"
DISPLAY_NAME = "Agent Skills Manager"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validate_path(value: str, expected: str) -> None:
    check(isinstance(value, str) and value == "./" + expected, f"Unexpected relative path: {value}")
    check((ROOT / expected).is_file(), f"Missing referenced file: {expected}")


def main() -> None:
    required = [
        "plugin.json", ".codex-plugin/plugin.json", "assets/icon.svg",
        "skills/manage-skills/SKILL.md", "skills/manage-skills/agents/openai.yaml",
        "README.md", "LICENSE", ".gitignore",
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
    validate_path(primary["extensions"]["com.openai"]["onboardingSkill"], "skills/manage-skills/SKILL.md")
    validate_path(compatible["extensions"]["com.openai"]["onboardingSkill"], "skills/manage-skills/SKILL.md")
    validate_path(compatible["skills"], "skills")

    skill_dir = ROOT / "skills"
    check(sorted(p.name for p in skill_dir.iterdir()) == ["manage-skills"], "Only manage-skills may be shipped")
    check(sorted(str(p.relative_to(skill_dir)) for p in skill_dir.rglob("SKILL.md")) == ["manage-skills/SKILL.md"], "Unexpected additional skill")
    check(not (ROOT / "sources.json").exists(), "User collection state cannot be bundled")

    skill = (skill_dir / "manage-skills/SKILL.md").read_text(encoding="utf-8")
    frontmatter = re.match(r"\\A---\\r?\\n(.*?)\\r?\\n---\\r?\\n", skill, re.DOTALL)
    check(frontmatter is not None, "SKILL.md needs YAML frontmatter")
    meta = yaml.safe_load(frontmatter.group(1))
    check(isinstance(meta, dict) and meta.get("name") == "manage-skills", "Invalid skill name")
    check(isinstance(meta.get("description"), str) and meta["description"].strip(), "Description required")
    check('managed_by: "skills-manager-public"' in skill, "User-collection marker changed")
    openai = yaml.safe_load((skill_dir / "manage-skills/agents/openai.yaml").read_text(encoding="utf-8"))
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
