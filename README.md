# Hypervv

Packer templates for hyperv generation 2

## Prerequisite

- Python

  - `>= 3.8`

- Packer

- Windows with Hyper-V
  - External switch

## How to use

1. install dependency

   - `pip install .`

2. Build image (commands are described in the below section)

### Ubuntu 2004 (focal)

- Build command
  - `python -m hypervv build_ubuntu_2004`
- Output directory
  - `build/ubuntu.2004`
- Sample vagrant
  - `tests/ubuntu_2004`

### OpenSUSE MicroOS

- Build command
  - `python -m hypervv build_opensuse_microos`
- Output directory
  - `build/opensuse.microos`
- Sample vagrant
  - `tests/opensuse_microos`
