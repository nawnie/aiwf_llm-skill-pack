#!/usr/bin/env python3
"""Create a starter aiwf-model-loader contract JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def build_contract(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "model_id": args.model_id,
        "local_path": args.local_path or "",
        "family": args.family,
        "format": args.format,
        "architecture": "",
        "source_urls": args.source_url or [],
        "asset_layout": {
            "required_files": [],
            "optional_files": [],
            "components": {
                "base": "",
                "vae": "",
                "text_encoder": "",
                "tokenizer": "",
                "projector": "",
                "adapters": [],
            },
        },
        "backend": {
            "selected": args.backend,
            "allowed": [],
            "forbidden": [],
            "reason": "",
        },
        "precision_policy": {
            "default": "",
            "components": {
                "base": "",
                "vae": "",
                "text_encoder": "",
                "prompt_encoding_device": "",
            },
            "offload": "",
            "unsupported": [],
        },
        "quantization_policy": {
            "format": "",
            "minimum_viable": "",
            "preferred_quality": "",
            "requires_calibration_or_imatrix": False,
            "backend_support": "",
        },
        "lora_policy": {
            "supported": False,
            "compatible_bases": [],
            "adapter_formats": [],
            "target_modules": [],
            "scale_range": "",
            "trigger_words": [],
            "fuse_unload_behavior": "",
            "rejection_rules": [],
        },
        "preflight": {
            "checks": [],
            "blocked_reasons": [],
            "warnings": [],
        },
        "fallbacks": {
            "allowed": [],
            "forbidden": [],
        },
        "tests": {
            "no_gpu": [],
            "loader_smoke": [],
            "full_generation_optional": [],
        },
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-id", required=True, help="Model id, display name, or local path label.")
    parser.add_argument("--family", required=True, help="Model family, for example sana, flux, wan, qwen, llama.")
    parser.add_argument("--backend", required=True, help="Selected backend, for example native, diffusers, llama.cpp.")
    parser.add_argument("--format", required=True, help="Artifact format, for example safetensors, gguf, diffusers.")
    parser.add_argument("--local-path", help="Optional local model path.")
    parser.add_argument("--source-url", action="append", help="Source URL. May be repeated.")
    parser.add_argument("--out", help="Output JSON path. Defaults to stdout.")
    args = parser.parse_args()

    payload = json.dumps(build_contract(args), indent=2, sort_keys=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
        print(out)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
