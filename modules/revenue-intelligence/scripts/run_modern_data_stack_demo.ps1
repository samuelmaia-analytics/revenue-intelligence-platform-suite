param(
    [ValidateSet("none", "bigquery", "snowflake")]
    [string]$Target = "none",
    [switch]$RunDbt,
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Resolve-Path (Join-Path $scriptDir "..")
$appVenvPython = Resolve-Path (Join-Path $projectDir ".venv\Scripts\python.exe")
$dbtVenvPython = Resolve-Path (Join-Path $projectDir ".venv-dbt\Scripts\python.exe")
$dbtDir = Join-Path $projectDir "dbt"
$profilesExample = Join-Path $dbtDir "profiles.yml.example"
$profilesFile = Join-Path $dbtDir "profiles.yml"

Write-Host "=== Revenue Intelligence Modern Data Stack Demo ==="
Write-Host "Project dir: $projectDir"
Write-Host "Warehouse target: $Target"
Write-Host "Run dbt: $RunDbt"

if (-not (Test-Path $appVenvPython)) {
    throw "Python da .venv nao encontrado em $appVenvPython"
}

if ($RunDbt -and -not (Test-Path $dbtVenvPython)) {
    throw "Python da .venv-dbt nao encontrado em $dbtVenvPython"
}

if (-not $SkipInstall) {
    Write-Host "`n[1/4] Instalando dependencias Python"
    & $appVenvPython -m pip install -r (Join-Path $projectDir "requirements.txt")
    & $appVenvPython -m pip install -r (Join-Path $projectDir "requirements-warehouse.txt")
    if ($RunDbt) {
        & $dbtVenvPython -m pip install -r (Join-Path $projectDir "requirements-dbt.txt")
    }
}

Write-Host "`n[2/4] Executando pipeline Python"
$env:RIP_WAREHOUSE_PROVIDER = $Target
& $appVenvPython (Join-Path $projectDir "main.py")

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
$dbtTarget = if ($Target -eq "snowflake") {
    "snowflake"
}
elseif ($Target -eq "bigquery") {
    "dev"
}
else {
    "ci"
}

Write-Host "`n[4/4] Executando dbt (target: $dbtTarget)"
Push-Location $dbtDir
try {
    & $dbtVenvPython -m dbt debug --target $dbtTarget
    & $dbtVenvPython -m dbt run --target $dbtTarget
    & $dbtVenvPython -m dbt test --target $dbtTarget
}
finally {
    Pop-Location
}

Write-Host "`nDemo concluida com sucesso."
