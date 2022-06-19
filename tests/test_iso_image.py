from collections import defaultdict
from email.policy import default
from typing import Collection, MutableMapping

from pathlib import Path
from hypervv.iso_image import IsoFileMap, generate_iso

from pytest import TempPathFactory
from pycdlib import PyCdlib


def test_generate_iso(tmp_path_factory: TempPathFactory) -> None:
    maps = [
        IsoFileMap(
            file_dep=Path("tests/assets/iso/file1.txt"),
            iso_mapping=Path("/directory/file1.txt"),
        ),
        IsoFileMap(
            file_dep=Path(
                "tests/assets/iso/nested/nested_nested/nested_nested_file1.txt"
            ),
            iso_mapping=Path("/directory/nested_nested_file1.txt"),
        ),
        IsoFileMap(
            file_dep=Path(
                "tests/assets/iso/nested/nested_nested/nested_nested_file2.txt"
            ),
            iso_mapping=Path("/directory/nested/nested_nested_file1.txt"),
        ),
    ]

    deps = [Path("tests/assets/iso")]

    tmp = tmp_path_factory.mktemp(basename="test_iso")
    output: Path = tmp / "test.iso"

    generate_iso(maps, deps, [output.resolve()])

    iso = PyCdlib()
    iso.open(str(output.resolve()))

    fileMap: MutableMapping[str, Collection[str]] = {}

    curr: str
    files: Collection[str]
    for (curr, _, files) in iso.walk(joliet_path="/"):
        fileMap[curr] = sorted(files)

    expected = {
        "/": sorted(["nested_file1.txt", "file2.txt"]),
        "/directory": sorted(["file1.txt", "nested_nested_file1.txt"]),
        "/directory/nested": sorted(["nested_nested_file1.txt"]),
    }

    assert expected == fileMap
