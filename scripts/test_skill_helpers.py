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

        convergence_script = ROOT / "skills" / "aiwf-qa-convergence" / "scripts" / "qa_convergence.py"
        qa_root = temp / "qa-project"
        source_dir = qa_root / "src"
        source_dir.mkdir(parents=True)
        source_file = source_dir / "app.py"
        source_file.write_text("print('ready')\n", encoding="utf-8")
        manifest = qa_root / "qa-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "target": "fixture",
                    "source_paths": ["src"],
                    "required_gates": [{"name": "unit", "command": "pytest"}],
                    "runtime_flows": ["launch"],
                }
            ),
            encoding="utf-8",
        )
        clean_report = qa_root / "clean-report.json"
        clean_report.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "lens": "unit",
                    "progress": True,
                    "gates": [{"name": "unit", "passed": True, "evidence": "unit.txt"}],
                    "findings": [],
                    "attempted_fixes": [],
                }
            ),
            encoding="utf-8",
        )
        clean_state = qa_root / "clean-state.json"
        run(
            convergence_script,
            "init",
            "--root",
            str(qa_root),
            "--manifest",
            str(manifest),
            "--state",
            str(clean_state),
        )
        run(convergence_script, "record", "--state", str(clean_state), "--report", str(clean_report))
        source_file.write_text("print('changed')\n", encoding="utf-8")
        reset_result = run(
            convergence_script,
            "record",
            "--state",
            str(clean_state),
            "--report",
            str(clean_report),
        )
        assert json.loads(reset_result.stdout)["clean_streak"] == 1
        clean_result = run(
            convergence_script,
            "record",
            "--state",
            str(clean_state),
            "--report",
            str(clean_report),
        )
        assert json.loads(clean_result.stdout)["status"] == "CLEAN"

        minor_report = qa_root / "minor-report.json"
        minor_report.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "lens": "runtime",
                    "progress": False,
                    "gates": [{"name": "smoke", "passed": True, "evidence": "smoke.png"}],
                    "findings": [
                        {
                            "fingerprint": "git:line-ending:app.py",
                            "severity": "info",
                            "status": "accepted",
                            "reason": "No build or runtime impact.",
                        }
                    ],
                    "attempted_fixes": [],
                }
            ),
            encoding="utf-8",
        )
        minor_state = qa_root / "minor-state.json"
        run(
            convergence_script,
            "init",
            "--root",
            str(qa_root),
            "--manifest",
            str(manifest),
            "--state",
            str(minor_state),
        )
        for _ in range(2):
            result = run(
                convergence_script,
                "record",
                "--state",
                str(minor_state),
                "--report",
                str(minor_report),
            )
            assert json.loads(result.stdout)["status"] == "IN_PROGRESS"
        accepted_result = run(
            convergence_script,
            "record",
            "--state",
            str(minor_state),
            "--report",
            str(minor_report),
        )
        assert json.loads(accepted_result.stdout)["status"] == "ACCEPTABLE_WITH_MINOR"

        blocking_report = qa_root / "blocking-report.json"
        blocking_report.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "lens": "runtime",
                    "progress": False,
                    "gates": [{"name": "smoke", "passed": False, "evidence": "failure.txt"}],
                    "findings": [
                        {
                            "fingerprint": "runtime:crash:launch",
                            "severity": "high",
                            "status": "open",
                        }
                    ],
                    "attempted_fixes": [],
                }
            ),
            encoding="utf-8",
        )
        stalled_state = qa_root / "stalled-state.json"
        run(
            convergence_script,
            "init",
            "--root",
            str(qa_root),
            "--manifest",
            str(manifest),
            "--state",
            str(stalled_state),
        )
        run(convergence_script, "record", "--state", str(stalled_state), "--report", str(blocking_report))
        stalled_result = run(
            convergence_script,
            "record",
            "--state",
            str(stalled_state),
            "--report",
            str(blocking_report),
        )
        assert json.loads(stalled_result.stdout)["status"] == "STALLED"

        escalation_data = json.loads(blocking_report.read_text(encoding="utf-8"))
        escalation_data["progress"] = True
        escalation_data["attempted_fixes"] = ["runtime:crash:launch"]
        escalation_report = qa_root / "escalation-report.json"
        escalation_report.write_text(json.dumps(escalation_data), encoding="utf-8")
        escalation_state = qa_root / "escalation-state.json"
        run(
            convergence_script,
            "init",
            "--root",
            str(qa_root),
            "--manifest",
            str(manifest),
            "--state",
            str(escalation_state),
        )
        for _ in range(2):
            result = run(
                convergence_script,
                "record",
                "--state",
                str(escalation_state),
                "--report",
                str(escalation_report),
            )
            assert json.loads(result.stdout)["status"] == "IN_PROGRESS"
        escalation_result = run(
            convergence_script,
            "record",
            "--state",
            str(escalation_state),
            "--report",
            str(escalation_report),
        )
        assert json.loads(escalation_result.stdout)["status"] == "ESCALATE"

        budget_state = qa_root / "budget-state.json"
        run(
            convergence_script,
            "init",
            "--root",
            str(qa_root),
            "--manifest",
            str(manifest),
            "--state",
            str(budget_state),
            "--max-cycles",
            "1",
        )
        budget_result = run(
            convergence_script,
            "record",
            "--state",
            str(budget_state),
            "--report",
            str(escalation_report),
        )
        assert json.loads(budget_result.stdout)["status"] == "BUDGET_EXHAUSTED"

    print("OK: runway, data inventory, security assessment, incident, and QA convergence helpers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
