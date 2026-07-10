from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills" / "aiwf-multi-agent-workspace" / "scripts" / "agent_workspace.py"


def run(env: dict[str, str], *args: str, input_text: str | None = None, expected: int = 0) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        input=input_text,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expected}: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    if expected != 0:
        return {"stderr": result.stderr}
    return json.loads(result.stdout)


def main() -> int:
    temp = Path(tempfile.mkdtemp(prefix="aiwf-agent-workspace-test-"))
    try:
        profile = temp / "profile"
        project = temp / "project"
        workspace = temp / "workspace"
        profile.mkdir()
        project.mkdir()
        env = os.environ.copy()
        env["USERPROFILE"] = str(profile)
        env["HOME"] = str(profile)

        first = run(env, "init", "--path", str(workspace), "--skip-acl")
        second = run(env, "init", "--path", str(workspace), "--skip-acl")
        assert first["workspace"] == second["workspace"] == str(workspace.resolve())

        registered = run(env, "project", "ensure", "--path", str(project))
        repeated = run(env, "project", "ensure", "--path", str(project))
        assert registered["project_id"] == repeated["project_id"]
        project_id = registered["project_id"]

        codex = run(env, "session", "start", "--project", project_id, "--provider", "codex", "--pid", str(os.getpid()))
        claude = run(env, "session", "start", "--project", project_id, "--provider", "claude", "--pid", str(os.getpid()))

        for index in range(7):
            user = f"Visible user request {index}"
            if index == 0:
                user += " " + "api_" + "key=" + "test-redaction-value-12345"
            begun = run(env, "turn", "begin", "--session", codex["session_id"], "--stdin", input_text=user)
            run(
                env,
                "turn",
                "finish",
                "--session",
                codex["session_id"],
                "--turn",
                begun["turn_id"],
                "--stdin",
                input_text=f"Visible assistant response {index}",
            )
        pending = run(env, "turn", "begin", "--session", codex["session_id"], "--stdin", input_text="Pending visible request")
        recent_path = workspace / "projects" / project_id / "conversation" / "recent.jsonl"
        recent = [json.loads(line) for line in recent_path.read_text(encoding="utf-8").splitlines() if line]
        assert len([row for row in recent if row["status"] == "complete"]) == 6
        assert any(row["turn_id"] == pending["turn_id"] and row["status"] == "pending" for row in recent)
        assert "test-redaction-value-12345" not in recent_path.read_text(encoding="utf-8")

        writer = run(env, "lease", "acquire", "--session", codex["session_id"], "--kind", "repo-write")
        conflict = run(env, "lease", "acquire", "--session", claude["session_id"], "--kind", "path-write", "--resource", str(project), expected=2)
        assert "conflicts" in conflict["stderr"]
        run(env, "lease", "release", "--session", codex["session_id"], "--lease", writer["lease_id"])
        claude_writer = run(env, "lease", "acquire", "--session", claude["session_id"], "--kind", "repo-write")
        run(env, "lease", "release", "--session", claude["session_id"], "--lease", claude_writer["lease_id"])

        resources = run(env, "resource", "status")
        over_cpu = resources["logical_cpus"] - resources["cpu_reserve"] + 1
        run(env, "lease", "acquire", "--session", codex["session_id"], "--kind", "cpu", "--amount", str(over_cpu), expected=2)
        if resources["gpus"]:
            gpu = run(env, "lease", "acquire", "--session", codex["session_id"], "--kind", "gpu", "--resource", "gpu:0")
            run(env, "lease", "acquire", "--session", claude["session_id"], "--kind", "gpu", "--resource", "gpu:0", expected=2)
            run(env, "lease", "release", "--session", codex["session_id"], "--lease", gpu["lease_id"])

        dead = run(env, "session", "start", "--project", project_id, "--provider", "test", "--pid", "999999")
        stale = run(env, "lease", "acquire", "--session", dead["session_id"], "--kind", "port", "--resource", "tcp:54321")
        lease_path = workspace / "leases" / "index.json"
        lease_index = json.loads(lease_path.read_text(encoding="utf-8"))
        old = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
        for lease in lease_index["leases"]:
            if lease["lease_id"] == stale["lease_id"]:
                lease["heartbeat_at"] = old
        lease_path.write_text(json.dumps(lease_index, indent=2) + "\n", encoding="utf-8")
        status = run(env, "lease", "status")
        assert stale["lease_id"] in status["reclaimed"]

        validated = run(env, "validate")
        assert validated["valid"] is True
        run(env, "session", "end", "--session", codex["session_id"])
        run(env, "session", "end", "--session", claude["session_id"])
        run(env, "session", "end", "--session", dead["session_id"])

        if os.name == "nt":
            acl_profile = temp / "acl-profile"
            acl_workspace = temp / "acl-workspace"
            acl_profile.mkdir()
            acl_env = env.copy()
            acl_env["USERPROFILE"] = str(acl_profile)
            acl_result = run(acl_env, "init", "--path", str(acl_workspace))
            assert acl_result["workspace"] == str(acl_workspace.resolve())
            acl_validation = run(acl_env, "validate")
            assert acl_validation["valid"] is True
            shutil.rmtree(acl_workspace)

        print("OK: shared agent workspace context, leases, resources, recovery, and ACLs")
        return 0
    finally:
        shutil.rmtree(temp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
