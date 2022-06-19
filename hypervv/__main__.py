import doit
from dotenv import load_dotenv

from hypervv.ubuntu_2004 import task_build_ubuntu_2004, task_test_ubuntu_2004

load_dotenv()

doit.run(globals())
