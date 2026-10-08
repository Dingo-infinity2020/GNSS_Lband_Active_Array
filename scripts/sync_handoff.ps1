$ErrorActionPreference = "Stop"

$CanonicalBranch = "project/r0-charts-scaffold"

Write-Host "=== GNSS_Lband_Active_Array sync ==="

$status = git status --porcelain
if ($LASTEXITCODE -ne 0) { throw "Not inside a valid Git repository." }
if ($status) {
    Write-Host "Working tree is not clean. Commit/stash/review changes before syncing:" -ForegroundColor Yellow
    Write-Host $status
    exit 2
}

git fetch origin
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git checkout $CanonicalBranch
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git pull --ff-only origin $CanonicalBranch
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$sha = git rev-parse HEAD
Write-Host ""
Write-Host "SYNC_PASS"
Write-Host "BRANCH=$CanonicalBranch"
Write-Host "HEAD=$sha"
Write-Host ""

if (-not (Test-Path "PROJECT_HANDOFF.md")) { throw "PROJECT_HANDOFF.md is missing after sync." }

Write-Host "=== Current handoff header ==="
Get-Content "PROJECT_HANDOFF.md" | Select-String -Pattern "^(HANDOFF_VERSION|CANONICAL_BRANCH|CURRENT_GATE|CURRENT_TASK_ID|TASK_OWNER|TASK_STATUS|SOLVER_PERMISSION|OPTIMIZATION_PERMISSION)=" | ForEach-Object { Write-Host $_.Line }

Write-Host ""
Write-Host "Read PROJECT_HANDOFF.md before doing any project work."
