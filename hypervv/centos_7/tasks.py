import os
from pathlib import Path
from typing import Any, Dict

from hypervv.utils import gen_file_list, build_packer_command, test_vagrant_box

name = "Ubuntu2204"
root = Path(__file__).resolve().parent / "templates"
output_box = Path("build/centos.7/packer_centos-7-gen2_hyperv.box")
kickstart = Path("http/centos.7/kickstart.cfg")

var_files = [
    Path("defaults/default.pkrvars.hcl"),
    Path("defaults/default.http.pkrvars.hcl"),
    Path("defaults/default.linux.credential.pkrvars.hcl"),
    Path("defaults/default.linux.pkrvars.hcl"),
]


def task_centos_7_build() -> Dict[str, Any]:

    file_dep_inc = [
        # Default configs
        *var_files,
        # Image
        root,
        # Kickstart
        kickstart,
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
