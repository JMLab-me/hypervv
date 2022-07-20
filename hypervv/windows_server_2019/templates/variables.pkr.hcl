variable "iso_url" {
    type = string
    default = "https://software-static.download.prss.microsoft.com/pr/download/17763.737.190906-2324.rs5_release_svc_refresh_SERVER_EVAL_x64FRE_en-us_1.iso"
}

variable "iso_checksum" {
    type = string
    default = "3022424f777b66a698047ba1c37812026b9714c5"
}

variable "username" {
    type = string
}

variable "password" {
    type = string
    sensitive = true
}

variable "winrm_timeout" {
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

variable "secondary_iso" {
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

variable "output_dir" {
    type = string
    default = "build/windows_server.2019"
}

variable "output_hv" {
    type = string
}

variable "output_box" {
    type = string
    default = "packer_{{.BuildName}}_{{.Provider}}.box"
}
