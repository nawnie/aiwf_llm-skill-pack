param(
    [string]$CodexSkillsDir = "$env:USERPROFILE\.codex\skills",
    [string]$AvoidAiWritingUrl = "https://raw.githubusercontent.com/conorbronsdon/avoid-ai-writing/main/SKILL.md",
    [switch]$SkipAvoidAiWriting,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsSource = Join-Path $repoRoot "skills"

if (-not (Test-Path -LiteralPath $skillsSource)) {
    throw "Missing skills folder: $skillsSource"
}

New-Item -ItemType Directory -Path $CodexSkillsDir -Force | Out-Null

$skillDirs = Get-ChildItem -LiteralPath $skillsSource -Directory
foreach ($skillDir in $skillDirs) {
    $target = Join-Path $CodexSkillsDir $skillDir.Name
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

if (-not $SkipAvoidAiWriting) {
    $avoidTarget = Join-Path $CodexSkillsDir "avoid-ai-writing"
    New-Item -ItemType Directory -Path $avoidTarget -Force | Out-Null
    $avoidSkill = Join-Path $avoidTarget "SKILL.md"
    Invoke-WebRequest -Uri $AvoidAiWritingUrl -OutFile $avoidSkill
    Write-Host "Downloaded avoid-ai-writing from $AvoidAiWritingUrl"
}

Write-Host "Install complete. Restart Codex so the loaded skill list refreshes."
