[CmdletBinding()]
param (
    [Parameter()]
    [string]
    $Key = "default",
    [Parameter(Mandatory=$true)]
    [string]
    $CachePath
)

$ErrorActionPreference = "Stop"

$CacheBasePath = "$CachePath\Caches\$Key"

if (-not (Test-Path -Path $CachePath -PathType "Container")) {
    throw [System.ArgumentException]"'$CachePath' is not a directory"
}

if (-not (Test-Path -Path "$CacheBasePath\cache.tar.gz")) {
    Write-Warning -Message "'$CacheBasePath\cache.tar.gz' is not exists"

    return
}

$params = @{
    FilePath = "tar.exe"
    ArgumentList = @("-xzvf", "$CacheBasePath\cache.tar.gz")
}

Start-Process @params -Wait -NoNewWindow
