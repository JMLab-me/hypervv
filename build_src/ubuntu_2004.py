import os
from pathlib import Path

from doit import task_params

from build_src.utils.common import test_vagrant_box

from .utils import gen_file_list, publish_box, Provider
from .utils.vagrant import Status, Vagrant

output_box = Path("build/ubuntu.2004/packer_ubuntu-2004-gen2_hyperv.box")


def task_build_ubuntu_2004():

    file_dep_inc = [
        # Default configs
        Path("defaults/default.pkrvars.hcl"),
        Path("defaults/default.credential.pkvars.hcl"),
        Path("defaults/default.linux.pkrvars.hcl"),
        # Image
        Path("ubuntu.2004"),
        # Cloud-init
        Path("http/cloud-init/ubuntu.2004"),
        # Scripts
        Path("scripts/linux"),
        Path("scripts/ubuntu"),
    ]

    return {
        "actions": [
            "packer build {} {} {} {} {} ubuntu.2004".format(
                '-var "headless={}"'.format(os.getenv("HYPERVV_HEADLESS", "true")),
                '-var "switch_name={}"'.format(os.getenv("HYPERVV_SWITCH_NAME")),
                '-var-file="defaults/default.pkrvars.hcl"',
                '-var-file="defaults/default.credential.pkvars.hcl"',
                '-var-file="defaults/default.linux.pkrvars.hcl"',
            )
        ],
        "file_dep": gen_file_list(file_dep_inc),
        "targets": [output_box],
    }


@task_params([{"name": "version", "default": "", "type": str, "long": "version"}])
def task_publish_ubuntu_2004(version: str):
    yield publish_box(
        box_name="Ubuntu2004",
        box_file=output_box,
        version=version,
        provider=Provider.Hyperv,
    )


def task_test_ubuntu_2004():
    yield test_vagrant_box(Path("tests/ubuntu.2004"))
