from collections import defaultdict
from typing import List, Mapping, Set, Collection, Optional, Tuple, Dict

from pathlib import Path
import os
import time
from dataclasses import dataclass

import requests
import shutil
from pycdlib import PyCdlib, udf, pycdlibexception


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


@dataclass(frozen=True)
class IsoFileMap:
    file_dep: Path
    iso_mapping: Path


def generate_iso(
    mapping: Collection[IsoFileMap],
    dependencies: Collection[str],
    targets: List[str],
):

    iso = PyCdlib()
    iso.new(udf="2.60")

    directory_set: Set[Path] = set()

    target = Path(targets[0])

    if not target.parent.exists():
        os.makedirs(target.parent)

    if target.exists():
        target.unlink()

    def _build_iso_paths() -> Mapping[Path, Collection[Path]]:
        file_map: Dict[Path, List[Path]] = defaultdict(list)

        for dep in dependencies:
            file_added: bool = False
            p = Path(dep)

            for m in mapping:
                if m.file_dep.resolve() == p.resolve():
                    file_added = True

                    file_map[p].append(m.iso_mapping)

            if not file_added:
                file_map[p].append(Path("/", p.name))

        return file_map

    def _create_dir(parent: Path):
        try:
            iso.add_directory(udf_path=parent.parent.as_posix())
        except pycdlibexception.PyCdlibInvalidInput:
            _create_dir(parent.parent)
            iso.add_directory(udf_path=parent.parent.as_posix())

    try:
        f_map = _build_iso_paths()

        for k, v in f_map.items():
            for i in v:
                try:
                    iso.add_file(k, udf_path=i.as_posix())
                except pycdlibexception.PyCdlibInvalidInput:
                    _create_dir(i)
                    iso.add_file(k, udf_path=i.as_posix())

        iso.write(target)

    finally:
        iso.close()


def download_cloudbase_init(targets: List[str]):
    url: str = "https://cloudbase.it/downloads/CloudbaseInitSetup_Stable_x64.msi"

    target = Path(targets[0])

    if target.exists():
        return

    if not target.parent.exists():
        os.makedirs(target.parent)

    with requests.get(url, stream=True) as r:
        with open(target, "wb") as f:
            shutil.copyfileobj(r.raw, f)
