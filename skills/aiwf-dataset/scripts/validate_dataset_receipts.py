#!/usr/bin/env python3
"""Read-only validation for local dataset receipt folders."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PLACEHOLDER_PATTERNS = [
    re.compile(r"\[(?:INSERT|Insert|Your|Add|Describe|Specify|TODO)[^\]]*\]"),
    re.compile(r"\b\d{4}-XX-XX\b"),
    re.compile(r"<!--\s*(?:add|fill|todo|insert)", re.IGNORECASE),
]

AI_LEAK_PATTERNS = [
    re.compile(r"contentReference\[", re.IGNORECASE),
    re.compile(r"oaicite", re.IGNORECASE),
    re.compile(r"citeturn\d+", re.IGNORECASE),
    re.compile(r"grok_card", re.IGNORECASE),
    re.compile(r"utm_source=(?:chatgpt\.com|copilot\.com|openai|claude\.ai|perplexity\.ai)", re.IGNORECASE),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local dataset manifests and JSONL receipts.")
    parser.add_argument("root", nargs="?", default="datasets", help="Dataset root or single dataset folder.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument(
        "--required-field",
        action="append",
        default=["id"],
        help="Required JSONL field. Repeatable. Defaults to id.",
    )
    return parser.parse_args()


def add_issue(issues: list[dict[str, str]], severity: str, path: Path, message: str) -> None:
    issues.append({"severity": severity, "path": str(path), "message": message})


def read_text(path: Path, issues: list[dict[str, str]]) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover - defensive fallback
            add_issue(issues, "error", path, f"Could not read text: {exc}")
            return ""
    except Exception as exc:
        add_issue(issues, "error", path, f"Could not read text: {exc}")
        return ""


def validate_json(path: Path, issues: list[dict[str, str]]) -> Any | None:
    text = read_text(path, issues)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        add_issue(issues, "error", path, f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return None


def validate_jsonl(path: Path, required_fields: list[str], issues: list[dict[str, str]]) -> dict[str, int]:
    stats = {"rows": 0, "missing_required": 0, "duplicate_ids": 0}
    seen_ids: set[str] = set()
    text = read_text(path, issues)
    if not text:
        return stats

    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            add_issue(issues, "error", path, f"Invalid JSONL at line {line_no}, column {exc.colno}: {exc.msg}")
            continue
        if not isinstance(row, dict):
            add_issue(issues, "error", path, f"JSONL line {line_no} is not an object")
            continue
        stats["rows"] += 1
        missing = [field for field in required_fields if field not in row or row[field] in (None, "")]
        if missing:
            stats["missing_required"] += 1
            add_issue(issues, "warning", path, f"Line {line_no} missing required fields: {', '.join(missing)}")
        row_id = row.get("id")
        if row_id is not None:
            key = str(row_id)
            if key in seen_ids:
                stats["duplicate_ids"] += 1
                add_issue(issues, "error", path, f"Duplicate id at line {line_no}: {key}")
            seen_ids.add(key)
    return stats


def scan_text_leaks(path: Path, issues: list[dict[str, str]]) -> None:
    if path.suffix.lower() not in {".md", ".txt", ".json", ".jsonl", ".csv", ".yaml", ".yml"}:
        return
    text = read_text(path, issues)
    if not text:
        return
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            add_issue(issues, "warning", path, f"Possible placeholder leak: {pattern.pattern}")
            break
    for pattern in AI_LEAK_PATTERNS:
        if pattern.search(text):
            add_issue(issues, "warning", path, f"Possible AI citation/tool leak: {pattern.pattern}")
            break


def dataset_dirs(root: Path) -> list[Path]:
    if any((root / name).exists() for name in ("manifest.json", "source_registry.json")):
        return [root]
    return sorted([p for p in root.iterdir() if p.is_dir()])


def validate_dataset(path: Path, required_fields: list[str]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    stats: dict[str, Any] = {
        "path": str(path),
        "json_files": 0,
        "jsonl_files": 0,
        "jsonl_rows": 0,
        "missing_receipts": [],
        "issues": issues,
    }

    expected = ["manifest.json", "source_registry.json", "AUDIT.md"]
    for name in expected:
        if not (path / name).exists():
            stats["missing_receipts"].append(name)
            add_issue(issues, "warning", path / name, "Expected receipt file is missing")

    for json_path in sorted(path.rglob("*.json")):
        stats["json_files"] += 1
        validate_json(json_path, issues)
        scan_text_leaks(json_path, issues)

    for jsonl_path in sorted(path.rglob("*.jsonl")):
        stats["jsonl_files"] += 1
        jsonl_stats = validate_jsonl(jsonl_path, required_fields, issues)
        stats["jsonl_rows"] += jsonl_stats["rows"]
        scan_text_leaks(jsonl_path, issues)

    for text_path in sorted(path.rglob("*")):
        if text_path.is_file() and text_path.suffix.lower() in {".md", ".txt", ".csv", ".yaml", ".yml"}:
            scan_text_leaks(text_path, issues)

    return stats


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    result: dict[str, Any] = {"root": str(root), "datasets": [], "summary": {}, "status": "pass"}

    if not root.exists():
        result["status"] = "fail"
        result["summary"] = {"errors": 1, "warnings": 0}
        result["datasets"] = [
            {
                "path": str(root),
                "issues": [{"severity": "error", "path": str(root), "message": "Root does not exist"}],
            }
        ]
        emit(result, args.json)
        return 1

    if not root.is_dir():
        result["status"] = "fail"
        result["summary"] = {"errors": 1, "warnings": 0}
        result["datasets"] = [
            {
                "path": str(root),
                "issues": [{"severity": "error", "path": str(root), "message": "Root is not a directory"}],
            }
        ]
        emit(result, args.json)
        return 1

    datasets = dataset_dirs(root)
    if not datasets:
        result["status"] = "fail"
        result["summary"] = {"errors": 1, "warnings": 0}
        result["datasets"] = [
            {
                "path": str(root),
                "issues": [{"severity": "error", "path": str(root), "message": "No dataset folders found"}],
            }
        ]
        emit(result, args.json)
        return 1

    result["datasets"] = [validate_dataset(path, args.required_field) for path in datasets]
    errors = sum(1 for dataset in result["datasets"] for issue in dataset["issues"] if issue["severity"] == "error")
    warnings = sum(1 for dataset in result["datasets"] for issue in dataset["issues"] if issue["severity"] == "warning")
    result["summary"] = {"datasets": len(datasets), "errors": errors, "warnings": warnings}

    if errors or (args.strict and warnings):
        result["status"] = "fail"

    emit(result, args.json)
    return 0 if result["status"] == "pass" else 1


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    summary = result.get("summary", {})
    print(f"status: {result.get('status')}")
    print(f"root: {result.get('root')}")
    if summary:
        print(
            "summary: "
            + ", ".join(f"{key}={value}" for key, value in summary.items())
        )
    for dataset in result.get("datasets", []):
        print(f"\n{dataset.get('path')}")
        print(f"  json_files: {dataset.get('json_files', 0)}")
        print(f"  jsonl_files: {dataset.get('jsonl_files', 0)}")
        print(f"  jsonl_rows: {dataset.get('jsonl_rows', 0)}")
        missing = dataset.get("missing_receipts") or []
        if missing:
            print(f"  missing_receipts: {', '.join(missing)}")
        for issue in dataset.get("issues", []):
            print(f"  [{issue['severity']}] {issue['path']}: {issue['message']}")


if __name__ == "__main__":
    sys.exit(main())
