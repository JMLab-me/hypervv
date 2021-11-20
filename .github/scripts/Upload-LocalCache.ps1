[CmdletBinding()]
param (
    [Parameter()]
    [string]
    $Key = "default",
    [Parameter(Mandatory=$true)]
    [string[]]
    $Targets,
    [Parameter(Mandatory=$true)]
    [string]
    $CachePath
)

$ErrorActionPreference = "Stop"

$CacheBasePath = "$CachePath\Caches\$Key"

if (-not (Test-Path -Path $CachePath -PathType "Container")) {
    throw [System.ArgumentException]"'$CachePath' is not a directory"
}

if (-not (Test-Path -Path "$CacheBasePath")) {
    New-Item -Path "$CacheBasePath" -ItemType "Directory"
}

[System.IO.FileInfo[]]$caches = @()

foreach ($target in $Targets) {
    if (-not (Test-Path -Path $target)) {
        Write-Warning "target '$target' is not exists"
        continue
    }

    if (Test-Path -Path $target -PathType "Leaf") {
        $caches += [System.IO.FileInfo]$target
    } else {
        $caches += Get-ChildItem -Path $target -Recurse -File
    }
}

[string[]]$tarArgs = @()
foreach ($cache in $caches) {
    $tarArgs += $(Resolve-Path -Path $cache.FullName -Relative)
}

$params = @{
    FilePath = "tar.exe"
    ArgumentList = @("-czvf", "$CacheBasePath\cache.tar.gz") + $tarArgs
}

Start-Process @params -Wait -NoNewWindow
