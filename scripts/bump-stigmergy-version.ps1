# Create the next Vn snapshot in the repo (run from repo root after editing stigmergy files).
# Usage: .\scripts\bump-stigmergy-version.ps1 -Notes "Short description"

param(
    [Parameter(Mandatory = $true)]
    [string]$Notes,
    [string]$InternalLabel = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$VersionsDir = Join-Path $RepoRoot "02-assessment-tasks\assessment-1-development\versions"
$DevDir = Join-Path $RepoRoot "02-assessment-tasks\assessment-1-development"
$LatestFile = Join-Path $VersionsDir "LATEST.txt"

$current = 0
if (Test-Path $LatestFile) {
    $current = [int](Get-Content $LatestFile -Raw).Trim()
}
$next = $current + 1
$folder = "V$next"
$dest = Join-Path $VersionsDir $folder

if (Test-Path $dest) {
    Write-Error "$folder already exists. Do not overwrite."
}

New-Item -ItemType Directory -Path $dest -Force | Out-Null

$files = @(
    "stigmergy-generator.py",
    "stigmergy-guide.html",
    "stigmergy-how-to.md",
    "stigmergy-text-catalog.md"
)
foreach ($f in $files) {
    Copy-Item (Join-Path $DevDir $f) (Join-Path $dest $f)
}

$commit = (git -C $RepoRoot rev-parse --short HEAD)
Set-Content -Path (Join-Path $dest "git-commit.txt") -Value $commit
Set-Content -Path (Join-Path $dest "VERSION.txt") -Value @(
    $folder,
    "Notes: $Notes",
    "Internal: $InternalLabel",
    "Git: $commit"
)
Set-Content -Path $LatestFile -Value $next

Write-Host "Created $folder (git $commit). Update VERSION-MANIFEST.md, then commit and push."
Write-Host "On Windows run: .\scripts\sync-claude-code-local.ps1"
