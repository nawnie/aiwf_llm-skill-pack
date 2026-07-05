# AI Chat, Training, And Serving Routing

Use this reference for local LLM chat app code, RAG, chat memory, tool calling, prompt-programmed outputs, LLM serving, and AI training/fine-tuning work.

## Stock Skills For AI Chat Code

- `local-ai-dev`: local app structure, venv, APIs, process/runtime behavior.
- `langchain`: chains, agents, tools, chat orchestration.
- `llamaindex`: RAG indexes, document ingestion, retrieval workflows.
- `sentence-transformers`: local embeddings.
- `faiss`, `qdrant-vector-search`, `chroma`: vector stores.
- `instructor`, `outlines`, `guidance`, `dspy`: structured outputs, prompt programs, evaluation/prototyping.
- `huggingface-tokenizers`: tokenizer behavior and local tokenizer assets.

## Stock Skills For Serving

- `llama-cpp`: GGUF LLM serving and llama.cpp-style local routes.
- `serving-llms-vllm`: vLLM OpenAI-compatible serving.
- `local-ai-dev`: Windows process wiring, ports, launchers, health checks.

## Stock Skills For AI Training

- `peft-fine-tuning`: LoRA/adapter fine-tuning.
- `fine-tuning-with-trl`: SFT, preference tuning, reward/post-training workflows.
- `axolotl`, `llama-factory`, `unsloth`: local/open-source LLM fine-tuning recipes.
- `huggingface-accelerate`, `deepspeed`, `pytorch-fsdp2`: distributed or memory-constrained training.
- `ml-training-recipes`: recipe sanity, precision, batch size, eval, and reproducibility.

## AIWF Cues

- "Build chat", "LLM chat", "conversation memory", "RAG", "tools", "assistant API": load this file and the chat skills above.
- "Serve model", "OpenAI compatible endpoint", "local chat server", "GGUF chat": add `llama-cpp` or `serving-llms-vllm`.
- "Train", "fine-tune", "LoRA", "SFT", "DPO", "post-train": add training skills and inspect engine boundaries before running anything long.

## Guardrails

- Do not start long training jobs unless explicitly requested.
- Do not overwrite datasets, adapters, or model outputs without explicit instruction.
- Prefer dry-run, import checks, tokenizer checks, API route tests, and worker probes before full training/serving runs.
- Keep chat app memory and dataset generation separate unless the user explicitly asks to connect them.
