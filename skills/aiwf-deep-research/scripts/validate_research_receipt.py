from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "request.md",
    "source_plan.json",
    "queries.jsonl",
    "sources.jsonl",
    "claims.jsonl",
    "source_weights.jsonl",
    "contradictions.jsonl",
    "research_brief.md",
]

CLAIM_THRESHOLDS = {
    "scientific_mechanism": 85,
    "engineering_mechanism": 85,
    "implementation_feasibility": 70,
    "api_runtime_behavior": 70,
    "model_resource_availability": 60,
    "educational_background": 55,
    "practitioner_context": 25,
    "open_question": 0,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path.name}:{line_no}: record must be an object")
        records.append(value)
    return records


def require_fields(record: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in record or record[field] in ("", None, []):
            errors.append(f"{label} missing required field: {field}")


def int_weight(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def validate(run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    run_dir = run_dir.resolve()

    if not run_dir.exists() or not run_dir.is_dir():
        errors.append(f"run_dir does not exist or is not a directory: {run_dir}")
        return {"status": "failed", "errors": errors, "warnings": warnings}

    for filename in REQUIRED_FILES:
        if not (run_dir / filename).exists():
            errors.append(f"missing required file: {filename}")

    if (run_dir / "source_plan.json").exists():
        try:
            source_plan = read_json(run_dir / "source_plan.json")
            require_fields(source_plan, ["request", "domains", "target_sources", "excluded_sources", "query_templates"], "source_plan", errors)
        except Exception as exc:
            errors.append(f"source_plan.json invalid: {exc}")

    sources: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []

    for filename, target in [
        ("sources.jsonl", "sources"),
        ("claims.jsonl", "claims"),
        ("contradictions.jsonl", "contradictions"),
        ("queries.jsonl", "queries"),
        ("source_weights.jsonl", "source_weights"),
    ]:
        path = run_dir / filename
        if not path.exists():
            continue
        try:
            records = read_jsonl(path)
        except Exception as exc:
            errors.append(str(exc))
            continue
        if target == "sources":
            sources = records
        elif target == "claims":
            claims = records
        elif target == "contradictions":
            contradictions = records

    source_ids = {str(src.get("id")) for src in sources if src.get("id")}
    for source in sources:
        label = f"source {source.get('id', '<missing id>')}"
        require_fields(source, ["id", "title", "url_or_path", "source_class", "allowed_use", "evidence_weight", "weight_reason"], label, errors)
        weight = int_weight(source.get("evidence_weight"))
        if weight is None or not 0 <= weight <= 100:
            errors.append(f"{label} evidence_weight must be an integer from 0 to 100")

    for claim in claims:
        label = f"claim {claim.get('id', '<missing id>')}"
        require_fields(claim, ["id", "claim", "claim_type", "source_ids", "evidence_weight", "weight_reason", "verification_state"], label, errors)
        weight = int_weight(claim.get("evidence_weight"))
        if weight is None or not 0 <= weight <= 100:
            errors.append(f"{label} evidence_weight must be an integer from 0 to 100")
            continue
        claim_type = str(claim.get("claim_type", ""))
        threshold = CLAIM_THRESHOLDS.get(claim_type)
        if threshold is None:
            errors.append(f"{label} unknown claim_type: {claim_type}")
        elif bool(claim.get("used_in_final")) and weight < threshold:
            errors.append(f"{label} used_in_final weight {weight} is below threshold {threshold} for {claim_type}")
        ids = claim.get("source_ids")
        if isinstance(ids, list):
            missing = [source_id for source_id in ids if str(source_id) not in source_ids]
            if missing and sources:
                errors.append(f"{label} references missing source_ids: {missing}")
        else:
            errors.append(f"{label} source_ids must be a list")
        if claim_type in {"scientific_mechanism", "engineering_mechanism"} and bool(claim.get("used_in_final")):
            classes = [src.get("source_class") for src in sources if src.get("id") in set(ids or [])]
            if not any(str(value).startswith(("tier0", "tier1")) for value in classes):
                errors.append(f"{label} final scientific/engineering claim lacks Tier 0 or Tier 1 support")

    for contradiction in contradictions:
        label = f"contradiction {contradiction.get('id', '<missing id>')}"
        require_fields(contradiction, ["id", "claim_ids", "source_ids", "resolution_rule", "remaining_uncertainty"], label, errors)

    if not sources:
        warnings.append("No sources recorded yet.")
    if not claims:
        warnings.append("No claims recorded yet.")

    status = "passed" if not errors else "failed"
    return {
        "status": status,
        "run_dir": str(run_dir),
        "counts": {
            "sources": len(sources),
            "claims": len(claims),
            "contradictions": len(contradictions),
        },
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AIWF deep research run receipt.")
    parser.add_argument("run_dir")
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    result = validate(run_dir)
    if run_dir.exists() and run_dir.is_dir():
        (run_dir / "validation.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
