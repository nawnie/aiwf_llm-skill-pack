from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, check=False)
    if result.returncode != expected:
        raise AssertionError(
            f"{script.name} returned {result.returncode}, expected {expected}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="aiwf-helper-tests-") as temporary:
        temp = Path(temporary)

        runway_script = ROOT / "skills" / "aiwf-startup-finance-funding" / "scripts" / "calculate_runway.py"
        runway_input = temp / "runway.json"
        runway_output = temp / "runway-result.json"
        runway_input.write_text(
            json.dumps(
                {
                    "currency": "USD",
                    "starting_cash": 1000,
                    "scenarios": [
                        {
                            "name": "base",
                            "months": [
                                {"month": "2026-08", "inflows": 100, "outflows": 400},
                                {"month": "2026-09", "inflows": 100, "outflows": 900},
                            ],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        run(runway_script, "--input", str(runway_input), "--output", str(runway_output))
        runway = json.loads(runway_output.read_text(encoding="utf-8"))
        assert runway["scenario_results"][0]["funded_months_in_horizon"] == 1
        assert runway["scenario_results"][0]["depletion_month"] == "2026-09"

        inventory_script = ROOT / "skills" / "aiwf-data-privacy-protection" / "scripts" / "validate_data_inventory.py"
        inventory = temp / "inventory.json"
        inventory.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "inventory_id": "test",
                    "owner": "security",
                    "updated_at": "2026-07-10T00:00:00Z",
                    "records": [
                        {
                            "id": "leads",
                            "name": "Lead fields",
                            "purpose": "Respond to inquiries",
                            "subjects": ["prospects"],
                            "fields": ["email", "company"],
                            "sensitivity": "personal",
                            "source": "contact form",
                            "locations": ["database"],
                            "access_roles": ["sales"],
                            "encryption": "documented separately",
                            "retention": "defined policy",
                            "deletion": "verified workflow",
                            "backup": "expires with schedule",
                            "incident_owner": "security",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        valid_inventory = run(inventory_script, "--input", str(inventory))
        assert json.loads(valid_inventory.stdout)["valid"] is True
        inventory.write_text(json.dumps({"schema_version": 1, "records": []}), encoding="utf-8")
        invalid_inventory = run(inventory_script, "--input", str(inventory), expected=1)
        assert json.loads(invalid_inventory.stdout)["valid"] is False

        assessment_script = ROOT / "skills" / "aiwf-security-guardrails" / "scripts" / "create_security_assessment.py"
        assessment = temp / "assessment.json"
        run(assessment_script, "--output", str(assessment), "--title", "Test", "--owner", "Shawn", "--scope", "Local fixture")
        assessment_data = json.loads(assessment.read_text(encoding="utf-8"))
        assert assessment_data["authorization"]["status"] == "unverified"
        run(assessment_script, "--output", str(assessment), "--title", "Test", "--owner", "Shawn", "--scope", "Local fixture", expected=2)

        incident_script = ROOT / "skills" / "aiwf-incident-response-recovery" / "scripts" / "create_incident_case.py"
        case_dir = temp / "incident"
        created = run(incident_script, "--output", str(case_dir), "--title", "Suspected key leak", "--owner", "Shawn")
        assert json.loads(created.stdout)["case_id"].startswith("IR-")
        assert (case_dir / "incident.json").exists()
        assert (case_dir / "timeline.jsonl").exists()
        run(incident_script, "--output", str(case_dir), "--title", "Duplicate", "--owner", "Shawn", expected=2)

    print("OK: runway, data inventory, security assessment, and incident helpers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
