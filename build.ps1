$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$venvPython = Join-Path $projectRoot ".venv/Scripts/python.exe"
$python = $venvPython
if (-not (Test-Path $python)) {
    $python = "C:/Users/erickson/AppData/Local/Programs/Python/Python312/python.exe"
}
if (-not (Test-Path $python)) {
    $python = "python"
}

$appPath = Join-Path $projectRoot "app.py"
$iconPath = Join-Path $projectRoot "app.ico"
$outputExe = Join-Path $projectRoot "app.exe"
$pyInstallerRoot = Join-Path $env:TEMP "longpath-pyinstaller"
$pyInstallerWork = Join-Path $pyInstallerRoot "build"
$pyInstallerSpec = Join-Path $pyInstallerRoot "spec"

if (-not (Test-Path $appPath)) {
    throw "Archivo principal no encontrado: $appPath"
}
if (-not (Test-Path $iconPath)) {
    throw "Icono no encontrado: $iconPath"
}
if (Test-Path $pyInstallerRoot) {
    Remove-Item $pyInstallerRoot -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $pyInstallerWork -Force | Out-Null
New-Item -ItemType Directory -Path $pyInstallerSpec -Force | Out-Null
if (Test-Path $outputExe) {
    Remove-Item $outputExe -Force
}

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name "app" `
    --icon "$iconPath" `
    --distpath "$projectRoot" `
    --workpath "$pyInstallerWork" `
    --specpath "$pyInstallerSpec" `
    "$appPath"

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller fallo con codigo de salida $LASTEXITCODE"
}
if (-not (Test-Path $outputExe)) {
    throw "No se genero el ejecutable esperado: $outputExe"
}

Write-Host "Build finalizado. EXE generado en: $outputExe"
