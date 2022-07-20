# Hypervv

Packer templates for hyperv generation 2

## Fetures

- Hyper-V Generation 2 images
- Secure boot enabled

## Prerequisite

- Python

  - `>= 3.8`

- Packer

- Windows with Hyper-V
  - External switch

## How to use

1. install dependency

   - `pip install .`

2. setup dotenv

   1. copy .env.sample to .env
   2. fill sample as you want

3. Build image (commands are described in the below section)

### Ubuntu 2004 LTS (focal)

- Build command
  - `python -m hypervv ubuntu_2004_build`
- Output directory
  - `build/ubuntu.2004`
- Sample vagrant
  - `tests/ubuntu_2004`

### Ubuntu 2204 (jammy)

- Build command
  - `python -m hypervv ubuntu_2204_build`
- Output directory
  - `build/ubuntu.2204`
- Sample vagrant
  - `tests/ubuntu_2204`

### OpenSUSE MicroOS

- Build command
  - `python -m hypervv opensuse_microos_build`
- Output directory
  - `build/opensuse.microos`
- Sample vagrant
  - `tests/opensuse_microos`

# References

- [packer-kvm](https://github.com/goffinet/packer-kvm)
- [packer-Win2019](https://github.com/eaksel/packer-Win2019)
- [Best Practices with Packer and Windows](https://hodgkins.io/best-practices-with-packer-and-windows#disable-winrm-on-build-completion-and-only-enable-it-on-first-boot)
- [packer-CentOS7](https://github.com/eaksel/packer-CentOS7)
