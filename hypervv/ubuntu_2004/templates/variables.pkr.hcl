variable "iso_url" {
    type = string
    default = "https://mirror.kakao.com/ubuntu-releases/focal/ubuntu-20.04.4-live-server-amd64.iso"
}

variable "iso_checksum" {
    type = string
    default = "28ccdb56450e643bad03bb7bcf7507ce3d8d90e8bf09e38f6bd9ac298a98eaad"
}

variable "username" {
    type = string
}

variable "password" {
    type = string
    sensitive = true
}

variable "ssh_timeout" {
    type = string
    default = "7200s"
}

variable "headless" {
    type = bool
    default = false
}

variable "switch_name" {
    type = string
}

variable "boot_wait" {
    type = string
}

variable "http_directory" {
    type = string
}

variable "cloud_init_uri" {
    type = string
    default = "http://{{.HTTPIP}}:{{.HTTPPort}}/cloud-init/ubuntu.2004/"
}

variable "keep_registered" {
    type = bool
    default = false
}

variable "keep_input_artifact" {
    type = bool
    default = false
}

variable "output_dir" {
    type = string
    default = "build/ubuntu.2004"
}

variable "output_hv" {
    type = string
}

variable "output_box" {
    type = string
    default = "packer_{{.BuildName}}_{{.Provider}}.box"
}
