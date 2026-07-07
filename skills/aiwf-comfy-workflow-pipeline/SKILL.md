---
name: aiwf-comfy-workflow-pipeline
description: Convert ComfyUI workflow JSON, API-format prompts, node graphs, or saved workflows into source-backed Python pipeline plans, conversion reports, and executable skeletons for AIWF Studio or local ComfyUI API work. Use when Shawn asks to translate ComfyUI workflows or custom-node graphs into Python, inspect ComfyUI nodes, map workflow inputs, identify missing custom nodes, produce an AIWF pipeline implementation plan, or generate a safe Python wrapper/skeleton without running GPU generation.
---

# AIWF Comfy Workflow Pipeline

## Overview

Use this skill to turn a ComfyUI graph into a practical Python implementation path. Default to analysis, skeletons, and gap ledgers first; do not claim a complete native AIWF pipeline conversion unless each node has a verified Python equivalent.

## Core Workflow

1. Identify the workflow format.
   - API prompt format: a dict keyed by node id, each node containing `class_type` and `inputs`.
   - Wrapped prompt format: a dict with a top-level `prompt` field containing the API prompt.
   - UI save format: a dict with `nodes`, `links`, layout, groups, or `widgets_values`.
2. Prefer API format for execution-facing conversion. If the user provides UI save format, either ask for `File -> Export Workflow (API)` or run a best-effort conversion and mark unresolved widget mappings.
3. Gather node metadata when possible.
   - Use a live ComfyUI `/object_info` export when the server is available.
   - Use the local workflow only when the server is unavailable, and label custom-node confidence as partial.
4. Run the helper script for deterministic inventory and skeleton generation:

```powershell
python "C:\Users\Shawn\.codex\skills\aiwf-comfy-workflow-pipeline\scripts\comfy_workflow_to_pipeline.py" "path\workflow_api.json" --output-dir "path\out"
```

With node definitions:

```powershell
python "C:\Users\Shawn\.codex\skills\aiwf-comfy-workflow-pipeline\scripts\comfy_workflow_to_pipeline.py" "path\workflow.json" --object-info "path\object_info.json" --output-dir "path\out"
```

5. Read the generated `conversion_report.md`, `workflow_analysis.json`, and `pipeline_skeleton.py`.
6. Implement native AIWF code only after the report separates:
   - directly mappable nodes,
   - API-wrapper-only nodes,
   - custom nodes needing source inspection,
   - model/file prerequisites,
   - dynamic or UI-only nodes that cannot be converted safely.

## Implementation Rules

- Keep conversion deterministic and read-only until Shawn explicitly asks to run generation.
- Do not download models, start training, or run VRAM-heavy workflows.
- Treat ComfyUI custom nodes as Python packages that may have side effects. Inspect source and metadata before importing them.
- Prefer a ComfyUI API wrapper for unknown or large custom-node workflows; prefer native AIWF implementation only for known node families with existing AIWF engines.
- Preserve node ids and class names in generated skeletons so validation errors from ComfyUI remain traceable.
- For missing nodes, report the `class_type`, node id, title, and upstream/downstream edges instead of guessing behavior.
- For UI save format, do not pretend visual layout fields are executable pipeline data.

## AIWF Mapping Heuristics

Use these as first-pass labels, not final implementation proof:

- `CheckpointLoaderSimple`, `UNETLoader`, `CLIPLoader`, `DualCLIPLoader`, `VAELoader`: model loading.
- `CLIPTextEncode`: prompt or conditioning.
- `EmptyLatentImage`, `LoadImage`, `LoadImageMask`: input or latent source.
- `KSampler`, `KSamplerAdvanced`: diffusion sampling.
- `VAEDecode`, `VAEDecodeTiled`: decode.
- `LoraLoader`, `LoraLoaderModelOnly`: LoRA application.
- `ControlNetLoader`, `ControlNetApply`, `ControlNetApplyAdvanced`: ControlNet branch.
- `SaveImage`, `PreviewImage`, `SaveImageWebsocket`: output sink.

If the workflow includes video, GGUF, VLM, audio, masking, face, or custom loader nodes, route into the relevant AIWF skill after this analysis.

## References

Read `references/conversion-policy.md` when deciding whether to generate an API wrapper, a native AIWF plan, or a mixed adapter plan.
