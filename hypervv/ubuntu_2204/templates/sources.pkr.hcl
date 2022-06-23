source "hyperv-iso" "ubuntu-2204-gen2" {
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
        "set gfxpayload=keep<enter>",
        "linux /casper/vmlinuz --- autoinstall ds=\"nocloud-net;seedfrom=${var.cloud_init_uri}\"<wait><enter>",
        "initrd /casper/initrd<enter>",
        "boot<enter>"
    ]

    first_boot_device = "SCSI:0:0"

    shutdown_command = "echo '${var.username}' | sudo -S shutdown -P now"

    keep_registered = var.keep_registered
    output_directory = "${var.output_dir}/${var.output_hv}"
}
