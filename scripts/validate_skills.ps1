param(
  [string]$Root = ""
)

$ErrorActionPreference = "Stop"

if (-not $Root) {
  $Root = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
}

$validator = "C:\Users\Shawn\.codex\skills\.system\skill-creator\scripts\quick_validate.py"
if (-not (Test-Path -LiteralPath $validator)) {
  throw "Missing validator: $validator"
}

$skillsDir = Join-Path $Root "skills"
$skills = Get-ChildItem -Directory -LiteralPath $skillsDir | Sort-Object Name

foreach ($skill in $skills) {
  Write-Output "Validating $($skill.Name)"
  python -X utf8 $validator $skill.FullName
}

Write-Output "Validated $($skills.Count) skills."
