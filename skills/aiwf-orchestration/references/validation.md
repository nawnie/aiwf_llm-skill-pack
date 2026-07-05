# Validation Routing

Use this reference for tests, smoke runs, preflight checks, and no-GUI validation.

## Stock Skills

- `local-ai-dev`: repo commands, venv, Windows execution, focused tests.
- `ml-training-recipes`: validation discipline for performance and precision changes.
- `avoid-ai-writing`: required whenever GitHub skills are used or non-gitignored files are written.
- Add domain skills only for the changed surface, such as `stable-diffusion-image-generation` for pipeline behavior or `hugging-face:huggingface-gradio` for Gradio.

## Preferred Commands

```powershell
venv\Scripts\python.exe scripts\smoke_models_and_pipelines.py
venv\Scripts\python.exe scripts\smoke_backend.py --video --list
venv\Scripts\python.exe -m pytest tests\individual_tests\test_pipeline_preflight.py tests\individual_tests\test_pipeline_registry.py -q
```

## Targeted Test Map

- Pipeline registry/preflight: `tests\individual_tests\test_pipeline_preflight.py`, `tests\individual_tests\test_pipeline_registry.py`
- Wan: `tests\individual_tests\test_wan*.py`
- LTX: `tests\individual_tests\test_ltx.py`, `tests\individual_tests\test_worker_tenant.py`
- Model downloads/catalog: `tests\individual_tests\test_model_download.py`
- React/API: choose tests near `frontend` or `aiwf/web/pro_api.py`
- Chat/training: prefer dry-run, import, route, API, or worker probe tests before long execution.

## Guardrails

- Prefer narrow tests first, then broaden only when shared behavior changed.
- Use list/preflight/dry-run/probe modes when GPU generation or training is not required.
- For any changed path whose ignored status is unclear, run `git check-ignore -q -- <path>`. If it is not ignored, audit new or edited prose with `avoid-ai-writing` before finalizing.
- For GitHub skill work, audit PR text, comments, reviews, commit messages, release notes, and issue text with `avoid-ai-writing`.
- Report skipped or unrun tests honestly.
