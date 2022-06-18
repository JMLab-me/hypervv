from typing import Collection, List, Mapping

import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from pycdlib import PyCdlib, pycdlibexception


@dataclass(frozen=True)
class IsoFileMap:
    file_dep: Path
    iso_mapping: Path


def generate_iso(
    mapping: Collection[IsoFileMap],
    dependencies: Collection[str],
    targets: Collection[str],
    label: str = "Data",
) -> Path:
    """
    Generate ISO image from given file or directories

    if no mapping found, default behaivor is flat all files to root directory of ISO

    - /some/nested/directory/files.txt > /files.txt

    if you want to remap files (like preserve the directory structures), then should provide
    iso mapping information

    :param mapping: remap or rename files (support files only)
    :param dependencies: files or directories to include (both files and directories are supported)
    :param targets: ISO image output (only first element of list is used)
    :param label: Label of ISO file (default value is "Data")
    """

    iso = PyCdlib()
    iso.new(joliet=3, vol_ident=label)

    target = Path(next(iter(targets), ""))

    if not target.parent.exists():
        os.makedirs(target.parent)

    if target.exists():
        target.unlink()

    def _create_dir(parent: Path) -> None:
        try:
            iso.add_directory(joliet_path=parent.parent.as_posix())
        except pycdlibexception.PyCdlibInvalidInput:
            _create_dir(parent.parent)
            iso.add_directory(joliet_path=parent.parent.as_posix())

    try:
        f_map = _build_iso_paths(mapping, dependencies)

        for k, v in f_map.items():
            for i in v:
                try:
                    iso.add_file(k, joliet_path=i.as_posix())
                except pycdlibexception.PyCdlibInvalidInput as e:
                    if not "Could not find path" in e.args:
                        raise e

                    _create_dir(i)
                    iso.add_file(k, joliet_path=i.as_posix())

        iso.write(target)

    finally:
        iso.close()

    return target


def _build_iso_paths(
    mapping: Collection[IsoFileMap], dependencies: Collection[str]
) -> Mapping[Path, Collection[Path]]:
    file_map: Mapping[Path, List[Path]] = defaultdict(list)

    resolved: List[Path] = []
    for dep in dependencies:
        p = Path(dep)

        assert p.exists()

        _resolve(p, resolved, 1)

    for p in resolved:
        file_added: bool = False
        for m in mapping:
            if m.file_dep.resolve() == p.resolve():
                file_added = True

                file_map[p].append(m.iso_mapping)

        if not file_added:
            file_map[p].append(Path("/", p.name))

    return file_map


def _resolve(dir: Path, resolved: List[Path], depth: int) -> None:
    if depth > 5:
        raise RecursionError("Too much depth!")

    if dir.is_dir():
        walk = dir.glob("**/*")

        for w in walk:
            _resolve(w, resolved, depth)
    else:
        resolved.append(dir)
