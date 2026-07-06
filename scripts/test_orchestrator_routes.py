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
    spec.loader.exec_module(module)
    return module


def main() -> int:
    router = load_router()
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    for case in cases:
        selected = [entry["skill"] for entry in router.route(case["prompt"])]
        missing = [skill for skill in case["must_include"] if skill not in selected]
        if missing:
            failures.append(f"{case['name']}: missing {missing}; selected {selected}")
        else:
            print(f"route ok: {case['name']} -> {', '.join(selected)}")
    if failures:
        print("route test failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
