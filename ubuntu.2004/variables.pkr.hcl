variable "iso_url" {
    type = string
    default = "https://releases.ubuntu.com/20.04.3/ubuntu-20.04.3-live-server-amd64.iso"
}

variable "iso_checksum" {
    type = string
    default = "f8e3086f3cea0fb3fefb29937ab5ed9d19e767079633960ccb50e76153effc98"
}

variable "ssh_username" {
    type = string
}

variable "ssh_password" {
    type = string
    sensitive = true
}

variable "ssh_timeout" {
    type = string
    default = "7200s"
}

variable "boot_wait" {
    type = string
}

variable "http_directory" {
    type = string
}

variable "cloud_init_uri" {
    type = string
}

variable "keep_registered" {
    type = bool
    default = false
}

variable "keep_input_artifact" {
    type = bool
    default = false
}
