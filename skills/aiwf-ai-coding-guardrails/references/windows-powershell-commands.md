# Windows / PowerShell command crib sheet

## Environment

```powershell
python --version
py -0p
node --version
npm --version
pnpm --version
yarn --version
```

## Git

```powershell
git status --short
git diff --stat
git diff --name-only
git diff -- path\to\file.ext
```

## Files

```powershell
Get-ChildItem -Force -Name
Get-ChildItem -Recurse -Filter package.json -Depth 3
New-Item -ItemType Directory -Force .\logs
Remove-Item -Recurse -Force .\dist
Copy-Item -Recurse .\src .\src_backup
```

## Environment variables

```powershell
$env:PYTHONPATH = "."
$env:NODE_ENV = "development"
```

## Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python -m ruff check .
pyright
```

## JavaScript package managers

```powershell
npm ci
npm run build
npm run test
npm run typecheck

pnpm install --frozen-lockfile
pnpm build
pnpm test
pnpm typecheck

yarn install --immutable
yarn build
yarn test
yarn typecheck
```

## CMake

```powershell
cmake --list-presets
cmake --preset default
cmake --build --preset default
ctest --preset default --output-on-failure
```

## Common Bash to PowerShell translations

| Bash | PowerShell |
|---|---|
| `export FOO=bar` | `$env:FOO = "bar"` |
| `rm -rf dist` | `Remove-Item -Recurse -Force .\dist` |
| `cp -r src dest` | `Copy-Item -Recurse .\src .\dest` |
| `mkdir -p logs` | `New-Item -ItemType Directory -Force .\logs` |
