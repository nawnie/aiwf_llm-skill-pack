from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SKILLS = {
    "aiwf-orchestration",
    "aiwf-deep-research",
    "aiwf-dataset",
    "aiwf-avoid-ai-design",
    "aiwf-avoid-ai-pushes",
}

REQUIRED_ORCHESTRATION_TOKENS = {
    "AIWF_MAX_AGENT_SPAWN",
    "AIWF_MAX_LOOPS_WITHOUT_PROGRESS",
    "AIWF_AI_AVOIDANCE_LEVEL",
    "AIWF_DEEP_RESEARCH_EXTRA_URLS",
    "AIWF_ALWAYS_ON_SKILLS",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_skill_name(skill_file: Path) -> str | None:
    text = read_text(skill_file)
    match = re.search(r"^name:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.exists():
        return [f"missing skills folder: {skills_root}"]

    found_dirs = {path.name for path in skills_root.iterdir() if path.is_dir()}
    missing = sorted(REQUIRED_SKILLS - found_dirs)
    if missing:
        errors.append(f"missing skill folders: {', '.join(missing)}")

    if "avoid-ai-writing" in found_dirs:
        errors.append("avoid-ai-writing must not be vendored; install.ps1 downloads it")

    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue
        name = extract_skill_name(skill_file)
        if not name:
            errors.append(f"{skill_dir.name}: missing name field")
        elif not name.startswith("aiwf-"):
            errors.append(f"{skill_dir.name}: name does not start with aiwf-: {name}")
        elif name != skill_dir.name:
            errors.append(f"{skill_dir.name}: folder name does not match skill name: {name}")

    orchestration_file = skills_root / "aiwf-orchestration" / "SKILL.md"
    if orchestration_file.exists():
        orchestration_text = read_text(orchestration_file)
        for token in REQUIRED_ORCHESTRATION_TOKENS:
            if token not in orchestration_text:
                errors.append(f"aiwf-orchestration missing variable: {token}")

    deep_research_file = skills_root / "aiwf-deep-research" / "SKILL.md"
    if deep_research_file.exists() and "AIWF_DEEP_RESEARCH_EXTRA_URLS" not in read_text(deep_research_file):
        errors.append("aiwf-deep-research missing AIWF_DEEP_RESEARCH_EXTRA_URLS")

    pycache_paths = [str(path) for path in root.rglob("__pycache__")]
    if pycache_paths:
        errors.append(f"generated __pycache__ folders present: {', '.join(pycache_paths)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the AIWF skill pack layout.")
    parser.add_argument("--root", default=".", help="Repository root to validate.")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: validated {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
