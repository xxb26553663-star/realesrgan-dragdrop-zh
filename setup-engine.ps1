param([string]$Archive)
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip'
$expected = 'ABC02804E17982A3BE33675E4D471E91EA374E65B70167ABC09E31ACB412802D'
$destination = Join-Path $PSScriptRoot 'runtime'
if (Test-Path -LiteralPath $destination) {
    throw 'runtime already exists. Keep it as a backup or remove it manually before reinstalling.'
}
$stage = Join-Path $PSScriptRoot ('.engine-setup-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage | Out-Null
try {
    if ($Archive) {
        $zip = (Resolve-Path -LiteralPath $Archive).Path
    } else {
        $zip = Join-Path $stage 'engine.zip'
        Write-Host 'Downloading Real-ESRGAN from its official GitHub release (about 44 MB)...'
        Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $zip
    }
    if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash -ne $expected) {
        throw 'Downloaded archive SHA-256 mismatch. No engine was installed.'
    }
    $unpacked = Join-Path $stage 'unpacked'
    Expand-Archive -LiteralPath $zip -DestinationPath $unpacked
    $engines = @(Get-ChildItem -LiteralPath $unpacked -Filter 'realesrgan-ncnn-vulkan.exe' -File -Recurse)
    if ($engines.Count -ne 1) { throw 'Unexpected upstream archive layout.' }
    $engineRoot = $engines[0].Directory.FullName
    foreach ($model in @('realesr-animevideov3-x2', 'realesrgan-x4plus-anime', 'realesrgan-x4plus')) {
        foreach ($ext in @('.bin', '.param')) {
            if (!(Test-Path -LiteralPath (Join-Path $engineRoot ('models\' + $model + $ext)) -PathType Leaf)) {
                throw "Missing upstream model: $model$ext"
            }
        }
    }
    Copy-Item -LiteralPath $engineRoot -Destination $destination -Recurse
    Write-Host 'Ready. Drag images onto the launcher. Subsequent processing is entirely local.'
} finally {
    $fullStage = [IO.Path]::GetFullPath($stage)
    $prefix = [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\') + '\.engine-setup-'
    if (!$fullStage.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Unexpected temporary directory path.'
    }
    if ((Get-Item -LiteralPath $stage -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw 'Temporary directory became a reparse point; cleanup stopped.'
    }
    Remove-Item -LiteralPath $stage -Recurse -Force
}
