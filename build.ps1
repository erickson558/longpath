$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$python = "C:/Users/erickson/AppData/Local/Programs/Python/Python312/python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

$iconPath = Join-Path $projectRoot "app.ico"
if (-not (Test-Path $iconPath)) {
    throw "Icono no encontrado: $iconPath"
}

& $python -m PyInstaller `
    --noconfirm `
    --onefile `
    --windowed `
    --icon "$iconPath" `
    --distpath "$projectRoot" `
    --workpath "$projectRoot/build" `
    --specpath "$projectRoot/build" `
    "$projectRoot/app.py"

Write-Host "Build finalizado. EXE generado en: $projectRoot"
