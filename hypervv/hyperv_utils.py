from pathlib import Path
import subprocess
import importlib.resources


def get_vm_id(name: str) -> str:
    proc = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-WindowStyle",
            "Hidden",
            "-Command",
            f'Write-Host $(Get-Vm -Name "{name}").Id',
        ],
        universal_newlines=True,
        capture_output=True,
    )

    proc.check_returncode()

    return proc.stdout.splitlines()[0]


def delete_vm_by_name(name: str) -> None:
    proc = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-WindowStyle",
            "Hidden",
            "-Command",
            f'Remove-Vm -Name "{name}" -Force',
        ],
        universal_newlines=True,
        capture_output=True,
    )

    proc.check_returncode()


def create_vm(name: str, switch: str, disk: Path) -> str:
    script = importlib.resources.path("hypervv.scripts", "New-VmFromVhdx.ps1")

    proc = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-WindowStyle",
            "Hidden",
            "-File",
            str(script),
            "-Name",
            name,
            "-MemoryBytes",
            "1073741824",
            "-SwitchName",
            switch,
            "-DiskPath",
            str(disk.absolute()),
        ],
        capture_output=True,
    )

    proc.check_returncode()

    return get_vm_id(name)
