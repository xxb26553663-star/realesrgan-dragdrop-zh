$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    python -m PyInstaller --noconfirm --clean --onefile --console --exclude-module numpy --name RealesrganDragDrop --distpath dist --workpath build upscale.py
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed.' }
    $folder = Join-Path $PSScriptRoot 'dist\realesrgan-dragdrop-zh-windows-x64'
    if (Test-Path -LiteralPath $folder) { throw 'Release staging folder already exists.' }
    New-Item -ItemType Directory -Path $folder | Out-Null
    foreach ($file in @('README.md','LICENSE','THIRD_PARTY_NOTICES.md','VALIDATION.md','upscale.py','requirements.txt','setup-engine.ps1','初始化引擎.bat','超清化.bat','照片超清化.bat')) {
        Copy-Item -LiteralPath (Join-Path $PSScriptRoot $file) -Destination $folder
    }
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'licenses') -Destination $folder -Recurse
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'dist\RealesrganDragDrop.exe') -Destination $folder
    $zip = Join-Path $PSScriptRoot 'dist\realesrgan-dragdrop-zh-v1.0.0-windows-x64.zip'
    Compress-Archive -LiteralPath $folder -DestinationPath $zip
    Get-FileHash -LiteralPath $zip -Algorithm SHA256
} finally {
    Pop-Location
}
