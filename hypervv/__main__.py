import doit
from dotenv import load_dotenv

from hypervv.ubuntu_2004 import *
from hypervv.ubuntu_2204 import *
from hypervv.opensuse_microos import *
from hypervv.centos_7 import *

load_dotenv()

doit.run(globals())
