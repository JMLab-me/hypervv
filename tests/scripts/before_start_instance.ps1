[CmdletBinding()]
param (
    [Parameter()]
    [string]
    $VmName
)

$vm = Get-Vm -Name $VmName

$vmFirmware = $($vm | Get-VMFirmware)

$vmBootorder = $vmFirmware.BootOrder

Write-Host "Change bootorder"
$vmFirmware | Set-VMFirmware -BootOrder $vmBootorder[0],$vmBootorder[2],$vmBootorder[1]
