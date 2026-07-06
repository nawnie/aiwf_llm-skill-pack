from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def run_command(args: list[str]) -> dict[str, Any]:
    executable = shutil.which(args[0])
    if not executable:
        return {"available": False, "command": args, "returncode": None, "stdout": "", "stderr": "not found"}
    try:
        proc = subprocess.run(
            [executable, *args[1:]],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
        return {
            "available": True,
            "command": [executable, *args[1:]],
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"available": True, "command": args, "returncode": None, "stdout": "", "stderr": str(exc)}


def torch_probe() -> dict[str, Any]:
    try:
        import torch  # type: ignore
    except Exception as exc:
        return {"imported": False, "error": repr(exc)}

    result: dict[str, Any] = {
        "imported": True,
        "version": getattr(torch, "__version__", None),
        "cuda_version": getattr(getattr(torch, "version", None), "cuda", None),
        "cuda_available": False,
        "device_count": 0,
        "devices": [],
    }
    try:
        result["cuda_available"] = bool(torch.cuda.is_available())
        result["device_count"] = int(torch.cuda.device_count()) if result["cuda_available"] else int(torch.cuda.device_count())
        devices = []
        for index in range(result["device_count"]):
            devices.append(
                {
                    "index": index,
                    "name": torch.cuda.get_device_name(index),
                    "capability": list(torch.cuda.get_device_capability(index)),
                    "memory_total": torch.cuda.get_device_properties(index).total_memory,
                }
            )
        result["devices"] = devices
    except Exception as exc:
        result["cuda_probe_error"] = repr(exc)
    return result


def optional_module(name: str) -> dict[str, Any]:
    try:
        module = __import__(name)
        return {"imported": True, "version": getattr(module, "__version__", None)}
    except Exception as exc:
        return {"imported": False, "error": repr(exc)}


def collect() -> dict[str, Any]:
    return {
        "schema": "aiwf.gpu_runtime_snapshot.v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "python": {
            "executable": sys.executable,
            "version": sys.version,
            "platform": platform.platform(),
        },
        "commands": {
            "nvidia_smi": run_command(["nvidia-smi"]),
            "nvcc": run_command(["nvcc", "--version"]),
            "rocm_smi": run_command(["rocm-smi"]),
        },
        "python_packages": {
            "torch": torch_probe(),
            "torchvision": optional_module("torchvision"),
            "xformers": optional_module("xformers"),
            "tensorrt": optional_module("tensorrt"),
            "bitsandbytes": optional_module("bitsandbytes"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect a read-only GPU runtime snapshot.")
    parser.add_argument("--out", help="Optional JSON output path.")
    args = parser.parse_args()
    payload = collect()
    text = json.dumps(payload, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
