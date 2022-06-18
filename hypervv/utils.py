from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Union,
    Collection,
    Optional,
    Set,
    Tuple,
    Dict,
)

from mmap import mmap, ACCESS_READ
import hashlib

import requests

if TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path


def download_file_from_url(
    url: str, output: Union[str, bytes, PathLike[Any]], chunk_size: int = 8192
) -> None:

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(output, "wb") as f:
            for i, chunk in enumerate(r.iter_content(chunk_size)):
                if chunk:
                    f.write(chunk)


def calculate_sha256(
    target: Union[str, bytes, PathLike[Any]], buf_size: int = 8192
) -> str:
    sha256: str
    with open(target, "rb") as f, mmap(f.fileno(), 0, access=ACCESS_READ) as file:
        sha256 = hashlib.sha256(file).hexdigest()

    return sha256


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

    results = _resolve(include)

    excs = _resolve(exclude) if exclude is not None else set()

    return tuple(results - excs)


def build_packer_command(
    project: Path,
    options: List[str] = [],
    var_files: Collection[Path] = [],
    vars: Collection[Tuple[str, str]] = [],
) -> str:
    cmd = "packer build "

    cmd += " ".join(options)
    if len(options) > 0:
        cmd += " "

    vars_args = []
    for key, value in vars:
        vars_args.append(f'-var="{key}={value}"')

    cmd += " ".join(vars_args)
    if len(vars_args) > 0:
        cmd += " "

    var_files_args = []
    for var_file in var_files:
        var_files_args.append(f'-var-file="{str(var_file.absolute())}"')

    cmd += " ".join(var_files_args)
    cmd += f' "{project}"'

    return cmd
