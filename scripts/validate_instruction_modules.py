from __future__ import annotations

import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_pack  # noqa: E402


def main() -> int:
    errors: list[str] = []
    total_cases = 0
    total_sources = 0
    for skill_name in sorted(validate_pack.INSTRUCTION_MODULES):
        skill_dir = ROOT / "skills" / skill_name
        if not skill_dir.is_dir():
            errors.append(f"missing instruction module: {skill_name}")
            continue
        validate_pack.validate_instruction_module(skill_dir, errors)
        source = json.loads((skill_dir / "references" / "source-register.json").read_text(encoding="utf-8"))
        total_sources += len(source.get("sources", []))
        total_cases += len(
            [line for line in (skill_dir / "evals" / "cases.jsonl").read_text(encoding="utf-8").splitlines() if line]
        )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"OK: validated {len(validate_pack.INSTRUCTION_MODULES)} instruction modules, "
        f"{total_sources} sources, and {total_cases} eval cases"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
