from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def build_plan(args: argparse.Namespace) -> dict:
    return {
        "schema_version": "aiwf-serving-plan-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runtime": args.runtime,
        "model": args.model,
        "network": {
            "host": args.host,
            "port": args.port,
            "public_exposure": False,
            "auth_required": True,
        },
        "launch": {
            "command": "",
            "working_dir": "",
            "env_file": "",
            "log_path": "",
        },
        "api_contract": {
            "health": "",
            "models": "",
            "chat_completions": "",
            "completions": "",
            "streaming": "unknown",
            "openai_compatible": "unknown",
        },
        "operations": {
            "startup": "pending",
            "shutdown": "pending",
            "reload": "unknown",
            "unload": "unknown",
            "queueing": "unknown",
            "cancellation": "unknown",
            "telemetry": "unknown",
        },
        "smoke": {
            "health_probe": "pending",
            "model_list": "pending",
            "tiny_prompt": "pending",
            "bad_request_error_shape": "pending",
        },
        "stability": {
            "latency_probe": "not_requested",
            "load_loop": "not_requested",
            "resource_trace": "not_requested",
        },
        "blockers": [],
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AIWF inference serving plan JSON skeleton.")
    parser.add_argument("--runtime", required=True, choices=["vllm", "llama.cpp", "ollama", "fastapi", "gradio", "transformers", "diffusers", "other"])
    parser.add_argument("--model", required=True, help="Model id or local model path.")
    parser.add_argument("--out", required=True, help="Output plan JSON path.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host.")
    parser.add_argument("--port", type=int, default=8000, help="Port.")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_plan(args), indent=2) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
