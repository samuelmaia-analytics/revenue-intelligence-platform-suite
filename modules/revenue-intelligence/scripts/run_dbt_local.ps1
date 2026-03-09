param(
    [ValidateSet("ci", "dev", "snowflake")]
    [string]$Target = "ci",
    [switch]$WithTests
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Resolve-Path (Join-Path $scriptDir "..")
$dbtDir = Join-Path $projectDir "dbt"
$dbtPython = Join-Path $projectDir ".venv-dbt\Scripts\python.exe"
$profilesDir = Join-Path $projectDir ".github\dbt"
$profilesFile = Join-Path $profilesDir "profiles.yml"

if (-not (Test-Path $dbtPython)) {
    throw "dbt environment not found. Run scripts/setup_envs.ps1 first."
}

if (-not (Test-Path $profilesFile)) {
    New-Item -ItemType Directory -Force -Path $profilesDir | Out-Null
    @'
revenue_intelligence:
  target: ci
  outputs:
    ci:
      type: duckdb
      path: .github/dbt/revenue_intelligence.duckdb
      schema: analytics
      threads: 4
'@ | Set-Content -Path $profilesFile
}

$env:DBT_PROFILES_DIR = $profilesDir

Push-Location $dbtDir
try {
    & $dbtPython -m dbt deps --project-dir $dbtDir
    & $dbtPython -m dbt parse --project-dir $dbtDir --target $Target
    & $dbtPython -m dbt run --project-dir $dbtDir --target $Target
    if ($WithTests) {
        & $dbtPython -m dbt test --project-dir $dbtDir --target $Target
    }
}
finally {
    Pop-Location
}
