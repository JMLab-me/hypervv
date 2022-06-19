build {
    sources = [
        "source.hyperv-vmcx.opensuse_microos"
    ]

    post-processor "vagrant" {
        output = "${var.output_dir}/${var.output_box}_gen2.box"
    }
}
