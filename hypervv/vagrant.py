from typing import List, Optional, Iterable

import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


@dataclass
class VagrantMachineReadableOutput:
    timestamp: datetime
    target: str
    type: str
    data: List[str]


@dataclass
class Status:
    vm_name: str
    state: str
    provider: str


class Vagrant:
    def __init__(self, cwd: Optional[Path] = None):
        self.cwd = cwd if cwd is not None else Path.cwd()

    def status(self) -> List[Status]:
        cmd = ["vagrant", "status", "--machine-readable"]
        output = subprocess.run(
            cmd,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

        parsed = self._parse_vagrant_machine_readable_output(
            filter(None, output.stdout.split("\n"))
        )

        raw_provider = next(filter(lambda x: x.type == "provider-name", parsed))
        raw_states = filter(lambda x: x.type == "state", parsed)

        return list(
            map(
                lambda x: Status(x.target, x.data[0], raw_provider.data[0]),
                raw_states,
            )
        )

    def up(self, vm_name: Optional[str] = None) -> int:
        cmd = ["vagrant", "up", "--machine-readable"]

        if vm_name is not None:
            cmd.append(vm_name)

        output = subprocess.run(
            cmd,
            cwd=self.cwd,
            universal_newlines=True,
        )

        return output.returncode

    def destroy(self, vm_name: Optional[str] = None) -> int:
        cmd = ["vagrant", "destroy", "--force", "--machine-readable"]

        if vm_name is not None:
            cmd.append(vm_name)

        output = subprocess.run(
            cmd,
            cwd=self.cwd,
            universal_newlines=True,
        )

        return output.returncode

    def _parse_vagrant_machine_readable_output(
        self,
        output: Iterable[str],
    ) -> Iterable[VagrantMachineReadableOutput]:
        def _parse(x: str) -> VagrantMachineReadableOutput:
            parsed = x.split(",", 4)

            return VagrantMachineReadableOutput(
                datetime.fromtimestamp(int(parsed[0])),
                parsed[1],
                parsed[2],
                parsed[3].split(","),
            )

        return map(lambda x: _parse(x), output)
