variable "headless" {
    type = bool
}

variable "username" {
    type = string
}

variable "password" {
    type = string
}

variable "ssh_timeout" {
    type = string
}

variable "switch_name" {
    type = string
}

variable "secondary_iso" {
    type = string
}

variable "output_dir" {
    type = string
    default = "build/opensuse.microos"
}

variable "output_box" {
    type = string
    default = "packer_{{.BuildName}}_{{.Provider}}"
}
