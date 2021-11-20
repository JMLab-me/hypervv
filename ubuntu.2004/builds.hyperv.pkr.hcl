build {
    sources = [
        # "source.hyperv-iso.ubuntu-2004-gen1"
        "source.hyperv-iso.ubuntu-2004-gen2"
    ]

    provisioner "shell" {
        scripts = [
            "scripts/linux/vagrant.sh",
            "scripts/ubuntu/update.sh",
            "scripts/ubuntu/cleanup.sh"
        ]
    }

    post-processor "vagrant" {
        keep_input_artifact = var.keep_input_artifact
    }
}
