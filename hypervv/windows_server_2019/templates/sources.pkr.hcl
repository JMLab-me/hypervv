source "hyperv-iso" "windows-server-2019-standard-gen2" {
    generation = 2
    enable_secure_boot = true

    iso_url = var.iso_url
    iso_checksum = var.iso_checksum

    communicator = "winrm"
    winrm_username = var.username
    winrm_password = var.password
    winrm_timeout = var.winrm_timeout
    winrm_use_ssl = true
    winrm_insecure = true
    winrm_use_ntlm = true

    headless = var.headless
    switch_name = var.switch_name

    boot_wait = var.boot_wait
    boot_command = [
        "<esc><wait><esc><wait><esc><wait><esc><wait>"
    ]

    first_boot_device = "DVD"

    secondary_iso_images = [ "${var.secondary_iso}" ]

    shutdown_command = "E:\\PackerShutdown.cmd"
    shutdown_timeout = "1h"

    keep_registered = var.keep_registered
    output_directory = "${var.output_dir}/${var.output_hv}"
}
