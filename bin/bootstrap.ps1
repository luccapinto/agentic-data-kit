$ErrorActionPreference = "Stop"

$binPath = $PSScriptRoot
$amoPath = Join-Path $binPath "amo"
$adomdPath = Join-Path $binPath "adomd"
$tempPath = Join-Path $binPath "temp"
$nugetPath = Join-Path $binPath "nuget.exe"

Write-Host "Verificando estrutura de pastas..."
if (-not (Test-Path $amoPath)) { New-Item -ItemType Directory -Force -Path $amoPath | Out-Null }
if (-not (Test-Path $adomdPath)) { New-Item -ItemType Directory -Force -Path $adomdPath | Out-Null }

Write-Host "Baixando nuget.exe..."
if (-not (Test-Path $nugetPath)) {
    Invoke-WebRequest -Uri "https://dist.nuget.org/win-x86-commandline/latest/nuget.exe" -OutFile $nugetPath
}

Write-Host "Baixando pacotes AMO e ADOMD..."
& $nugetPath install Microsoft.AnalysisServices.retail.amd64 -OutputDirectory $tempPath -ExcludeVersion
& $nugetPath install Microsoft.AnalysisServices.AdomdClient.retail.amd64 -OutputDirectory $tempPath -ExcludeVersion

Write-Host "Copiando DLLs para pastas finais..."
$amoSource = Join-Path $tempPath "Microsoft.AnalysisServices.retail.amd64\lib\net45\*.dll"
Copy-Item -Path $amoSource -Destination $amoPath -Force

$adomdSource = Join-Path $tempPath "Microsoft.AnalysisServices.AdomdClient.retail.amd64\lib\net45\*.dll"
Copy-Item -Path $adomdSource -Destination $adomdPath -Force

Write-Host "Limpando arquivos temporarios..."
Remove-Item -Path $tempPath -Recurse -Force
Remove-Item -Path $nugetPath -Force

Write-Host "Bootstrap concluido com sucesso! DLLs instaladas em bin/amo/ e bin/adomd/."
