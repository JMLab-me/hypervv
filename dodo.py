from dotenv import load_dotenv

load_dotenv()

from build_src.common import task_login_vagrant_cloud
from build_src.ubuntu_2004 import (
    task_build_ubuntu_2004,
    task_publish_ubuntu_2004,
    task_test_ubuntu_2004,
)
