$ErrorActionPreference = 'Stop'

$frontendRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$nginxRoot = 'C:\Users\21918\Desktop\jianshang\nginx-1.20.2'
$distPath = Join-Path $frontendRoot 'dist'
$deployPath = Join-Path $nginxRoot 'html\InjuryAssessment-3051'

Write-Host 'Building frontend...'
Push-Location $frontendRoot
try {
    npm run build
}
finally {
    Pop-Location
}

if (-not (Test-Path $distPath)) {
    throw "Build output not found: $distPath"
}

if (Test-Path $deployPath) {
    Remove-Item -LiteralPath $deployPath -Recurse -Force
}

New-Item -ItemType Directory -Path $deployPath -Force | Out-Null
Copy-Item -Path (Join-Path $distPath '*') -Destination $deployPath -Recurse -Force

Write-Host "Frontend deployed to: $deployPath"
