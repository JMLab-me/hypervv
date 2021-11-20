source "hyperv-iso" "ubuntu-2004-gen1" {
    iso_url = var.iso_url
    iso_checksum = var.iso_checksum

    ssh_username = var.ssh_username
    ssh_password = var.ssh_password
    ssh_timeout = var.ssh_timeout

    http_directory = var.http_directory

    boot_wait = var.boot_wait
    boot_command = [
        "<tab><wait><tab><wait><tab><wait><tab><wait>",
        "<tab><wait><tab><wait><tab><wait><tab><wait>",
        "<tab><wait><tab><wait><tab><wait><tab><wait>",
        "<esc><f6><esc>",
        "autoinstall ds=nocloud-net;s=${var.cloud_init_uri}<wait><enter>"
    ]

    shutdown_command = "echo 'vagrant' | sudo -S shutdown -P now"

    keep_registered = var.keep_registered
}

source "hyperv-iso" "ubuntu-2004-gen2" {
    generation = 2
    enable_secure_boot = true
    secure_boot_template = "MicrosoftUEFICertificateAuthority"

    iso_url = var.iso_url
    iso_checksum = var.iso_checksum

    ssh_username = var.ssh_username
    ssh_password = var.ssh_password
    ssh_timeout = var.ssh_timeout

    http_directory = var.http_directory

    boot_wait = var.boot_wait
    boot_command = [
        "<esc><wait><esc><wait><esc><wait><esc><wait>",
        "set gfxpayload=keep<enter>",
        "linux /casper/vmlinuz quiet ",
        "autoinstall ds=nocloud-net\\;s=${var.cloud_init_uri} --- <enter>",
        "initrd /casper/initrd<enter>",
        "boot<enter>"
    ]

    shutdown_command = "echo 'vagrant' | sudo -S shutdown -P now"

    keep_registered = var.keep_registered
}
