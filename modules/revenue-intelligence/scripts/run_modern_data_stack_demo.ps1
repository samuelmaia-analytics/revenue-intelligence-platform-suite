param(
    [ValidateSet("none", "bigquery", "snowflake")]
    [string]$Target = "none",
    [switch]$RunDbt,
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Resolve-Path (Join-Path $scriptDir "..")
$venvPython = Resolve-Path (Join-Path $projectDir "..\..\.venv\Scripts\python.exe")
$dbtDir = Join-Path $projectDir "dbt"
$profilesExample = Join-Path $dbtDir "profiles.yml.example"
$profilesFile = Join-Path $dbtDir "profiles.yml"

Write-Host "=== Revenue Intelligence Modern Data Stack Demo ==="
Write-Host "Project dir: $projectDir"
Write-Host "Warehouse target: $Target"
Write-Host "Run dbt: $RunDbt"

if (-not (Test-Path $venvPython)) {
    throw "Python da .venv nao encontrado em $venvPython"
}

if (-not $SkipInstall) {
    Write-Host "`n[1/4] Instalando dependencias Python"
    & $venvPython -m pip install -r (Join-Path $projectDir "requirements.txt")
    & $venvPython -m pip install -r (Join-Path $projectDir "requirements-warehouse.txt")
    if ($RunDbt) {
        & $venvPython -m pip install -r (Join-Path $projectDir "requirements-dbt.txt")
    }
}

Write-Host "`n[2/4] Executando pipeline Python"
$env:RIP_WAREHOUSE_PROVIDER = $Target
& $venvPython (Join-Path $projectDir "main.py")

if (-not $RunDbt) {
    Write-Host "`nPipeline finalizado. dbt nao executado (use -RunDbt para habilitar)."
    exit 0
}

Write-Host "`n[3/4] Preparando dbt profile local"
if (-not (Test-Path $profilesFile)) {
    Copy-Item $profilesExample $profilesFile
    Write-Host "Criado: $profilesFile"
}

$env:DBT_PROFILES_DIR = $dbtDir
$dbtTarget = if ($Target -eq "snowflake") { "snowflake" } else { "dev" }

Write-Host "`n[4/4] Executando dbt (target: $dbtTarget)"
Push-Location $dbtDir
try {
    & $venvPython -m dbt debug --target $dbtTarget
    & $venvPython -m dbt run --target $dbtTarget
    & $venvPython -m dbt test --target $dbtTarget
}
finally {
    Pop-Location
}

Write-Host "`nDemo concluida com sucesso."
