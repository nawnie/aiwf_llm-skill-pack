from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "skills" / "aiwf-orchestrator" / "scripts" / "route_prompt.py"
CASES = ROOT / "scripts" / "orchestrator_route_cases.json"


def load_router():
    spec = importlib.util.spec_from_file_location("aiwf_route_prompt", ROUTER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load router: {ROUTER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    router = load_router()
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    covered: set[str] = set()

    for case in cases:
        selected = [entry["skill"] for entry in router.route(case["prompt"])]
        expected = case["expected"]
        covered.update(expected)
        if selected != expected:
            failures.append(f"{case['name']}: expected {expected}; selected {selected}")
            continue
        if len(selected) > router.MAX_SKILLS:
            failures.append(f"{case['name']}: selected {len(selected)} skills; max is {router.MAX_SKILLS}")
            continue
        if len(selected) != len(set(selected)):
            failures.append(f"{case['name']}: duplicate skills in {selected}")
            continue
        print(f"route ok: {case['name']} -> {', '.join(selected)}")

    source_skills = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    downstream = source_skills - {"aiwf-orchestrator"}
    missing_coverage = sorted(downstream - covered)
    unknown_expected = sorted(covered - source_skills)
    if missing_coverage:
        failures.append(f"route cases do not cover skills: {missing_coverage}")
    if unknown_expected:
        failures.append(f"route cases reference missing skills: {unknown_expected}")

    if failures:
        print("route test failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
