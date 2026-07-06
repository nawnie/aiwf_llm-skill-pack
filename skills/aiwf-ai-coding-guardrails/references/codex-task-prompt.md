# Codex task prompt template

Use this when starting Codex on a real repo.

```text
Use the installed guardrail skills before editing:
- aiwf-ai-coding-guardrails
- aiwf-repo-sentinel
- aiwf-web-api-ui-guardian, if FastAPI/Gradio/React/TS/JS/CSS/HTML is touched
- aiwf-python-cpp-hardener, if Python/C++/CMake is touched

Task:
<describe the issue or feature>

Constraints:
- Make the smallest repo-native patch.
- Do not create duplicate apps, routers, clients, components, or backup files.
- Do not switch package managers.
- Do not perform major dependency upgrades unless explicitly required.
- Do not delete, skip, or weaken tests to pass.
- Prefer PowerShell-safe commands for Windows instructions.
- Run relevant checks and report exact command results.

Before editing, report the detected package manager, runtime versions, framework versions, and validation commands you plan to use.
```
```
