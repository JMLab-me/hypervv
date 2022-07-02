variable "iso_url" {
    type = string
    default = "http://mirror.kakao.com/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-NetInstall-2009.iso"
}

variable "iso_checksum" {
    type = string
    default = "b79079ad71cc3c5ceb3561fff348a1b67ee37f71f4cddfec09480d4589c191d6"
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

variable "kickstart_uri" {
    type = string
    default = "http://{{.HTTPIP}}:{{.HTTPPort}}/centos.7/kickstart.cfg"
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
    default = "build/centos.7"
}

variable "output_hv" {
    type = string
}

variable "output_box" {
    type = string
    default = "packer_{{.BuildName}}_{{.Provider}}.box"
}
