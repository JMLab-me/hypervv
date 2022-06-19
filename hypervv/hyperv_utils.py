import subprocess


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
