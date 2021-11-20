from typing import Collection, Optional, Set, Tuple

from enum import Enum
import subprocess
from pathlib import Path

from doit.exceptions import TaskFailed

from build_src.utils.vagrant import Status, Vagrant


def gen_file_list(
    include: Collection[Path], exclude: Optional[Collection[Path]] = None
) -> Tuple[Path, ...]:
    def _resolve(paths: Collection[Path]) -> Set[Path]:
        ret: Set[Path] = set()

        for path in paths:
            if path.is_dir():
                files: Collection[Path] = [
                    x for x in path.resolve().glob("**/*") if x.is_file()
                ]
                ret.update(files)
            else:
                ret.add(path.resolve())

        return ret

    results: Set[Path] = _resolve(include)

    excs: Set[Path] = _resolve(exclude) if exclude is not None else set()

    return tuple(results - excs)


def test_vagrant_box(cwd: Path):
    def _execute():
        cwd = "tests/ubuntu.2004"

        vagrant = Vagrant(cwd)

        status: Status = vagrant.status()[0]

        if status.state == "running":
            vagrant.destroy()

        try:
            if vagrant.up() != 0:
                return False
        finally:
            vagrant.destroy()

    return {
        "name": f"test {cwd}",
        "actions": [_execute],
        "task_dep": ["build_ubuntu_2004"],
    }


class Provider(Enum):
    Hyperv = "hyperv"


def publish_box(box_name: str, box_file: Path, version: str, provider: Provider):
    def _execute():
        if not box_file.exists():
            return TaskFailed("box_file should be exists")

        if not version:
            return TaskFailed("version shoud not be empty")

        ret = subprocess.call(
            [
                "vagrant",
                "cloud",
                "publish",
                "--force",
                f"hypervv/{box_name}",
                version,
                provider.value,
                box_file,
            ]
        )

        if ret == 0:
            return True

        return ret

    return {
        "name": "publish {}".format(box_name),
        "actions": [_execute],
        "task_dep": ["login_vagrant_cloud"],
        "file_dep": [box_file],
    }
