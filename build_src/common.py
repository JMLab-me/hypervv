import subprocess

from doit import task_params
from doit.exceptions import TaskFailed


@task_params([{"name": "token", "default": "", "type": str, "long": "token"}])
def task_login_vagrant_cloud(token: str):
    def _execute():
        ret_whoami = subprocess.call(["vagrant", "cloud", "auth", "whoami"])

        if ret_whoami == 0:
            return True

        if not token:
            return TaskFailed("vagrant cloud token needed")

        ret_login = subprocess.call(
            ["vagrant", "cloud", "auth", "login", "--token", token]
        )

        if ret_login == 0:
            return True

        return TaskFailed("Failed to login vagrant cloud")

    return {
        "actions": [_execute],
    }
