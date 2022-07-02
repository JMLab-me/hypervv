build {
    sources = [
        "source.hyperv-iso.centos-7-gen2"
    ]

    provisioner "shell" {
        scripts = [
            "scripts/linux/vagrant.sh"
        ]
    }

    post-processor "vagrant" {
        keep_input_artifact = var.keep_input_artifact
        vagrantfile_template = "templates/Vagrantfile.template"
        output = "${var.output_dir}/${var.output_box}"
    }
}
