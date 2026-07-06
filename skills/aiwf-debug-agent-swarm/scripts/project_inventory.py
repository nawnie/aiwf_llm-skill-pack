#!/usr/bin/env python3
"""Create a compact debugging inventory for parallel code agents."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import Counter
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".codex",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".next",
    ".nuxt",
    ".turbo",
    "dist",
    "build",
    "target",
    ".gradle",
}

MANIFESTS = {
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
    "poetry.lock",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Makefile",
}

CONFIG_HINTS = {
    "AGENTS.md",
    "README.md",
    "README.rst",
    "pytest.ini",
    "tox.ini",
    "noxfile.py",
    "vitest.config.ts",
    "vitest.config.js",
    "jest.config.js",
    "jest.config.ts",
    "playwright.config.ts",
    "playwright.config.js",
    "tsconfig.json",
    ".github",
}

TEST_MARKERS = ("test", "spec", "__tests__", "tests")


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def run_git(root: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip()


def iter_files(root: Path, max_files: int) -> list[Path]:
    found: list[Path] = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        current_path = Path(current)
        for name in files:
            path = current_path / name
            found.append(path)
            if len(found) >= max_files:
                return found
    return found


def top_dirs(files: list[Path], root: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in files:
        parts = path.relative_to(root).parts
        counts[parts[0] if len(parts) > 1 else "." ] += 1
    return counts


def detect_commands(root: Path, files: list[Path]) -> list[str]:
    names = {path.name for path in files}
    commands: list[str] = []
    package_json = root / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = data.get("scripts", {})
            for key in ("test", "lint", "typecheck", "build", "dev"):
                if key in scripts:
                    runner = "pnpm" if "pnpm-lock.yaml" in names else "npm"
                    commands.append(f"{runner} run {key}")
        except (OSError, json.JSONDecodeError):
            commands.append("Inspect package.json scripts")
    if "pyproject.toml" in names or "pytest.ini" in names or any("tests" in path.parts for path in files):
        commands.append("python -m pytest")
    if "go.mod" in names:
        commands.append("go test ./...")
    if "Cargo.toml" in names:
        commands.append("cargo test")
    if "Makefile" in names:
        commands.append("make test")
    return list(dict.fromkeys(commands))


def write_inventory(root: Path, out: Path, max_files: int) -> None:
    files = iter_files(root, max_files)
    names = {path.name for path in files}
    manifests = sorted(rel(path, root) for path in files if path.name in MANIFESTS)
    configs = sorted(rel(path, root) for path in files if path.name in CONFIG_HINTS or any(part == ".github" for part in path.parts))
    tests = sorted(rel(path, root) for path in files if any(marker in path.name.lower() or marker in [p.lower() for p in path.parts] for marker in TEST_MARKERS))
    extensions = Counter(path.suffix.lower() or "[no extension]" for path in files)
    dirs = top_dirs(files, root)
    commands = detect_commands(root, files)
    status = run_git(root, ["status", "--short"])
    branch = run_git(root, ["branch", "--show-current"])

    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Debug Agent Swarm Inventory",
        "",
        f"- Root: `{root}`",
        f"- Git branch: `{branch or 'unknown'}`",
        f"- Files scanned: {len(files)}" + (" (truncated)" if len(files) >= max_files else ""),
        "",
        "## Git Status",
        "",
        "```text",
        status or "clean or unavailable",
        "```",
        "",
        "## Suggested Commands",
        "",
    ]
    if commands:
        lines.extend(f"- `{command}`" for command in commands)
    else:
        lines.append("- No obvious commands detected")
    lines.extend(["", "## Manifests And Locks", ""])
    if manifests:
        lines.extend(f"- `{item}`" for item in manifests)
    else:
        lines.append("- None detected")
    lines.extend(["", "## Instructions And Config", ""])
    if configs:
        lines.extend(f"- `{item}`" for item in configs[:80])
    else:
        lines.append("- None detected")
    lines.extend(["", "## Top Directories", ""])
    lines.extend(f"- `{name}`: {count} files" for name, count in dirs.most_common(25))
    lines.extend(["", "## Common Extensions", ""])
    lines.extend(f"- `{name}`: {count}" for name, count in extensions.most_common(25))
    lines.extend(["", "## Test-Like Paths", ""])
    if tests:
        lines.extend(f"- `{item}`" for item in tests[:120])
    else:
        lines.append("- None detected")
    lines.extend(["", "## Lane Seed Ideas", ""])
    for name, _count in dirs.most_common(12):
        if name != ".":
            lines.append(f"- Explorer lane for `{name}/`: architecture, error paths, tests, and likely ownership")
    if manifests:
        lines.append("- Explorer lane for build/test/dependency configuration")
    if tests:
        lines.append("- Explorer lane for failing or missing tests")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root to inventory")
    parser.add_argument("--out", default="", help="Markdown output path")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"--root must be an existing directory: {root}")
    out = Path(args.out).resolve() if args.out else root / ".codex" / "aiwf-debug-agent-swarm" / "inventory.md"
    write_inventory(root, out, args.max_files)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
