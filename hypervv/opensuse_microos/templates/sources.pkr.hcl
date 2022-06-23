source "hyperv-vmcx" "opensuse-microos-gen2" {
    clone_from_vm_name = "OpenSUSE.MicroOS"

    shutdown_command = "echo '${var.username}' | sudo -S shutdown -P now"

    ssh_username = "${var.username}"
    ssh_password = "${var.password}"

    secondary_iso_images = [ "${var.secondary_iso}" ]

    enable_secure_boot = true
    secure_boot_template = "MicrosoftUEFICertificateAuthority"

    switch_name = "${var.switch_name}"
    headless = "${var.headless}"
    ssh_timeout = "${var.ssh_timeout}"
}
