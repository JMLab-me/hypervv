import doit
from dotenv import load_dotenv

from hypervv.ubuntu_2004 import *
from hypervv.opensuse_microos import *

load_dotenv()

doit.run(globals())
