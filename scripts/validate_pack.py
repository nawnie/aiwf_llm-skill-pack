from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MAX_SKILL_LINES = 160
IMPLICIT_SKILL = "aiwf-orchestrator"
CORE_DOCS = (
    "AGENTS.md",
    "HANDOFF.md",
    "PROJECT_SKILLS.md",
    "README.md",
    "docs/projectskill-list.use-cases.json",
)
STALE_PATTERNS = {
    "retired orchestration lane": r"\baiwf-orchestration\b",
    "retired broad coding lane": r"\baiwf-ai-coding-guardrails\b",
    "retired broad web lane": r"\baiwf-web-api-ui-guardian\b",
    "retired broad native lane": r"\baiwf-python-cpp-hardener\b",
    "removed visual workflow product": r"\bcomfyui\b",
    "stale desktop path": r"desktop[\\/]sort desktop",
    "pinned ROS Humble docs": r"docs\.ros\.org/en/humble",
    "stale CSS snapshot": r"css-2025",
}
SCRIPT_REFERENCE = re.compile(
    r"(?:<this-skill>[\\/])?(scripts[\\/][A-Za-z0-9_.-]+\.py)",
    re.IGNORECASE,
)
SKILL_LITERAL = re.compile(r'["\'](aiwf-[a-z0-9-]+)["\']')


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(read_text(path))
    except FileNotFoundError:
        errors.append(f"missing JSON file: {path}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"expected JSON object in {path}")
        return {}
    return value


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def validate_skill(skill_dir: Path, implicit: set[str], errors: list[str]) -> None:
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    metadata_file = skill_dir / "agents" / "openai.yaml"

    if not skill_file.exists():
        errors.append(f"{skill_name}: missing SKILL.md")
        return
    text = read_text(skill_file)
    name = frontmatter_value(text, "name")
    description = frontmatter_value(text, "description")
    if name != skill_name:
        errors.append(f"{skill_name}: frontmatter name is {name!r}")
    if not skill_name.startswith("aiwf-"):
        errors.append(f"{skill_name}: folder does not start with aiwf-")
    if not description:
        errors.append(f"{skill_name}: missing frontmatter description")

    line_count = len(text.splitlines())
    if line_count > MAX_SKILL_LINES:
        errors.append(f"{skill_name}: SKILL.md has {line_count} lines; max is {MAX_SKILL_LINES}")

    if not metadata_file.exists():
        errors.append(f"{skill_name}: missing agents/openai.yaml")
    else:
        metadata = read_text(metadata_file)
        display_name = yaml_scalar(metadata, "display_name")
        expected_display = skill_name.replace("aiwf-", "aiwf_", 1)
        if display_name != expected_display:
            errors.append(
                f"{skill_name}: display_name is {display_name!r}; expected {expected_display!r}"
            )
        short_description = yaml_scalar(metadata, "short_description")
        if short_description is None or not 25 <= len(short_description) <= 64:
            errors.append(
                f"{skill_name}: short_description must be 25-64 characters; "
                f"got {len(short_description or '')}"
            )
        default_prompt = yaml_scalar(metadata, "default_prompt")
        if default_prompt is None or f"${skill_name}" not in default_prompt:
            errors.append(f"{skill_name}: default_prompt must mention ${skill_name}")
        policy = yaml_scalar(metadata, "allow_implicit_invocation")
        if policy not in {"true", "false"}:
            errors.append(f"{skill_name}: missing explicit allow_implicit_invocation policy")
        elif policy == "true":
            implicit.add(skill_name)

    markdown = "\n".join(
        read_text(path) for path in skill_dir.rglob("*.md") if path.is_file()
    )
    referenced_scripts: set[Path] = set()
    for match in SCRIPT_REFERENCE.finditer(markdown):
        relative = Path(match.group(1).replace("\\", "/"))
        referenced_scripts.add(relative)
        if not (skill_dir / relative).is_file():
            errors.append(f"{skill_name}: referenced helper is missing: {relative.as_posix()}")

    bundled_scripts = {
        path.relative_to(skill_dir)
        for path in skill_dir.glob("scripts/*.py")
        if path.is_file()
    }
    for path in sorted(bundled_scripts - referenced_scripts):
        errors.append(f"{skill_name}: bundled helper is not referenced: {path.as_posix()}")


def validate_stale_text(root: Path, errors: list[str]) -> None:
    targets = [path for path in (root / "skills").rglob("*") if path.is_file()]
    targets.extend(root / relative for relative in CORE_DOCS if (root / relative).is_file())
    for path in targets:
        if path.suffix.lower() not in {".md", ".json", ".py", ".yaml", ".yml"}:
            continue
        text = read_text(path)
        for label, pattern in STALE_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{path.relative_to(root)}: contains {label}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    manifest = load_json(root / "manifest.json", errors)
    plugin = load_json(root / ".codex-plugin" / "plugin.json", errors)
    if not skills_root.is_dir():
        return errors + [f"missing skills folder: {skills_root}"]

    source_skills = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    manifest_skills = manifest.get("skills")
    if manifest_skills != source_skills:
        errors.append("manifest skills must exactly match sorted source skill folders")

    retired = manifest.get("retired_skills", [])
    if not isinstance(retired, list):
        errors.append("manifest retired_skills must be a list")
        retired = []
    present_retired = sorted(set(retired) & set(source_skills))
    if present_retired:
        errors.append(f"retired skill folders are still present: {', '.join(present_retired)}")

    runtime_policy = manifest.get("runtime_policy", {})
    if runtime_policy.get("implicit_entrypoint") != IMPLICIT_SKILL:
        errors.append(f"manifest implicit_entrypoint must be {IMPLICIT_SKILL}")
    if runtime_policy.get("implicit_skill_count") != 1:
        errors.append("manifest implicit_skill_count must be 1")
    if runtime_policy.get("max_downstream_skills") != 4:
        errors.append("manifest max_downstream_skills must be 4")

    implicit: set[str] = set()
    for skill_dir in sorted(skills_root.iterdir()):
        if skill_dir.is_dir():
            validate_skill(skill_dir, implicit, errors)
    if implicit != {IMPLICIT_SKILL}:
        errors.append(f"implicit skills are {sorted(implicit)}; expected only {IMPLICIT_SKILL}")

    plugin_version = str(plugin.get("version", ""))
    manifest_version = str(manifest.get("version", ""))
    if plugin_version.split("+", 1)[0] != manifest_version:
        errors.append("plugin base version and pack manifest version do not match")
    if plugin.get("skills") != "./skills/":
        errors.append("plugin skills path must be ./skills/")
    for forbidden_key in ("mcpServers", "mcp_servers", "apps"):
        if forbidden_key in plugin:
            errors.append(f"skills-only plugin must not declare {forbidden_key}")
    capabilities = plugin.get("interface", {}).get("capabilities")
    if capabilities != ["Skills"]:
        errors.append("plugin capabilities must contain only Skills")

    router_file = skills_root / IMPLICIT_SKILL / "scripts" / "route_prompt.py"
    if not router_file.exists():
        errors.append(f"missing router helper: {router_file}")
    else:
        router_skills = set(SKILL_LITERAL.findall(read_text(router_file)))
        unknown = sorted(router_skills - set(source_skills))
        if unknown:
            errors.append(f"router references missing skills: {', '.join(unknown)}")

    deep_research = skills_root / "aiwf-deep-research" / "SKILL.md"
    if deep_research.exists() and "AIWF_DEEP_RESEARCH_EXTRA_URLS" not in read_text(deep_research):
        errors.append("aiwf-deep-research missing AIWF_DEEP_RESEARCH_EXTRA_URLS")

    validate_stale_text(root, errors)

    root_zips = sorted(path.name for path in root.glob("*.zip"))
    if root_zips:
        errors.append(f"ZIP files must live under dist: {', '.join(root_zips)}")
    pycache_paths = sorted(str(path.relative_to(root)) for path in root.rglob("__pycache__"))
    if pycache_paths:
        errors.append(f"generated __pycache__ folders present: {', '.join(pycache_paths)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the AIWF skill pack.")
    parser.add_argument("--root", default=".", help="Repository root to validate.")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    skill_count = len([path for path in (root / "skills").iterdir() if path.is_dir()])
    helper_count = len(list((root / "skills").glob("*/scripts/*.py")))
    print(f"OK: validated {skill_count} skills and {helper_count} bundled Python helpers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
