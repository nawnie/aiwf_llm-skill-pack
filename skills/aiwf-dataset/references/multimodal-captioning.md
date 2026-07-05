# Multimodal Captioning

Use this reference for image, video, audio, and caption datasets.

## Asset inventory

For every asset, record:

- `asset_id`
- `path_or_uri`
- `media_type`
- `source_id`
- `license`
- `hash`
- `width`
- `height`
- `duration_seconds`
- `fps`
- `codec`
- `captured_at`
- `validation_status`

Use standard metadata tools first. Use `ffprobe` for video/audio when available, image libraries for dimensions and hashes, and JSONL manifests for cross-file joins.

## Caption fields

Keep caption sources separate:

- `source_caption`: caption provided by the source or dataset.
- `model_caption`: generated caption.
- `verified_caption`: human-reviewed or source-verified caption.
- `caption_model`
- `caption_prompt_hash`
- `caption_confidence`
- `caption_reviewer`
- `caption_status`

Never overwrite source captions with model captions. If captions are regenerated, write a new field or new manifest version.

## Image workflow

1. Check file readability, dimensions, hash, license, and duplicates.
2. Use CLIP for image-text similarity and broad caption consistency checks.
3. Use SAM when masks, crops, objects, or segmentation-derived labels are needed.
4. Run NSFW and privacy checks for scraped, personal, or public-web images.
5. Record whether a caption is generated, source-provided, or verified.

## Video workflow

1. Extract metadata and reject corrupt files.
2. Segment scenes or clips with start/end timestamps.
3. Use Whisper for speech transcripts when audio is meaningful.
4. Caption clips, not only whole videos, unless the model target needs whole-video context.
5. Store parent video ID, clip ID, start/end, duration, transcript span, caption source, and verification status.

## Audio workflow

1. Extract duration, sample rate, channels, and codec.
2. Use Whisper or NeMo ASR for transcripts.
3. Keep raw transcript, normalized transcript, and verified transcript separate.
4. Filter by duration, language, WER when reference text exists, and audio quality.

## Generated media

Generated images, video, audio, and captions can be useful for guardrail, robustness, or annotation bootstrapping datasets. Mark them as synthetic and keep generator metadata:

- model or tool name,
- model version or checkpoint,
- prompt hash,
- seed when available,
- generation date,
- review status,
- intended training use.

Do not treat generated media as evidence for factual claims about the world.
