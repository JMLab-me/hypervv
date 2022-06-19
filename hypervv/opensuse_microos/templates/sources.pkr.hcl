source "hyperv-vmcx" "opensuse_microos" {
    clone_from_vm_name = "OpenSUSE.MicroOS"

    shutdown_command = "echo '${var.username}' | sudo -S shutdown -P now"

    ssh_username = "${var.username}"
    ssh_password = "${var.password}"

    secondary_iso_images = [ "${var.secondary_iso}" ]

    switch_name = "${var.switch_name}"
    headless = "${var.headless}"
    ssh_timeout = "${var.ssh_timeout}"
}
