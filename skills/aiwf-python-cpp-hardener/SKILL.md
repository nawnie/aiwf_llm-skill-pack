---
name: aiwf-python-cpp-hardener
description: AIWF Python, C++, and CMake hardening guardrail. Use for Python, C++, and CMake tasks to prevent environment drift, unsafe serialization, async blocking, typing shortcuts, compiler/generator assumptions, memory-safety mistakes, untested C++ changes, and brittle cross-platform commands.
---

# AIWF Python C++ Hardener

## Mission

Make Python and C++ changes boring, testable, and repo-native.

Prefer boring, testable, repo-native code over clever rewrites.

Read `references/windows-powershell-commands.md` for Windows-safe command examples. Read `references/source-map.md` only when source provenance for these guardrails matters.

---

## Python guardrails

### Environment discovery

Before editing Python code, inspect:

```text
Python version
pyproject.toml
requirements*.txt
setup.py
poetry.lock
uv.lock
Pipfile.lock
pytest.ini
ruff.toml
pyrightconfig.json
mypy.ini
Dockerfile
CI Python version
```

Do not assume Python 3.11+ or 3.12+ features if repo targets 3.10.

### Dependency rules

- Do not add dependencies without checking existing dependency style.
- Do not mix pip, Poetry, uv, and Pipenv lock strategies.
- Do not update broad dependency ranges as a side effect.
- Do not remove pins to make install work.

### Type safety rules

Avoid broad type silencing:

```python
# type: ignore
Any
cast(Any, ...)
except Exception: pass
```

Use explicit models, protocols, TypedDicts, dataclasses, Pydantic models, or narrow boundary validation depending on repo style.

### Async rules

Inside `async def`, avoid blocking calls:

```python
time.sleep()
requests.get()
subprocess.run()
open(...).read() for large files
CPU-heavy loops
GPU-heavy generation inline without queue/worker/progress
```

Use:

- async libraries where available
- thread/process offload where appropriate
- job queues for long-running tasks
- timeouts and cancellation where repo supports it

### Error handling rules

Do not use empty broad catches.

Bad:

```python
try:
    do_work()
except Exception:
    pass
```

Better:

```python
try:
    do_work()
except SpecificError as exc:
    logger.warning("Work failed: %s", exc)
    raise
```

### Serialization and security rules

Do not use unsafe serialization on untrusted data:

```python
pickle.load(...)
yaml.load(...)
eval(...)
exec(...)
```

Prefer:

```python
json
yaml.safe_load
pydantic validation
explicit parsers
```

### File/path rules

- Use `pathlib` where repo allows.
- Avoid hardcoded Windows drive letters unless user explicitly gave one.
- Avoid assuming `/tmp` on Windows.
- Protect against path traversal on uploads/extraction.
- Validate file size and extension when handling uploads.

### Test rules

For Python fixes:

1. Run the narrow relevant pytest if possible.
2. Run `ruff check` if repo uses Ruff.
3. Run `pyright` or `mypy` if configured.
4. Do not skip failing tests to pass.

PowerShell examples:

```powershell
python -m pytest tests\test_target.py -q
python -m ruff check .
pyright
```

---

## C++ guardrails

### Toolchain discovery

Before editing C++ code, inspect:

```text
CMakeLists.txt
CMakePresets.json
CMakeUserPresets.json
vcpkg.json
conanfile.*
compile_commands.json
.github/workflows/*
README build instructions
configured C++ standard
compiler target
```

Do not assume Ninja, Visual Studio, MSVC, clang, clang-cl, GCC, MinGW, or WSL.

### CMake rules

If `CMakePresets.json` exists, use presets.

Prefer:

```powershell
cmake --list-presets
cmake --preset <name>
cmake --build --preset <name>
ctest --preset <name> --output-on-failure
```

Do not invent a generator unless no presets exist and the user approves.

### C++ standard rules

Check the configured standard before using:

- concepts
- ranges
- coroutines
- modules
- `std::format`
- `std::span`
- `std::expected`
- designated initializers

Do not smuggle C++20/23 into a C++17 project.

### Memory safety rules

Prefer:

- RAII
- value types
- smart pointers when ownership is needed
- `std::vector`, `std::array`, `std::string`, `std::span`
- bounds-aware logic
- clear ownership contracts

Avoid:

```cpp
new/delete in ordinary application code
raw owning pointers
strcpy/sprintf
manual buffer management
unchecked indexing
use-after-move
returning references to locals
shared_ptr everywhere without ownership reason
```

### Error handling rules

Follow repo convention:

- exceptions
- `std::optional`
- result/error types
- status codes

Do not mix styles randomly.

### Performance rules

Avoid performance cargo cults.

Do not add micro-optimizations before proving the bottleneck.

Check:

- unnecessary copies
- pass by value vs const ref vs move
- allocation in hot loops
- string conversions
- virtual dispatch in hot paths
- cache behavior only when measured

### C++ validation rules

Where configured, run:

```powershell
cmake --build --preset <name>
ctest --preset <name> --output-on-failure
clang-tidy
cppcheck
```

For memory-sensitive changes, prefer sanitizer builds if available:

```text
AddressSanitizer
UndefinedBehaviorSanitizer
ThreadSanitizer where appropriate
```

---

## Cross-language shell rules

For user-facing commands, prefer PowerShell when the repo/user is Windows-oriented.

PowerShell-safe examples:

```powershell
New-Item -ItemType Directory -Force .\build
Remove-Item -Recurse -Force .\build
Copy-Item -Recurse .\src .\backup-src
$env:PYTHONPATH = "."
```

Avoid assuming Bash unless repo uses Bash.

## Final response add-on

For Python/C++ work, final response must include:

```text
Runtime/toolchain checked:
- Python: <version or not checked>
- CMake preset/compiler: <value or not checked>

Validation:
- <command> -> passed/failed/not run
```
