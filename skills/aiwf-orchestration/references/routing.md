# AIWF Routing Index

Use this file first, then load only the focused reference files that match the user's prompt.

## Reference Files

| Prompt signal | Load |
| --- | --- |
| Flux, SDXL, Qwen Image, Sana, Z-Image, Klein, image generation pipelines | [image-pipelines.md](image-pipelines.md) |
| Wan, LTX, video generation, I2V, VAE channel checks, video workers | [video-pipelines.md](video-pipelines.md) |
| Audio generation, MusicGen, AudioGen, EnCodec, text-to-music, text-to-sound | `audiocraft-audio-generation`; add `hugging-face:hf-cli` for model downloads and `hugging-face:huggingface-gradio` for Gradio wiring |
| Speech recognition, audio input, transcription | `whisper`; add `hugging-face:hf-cli` for model downloads |
| Masks, segmentation, captioning, image-text search, VLM chat | `segment-anything-model`, `clip`, `blip-2-vision-language`, `llava`; add image or chat references only when the task crosses those lanes |
| Hugging Face, download, checkpoint list, model catalog, safetensors/GGUF placement | [model-assets-downloads.md](model-assets-downloads.md) |
| Deep research, source weighting, literature review, claim ledger, arXiv, Civitai, Reddit limits, open-source library checks, academic sources, college, graduate, postgraduate, thesis, dissertation, quantum physics, robotics, mechanical engineering | `aiwf-deep-research` |
| FlashAttention, SDPA, xFormers, GGUF, bitsandbytes, NF4, FP8, speed, VRAM | [quantization-optimization.md](quantization-optimization.md) |
| Gradio, React, tabs, frontend, UI defaults, API wiring | [ui-routing.md](ui-routing.md) |
| AI-looking design, teal everywhere, generic generated UI, de-slop UI, default Gradio/shadcn styling, AI-looking PDF reports, document layout cleanup, web page design tells | `aiwf-avoid-ai-design` plus [ui-routing.md](ui-routing.md) when code changes may follow |
| User pain, UX friction, onboarding issues, docs/help problems, support pain, current complaints for a named product | `product-design:research` plus [ui-routing.md](ui-routing.md) when UI changes may follow |
| Smoke tests, preflight, model validation, pipeline registry, backend list mode | [validation.md](validation.md) |
| AI chat code, RAG, chat memory, LLM APIs, LLM serving, fine-tuning, training engines | [chat-training-serving.md](chat-training-serving.md) |
| GitHub skills, PR/issue text, commit/release notes, docs, README, non-gitignored repo file edits | `aiwf-avoid-ai-pushes` plus the relevant focused reference |

## Base Stock Skills

Always prefer the smallest useful set:

- General local AIWF code/runtime work: `local-ai-dev`
- Diffusers model or pipeline implementation: `stable-diffusion-image-generation`
- Audio generation: `audiocraft-audio-generation`
- Speech/audio input: `whisper`
- Vision helper pipelines: `segment-anything-model`, `clip`, `blip-2-vision-language`, `llava`
- Hugging Face model operations: `hugging-face:hf-cli`
- Source-backed deep research: `aiwf-deep-research`
- Gradio only: `hugging-face:huggingface-gradio`
- React only: `build-web-apps:react-best-practices`
- AI-looking UI, Gradio, React, web, PDF, document, or dashboard design cleanup: `aiwf-avoid-ai-design`
- Product UX research: `product-design:research`
- GGUF routes: `gguf-quantization`
- bitsandbytes/NF4/INT8 routes: `quantizing-models-bitsandbytes`
- LLM AWQ/GPTQ/HQQ routes: `awq-quantization`, `gptq`, `hqq-quantization`
- Attention/perf work: `optimizing-attention-flash`, `ml-training-recipes`
- AI chat/RAG work: `langchain`, `llamaindex`, `sentence-transformers`, `faiss`, `qdrant-vector-search`, `chroma`
- LLM prompt/programming helpers: `instructor`, `outlines`, `guidance`, `dspy`
- LLM serving: `llama-cpp`, `serving-llms-vllm`
- AI training/fine-tuning: `peft-fine-tuning`, `fine-tuning-with-trl`, `axolotl`, `llama-factory`, `unsloth`, `huggingface-accelerate`
- GitHub-facing or non-gitignored file writing: `aiwf-avoid-ai-pushes`

## GitHub And Non-Ignored File Guard

Select `aiwf-avoid-ai-pushes` whenever any GitHub skill is selected or a task writes public prose to a file that is not ignored by `.gitignore`.

Use `git check-ignore -q -- <path>` when status is unclear:

- exit code 0: ignored, route through `aiwf-avoid-ai-pushes` only if the content is still public-facing prose.
- non-zero: not ignored, route through `aiwf-avoid-ai-pushes` for new or edited prose.

For code files, audit only prose-bearing spans such as comments, docstrings, UI copy, prompt templates, generated messages, markdown, and docs.

## Selection Rule

If the prompt spans several areas, load the minimum matching references. For example, "download Wan GGUF and add preflight" means load model assets, quantization, video pipelines, and validation. It does not need UI routing unless the user asks for Gradio or React.
