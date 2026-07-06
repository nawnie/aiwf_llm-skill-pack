# Training readiness

Use this checklist before recommending a launch command.

## Dataset gate

- Source and license are recorded.
- Private or sensitive rows are excluded or explicitly allowed by Shawn.
- Format matches the trainer: chat JSONL, completion JSONL, image-caption pairs, video-caption pairs, or project-local schema.
- Train, validation, and optional test splits exist or are deliberately skipped with a reason.
- Duplicate rows, near-duplicate images, and eval contamination have been checked when practical.
- Sample count, token count, image count, or video duration is enough for the objective.

## Model gate

- Base model path, architecture, tokenizer, and license are known.
- Adapter target modules or image model family are known.
- Quantization and dtype match the intended trainer.
- Required sidecars are present: tokenizer, config, VAE, text encoder, scheduler, projector, or model index.

## Hardware gate

- GPU model and VRAM are known.
- RAM and disk budget fit the dataset, cache, checkpoints, and exports.
- Batch size, sequence length, resolution, frame count, and gradient accumulation are explicit.
- Low-VRAM paths are named: QLoRA, gradient checkpointing, CPU offload, 8-bit optimizer, smaller context, smaller resolution, or adapter-only training.

## Trainer gate

- Trainer choice is tied to the model family and dataset shape.
- Resume behavior is defined before the run starts.
- Output folder is unique and non-overwriting.
- Checkpoint cadence, retention, and final export are explicit.
- Logs capture command, config, git state when available, GPU, and package versions.

## Post-training gate

- Adapter load smoke is planned.
- Eval suite or prompt suite is planned.
- Baseline comparison is named.
- Export includes adapter, config, tokenizer or metadata, and a receipt.
