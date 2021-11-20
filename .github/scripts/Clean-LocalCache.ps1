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

if (-not (Test-Path -Path $CachePath -PathType "Container")) {
    throw [System.ArgumentException]"'$CachePath' is not a directory"
}

if (-not (Test-Path -Path "$CachePath\Caches\$Key")) {
    Write-Warning -Message "'$CachePath\Caches\$Key' is not exists"

    return
}

Remove-Item -Path "$CachePath\Caches\$Key" -Recurse -Force
