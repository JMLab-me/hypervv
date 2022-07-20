build {
    sources = [
        "source.hyperv-iso.windows-server-2019-standard-gen2"
    ]

    post-processor "vagrant" {
        keep_input_artifact = var.keep_input_artifact
        vagrantfile_template = "templates/Vagrantfile.windows.template"
        output = "${var.output_dir}/${var.output_box}"
    }
}
