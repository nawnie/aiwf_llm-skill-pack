param(
    [string]$CodexSkillsDir = "$env:USERPROFILE\.codex\skills",
    [switch]$Force,
    [switch]$PruneRetired,
    [switch]$PruneOnly
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsSource = Join-Path $repoRoot "skills"
$manifestPath = Join-Path $repoRoot "manifest.json"

if (-not (Test-Path -LiteralPath $skillsSource -PathType Container)) {
    throw "Missing skills folder: $skillsSource"
}
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Missing manifest: $manifestPath"
}
if ($PruneOnly -and -not $PruneRetired) {
    throw "-PruneOnly requires -PruneRetired."
}

New-Item -ItemType Directory -Path $CodexSkillsDir -Force | Out-Null
$installRoot = [System.IO.Path]::GetFullPath($CodexSkillsDir)
$installPrefix = $installRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

function Assert-InstallChild([string]$Path) {
    $resolved = [System.IO.Path]::GetFullPath($Path)
    if (-not $resolved.StartsWith($installPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to modify path outside install root: $resolved"
    }
}

if ($PruneRetired) {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    foreach ($skillName in @($manifest.retired_skills)) {
        $target = Join-Path $installRoot $skillName
        Assert-InstallChild $target
        if (Test-Path -LiteralPath $target -PathType Container) {
            Remove-Item -LiteralPath $target -Recurse -Force
            Write-Host "Pruned retired skill $skillName"
        }
    }
}

if ($PruneOnly) {
    Write-Host "Retired-skill pruning complete. No active skills were copied."
    return
}

$skillDirs = Get-ChildItem -LiteralPath $skillsSource -Directory | Sort-Object Name
foreach ($skillDir in $skillDirs) {
    $target = Join-Path $installRoot $skillDir.Name
    Assert-InstallChild $target
    if ((Test-Path -LiteralPath $target) -and -not $Force) {
        Write-Host "Skipping existing skill: $($skillDir.Name). Use -Force to replace it."
        continue
    }
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
    Copy-Item -LiteralPath $skillDir.FullName -Destination $target -Recurse
    Write-Host "Installed $($skillDir.Name)"
}

Write-Host "Install complete: $($skillDirs.Count) skills. Start a new Codex chat to refresh the loaded skill list."
