# Research Source Map

This pack was built from two research passes focused on common AI coding mistakes and real coding-agent failure modes.

## Main failure categories captured

- Version drift
- Package-manager drift
- Shell/OS mistakes, especially Windows and PowerShell
- Repo duplication and parallel architecture
- Test cheating and fake-green behavior
- Frontend/backend contract drift
- FastAPI/Pydantic migration traps
- Gradio root-path/proxy/SSR traps
- React/Vite/TypeScript build and runtime traps
- Python async, typing, serialization, and environment mistakes
- C++/CMake generator, compiler, ABI, and memory-safety mistakes
- Unsafe repo setup scripts and over-broad credentials
- UI/UX failures from AI-generated React/CSS/HTML

## Representative sources used during research

Official docs and project docs:

- FastAPI migration and client generation docs
- Pydantic migration docs
- Gradio Blocks and mount docs
- Vite guide and release notes
- React 19 upgrade guide
- Node ESM docs
- TypeScript module docs
- npm scripts and npm ci docs
- pnpm install/deploy docs
- Yarn install docs
- PowerShell execution policy docs
- Python venv, pickle, distutils/PEP 632 docs
- SQLAlchemy 2.0 migration docs
- CMake presets and ctest docs
- clang/clang-tidy docs
- cppcheck docs
- Ruff and Pyright docs
- Testing Library, Playwright, Vitest, Lighthouse docs

Community and issue evidence:

- Reddit developer complaints about AI coding assistants producing almost-right code, poor tests, and missing repo context
- GitHub issues for Vite Node/version failures
- GitHub issues for Gradio proxy/root_path/SSR problems
- Stack Overflow CMake compiler and Ninja setup failures
- npm CLI and node-gyp issue reports
- Public reporting and security research on coding-agent overreach and repo setup risks

## Design translation

The source evidence was converted into four skill surfaces:

1. `aiwf-ai-coding-guardrails`: master behavior contract.
2. `aiwf-repo-sentinel`: repo preflight, diff discipline, package-manager discipline, test integrity.
3. `aiwf-web-api-ui-guardian`: FastAPI/Gradio/React/TS/JS/HTML/CSS and API contract protection.
4. `aiwf-python-cpp-hardener`: Python/C++/CMake safety and validation.

## Practical principle

The pack assumes AI coding failures usually come from insufficient repository truth, not lack of code syntax knowledge.

So the skills force Codex to:

```text
probe → patch narrowly → prove with command output
```
