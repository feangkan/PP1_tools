# Sync PP1_tools stigmergy versions to D:\Claude code without overwriting old Vn folders.
# Usage:
#   cd D:\Claude code\PP1_tools
#   git pull
#   .\scripts\sync-claude-code-local.ps1

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SourceVersions = Join-Path $RepoRoot "02-assessment-tasks\assessment-1-development\versions"
$DestRoot = "D:\Claude code\PP1_stigmergy"

if (-not (Test-Path $SourceVersions)) {
    Write-Error "Version folder not found: $SourceVersions"
}

if (-not (Test-Path "D:\Claude code")) {
    New-Item -ItemType Directory -Path "D:\Claude code" -Force | Out-Null
}

New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null

$LatestFile = Join-Path $SourceVersions "LATEST.txt"
$Latest = "0"
if (Test-Path $LatestFile) {
    $Latest = (Get-Content $LatestFile -Raw).Trim()
}

Write-Host "Repo: $RepoRoot"
Write-Host "Copying version folders to: $DestRoot"
Write-Host "Latest in repo: V$Latest"

$versionDirs = Get-ChildItem -Path $SourceVersions -Directory | Where-Object { $_.Name -match '^V\d+$' }
$copied = 0
$skipped = 0

foreach ($dir in $versionDirs) {
    $dest = Join-Path $DestRoot $dir.Name
    if (-not (Test-Path $dest)) {
        Copy-Item -Path $dir.FullName -Destination $dest -Recurse
        Write-Host "  COPY $($dir.Name) -> $dest"
        $copied++
        continue
    }
    Write-Host "  KEEP $($dir.Name) folder (no overwrite)"
    $skipped++
    Get-ChildItem -Path $dir.FullName -File | ForEach-Object {
        $target = Join-Path $dest $_.Name
        if (-not (Test-Path $target)) {
            Copy-Item $_.FullName $target
            Write-Host "    ADD new file $($_.Name)"
        }
    }
}

# Also sync live working copy (always updated) beside version folders
$LiveDest = Join-Path $DestRoot "_live"
New-Item -ItemType Directory -Path $LiveDest -Force | Out-Null
$liveFiles = @(
    "stigmergy-generator.py",
    "stigmergy-generator-V$Latest.py",
    "stigmergy-guide.html",
    "stigmergy-how-to.md",
    "stigmergy-text-catalog.md"
)
$DevFolder = Join-Path $RepoRoot "02-assessment-tasks\assessment-1-development"
foreach ($f in $liveFiles) {
    $src = Join-Path $DevFolder $f
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination (Join-Path $LiveDest $f) -Force
    }
}
Write-Host "  LIVE _live\ updated (working copy, overwrites OK)"

Write-Host ""
Write-Host "Done. Copied $copied new version(s), skipped $skipped existing."
Write-Host "Open Rhino script: $DestRoot\V$Latest\stigmergy-generator-V$Latest.py"
Write-Host "Or latest working: $LiveDest\stigmergy-generator-V$Latest.py"
