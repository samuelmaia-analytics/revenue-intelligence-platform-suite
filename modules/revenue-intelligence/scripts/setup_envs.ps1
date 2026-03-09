param(
    [switch]$SkipUpgradePip
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Resolve-Path (Join-Path $scriptDir "..")

$appVenvPython = Join-Path $projectDir ".venv\Scripts\python.exe"
$dbtVenvPython = Join-Path $projectDir ".venv-dbt\Scripts\python.exe"

Write-Host "=== Setup Python Environments (app + dbt) ==="
Write-Host "Project dir: $projectDir"

if (-not (Test-Path $appVenvPython)) {
    Write-Host "`n[1/6] Creating app venv (.venv)"
    py -3.11 -m venv (Join-Path $projectDir ".venv")
}

if (-not (Test-Path $dbtVenvPython)) {
    Write-Host "`n[2/6] Creating dbt venv (.venv-dbt)"
    py -3.11 -m venv (Join-Path $projectDir ".venv-dbt")
}

if (-not $SkipUpgradePip) {
    Write-Host "`n[3/6] Upgrading pip in both envs"
    & $appVenvPython -m pip install --upgrade pip
    & $dbtVenvPython -m pip install --upgrade pip
}

Write-Host "`n[4/6] Installing app dependencies in .venv"
& $appVenvPython -m pip install -r (Join-Path $projectDir "requirements.txt")
& $appVenvPython -m pip install -r (Join-Path $projectDir "requirements-dev.txt")

Write-Host "`n[5/6] Installing dbt dependencies in .venv-dbt"
& $dbtVenvPython -m pip install -r (Join-Path $projectDir "requirements-dbt.txt")

Write-Host "`n[6/6] Setup complete"
Write-Host "Use app env: .\\.venv\\Scripts\\Activate.ps1"
Write-Host "Use dbt env: .\\.venv-dbt\\Scripts\\Activate.ps1"
