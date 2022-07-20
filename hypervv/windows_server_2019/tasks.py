import os
from pathlib import Path
from typing import Any, Dict
from hypervv.iso_image import IsoFileMap, generate_iso

from hypervv.utils import gen_file_list, build_packer_command, test_vagrant_box

name = "WindowsServer2019"
root = Path(__file__).resolve().parent / "templates"
output_box = Path(
    "build/windows_server.2019/packer_windows-server-2019-gen2_hyperv.box"
)
secondary_iso = Path("packer_cache/windows_server_2019_secondary_iso.iso")

var_files = [
    Path("defaults/default.pkrvars.hcl"),
    Path("defaults/default.windows.credentials.pkrvars.hcl"),
    Path("defaults/default.windows.pkrvars.hcl"),
]


def task_windows_server_2019_build_secondary_iso() -> Dict[str, Any]:
    deps = gen_file_list([root / "secondary_images", Path("scripts/windows")])
    target = secondary_iso
    maps = [
        IsoFileMap(
            file_dep=root / "secondary_images/Autounattend.Standard.xml",
            iso_mapping=Path("/Autounattend.xml"),
        ),
        IsoFileMap(
            file_dep=root / "secondary_images/Answerfile.Sysprep.xml",
            iso_mapping=Path("/Answerfile.Sysprep.xml"),
        ),
    ]

    def _execute() -> None:
        generate_iso(maps, deps, [target.resolve()])

    return {"actions": [_execute], "file_dep": deps, "targets": [target]}


def task_windows_server_2019_build() -> Dict[str, Any]:

    file_dep_inc = [
        # Default configs
        *var_files,
        # Image
        root,
    ]

    return {
        "actions": [
            build_packer_command(
                root,
                var_files=var_files,
                vars=[
                    ("switch_name", os.getenv("HYPERVV_SWITCH_NAME", "")),
                    ("secondary_iso", str(secondary_iso.absolute())),
                ],
            )
        ],
        "file_dep": gen_file_list(file_dep_inc),
        "task_dep": ["windows_server_2019_build_secondary_iso"],
        "targets": [output_box],
    }
