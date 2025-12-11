# Build Android APK from Windows using WSL2 Ubuntu
# Usage: run in PowerShell from project root
#   powershell -ExecutionPolicy Bypass -File .\build-android.ps1

$projectWinPath = (Get-Location).Path
$projectWslPath = "/mnt/" + ($projectWinPath.Substring(0,1).ToLower()) + $projectWinPath.Substring(1).Replace("\\","/")

$cmd = @"
set -e
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git openjdk-17-jdk unzip libffi-dev libssl-dev
pip3 install --user buildozer cython
cd $projectWslPath
buildozer android debug
"@

wsl bash -lc $cmd

$apkPath = Join-Path $projectWinPath "bin"
Write-Host "If build succeeded, APK is in: $apkPath"