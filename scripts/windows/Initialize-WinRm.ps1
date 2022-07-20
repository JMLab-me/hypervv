$Cert = New-SelfSignedCertificate -CertstoreLocation Cert:\LocalMachine\My -DnsName "WinRMCertificate"

# Setup WinRM
Enable-PSRemoting -SkipNetworkProfileCheck -Force

# Disable WinRM over HTTP
Get-ChildItem WSMan:\Localhost\listener | Where-Object -Property Keys -eq "Transport=HTTP" | Remove-Item -Recurse
Disable-NetFirewallRule -Name "WINRM-HTTP-In-TCP" -All

# Add HTTPS Listener and open firewall
New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -CertificateThumbPrint $Cert.Thumbprint -Force
New-NetFirewallRule -DisplayName "Windows Remote Management (HTTPS-In)" -Name "WINRM-HTTPS-In-TCP" -Profile Any -LocalPort 5986 -Protocol TCP
