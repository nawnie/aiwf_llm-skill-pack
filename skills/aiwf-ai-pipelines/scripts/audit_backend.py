from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


INTERESTING_FILES = [
    "AGENTS.md",
    "docs/qa/pipeline_feature_testing_matrix.csv",
    "outputs/failures/index.jsonl",
    "outputs/dev-trace.log",
    "aiwf.log",
    "aiwf/services/pipeline_registry.py",
    "aiwf/services/pipeline_preflight.py",
    "aiwf/services/pipeline_readiness.py",
    "aiwf/web/pro_api.py",
    "aiwf/api/v1/routes.py",
    "frontend/src/api.ts",
]

CODE_GLOBS = [
    "aiwf/services/**/*.py",
    "aiwf/infrastructure/**/*.py",
    "aiwf/web/**/*.py",
    "aiwf/api/**/*.py",
    "frontend/src/api.ts",
    "tests/individual_tests/test_*pipeline*.py",
    "tests/individual_tests/test_*runtime*.py",
    "tests/individual_tests/test_*pro_api*.py",
    "tests/individual_tests/test_*wan*.py",
    "tests/individual_tests/test_*sana*.py",
    "tests/individual_tests/test_*ltx*.py",
    "tests/individual_tests/test_*qwen*.py",
]

FAMILY_PATTERNS = {
    "flux": re.compile(r"\bflux\b|flux2|flux\.2|klein|z[-_ ]?image", re.I),
    "qwen": re.compile(r"\bqwen\b|nunchaku", re.I),
    "sana": re.compile(r"\bsana\b", re.I),
    "wan": re.compile(r"\bwan\b|ti2v|i2v", re.I),
    "ltx": re.compile(r"\bltx\b", re.I),
    "sd": re.compile(r"\bsd1?5\b|sdxl|sd3|stable.?diffusion|inpaint", re.I),
    "llm": re.compile(r"\bllm\b|llama|ollama|vllm|gguf|chat|rag|lm[-_ ]?eval", re.I),
    "ui_api": re.compile(r"pro_api|api/v1|frontend|gradio|runtime/stream|client-events|client-errors", re.I),
}


def read_text(path: Path, limit: int = 2_000_000) -> str:
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    if len(data) > limit:
        data = data[-limit:]
    return data.decode("utf-8", errors="replace")


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def classify_family(text: str) -> set[str]:
    return {name for name, pattern in FAMILY_PATTERNS.items() if pattern.search(text)}


def parse_matrix(root: Path) -> tuple[list[dict[str, Any]], Counter]:
    path = root / "docs/qa/pipeline_feature_testing_matrix.csv"
    if not path.exists():
        return [], Counter()
    rows: list[dict[str, Any]] = []
    counts: Counter = Counter()
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(dict(row))
            status = (
                row.get("current_status")
                or row.get("status")
                or row.get("Status")
                or ""
            ).strip() or "unknown"
            counts[status] += 1
    return rows, counts


def parse_failures(root: Path) -> list[dict[str, Any]]:
    path = root / "outputs/failures/index.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-200:]
    failures: list[dict[str, Any]] = []
    for line in lines:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        request = row.get("request") or {}
        error = row.get("error") or {}
        text = " ".join(
            str(part or "")
            for part in [
                row.get("kind"),
                row.get("stage"),
                request.get("checkpoint_id"),
                request.get("model_id"),
                error.get("type"),
                error.get("message"),
            ]
        )
        failures.append(
            {
                "created_at": row.get("created_at"),
                "kind": row.get("kind"),
                "stage": row.get("stage"),
                "status": row.get("status"),
                "checkpoint_id": request.get("checkpoint_id") or request.get("model_id"),
                "error_type": error.get("type"),
                "error": str(error.get("message") or "")[:500],
                "families": sorted(classify_family(text)),
            }
        )
    return failures


def scan_code(root: Path) -> dict[str, Any]:
    files: set[Path] = set()
    for pattern in CODE_GLOBS:
        files.update(path for path in root.glob(pattern) if path.is_file())
    family_files: dict[str, list[str]] = defaultdict(list)
    route_terms: Counter = Counter()
    tests_by_family: dict[str, list[str]] = defaultdict(list)
    suspicious: list[dict[str, str]] = []
    for path in sorted(files):
        text = read_text(path, limit=300_000)
        relative = rel(root, path)
        families = classify_family(relative + "\n" + text)
        for family in families:
            family_files[family].append(relative)
            if relative.startswith("tests/"):
                tests_by_family[family].append(relative)
        for term in ["/api/pro", "runtime/stream", "interrupt", "pending_count", "active_job", "GGUF", "from_pretrained", "from_single_file", "model_index.json"]:
            if term in text:
                route_terms[term] += 1
        for pattern in ["TODO", "FIXME", "not-wired", "unsupported-no-route", "broken-runtime"]:
            if pattern in text:
                suspicious.append({"file": relative, "marker": pattern})
    return {
        "family_files": {k: sorted(set(v))[:40] for k, v in sorted(family_files.items())},
        "tests_by_family": {k: sorted(set(v))[:30] for k, v in sorted(tests_by_family.items())},
        "route_terms": dict(route_terms),
        "markers": suspicious[:80],
        "files_scanned": len(files),
    }


def scan_models(root: Path) -> dict[str, Any]:
    model_root = root / "models"
    if not model_root.exists():
        return {"exists": False, "families": {}, "notable_files": []}
    families: dict[str, dict[str, Any]] = {}
    notable: list[dict[str, Any]] = []
    for path in model_root.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in {".safetensors", ".gguf", ".json", ".pt", ".pth", ".onnx"}:
            continue
        relative = rel(root, path)
        fams = classify_family(relative)
        for family in fams or {"unknown"}:
            item = families.setdefault(family, {"count": 0, "bytes": 0})
            item["count"] += 1
            try:
                item["bytes"] += path.stat().st_size
            except OSError:
                pass
        if suffix in {".safetensors", ".gguf", ".onnx"} and len(notable) < 100:
            try:
                size = path.stat().st_size
            except OSError:
                size = 0
            notable.append({"path": relative, "size_gb": round(size / (1024**3), 3), "suffix": suffix})
    return {"exists": True, "families": families, "notable_files": notable}


def build_findings(matrix_counts: Counter, failures: list[dict[str, Any]], code: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    failed = [f for f in failures if f.get("error")]
    if failed:
        counts = Counter(f.get("error_type") or "unknown" for f in failed)
        findings.append(
            {
                "severity": "high",
                "category": "broken-runtime",
                "summary": f"Recent failure log has {len(failed)} failed generation records; top error types: {dict(counts.most_common(5))}.",
            }
        )
    for status in ["broken-runtime", "unsupported-no-route", "metadata-only", "blocked-cleanly"]:
        if matrix_counts.get(status):
            findings.append(
                {
                    "severity": "medium" if status in {"broken-runtime", "unsupported-no-route"} else "low",
                    "category": "status-matrix",
                    "summary": f"QA matrix contains {matrix_counts[status]} `{status}` route(s).",
                }
            )
    markers = code.get("markers") or []
    if markers:
        findings.append(
            {
                "severity": "low",
                "category": "source-markers",
                "summary": f"Source scan found {len(markers)} markers such as TODO, not-wired, unsupported-no-route, or broken-runtime.",
            }
        )
    return findings


def write_markdown(out_path: Path, data: dict[str, Any]) -> None:
    lines: list[str] = []
    lines.append("# AI Pipeline Backend Audit")
    lines.append("")
    lines.append(f"Generated: {data['generated_at']}")
    lines.append(f"Root: `{data['root']}`")
    lines.append("")
    lines.append("## Local Artifacts")
    for item in data["artifacts"]:
        lines.append(f"- `{item['path']}`: {'present' if item['exists'] else 'missing'}")
    lines.append("")
    lines.append("## Status Counts")
    if data["matrix_counts"]:
        for key, value in sorted(data["matrix_counts"].items()):
            lines.append(f"- `{key}`: {value}")
    else:
        lines.append("- No QA matrix found.")
    lines.append("")
    lines.append("## Findings")
    if data["findings"]:
        for finding in data["findings"]:
            lines.append(f"- **{finding['severity']} / {finding['category']}**: {finding['summary']}")
    else:
        lines.append("- No local crawler findings.")
    lines.append("")
    lines.append("## Recent Failure Families")
    family_counts: Counter = Counter()
    for failure in data["failures"]:
        for family in failure.get("families") or ["unknown"]:
            family_counts[family] += 1
    if family_counts:
        for family, count in family_counts.most_common():
            lines.append(f"- `{family}`: {count}")
    else:
        lines.append("- No recent failure records parsed.")
    lines.append("")
    lines.append("## Code Coverage Seeds")
    for family, files in data["code"]["family_files"].items():
        tests = data["code"]["tests_by_family"].get(family, [])
        lines.append(f"- `{family}`: {len(files)} source seed(s), {len(tests)} test seed(s)")
    lines.append("")
    lines.append("## Next Agent Lanes")
    lines.append("- Image runtime: Diffusers, Flux/Flux.2/Z-Image/Qwen/Sana source-model alignment.")
    lines.append("- Video runtime: Sana Video, Wan GGUF/Diffusers, LTX route and VRAM/offload contracts.")
    lines.append("- LLM/GGUF: llama.cpp/GGUF/eval-harness readiness and UI exposure.")
    lines.append("- UI/API: FastAPI/React/Gradio connector state, errors, progress, and cancellation.")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit local AI pipeline backend wiring.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--out", default=None, help="Output directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out).resolve() if args.out else root / ".codex" / "aiwf-ai-pipelines" / "latest"
    out.mkdir(parents=True, exist_ok=True)

    artifacts = [{"path": item, "exists": (root / item).exists()} for item in INTERESTING_FILES]
    matrix_rows, matrix_counts = parse_matrix(root)
    failures = parse_failures(root)
    code = scan_code(root)
    models = scan_models(root)
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "artifacts": artifacts,
        "matrix_counts": dict(matrix_counts),
        "matrix_sample": matrix_rows[:50],
        "failures": failures[-80:],
        "code": code,
        "models": models,
        "findings": build_findings(matrix_counts, failures, code),
    }
    (out / "audit.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    write_markdown(out / "audit.md", data)
    print(f"Wrote {out / 'audit.md'}")
    print(f"Wrote {out / 'audit.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
