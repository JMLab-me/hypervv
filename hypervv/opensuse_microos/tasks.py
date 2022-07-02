import os
from pathlib import Path
import tempfile
from typing import Any, Dict
import lzma
import subprocess

from hypervv.hyperv_utils import create_vm, delete_vm_by_name, get_vm_id
from hypervv.iso_image import IsoFileMap, generate_iso
from hypervv.utils import (
    calculate_sha256,
    decode,
    download_file_from_url,
    gen_file_list,
    build_packer_command,
    test_vagrant_box,
)

name = "OpenSUSE.MicroOS"
root = Path(__file__).resolve().parent / "templates"
archive_url = "https://download.opensuse.org/tumbleweed/appliances/openSUSE-MicroOS.x86_64-MS-HyperV.vhdx.xz"
archive_path = Path("packer_cache/openSUSE-MicroOS.x86_64-MS-HyperV.vhdx.xz")
hash_url = f"{archive_url}.sha256"
vhdx_path = Path("packer_cache/openSUSE-MicroOS.x86_64-MS-HyperV.vhdx")
secondary_iso = Path("packer_cache/openSUSE-MicroOS.x86_64-MS-HyperV-secondary-iso.iso")
var_files = [
    Path("defaults/default.pkrvars.hcl"),
    Path("defaults/default.linux.credential.pkrvars.hcl"),
    Path("defaults/default.linux.pkrvars.hcl"),
]
output_box = Path("build/opensuse.microos/packer_opensuse-microos-gen2_hyperv.box")


def task_opensuse_microos_download_vhdx() -> Dict[str, Any]:
    target = archive_path

    if not target.parent.exists():
        os.makedirs(target.parent)

    def _execute() -> None:
        download_file_from_url(archive_url, target)

    uptodate = False
    hash = tempfile.NamedTemporaryFile(delete=False)
    download_file_from_url(hash_url, hash.name)

    if target.exists():
        sha256 = calculate_sha256(target)

        with open(hash.name, "r") as f:
            ref_hash = f.readline().split(" ")[0]

        if ref_hash == sha256:
            uptodate = True

    return {"actions": [_execute], "targets": [target], "uptodate": [uptodate]}


def task_opensuse_microos_extract_vhdx() -> Dict[str, Any]:
    source = archive_path
    target = vhdx_path

    def _execute() -> None:
        with open(target, "wb") as f:
            f.write(lzma.open(source).read())

    return {
        "file_dep": [source],
        "actions": [_execute],
        "task_dep": ["opensuse_microos_download_vhdx"],
        "targets": [target],
    }


def task_opensuse_microos_build_secondary_iso() -> Dict[str, Any]:
    deps = gen_file_list([root / "secondary_images"])
    target = secondary_iso
    maps = [
        IsoFileMap(
            file_dep=root / "secondary_images/ignition/config.ign",
            iso_mapping=Path("/ignition/config.ign"),
        )
    ]

    def _execute() -> None:
        generate_iso(maps, deps, [target.resolve()], label="ignition")

    return {"actions": [_execute], "file_dep": deps, "targets": [target]}


def task_opensuse_microos_create_vm() -> Dict[str, Any]:
    target = Path(f"packer_cache/{name}.vm_id.txt")

    def _execute() -> None:
        try:
            vm_id = create_vm(name, os.getenv("HYPERVV_SWITCH_NAME", ""), vhdx_path)
        except subprocess.CalledProcessError as e:
            print(decode(e.stderr))
            raise

        with (open(target, "w")) as f:
            f.write(vm_id)

    uptodate = False
    if target.exists():
        prev_id = ""
        with (open(target, "r")) as f:
            prev_id = f.readline()

        try:
            curr_id = get_vm_id(name)

            if prev_id == curr_id:
                uptodate = True
        except subprocess.CalledProcessError:
            target.unlink()

    return {
        "actions": [_execute],
        "task_dep": ["opensuse_microos_extract_vhdx"],
        "uptodate": [uptodate],
    }


def task_opensuse_microos_build() -> Dict[str, Any]:
    file_deps = [*var_files, root, vhdx_path, secondary_iso]

    action = build_packer_command(
        project=root,
        vars=[
            ("switch_name", os.getenv("HYPERVV_SWITCH_NAME", "")),
            ("secondary_iso", str(secondary_iso.absolute())),
        ],
        var_files=var_files,
    )

    return {
        "actions": [action],
        "file_dep": gen_file_list(file_deps),
        "setup": ["opensuse_microos_create_vm"],
        "task_dep": [
            "opensuse_microos_extract_vhdx",
            "opensuse_microos_build_secondary_iso",
        ],
        "teardown": [(delete_vm_by_name, (name,))],
        "targets": [output_box],
    }


def task_opensuse_microos_test() -> Dict[str, Any]:
    test_root = Path("tests/opensuse_microos")

    return {
        "actions": [test_vagrant_box(test_root)],
        "task_dep": ["opensuse_microos_build"],
    }
