param(
    [string]$Target = "$env:USERPROFILE\plugins\aiwf-llm-skill-pack",
    [switch]$SkipCodexAdd,
    [switch]$TryCodexCli,
    [int]$CodexTimeoutSeconds = 30
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$targetPath = [System.IO.Path]::GetFullPath($Target)
if ([System.IO.Path]::GetFileName($targetPath) -ne "aiwf-llm-skill-pack") {
    throw "Plugin target must end in aiwf-llm-skill-pack: $targetPath"
}

$packValidator = Join-Path $root "scripts\validate_pack.py"
$pluginTools = Join-Path $env:USERPROFILE ".codex\skills\.system\plugin-creator\scripts"
$pluginValidator = Join-Path $pluginTools "validate_plugin.py"
$cachebuster = Join-Path $pluginTools "update_plugin_cachebuster.py"

& python $packValidator --root $root
if ($LASTEXITCODE -ne 0) {
    throw "Pack validation failed."
}
if (-not (Test-Path -LiteralPath $pluginValidator -PathType Leaf)) {
    throw "Missing Codex plugin validator: $pluginValidator"
}
& python $pluginValidator $root
if ($LASTEXITCODE -ne 0) {
    throw "Codex plugin validation failed."
}

New-Item -ItemType Directory -Force -Path $targetPath | Out-Null
foreach ($directory in @(".codex-plugin", "docs", "scripts", "skills")) {
    $managedTarget = Join-Path $targetPath $directory
    if (Test-Path -LiteralPath $managedTarget) {
        Remove-Item -LiteralPath $managedTarget -Recurse -Force
    }
    Copy-Item -LiteralPath (Join-Path $root $directory) -Destination $managedTarget -Recurse
}

foreach ($file in @(
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "HANDOFF.md",
    "install.ps1",
    "LICENSE",
    "manifest.json",
    "PROJECT_SKILLS.md",
    "README.md",
    "skillfindings.md"
)) {
    $source = Join-Path $root $file
    if (Test-Path -LiteralPath $source -PathType Leaf) {
        Copy-Item -LiteralPath $source -Destination (Join-Path $targetPath $file) -Force
    }
}

if (Test-Path -LiteralPath $cachebuster -PathType Leaf) {
    & python $cachebuster $targetPath
    if ($LASTEXITCODE -ne 0) {
        throw "Plugin cachebuster update failed."
    }
}

& python (Join-Path $targetPath "scripts\validate_pack.py") --root $targetPath
if ($LASTEXITCODE -ne 0) {
    throw "Mirrored plugin pack validation failed."
}
& python $pluginValidator $targetPath
if ($LASTEXITCODE -ne 0) {
    throw "Mirrored Codex plugin validation failed."
}

if (-not $SkipCodexAdd) {
    $cliStatus = "skipped"
    $codexCommand = if ($TryCodexCli) { Get-Command codex -ErrorAction SilentlyContinue } else { $null }
    if ($TryCodexCli -and -not $codexCommand) {
        $cliStatus = "unavailable"
    }
    elseif ($codexCommand) {
        $stdoutPath = Join-Path ([System.IO.Path]::GetTempPath()) ("aiwf-codex-stdout-" + [System.Guid]::NewGuid().ToString("N") + ".log")
        $stderrPath = Join-Path ([System.IO.Path]::GetTempPath()) ("aiwf-codex-stderr-" + [System.Guid]::NewGuid().ToString("N") + ".log")
        try {
            $process = Start-Process -FilePath $codexCommand.Source `
                -ArgumentList @("plugin", "add", "aiwf-llm-skill-pack@personal") `
                -PassThru -WindowStyle Hidden `
                -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
            if ($process.WaitForExit($CodexTimeoutSeconds * 1000)) {
                $cliStatus = if ($process.ExitCode -eq 0) { "completed" } else { "failed:$($process.ExitCode)" }
            }
            else {
                try { $process.Kill($true) } catch { $process.Kill() }
                $cliStatus = "timed-out"
            }
        }
        catch {
            $cliStatus = "error:$($_.Exception.Message)"
        }
        finally {
            if ($process) { $process.Dispose() }
            Remove-Item -LiteralPath $stdoutPath,$stderrPath -Force -ErrorAction SilentlyContinue
        }
    }

    $pluginData = Get-Content -LiteralPath (Join-Path $targetPath ".codex-plugin\plugin.json") -Raw | ConvertFrom-Json
    $cacheRoot = [System.IO.Path]::GetFullPath(
        (Join-Path $env:USERPROFILE ".codex\plugins\cache\personal\aiwf-llm-skill-pack")
    )
    New-Item -ItemType Directory -Force -Path $cacheRoot | Out-Null
    $cachePrefix = $cacheRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    $cacheTarget = [System.IO.Path]::GetFullPath((Join-Path $cacheRoot $pluginData.version))
    if (-not $cacheTarget.StartsWith($cachePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to write outside the plugin cache root: $cacheTarget"
    }
    if (Test-Path -LiteralPath $cacheTarget) {
        Remove-Item -LiteralPath $cacheTarget -Recurse -Force
    }
    Copy-Item -LiteralPath $targetPath -Destination $cacheTarget -Recurse -Force

    $configPath = Join-Path $env:USERPROFILE ".codex\config.toml"
    if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
        New-Item -ItemType File -Force -Path $configPath | Out-Null
    }
    $lines = [System.Collections.Generic.List[string]]::new()
    foreach ($line in @(Get-Content -LiteralPath $configPath)) { $lines.Add($line) }
    $header = '[plugins."aiwf-llm-skill-pack@personal"]'
    $headerIndex = -1
    for ($index = 0; $index -lt $lines.Count; $index++) {
        if ($lines[$index].Trim() -eq $header) { $headerIndex = $index; break }
    }
    $configChanged = $false
    if ($headerIndex -lt 0) {
        if ($lines.Count -gt 0 -and $lines[$lines.Count - 1] -ne "") { $lines.Add("") }
        $lines.Add($header)
        $lines.Add("enabled = true")
        $configChanged = $true
    }
    else {
        $sectionEnd = $lines.Count
        for ($index = $headerIndex + 1; $index -lt $lines.Count; $index++) {
            if ($lines[$index] -match '^\s*\[') { $sectionEnd = $index; break }
        }
        $enabledIndex = -1
        for ($index = $headerIndex + 1; $index -lt $sectionEnd; $index++) {
            if ($lines[$index] -match '^\s*enabled\s*=') { $enabledIndex = $index; break }
        }
        if ($enabledIndex -lt 0) {
            $lines.Insert($headerIndex + 1, "enabled = true")
            $configChanged = $true
        }
        elseif ($lines[$enabledIndex].Trim() -ne "enabled = true") {
            $lines[$enabledIndex] = "enabled = true"
            $configChanged = $true
        }
    }
    if ($configChanged) {
        [System.IO.File]::WriteAllLines($configPath, $lines, [System.Text.UTF8Encoding]::new($false))
    }

    & python (Join-Path $cacheTarget "scripts\validate_pack.py") --root $cacheTarget
    if ($LASTEXITCODE -ne 0) {
        throw "Installed plugin-cache pack validation failed."
    }
    & python $pluginValidator $cacheTarget
    if ($LASTEXITCODE -ne 0) {
        throw "Installed plugin-cache validation failed."
    }
    Write-Host "Codex CLI status: $cliStatus"
    Write-Host "Installed validated plugin cache at $cacheTarget"
}

Write-Host "Personal plugin source refreshed at $targetPath"
Write-Host "Start a new Codex chat so the 56-skill #techstartup pack is reloaded."
