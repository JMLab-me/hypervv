build {
    sources = [
        "source.hyperv-vmcx.opensuse-microos-gen2"
    ]

    post-processor "vagrant" {
        keep_input_artifact = var.keep_input_artifact
        vagrantfile_template = "templates/Vagrantfile.template"
        output = "${var.output_dir}/${var.output_box}"
    }
}
