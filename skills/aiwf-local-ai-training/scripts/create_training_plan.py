from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def build_plan(args: argparse.Namespace) -> dict:
    return {
        "schema_version": "aiwf-training-plan-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "objective": args.objective or "",
        "task": args.task,
        "model": {
            "base": args.model,
            "family": args.family or "",
            "license": "",
            "source_urls": [],
        },
        "method": args.method,
        "trainer": args.trainer or "",
        "dataset": {
            "path": args.dataset,
            "schema": "",
            "license_status": "unreviewed",
            "privacy_status": "unreviewed",
            "splits": {"train": "", "validation": "", "test": ""},
            "counts": {},
            "readiness": "pending",
        },
        "hardware": {
            "gpu": "",
            "vram_gb": args.vram_gb,
            "ram_gb": None,
            "disk_free_gb": None,
            "fit_status": "pending",
        },
        "training_config": {
            "precision": "",
            "quantization": "",
            "sequence_length": None,
            "resolution": "",
            "batch_size": None,
            "gradient_accumulation": None,
            "learning_rate": None,
            "epochs_or_steps": "",
        },
        "checkpoint_policy": {
            "output_dir": args.output_dir or "",
            "resume_from": "",
            "save_every": "",
            "retention": "",
            "non_overwrite": True,
        },
        "export_policy": {
            "adapter_only": True,
            "merged_export": False,
            "required_files": [],
        },
        "validation": {
            "config_parse": "pending",
            "tiny_dry_run": "not_requested",
            "adapter_load_smoke": "pending",
            "eval_plan": "pending",
        },
        "blockers": [],
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AIWF local training plan JSON skeleton.")
    parser.add_argument("--model", required=True, help="Base model id or local path.")
    parser.add_argument("--method", required=True, choices=["lora", "qlora", "full-finetune", "embedding", "dreambooth", "adapter", "other"])
    parser.add_argument("--dataset", required=True, help="Dataset path or id.")
    parser.add_argument("--out", required=True, help="Output plan JSON path.")
    parser.add_argument("--task", default="llm", choices=["llm", "image", "video", "multimodal", "dataset-only", "other"])
    parser.add_argument("--family", default="", help="Model family, such as llama, flux, sdxl, wan, qwen.")
    parser.add_argument("--trainer", default="", help="Preferred trainer, if already chosen.")
    parser.add_argument("--objective", default="", help="Short training objective.")
    parser.add_argument("--vram-gb", type=float, default=None, help="Available GPU VRAM in GB.")
    parser.add_argument("--output-dir", default="", help="Training output/checkpoint directory.")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_plan(args), indent=2) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
