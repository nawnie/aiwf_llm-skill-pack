param(
  [string]$Root = "",
  [string]$Out = ""
)

$ErrorActionPreference = "Stop"
$defaultOut = -not $Out

if (-not $Root) {
  $Root = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
}

if (-not $Out) {
  $dist = Join-Path $Root "dist"
  New-Item -ItemType Directory -Force -Path $dist | Out-Null
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $Out = Join-Path $dist "agent-skills-$stamp.zip"
}

$outDir = Split-Path -Parent $Out
if ($outDir) {
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

$stage = Join-Path ([System.IO.Path]::GetTempPath()) ("agent-skills-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $stage | Out-Null

try {
  foreach ($name in @("AGENTS.md", "HANDOFF.md", "PROJECT_SKILLS.md", "README.md", "LICENSE", "install.ps1", "manifest.json", "skillfindings.md")) {
    $source = Join-Path $Root $name
    if (Test-Path -LiteralPath $source) {
      Copy-Item -LiteralPath $source -Destination $stage
    }
  }

  $docs = Join-Path $Root "docs"
  if (Test-Path -LiteralPath $docs) {
    Copy-Item -LiteralPath $docs -Destination $stage -Recurse
  }

  Copy-Item -LiteralPath (Join-Path $Root "skills") -Destination $stage -Recurse
  Copy-Item -LiteralPath (Join-Path $Root "scripts") -Destination $stage -Recurse

  Get-ChildItem -LiteralPath $stage -Recurse -Directory -Force |
    Where-Object { $_.Name -eq "__pycache__" } |
    Remove-Item -Recurse -Force
  Get-ChildItem -LiteralPath $stage -Recurse -File -Force |
    Where-Object { $_.Extension -in @(".pyc", ".pyo") } |
    Remove-Item -Force

  if (Test-Path -LiteralPath $Out) {
    Remove-Item -LiteralPath $Out -Force
  }

  Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $Out -Force
  if ($defaultOut) {
    $latest = Join-Path $outDir "agent-skills-latest.zip"
    Copy-Item -LiteralPath $Out -Destination $latest -Force
  }
  Write-Output $Out
}
finally {
  if (Test-Path -LiteralPath $stage) {
    Remove-Item -LiteralPath $stage -Recurse -Force
  }
}
