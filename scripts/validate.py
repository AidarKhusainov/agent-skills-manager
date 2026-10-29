#!/usr/bin/env python3
"""Validate package structure and metadata, not agent behavior or prose headings."""

import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "agent-skills-manager"
DISPLAY = "Agent Skills Manager"
RELEASE_BRANCH = "master"  # GitHub's default / canonical release branch.
REPO_URL = "https://github.com/AidarKhusainov/agent-skills-manager.git"
REQUIRED = (
    "VERSION", "plugin.json", ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json",
    "skills/manage/SKILL.md", "skills/manage/agents/openai.yaml",
    "assets/icon.svg", "README.md", "LICENSE", ".gitignore",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b"),
)
EXCLUDED_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache"}
SCANNED_SUFFIXES = {".json", ".yaml", ".yml", ".py", ".md", ".txt", ".sh", ".toml"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(root: Path, name: str) -> dict:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"{name}: duplicate JSON key {key}")
            result[key] = value
        return result

    value = json.loads((root / name).read_text(encoding="utf-8"), object_pairs_hook=unique)
    require(isinstance(value, dict), f"{name}: expected JSON object")
    return value


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.name}: expected YAML mapping")
    return value


def text_field(value, label: str, limit: int = 1000) -> None:
    require(isinstance(value, str) and 0 < len(value.strip()) <= limit, f"Invalid {label}")


def package_path(root: Path, value, expected: str) -> None:
    require(isinstance(value, str) and value == "./" + expected, f"Invalid package path: {value}")
    require((root / expected).exists(), f"Missing package path: {expected}")


def validate_links(root: Path, source: Path) -> None:
    """Validate local Markdown inline references; do not inspect their prose."""
    content = source.read_text(encoding="utf-8")
    for raw in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)]+)\)", content):
        dest = raw.strip().split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(dest)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        path = unquote(parsed.path)
        normalized = PurePosixPath(path)
        require(not normalized.is_absolute() and "\\" not in path and "\x00" not in path,
                f"Unsafe Markdown reference in {source.relative_to(root)}: {dest}")
        resolved = (source.parent / path).resolve()
        require(resolved.is_relative_to(root.resolve()) and resolved.is_file(),
                f"Broken Markdown reference in {source.relative_to(root)}: {dest}")


def validate_public_files(root: Path) -> None:
    """Reject user state, common credential artifacts, symlinks, and token material."""
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(p in EXCLUDED_DIRS for p in rel.parts):
            continue
        require(not path.is_symlink(), f"Symlink not allowed in public package: {rel}")
        if not path.is_file():
            continue
        name = path.name.lower()
        require(name != "sources.json", f"User source ledger must not ship: {rel}")
        require(not (name == ".env" or name.startswith(".env.") or
                     name in {"credentials.json", "secrets.json", "id_rsa", "id_ed25519"} or
                     path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}),
                f"Credential-like file must not ship: {rel}")
        if path.suffix.lower() in SCANNED_SUFFIXES or name == ".gitignore":
            require(path.stat().st_size <= 1_000_000, f"Oversized source file: {rel}")
            content = path.read_text(encoding="utf-8")
            require(not any(pattern.search(content) for pattern in SECRET_PATTERNS),
                    f"Possible credential in public file: {rel}")


def validate(root: Path = ROOT) -> None:
    root = Path(root).resolve()
    for name in REQUIRED:
        require((root / name).is_file(), f"Missing required file: {name}")
    validate_public_files(root)

    primary = load_json(root, "plugin.json")
    compatible = load_json(root, ".codex-plugin/plugin.json")
    for name, manifest in (("plugin.json", primary), (".codex-plugin/plugin.json", compatible)):
        require(manifest.get("name") == PACKAGE, f"{name}: invalid package name")
        text_field(manifest.get("description"), f"{name} description")
        author = manifest.get("author")
        require(isinstance(author, dict), f"{name}: missing author")
        text_field(author.get("name"), f"{name} author")
        require("email" not in author, f"{name}: do not publish author email")
        require(isinstance(manifest.get("keywords"), list), f"{name}: keywords must be a list")
    version = primary.get("version")
    expected_version = (root / "VERSION").read_text(encoding="utf-8").strip()
    require(re.fullmatch(r"(?:0|[1-9]\\d*)\\.(?:0|[1-9]\\d*)\\.(?:0|[1-9]\\d*)(?:-[0-9A-Za-z.-]+)?", expected_version) is not None,
            "VERSION: invalid semantic version")
    require(isinstance(version, str) and re.fullmatch(r"0|[1-9]\d*", version.split(".")[0]) is not None
            and re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?", version) is not None,
            "Invalid semantic version")
    require(version == expected_version,
            f"Manifest version {version!r} does not match VERSION {expected_version!r}")
    for field in ("name", "version", "description", "author", "keywords"):
        require(primary.get(field) == compatible.get(field), f"Manifest mismatch: {field}")
    package_path(root, compatible.get("skills"), "skills")
    openai_primary = primary.get("extensions", {}).get("com.openai", {})
    openai_compat = compatible.get("extensions", {}).get("com.openai", {})
    require(isinstance(openai_primary, dict) and isinstance(openai_compat, dict), "Missing OpenAI extension")
    package_path(root, openai_primary.get("onboardingSkill"), "skills/manage/SKILL.md")
    package_path(root, openai_compat.get("onboardingSkill"), "skills/manage/SKILL.md")
    ui = openai_primary.get("interface")
    require(isinstance(ui, dict) and ui == compatible.get("interface"), "Manifest UI metadata mismatch")
    require(ui.get("displayName") == DISPLAY, "Unexpected display name")
    for field in ("shortDescription", "longDescription", "developerName", "category"):
        text_field(ui.get(field), f"interface.{field}")
    caps = ui.get("capabilities")
    require(isinstance(caps, list) and caps and all(isinstance(c, str) and c.strip() for c in caps),
            "Invalid capabilities")
    prompts = ui.get("defaultPrompt")
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 5 and
            all(isinstance(p, str) and 0 < len(p.strip()) <= 300 for p in prompts),
            "Invalid onboarding prompts")
    for icon in ("logo", "composerIcon"):
        package_path(root, ui.get(icon), "assets/icon.svg")

    marketplace = load_json(root, ".agents/plugins/marketplace.json")
    require(marketplace.get("name") == PACKAGE and
            marketplace.get("interface", {}).get("displayName") == DISPLAY,
            "Marketplace identity mismatch")
    entries = marketplace.get("plugins")
    require(isinstance(entries, list) and len(entries) == 1, "Marketplace must ship exactly one plugin")
    entry = entries[0]
    require(entry.get("name") == PACKAGE and entry.get("category") == ui["category"],
            "Marketplace entry metadata mismatch")
    require(entry.get("source") == {"source": "url", "url": REPO_URL, "ref": RELEASE_BRANCH},
            f"Marketplace must track canonical release branch {RELEASE_BRANCH}")
    require(entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "Marketplace policy mismatch")

    skills = root / "skills"
    require(sorted(p.name for p in skills.iterdir()) == ["manage"],
            "Public package must contain only the manager skill")
    require(sorted(str(p.relative_to(skills)) for p in skills.rglob("SKILL.md")) == ["manage/SKILL.md"],
            "Public package contains a third-party skill")
    skill_path = skills / "manage/SKILL.md"
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)",
                     skill_path.read_text(encoding="utf-8"), flags=re.DOTALL)
    require(match is not None, "Missing SKILL.md YAML frontmatter")
    metadata = yaml.safe_load(match.group(1))
    require(isinstance(metadata, dict) and metadata.get("name") == "manage", "Invalid skill metadata name")
    text_field(metadata.get("description"), "SKILL.md description")
    agent = load_yaml(skills / "manage/agents/openai.yaml")
    agent_ui = agent.get("interface")
    require(isinstance(agent_ui, dict), "Missing skill interface")
    require(agent_ui.get("display_name") == DISPLAY, "Skill display name mismatch")
    text_field(agent_ui.get("short_description"), "Skill short description")
    text_field(agent_ui.get("default_prompt"), "Skill default prompt")
    for link_path in [skill_path, *(skills / "manage/references").glob("*.md")]:
        validate_links(root, link_path)
    ElementTree.parse(root / "assets/icon.svg")


def main() -> int:
    try:
        validate()
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError,
            yaml.YAMLError, ElementTree.ParseError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    print("OK: package structure, manifests, YAML, references, marketplace, and public boundary")
    return 0


if __name__ == "__main__":
    sys.exit(main())
