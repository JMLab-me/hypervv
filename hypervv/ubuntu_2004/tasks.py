import os
from pathlib import Path
from typing import Any, Dict

from hypervv.utils import gen_file_list, build_packer_command, test_vagrant_box

name = "Ubuntu2004"
root = Path(__file__).resolve().parent / "templates"
output_box = Path("build/ubuntu.2004/packer_ubuntu-2004-gen2_hyperv.box")
cloud_init = Path("http/cloud-init/ubuntu.2004")

var_files = [
    Path("defaults/default.pkrvars.hcl"),
    Path("defaults/default.credential.pkrvars.hcl"),
    Path("defaults/default.linux.pkrvars.hcl"),
]


def task_ubuntu_2004_build() -> Dict[str, Any]:

    file_dep_inc = [
        # Default configs
        *var_files,
        # Image
        root,
        # Cloud-init
        cloud_init,
        # Scripts
        Path("scripts/linux"),
        Path("scripts/ubuntu"),
    ]

    return {
        "actions": [
            build_packer_command(
                root,
                var_files=var_files,
                vars=[("switch_name", os.getenv("HYPERVV_SWITCH_NAME", ""))],
            )
        ],
        "file_dep": gen_file_list(file_dep_inc),
        "targets": [output_box],
    }


def task_ubuntu_2004_test() -> Dict[str, Any]:
    test_root = Path("tests/ubuntu_2004")

    return {
        "actions": [test_vagrant_box(test_root)],
        "task_dep": ["ubuntu_2004_build"],
    }
