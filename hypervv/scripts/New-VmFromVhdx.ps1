[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]
    $Name,
    [Parameter(Mandatory=$true)]
    [long]
    $MemoryBytes,
    [Parameter(Mandatory=$true)]
    [string]
    $SwitchName,
    [Parameter(Mandatory=$true)]
    [string]
    $DiskPath
)

$ErrorActionPreference = "Stop"

try {
    $vm = Get-Vm -Name "$Name"

    throw "VM $Name is already exists"
}
catch [Microsoft.HyperV.PowerShell.VirtualizationException] {}

$vm = New-VM -Name $Name -MemoryStartupBytes $MemoryBytes -Generation 2 -SwitchName $SwitchName

$vm | Add-VMHardDiskDrive -Path $DiskPath

$bootOrder = $($vm | Get-VMFirmware).BootOrder

$vm | Set-VMFirmware -BootOrder $bootOrder[1],$bootOrder[0] -SecureBootTemplate "MicrosoftUEFICertificateAuthority"

$disabledIntServices = $($vm | Get-VMIntegrationService) | Where-Object {$_.Enabled -eq $false}

if ($disabledIntServices) {
    $vm | Enable-VMIntegrationService -Name $disabledIntServices.Name
}

return $vm
