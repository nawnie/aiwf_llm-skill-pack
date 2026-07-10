from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MAX_SKILL_LINES = 160
IMPLICIT_SKILL = "aiwf-orchestrator"
EXPECTED_SKILL_COUNT = 56
EXPECTED_HELPER_COUNT = 22
CATALOG_BEGIN = "<!-- AIWF-SKILL-CATALOG:BEGIN -->"
CATALOG_END = "<!-- AIWF-SKILL-CATALOG:END -->"
INSTRUCTION_MODULES = {
    "aiwf-aeo-geo",
    "aiwf-application-api-security",
    "aiwf-data-privacy-protection",
    "aiwf-google-ads-business",
    "aiwf-incident-response-recovery",
    "aiwf-local-device-security",
    "aiwf-meta-business",
    "aiwf-multi-agent-workspace",
    "aiwf-online-infrastructure-security",
    "aiwf-software-ai-supply-chain-security",
    "aiwf-startup-finance-funding",
    "aiwf-startup-marketing-growth",
    "aiwf-youtube-adsense",
}
SECURITY_MODULES = {
    "aiwf-application-api-security",
    "aiwf-data-privacy-protection",
    "aiwf-incident-response-recovery",
    "aiwf-local-device-security",
    "aiwf-online-infrastructure-security",
    "aiwf-software-ai-supply-chain-security",
}
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
CATALOG_SKILL = re.compile(r"\|\s*`(aiwf-[a-z0-9-]+)`\s*\|")


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


def validate_instruction_module(skill_dir: Path, errors: list[str]) -> None:
    skill_name = skill_dir.name
    source_path = skill_dir / "references" / "source-register.json"
    eval_path = skill_dir / "evals" / "cases.jsonl"
    source_register = load_json(source_path, errors)
    if source_register.get("schema_version") != 1:
        errors.append(f"{skill_name}: source register schema_version must be 1")
    if source_register.get("skill") != skill_name:
        errors.append(f"{skill_name}: source register skill does not match")
    if not re.fullmatch(r"20\d\d-\d\d-\d\d", str(source_register.get("verified_on", ""))):
        errors.append(f"{skill_name}: source register needs verified_on YYYY-MM-DD")
    sources = source_register.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list) or not sources:
        errors.append(f"{skill_name}: source register needs a non-empty sources list")
        sources = []
    for index, source in enumerate(sources):
        prefix = f"{skill_name}: sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "title", "publisher", "url", "status", "version", "retrieved_at", "volatility", "supports"):
            if not source.get(field):
                errors.append(f"{prefix} missing {field}")
        source_id = source.get("id")
        if isinstance(source_id, str):
            if source_id in source_ids:
                errors.append(f"{skill_name}: duplicate source id {source_id}")
            source_ids.add(source_id)
        url = str(source.get("url", ""))
        if not url.startswith("https://") or "example.com" in url:
            errors.append(f"{prefix} must use a real HTTPS source URL")
        if not isinstance(source.get("supports"), list):
            errors.append(f"{prefix}.supports must be a list")

    if not eval_path.exists():
        errors.append(f"{skill_name}: missing evals/cases.jsonl")
        return
    cases: list[dict] = []
    for line_number, line in enumerate(read_text(eval_path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{skill_name}: invalid eval JSON on line {line_number}: {exc}")
            continue
        if not isinstance(case, dict):
            errors.append(f"{skill_name}: eval line {line_number} must be an object")
            continue
        cases.append(case)
    minimum = 10 if skill_name in SECURITY_MODULES else 8
    if len(cases) < minimum:
        errors.append(f"{skill_name}: needs at least {minimum} eval cases; found {len(cases)}")
    case_ids: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"{skill_name}: eval[{index}]"
        for field in ("id", "instruction", "expected_skill", "mode", "expected_response_outline", "required", "forbidden", "source_ids"):
            if field not in case:
                errors.append(f"{prefix} missing {field}")
        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in case_ids:
                errors.append(f"{skill_name}: duplicate eval id {case_id}")
            case_ids.add(case_id)
        if case.get("expected_skill") != skill_name:
            errors.append(f"{prefix} expected_skill must be {skill_name}")
        for field in ("expected_response_outline", "required", "forbidden", "source_ids"):
            if not isinstance(case.get(field), list):
                errors.append(f"{prefix}.{field} must be a list")
        unknown_sources = sorted(set(case.get("source_ids", [])) - source_ids) if isinstance(case.get("source_ids"), list) else []
        if unknown_sources:
            errors.append(f"{prefix} references unknown source ids: {', '.join(unknown_sources)}")


def validate_catalog(root: Path, source_skills: list[str], errors: list[str]) -> None:
    readme_path = root / "README.md"
    text = read_text(readme_path)
    if CATALOG_BEGIN not in text or CATALOG_END not in text:
        errors.append("README missing AIWF skill catalog markers")
        return
    block = text.split(CATALOG_BEGIN, 1)[1].split(CATALOG_END, 1)[0]
    catalog_skills = CATALOG_SKILL.findall(block)
    if sorted(catalog_skills) != source_skills:
        errors.append("README skill catalog must list every manifest skill exactly once")
    duplicates = sorted({name for name in catalog_skills if catalog_skills.count(name) > 1})
    if duplicates:
        errors.append(f"README skill catalog has duplicate skills: {', '.join(duplicates)}")
    for line in block.splitlines():
        if not CATALOG_SKILL.search(line):
            continue
        columns = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(columns) != 4:
            errors.append(f"README catalog row must have four columns: {line}")
            continue
        if not columns[0] or not columns[2] or not columns[3]:
            errors.append(f"README catalog row has an empty explanatory cell: {line}")
        if len(columns[2]) > 180 or len(columns[3]) > 180:
            errors.append(f"README catalog explanation is too long: {columns[1]}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    manifest = load_json(root / "manifest.json", errors)
    plugin = load_json(root / ".codex-plugin" / "plugin.json", errors)
    if not skills_root.is_dir():
        return errors + [f"missing skills folder: {skills_root}"]

    source_skills = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    if len(source_skills) != EXPECTED_SKILL_COUNT:
        errors.append(f"expected {EXPECTED_SKILL_COUNT} source skills; found {len(source_skills)}")
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
            if skill_dir.name in INSTRUCTION_MODULES:
                validate_instruction_module(skill_dir, errors)
    if implicit != {IMPLICIT_SKILL}:
        errors.append(f"implicit skills are {sorted(implicit)}; expected only {IMPLICIT_SKILL}")
    if manifest.get("release_codename") != "techstartup":
        errors.append("manifest release_codename must be techstartup")

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
    validate_catalog(root, source_skills, errors)

    root_zips = sorted(path.name for path in root.glob("*.zip"))
    if root_zips:
        errors.append(f"ZIP files must live under dist: {', '.join(root_zips)}")
    pycache_paths = sorted(str(path.relative_to(root)) for path in root.rglob("__pycache__"))
    if pycache_paths:
        errors.append(f"generated __pycache__ folders present: {', '.join(pycache_paths)}")
    helper_count = len(list(skills_root.glob("*/scripts/*.py")))
    if helper_count != EXPECTED_HELPER_COUNT:
        errors.append(f"expected {EXPECTED_HELPER_COUNT} bundled Python helpers; found {helper_count}")
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
