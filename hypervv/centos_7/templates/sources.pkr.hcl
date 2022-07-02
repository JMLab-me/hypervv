source "hyperv-iso" "centos-7-gen2" {
    generation = 2
    enable_secure_boot = true
    secure_boot_template = "MicrosoftUEFICertificateAuthority"

    iso_url = var.iso_url
    iso_checksum = var.iso_checksum

    ssh_username = var.username
    ssh_password = var.password
    ssh_timeout = var.ssh_timeout

    http_directory = var.http_directory

    headless = var.headless
    switch_name = var.switch_name

    boot_wait = var.boot_wait
    boot_command = [
        "<esc><wait><esc><wait><esc><wait><esc><wait>",
        "c<wait>",
        "linuxefi /images/pxeboot/vmlinuz inst.stage2=hd:LABEL=CentOS\\x207\\x20x\\86_64 ks=${var.kickstart_uri}<enter><wait>",
        "initrdefi /images/pxeboot/initrd.img<enter><wait>",
        "boot<enter>"
    ]

    first_boot_device = "DVD"

    shutdown_command = "echo '${var.username}' | sudo -S shutdown -P now"

    keep_registered = var.keep_registered
    output_directory = "${var.output_dir}/${var.output_hv}"
}
